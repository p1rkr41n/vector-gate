use std::io;
use std::os::unix::io::AsRawFd;
use std::sync::atomic::{AtomicUsize, Ordering};
use std::time::Duration;
use tokio::io::Interest;
use tokio::net::TcpStream;

/// Hardware page size on Linux x86_64 (4 KB)
pub const PAGE_SIZE: usize = 4096;
/// Default baseline Linux pipe capacity (16 pages = 64 KB)
pub const DEFAULT_PIPE_PAGES: usize = 16;
/// Maximum allowable Linux kernel pipe capacity (64 pages = 256 KB)
/// Reduced from 256 pages (1MB) to 64 pages (256KB) to conserve 75% Linux kernel page pool.
pub const MAX_PIPE_PAGES: usize = 64;
/// Maximum pipe capacity in bytes (262,144 bytes)
pub const MAX_PIPE_CAPACITY: usize = MAX_PIPE_PAGES * PAGE_SIZE;

/// Idle connection timeout for splice operations (30 seconds)
pub const SPLICE_IDLE_TIMEOUT: Duration = Duration::from_secs(30);
/// Graceful flush timeout for pending Lumberjack ACKs during half-close (5 seconds)
pub const FLUSH_TIMEOUT: Duration = Duration::from_secs(5);

/// RAproxy Kernel Pipe for Zero-Copy Splice Operations
/// Supports manual page threshold configuration (1-64 pages) and dynamic elastic resizing.
pub struct KernelPipe {
    pub read_fd: libc::c_int,
    pub write_fd: libc::c_int,
    pub capacity: AtomicUsize,
    pub adaptive: bool,
}

impl KernelPipe {
    pub fn new(initial_pages: usize, adaptive: bool) -> io::Result<Self> {
        let mut fds = [0; 2];
        let res = unsafe { libc::pipe2(fds.as_mut_ptr(), libc::O_NONBLOCK | libc::O_CLOEXEC) };
        if res < 0 {
            return Err(io::Error::last_os_error());
        }

        // Clamp between 1 and 64 pages. Default to 16 pages (64KB) if 0
        let pages = if initial_pages == 0 {
            DEFAULT_PIPE_PAGES
        } else {
            initial_pages.clamp(1, MAX_PIPE_PAGES)
        };
        let target_bytes = pages * PAGE_SIZE;

        let mut actual_cap = target_bytes;
        let ret = unsafe { libc::fcntl(fds[1], libc::F_SETPIPE_SZ, target_bytes as libc::c_int) };
        if ret > 0 {
            actual_cap = ret as usize;
        }

        Ok(Self {
            read_fd: fds[0],
            write_fd: fds[1],
            capacity: AtomicUsize::new(actual_cap),
            adaptive,
        })
    }
}

impl Drop for KernelPipe {
    fn drop(&mut self) {
        unsafe {
            libc::close(self.read_fd);
            libc::close(self.write_fd);
        }
    }
}

/// Perform zero-copy bidirectional streaming between client and backend TCP streams
/// using Linux kernel `splice(2)`.
///
/// Implements Graceful Half-Close: When client closes write stream (EOF), sends TCP FIN
/// to backend via `backend_write.shutdown().await` and keeps `b2c` future alive for up to
/// `FLUSH_TIMEOUT` (5 seconds) so Vector Core can transfer application ACKs (e.g. Lumberjack ACK)
/// back to client. Prevents duplicate logs and window synchronization errors in Beats.
pub async fn zero_copy_splice_bidirectional(
    client: &mut TcpStream,
    backend: &mut TcpStream,
    initial_pipe_pages: usize,
    adaptive: bool,
) -> io::Result<()> {
    let pipe_c2b = KernelPipe::new(initial_pipe_pages, adaptive)?;
    let pipe_b2c = KernelPipe::new(initial_pipe_pages, adaptive)?;

    let (client_read, client_write) = client.split();
    let (backend_read, mut backend_write) = backend.split();

    let c2b = splice_direction_stream(&client_read, &backend_write, &pipe_c2b);
    let b2c = splice_direction_stream(&backend_read, &client_write, &pipe_b2c);
    tokio::pin!(b2c);

    tokio::select! {
        res_c2b = c2b => {
            match res_c2b {
                Ok(()) => {
                    // Client finished sending (EOF). Half-close write direction to backend.
                    use tokio::io::AsyncWriteExt;
                    let _ = backend_write.shutdown().await;
                    // Keep b2c future running for up to FLUSH_TIMEOUT (5s) to flush pending ACKs back to client.
                    // Absolutely do NOT cancel b2c abruptly.
                    let _ = tokio::time::timeout(FLUSH_TIMEOUT, &mut b2c).await;
                    Ok(())
                }
                Err(e) => Err(e),
            }
        }
        res_b2c = &mut b2c => {
            res_b2c
        }
    }
}

pub async fn splice_direction_stream<'a>(
    src: &tokio::net::tcp::ReadHalf<'a>,
    dst: &tokio::net::tcp::WriteHalf<'a>,
    pipe: &KernelPipe,
) -> io::Result<()> {
    let src_stream = src.as_ref();
    let dst_stream = dst.as_ref();
    let src_fd = src_stream.as_raw_fd();
    let dst_fd = dst_stream.as_raw_fd();

    loop {
        let pipe_w = pipe.write_fd;
        let cur_cap = pipe.capacity.load(Ordering::Relaxed);

        let n = match tokio::time::timeout(
            SPLICE_IDLE_TIMEOUT,
            src_stream.async_io(Interest::READABLE, || {
                let res = unsafe {
                    libc::splice(
                        src_fd,
                        std::ptr::null_mut(),
                        pipe_w,
                        std::ptr::null_mut(),
                        cur_cap,
                        libc::SPLICE_F_NONBLOCK | libc::SPLICE_F_MOVE,
                    )
                };
                if res < 0 {
                    Err(io::Error::last_os_error())
                } else {
                    Ok(res)
                }
            }),
        )
        .await
        {
            Ok(Ok(bytes)) => bytes,
            Ok(Err(e)) => return Err(e),
            Err(_) => {
                return Err(io::Error::new(
                    io::ErrorKind::TimedOut,
                    "Splice idle connection timeout",
                ));
            }
        };

        if n == 0 {
            // EOF reached from source
            return Ok(());
        }

        // Adaptive Elastic Expansion: If pipe is saturated by incoming burst, double capacity up to MAX_PIPE_CAPACITY (256KB)
        if pipe.adaptive && n as usize == cur_cap && cur_cap < MAX_PIPE_CAPACITY {
            let next_target = (cur_cap * 2).min(MAX_PIPE_CAPACITY);
            let ret = unsafe { libc::fcntl(pipe_w, libc::F_SETPIPE_SZ, next_target as libc::c_int) };
            if ret > 0 {
                pipe.capacity.store(ret as usize, Ordering::Relaxed);
            }
        }

        let mut written: usize = 0;
        let total = n as usize;
        while written < total {
            let pipe_r = pipe.read_fd;
            let to_write = total - written;

            let m = dst_stream
                .async_io(Interest::WRITABLE, || {
                    let res = unsafe {
                        libc::splice(
                            pipe_r,
                            std::ptr::null_mut(),
                            dst_fd,
                            std::ptr::null_mut(),
                            to_write,
                            libc::SPLICE_F_NONBLOCK | libc::SPLICE_F_MOVE,
                        )
                    };
                    if res < 0 {
                        Err(io::Error::last_os_error())
                    } else {
                        Ok(res)
                    }
                })
                .await?;

            if m == 0 {
                return Err(io::Error::new(
                    io::ErrorKind::WriteZero,
                    "Kernel pipe splice write 0",
                ));
            }

            written += m as usize;
        }
    }
}
