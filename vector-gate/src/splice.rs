use std::io;
use std::os::unix::io::AsRawFd;
use std::sync::atomic::{AtomicUsize, Ordering};
use tokio::io::Interest;
use tokio::net::TcpStream;

/// Hardware page size on Linux x86_64 (4 KB)
pub const PAGE_SIZE: usize = 4096;
/// Default baseline Linux pipe capacity (16 pages = 64 KB)
pub const DEFAULT_PIPE_PAGES: usize = 16;
/// Maximum allowable unprivileged Linux kernel pipe capacity (256 pages = 1 MB)
pub const MAX_PIPE_PAGES: usize = 256;
/// Maximum pipe capacity in bytes (1,048,576 bytes)
pub const MAX_PIPE_CAPACITY: usize = MAX_PIPE_PAGES * PAGE_SIZE;

/// RAproxy Kernel Pipe for Zero-Copy Splice Operations
/// Supports manual page threshold configuration (1-256 pages) and dynamic elastic resizing.
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

        // Clamp between 1 and 256 pages. Default to 16 pages (64KB) if 0
        let pages = if initial_pages == 0 {
            DEFAULT_PIPE_PAGES
        } else {
            initial_pages.clamp(1, MAX_PIPE_PAGES)
        };
        let target_bytes = pages * PAGE_SIZE;

        let mut actual_cap = DEFAULT_PIPE_PAGES * PAGE_SIZE;
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
pub async fn zero_copy_splice_bidirectional(
    client: &mut TcpStream,
    backend: &mut TcpStream,
    initial_pipe_pages: usize,
    adaptive: bool,
) -> io::Result<()> {
    let pipe_c2b = KernelPipe::new(initial_pipe_pages, adaptive)?;
    let pipe_b2c = KernelPipe::new(initial_pipe_pages, adaptive)?;

    let c2b = splice_direction(client, backend, &pipe_c2b);
    let b2c = splice_direction(backend, client, &pipe_b2c);

    tokio::select! {
        res1 = c2b => res1,
        res2 = b2c => res2,
    }
}

async fn splice_direction(
    src: &TcpStream,
    dst: &TcpStream,
    pipe: &KernelPipe,
) -> io::Result<()> {
    loop {
        let src_fd = src.as_raw_fd();
        let pipe_w = pipe.write_fd;
        let cur_cap = pipe.capacity.load(Ordering::Relaxed);

        let n = src
            .async_io(Interest::READABLE, || {
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
            })
            .await?;

        if n == 0 {
            // EOF reached from source
            return Ok(());
        }

        // Adaptive Elastic Expansion: If pipe is saturated by incoming burst, double the capacity up to 1MB
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
            let dst_fd = dst.as_raw_fd();
            let pipe_r = pipe.read_fd;
            let to_write = total - written;

            let m = dst
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

