use std::env;
use std::net::SocketAddr;
use std::path::{Path, PathBuf};
use std::sync::atomic::{AtomicBool, AtomicI32, AtomicU64, Ordering};
use std::sync::Arc;
use std::time::Duration;
use tokio::io::{AsyncReadExt, AsyncWriteExt};
use tokio::net::{TcpListener, TcpStream};
use tokio::signal::unix::{signal, SignalKind};

mod config;
mod splice;

use config::{
    CompiledRoute, GateConfig, PredefinedProtocol, RouteCondition, UnifiedVectorConfig,
};

#[derive(Debug, Clone)]
pub struct RuntimeConfig {
    pub bind: SocketAddr,
    pub routes: Vec<CompiledRoute>,
    pub inspect_timeout_ms: u64,
    pub zero_copy: bool,
    pub reuse_port: bool,
    pub defer_accept: bool,
    pub tcp_nodelay: bool,
    pub pipe_buffer: usize,
    pub pipe_adaptive: bool,
    pub transparent_ip: bool,
}

impl Default for RuntimeConfig {
    fn default() -> Self {
        let gate = GateConfig {
            enabled: true,
            gate_type: "any".into(),
            address: "0.0.0.0:5000".parse().unwrap(),
            options: Default::default(),
            routes: None,
            routing: None,
            custom_rules: Vec::new(),
        };
        let routes = gate.compile_routes().unwrap_or_default();
        Self {
            bind: "0.0.0.0:5000".parse().unwrap(),
            routes,
            inspect_timeout_ms: 200,
            zero_copy: true,
            reuse_port: true,
            defer_accept: true,
            tcp_nodelay: true,
            pipe_buffer: 16,
            pipe_adaptive: true,
            transparent_ip: false,
        }
    }
}

impl RuntimeConfig {
    pub fn from_gate_config(gate: &GateConfig) -> Self {
        let routes = gate.compile_routes().unwrap_or_default();
        Self {
            bind: gate.address,
            routes,
            inspect_timeout_ms: gate.options.inspect_timeout_ms,
            zero_copy: gate.options.zero_copy,
            reuse_port: gate.options.reuse_port,
            defer_accept: gate.options.defer_accept,
            tcp_nodelay: gate.options.tcp_nodelay,
            pipe_buffer: gate.options.resolved_pipe_pages(),
            pipe_adaptive: gate.options.pipe_adaptive,
            transparent_ip: gate.options.transparent_ip,
        }
    }
}

pub struct Stats {
    pub total_connections: AtomicU64,
    pub custom_conns: AtomicU64,
    pub syslog_conns: AtomicU64,
    pub beats_conns: AtomicU64,
    pub fluent_conns: AtomicU64,
    pub splunk_conns: AtomicU64,
    pub datadog_conns: AtomicU64,
    pub aws_firehose_conns: AtomicU64,
    pub heroku_conns: AtomicU64,
    pub prom_rw_conns: AtomicU64,
    pub prom_pg_conns: AtomicU64,
    pub otel_conns: AtomicU64,
    pub vector_native_conns: AtomicU64,
    pub statsd_conns: AtomicU64,
    pub dnstap_conns: AtomicU64,
    pub http_conns: AtomicU64,
    pub raw_conns: AtomicU64,
    pub start_time: std::time::Instant,
}

impl Default for Stats {
    fn default() -> Self {
        Self {
            total_connections: AtomicU64::new(0),
            custom_conns: AtomicU64::new(0),
            syslog_conns: AtomicU64::new(0),
            beats_conns: AtomicU64::new(0),
            fluent_conns: AtomicU64::new(0),
            splunk_conns: AtomicU64::new(0),
            datadog_conns: AtomicU64::new(0),
            aws_firehose_conns: AtomicU64::new(0),
            heroku_conns: AtomicU64::new(0),
            prom_rw_conns: AtomicU64::new(0),
            prom_pg_conns: AtomicU64::new(0),
            otel_conns: AtomicU64::new(0),
            vector_native_conns: AtomicU64::new(0),
            statsd_conns: AtomicU64::new(0),
            dnstap_conns: AtomicU64::new(0),
            http_conns: AtomicU64::new(0),
            raw_conns: AtomicU64::new(0),
            start_time: std::time::Instant::now(),
        }
    }
}

impl Stats {
    pub fn render_prometheus(&self) -> String {
        format!(
            "# HELP vector_gate_total_connections_total Total client TCP connections accepted by Vector Gate\n\
             # TYPE vector_gate_total_connections_total counter\n\
             vector_gate_total_connections_total {}\n\
             # HELP vector_gate_protocol_connections_total Connections classified by protocol\n\
             # TYPE vector_gate_protocol_connections_total counter\n\
             vector_gate_protocol_connections_total{{protocol=\"syslog\"}} {}\n\
             vector_gate_protocol_connections_total{{protocol=\"beats\"}} {}\n\
             vector_gate_protocol_connections_total{{protocol=\"fluent\"}} {}\n\
             vector_gate_protocol_connections_total{{protocol=\"splunk\"}} {}\n\
             vector_gate_protocol_connections_total{{protocol=\"datadog\"}} {}\n\
             vector_gate_protocol_connections_total{{protocol=\"aws_firehose\"}} {}\n\
             vector_gate_protocol_connections_total{{protocol=\"heroku\"}} {}\n\
             vector_gate_protocol_connections_total{{protocol=\"prom_rw\"}} {}\n\
             vector_gate_protocol_connections_total{{protocol=\"prom_pg\"}} {}\n\
             vector_gate_protocol_connections_total{{protocol=\"otel\"}} {}\n\
             vector_gate_protocol_connections_total{{protocol=\"vector_native\"}} {}\n\
             vector_gate_protocol_connections_total{{protocol=\"statsd\"}} {}\n\
             vector_gate_protocol_connections_total{{protocol=\"dnstap\"}} {}\n\
             vector_gate_protocol_connections_total{{protocol=\"http\"}} {}\n\
             vector_gate_protocol_connections_total{{protocol=\"custom\"}} {}\n\
             vector_gate_protocol_connections_total{{protocol=\"raw\"}} {}\n\
             # HELP vector_gate_uptime_seconds Process uptime in seconds\n\
             # TYPE vector_gate_uptime_seconds gauge\n\
             vector_gate_uptime_seconds {}\n",
            self.total_connections.load(Ordering::Relaxed),
            self.syslog_conns.load(Ordering::Relaxed),
            self.beats_conns.load(Ordering::Relaxed),
            self.fluent_conns.load(Ordering::Relaxed),
            self.splunk_conns.load(Ordering::Relaxed),
            self.datadog_conns.load(Ordering::Relaxed),
            self.aws_firehose_conns.load(Ordering::Relaxed),
            self.heroku_conns.load(Ordering::Relaxed),
            self.prom_rw_conns.load(Ordering::Relaxed),
            self.prom_pg_conns.load(Ordering::Relaxed),
            self.otel_conns.load(Ordering::Relaxed),
            self.vector_native_conns.load(Ordering::Relaxed),
            self.statsd_conns.load(Ordering::Relaxed),
            self.dnstap_conns.load(Ordering::Relaxed),
            self.http_conns.load(Ordering::Relaxed),
            self.custom_conns.load(Ordering::Relaxed),
            self.raw_conns.load(Ordering::Relaxed),
            self.start_time.elapsed().as_secs(),
        )
    }

    pub fn record(&self, condition: &RouteCondition) {
        self.total_connections.fetch_add(1, Ordering::Relaxed);
        match condition {
            RouteCondition::MagicBytes { .. } => {
                self.custom_conns.fetch_add(1, Ordering::Relaxed);
            }
            RouteCondition::Predefined(proto) => {
                match proto {
                    PredefinedProtocol::Syslog => self.syslog_conns.fetch_add(1, Ordering::Relaxed),
                    PredefinedProtocol::Beats => self.beats_conns.fetch_add(1, Ordering::Relaxed),
                    PredefinedProtocol::Fluent => self.fluent_conns.fetch_add(1, Ordering::Relaxed),
                    PredefinedProtocol::SplunkHec => self.splunk_conns.fetch_add(1, Ordering::Relaxed),
                    PredefinedProtocol::DatadogIntake => self.datadog_conns.fetch_add(1, Ordering::Relaxed),
                    PredefinedProtocol::AwsFirehose => self.aws_firehose_conns.fetch_add(1, Ordering::Relaxed),
                    PredefinedProtocol::HerokuLogs => self.heroku_conns.fetch_add(1, Ordering::Relaxed),
                    PredefinedProtocol::PrometheusRemoteWrite => self.prom_rw_conns.fetch_add(1, Ordering::Relaxed),
                    PredefinedProtocol::PrometheusPushgateway => self.prom_pg_conns.fetch_add(1, Ordering::Relaxed),
                    PredefinedProtocol::OpenTelemetry => self.otel_conns.fetch_add(1, Ordering::Relaxed),
                    PredefinedProtocol::VectorNative => self.vector_native_conns.fetch_add(1, Ordering::Relaxed),
                    PredefinedProtocol::Statsd => self.statsd_conns.fetch_add(1, Ordering::Relaxed),
                    PredefinedProtocol::Dnstap => self.dnstap_conns.fetch_add(1, Ordering::Relaxed),
                    PredefinedProtocol::GenericHttp => self.http_conns.fetch_add(1, Ordering::Relaxed),
                    PredefinedProtocol::RawSocket => self.raw_conns.fetch_add(1, Ordering::Relaxed),
                };
            }
        }
    }
}

#[inline]
pub fn is_http_signature(buf: &[u8]) -> bool {
    buf.starts_with(b"POST ")
        || buf.starts_with(b"GET ")
        || buf.starts_with(b"PUT ")
        || buf.starts_with(b"HEAD ")
        || buf.starts_with(b"DELETE ")
        || buf.starts_with(b"OPTIONS ")
}

#[inline]
fn check_http_details<F: FnOnce(&str, &str) -> bool>(buf: &[u8], predicate: F) -> bool {
    if !is_http_signature(buf) {
        return false;
    }
    if let Ok(text) = std::str::from_utf8(buf) {
        let mut path = "/";
        if let Some(first_line) = text.lines().next() {
            let parts: Vec<&str> = first_line.split_whitespace().collect();
            if parts.len() >= 2 {
                path = parts[1];
            }
        }
        predicate(path, text)
    } else {
        false
    }
}

/// Matches buffer against a predefined protocol
pub fn match_predefined_protocol(buf: &[u8], proto: PredefinedProtocol) -> bool {
    if buf.is_empty() {
        return proto == PredefinedProtocol::RawSocket;
    }

    match proto {
        PredefinedProtocol::Syslog => {
            // Traditional Syslog: starts with '<' (<PRI>...)
            if buf[0] == b'<' {
                return true;
            }
            // RFC 6587: Octet-Counted framing (e.g. "128 <14>1...")
            if buf[0].is_ascii_digit() {
                if let Some(space_pos) = buf.iter().take(10).position(|&b| b == b' ') {
                    if space_pos > 0 && buf[..space_pos].iter().all(|b| b.is_ascii_digit()) {
                        if buf.len() > space_pos + 1 && buf[space_pos + 1] == b'<' {
                            return true;
                        }
                    }
                }
            }
            false
        }
        PredefinedProtocol::Beats => buf[0] == 0x32 || buf[0] == 0x31,
        PredefinedProtocol::Fluent => (0x92..=0x94).contains(&buf[0]),
        PredefinedProtocol::VectorNative => {
            if buf.starts_with(b"PRI * HTTP/2.0\r\n\r\nSM\r\n\r\n") {
                // If it contains opentelemetry path/service, don't match vector native
                if let Ok(text) = std::str::from_utf8(buf) {
                    !text.to_lowercase().contains("opentelemetry")
                } else {
                    true
                }
            } else {
                false
            }
        }
        PredefinedProtocol::Dnstap => buf.len() >= 4 && buf[0..4] == [0, 0, 0, 0],
        PredefinedProtocol::Statsd => {
            if let Ok(text) = std::str::from_utf8(buf) {
                if let Some(first_line) = text.lines().next() {
                    first_line.contains(':')
                        && (first_line.contains("|c")
                            || first_line.contains("|g")
                            || first_line.contains("|ms")
                            || first_line.contains("|h")
                            || first_line.contains("|s"))
                } else {
                    false
                }
            } else {
                false
            }
        }
        PredefinedProtocol::SplunkHec => check_http_details(buf, |path, text| {
            path.starts_with("/services/collector") || text.contains("Splunk")
        }),
        PredefinedProtocol::DatadogIntake => check_http_details(buf, |path, text| {
            path.starts_with("/v1/input")
                || path.starts_with("/api/v1/logs")
                || path.starts_with("/api/v2/logs")
                || text.contains("DD-API-KEY")
        }),
        PredefinedProtocol::AwsFirehose => check_http_details(buf, |path, text| {
            path.starts_with("/aws/firehose")
                || text.contains("X-Amz-Firehose-")
                || text.contains("Amazon Kinesis")
        }),
        PredefinedProtocol::HerokuLogs => check_http_details(buf, |path, text| {
            path.starts_with("/heroku")
                || path.starts_with("/events")
                || text.contains("Logplex-Drain-Token")
                || text.contains("Logplex")
                || text.contains("application/logplex-1")
        }),
        PredefinedProtocol::PrometheusRemoteWrite => check_http_details(buf, |path, text| {
            path.starts_with("/api/v1/write")
                || path.starts_with("/write")
                || text.contains("X-Prometheus-Remote-Write-Version")
        }),
        PredefinedProtocol::PrometheusPushgateway => {
            check_http_details(buf, |path, _text| path.starts_with("/metrics/job/"))
        }
        PredefinedProtocol::OpenTelemetry => {
            if buf.starts_with(b"PRI * HTTP/2.0\r\n\r\nSM\r\n\r\n") {
                if let Ok(text) = std::str::from_utf8(buf) {
                    text.to_lowercase().contains("opentelemetry")
                } else {
                    false
                }
            } else {
                check_http_details(buf, |path, text| {
                    path.starts_with("/v1/logs")
                        || path.starts_with("/v1/traces")
                        || path.starts_with("/v1/metrics")
                        || path.starts_with("/opentelemetry")
                        || text.contains("opentelemetry")
                })
            }
        }
        PredefinedProtocol::GenericHttp => is_http_signature(buf),
        PredefinedProtocol::RawSocket => true, // Fallback catch-all
    }
}

/// Unified linear route evaluation: First-Match-Wins
pub fn sniff_unified_route<'a>(
    buf: &[u8],
    routes: &'a [CompiledRoute],
) -> Option<&'a CompiledRoute> {
    for route in routes {
        match &route.condition {
            RouteCondition::MagicBytes { bytes, offset } => {
                let end = offset + bytes.len();
                if buf.len() >= end && &buf[*offset..end] == &bytes[..] {
                    return Some(route);
                }
            }
            RouteCondition::Predefined(proto) => {
                if match_predefined_protocol(buf, *proto) {
                    return Some(route);
                }
            }
        }
    }
    None
}

fn create_reuseport_listener(addr: SocketAddr, cfg: &RuntimeConfig) -> std::io::Result<TcpListener> {
    let domain = match addr {
        SocketAddr::V4(_) => socket2::Domain::IPV4,
        SocketAddr::V6(_) => socket2::Domain::IPV6,
    };
    let socket = socket2::Socket::new(domain, socket2::Type::STREAM, Some(socket2::Protocol::TCP))?;

    socket.set_reuse_address(true)?;
    if cfg.reuse_port {
        let _ = socket.set_reuse_port(true);
    }
    if let SocketAddr::V6(_) = addr {
        let _ = socket.set_only_v6(false);
    }
    socket.set_nonblocking(true)?;
    if cfg.tcp_nodelay {
        let _ = socket.set_nodelay(true);
    }
    let _ = socket.set_recv_buffer_size(512 * 1024);
    let _ = socket.set_send_buffer_size(512 * 1024);

    #[cfg(target_os = "linux")]
    if cfg.defer_accept {
        use std::os::unix::io::AsRawFd;
        let fd = socket.as_raw_fd();
        let timeout: libc::c_int = 1;
        unsafe {
            libc::setsockopt(
                fd,
                libc::IPPROTO_TCP,
                libc::TCP_DEFER_ACCEPT,
                &timeout as *const _ as *const libc::c_void,
                std::mem::size_of_val(&timeout) as libc::socklen_t,
            );
        }
    }

    socket.bind(&addr.into())?;
    socket.listen(4096)?;

    let std_listener: std::net::TcpListener = socket.into();
    TcpListener::from_std(std_listener)
}

/// Configure TCP socket with aggressive Keepalive and RFC 5482 TCP_USER_TIMEOUT
/// to immediately detect dead network connections and prevent ghost connections.
fn configure_robust_socket(stream: &tokio::net::TcpStream) {
    use std::os::unix::io::AsRawFd;
    let fd = stream.as_raw_fd();
    if fd < 0 {
        return;
    }
    let sock = socket2::SockRef::from(stream);

    // 1. SO_KEEPALIVE = true & TCP Keepalive: 10s idle, 5s interval
    let _ = sock.set_keepalive(true);
    let keepalive = socket2::TcpKeepalive::new()
        .with_time(Duration::from_secs(10))
        .with_interval(Duration::from_secs(5));
    let _ = sock.set_tcp_keepalive(&keepalive);

    // 2. TCP_USER_TIMEOUT = 15000 (15 seconds) via setsockopt
    #[cfg(target_os = "linux")]
    unsafe {
        let timeout_ms: libc::c_uint = 15000;
        libc::setsockopt(
            fd,
            libc::IPPROTO_TCP,
            libc::TCP_USER_TIMEOUT,
            &timeout_ms as *const _ as *const libc::c_void,
            std::mem::size_of_val(&timeout_ms) as libc::socklen_t,
        );
    }
}

/// Setup Linux policy routing for loopback reflection with IP_TRANSPARENT
pub fn setup_transparent_ip_routing() {
    #[cfg(target_os = "linux")]
    {
        println!("🔧 [Transparent IP] Initializing Linux kernel policy routing for loopback reflection...");
        let cmds = [
            ("ip", vec!["rule", "add", "from", "127.0.0.1/32", "lookup", "100"]),
            ("ip", vec!["route", "add", "local", "0.0.0.0/0", "dev", "lo", "table", "100"]),
            ("ip", vec!["-6", "rule", "add", "from", "::1/128", "lookup", "100"]),
            ("ip", vec!["-6", "route", "add", "local", "::/0", "dev", "lo", "table", "100"]),
        ];

        for (prog, args) in &cmds {
            let res = std::process::Command::new(prog).args(args).output();
            match res {
                Ok(out) => {
                    if out.status.success() {
                        println!("   ✅ Policy routing rule applied: {} {}", prog, args.join(" "));
                    } else {
                        let stderr = String::from_utf8_lossy(&out.stderr);
                        if stderr.contains("File exists") {
                            println!("   ℹ️ Policy routing rule already active: {} {}", prog, args.join(" "));
                        } else {
                            println!("   ℹ️ Policy routing note ({} {}): {}", prog, args.join(" "), stderr.trim());
                        }
                    }
                }
                Err(e) => {
                    eprintln!("   ⚠️ Notice: Unable to execute '{} {}': {}", prog, args.join(" "), e);
                }
            }
        }
    }
}

/// Attempt transparent connection preserving client IP via IP_TRANSPARENT
async fn try_connect_transparent(
    backend_addr: SocketAddr,
    peer_addr: SocketAddr,
) -> std::io::Result<TcpStream> {
    #[cfg(target_os = "linux")]
    {
        use std::os::unix::io::AsRawFd;

        // Normalize IPv4-mapped IPv6 address (::ffff:x.x.x.x) to native IPv4
        let effective_peer = match peer_addr {
            SocketAddr::V6(v6) => {
                if let Some(v4) = v6.ip().to_ipv4() {
                    SocketAddr::new(std::net::IpAddr::V4(v4), v6.port())
                } else {
                    peer_addr
                }
            }
            SocketAddr::V4(_) => peer_addr,
        };

        let socket = match backend_addr {
            SocketAddr::V4(_) => {
                if !effective_peer.is_ipv4() {
                    return Err(std::io::Error::new(
                        std::io::ErrorKind::InvalidInput,
                        "Address family mismatch: backend is IPv4 but peer is IPv6",
                    ));
                }
                tokio::net::TcpSocket::new_v4()?
            }
            SocketAddr::V6(_) => {
                if !effective_peer.is_ipv6() {
                    return Err(std::io::Error::new(
                        std::io::ErrorKind::InvalidInput,
                        "Address family mismatch: backend is IPv6 but peer is IPv4",
                    ));
                }
                tokio::net::TcpSocket::new_v6()?
            }
        };

        let fd = socket.as_raw_fd();
        let optval: libc::c_int = 1;

        let (level, optname) = match effective_peer {
            SocketAddr::V4(_) => (libc::SOL_IP, libc::IP_TRANSPARENT),
            SocketAddr::V6(_) => (libc::SOL_IPV6, libc::IPV6_TRANSPARENT),
        };

        let res = unsafe {
            libc::setsockopt(
                fd,
                level,
                optname,
                &optval as *const _ as *const libc::c_void,
                std::mem::size_of_val(&optval) as libc::socklen_t,
            )
        };

        if res != 0 {
            return Err(std::io::Error::last_os_error());
        }

        let _ = socket.set_reuseaddr(true);
        let bind_addr = SocketAddr::new(effective_peer.ip(), 0);
        socket.bind(bind_addr)?;

        // Connect with 500ms timeout to detect any kernel routing drop and failover swiftly
        let connect_fut = socket.connect(backend_addr);
        match tokio::time::timeout(Duration::from_millis(500), connect_fut).await {
            Ok(conn_res) => conn_res,
            Err(_) => Err(std::io::Error::new(
                std::io::ErrorKind::TimedOut,
                "Transparent connection timed out (policy routing may not be configured)",
            )),
        }
    }
    #[cfg(not(target_os = "linux"))]
    {
        let _ = (backend_addr, peer_addr);
        Err(std::io::Error::new(
            std::io::ErrorKind::Unsupported,
            "Transparent IP is only supported on Linux",
        ))
    }
}

/// Establish connection to backend with transparent IP and automatic graceful fallback
async fn connect_backend(
    backend_addr: SocketAddr,
    peer_addr: SocketAddr,
    transparent_ip: bool,
) -> std::io::Result<TcpStream> {
    if transparent_ip {
        match try_connect_transparent(backend_addr, peer_addr).await {
            Ok(stream) => return Ok(stream),
            Err(e) => {
                static FALLBACK_REPORTED: AtomicBool = AtomicBool::new(false);
                if !FALLBACK_REPORTED.swap(true, Ordering::Relaxed) {
                    eprintln!(
                        "⚠️ [Transparent IP] Failed to establish transparent socket from {} to {}: {}. Gracefully falling back to standard loopback connection (zero downtime).",
                        peer_addr, backend_addr, e
                    );
                }
            }
        }
    }
    TcpStream::connect(backend_addr).await
}

async fn handle_connection(
    mut client_stream: TcpStream,
    peer_addr: SocketAddr,
    config: Arc<RuntimeConfig>,
    stats: Arc<Stats>,
) {
    configure_robust_socket(&client_stream);
    if config.tcp_nodelay {
        let _ = client_stream.set_nodelay(true);
    }

    let mut initial_buf = vec![0u8; 4096];
    let n = match tokio::time::timeout(
        Duration::from_millis(config.inspect_timeout_ms),
        client_stream.read(&mut initial_buf),
    )
    .await
    {
        Ok(Ok(bytes_read)) if bytes_read > 0 => bytes_read,
        Ok(Ok(_)) => return,
        Ok(Err(e)) => {
            eprintln!("[WARN] Read error from {}: {}", peer_addr, e);
            return;
        }
        Err(_) => 0,
    };

    if n > 0 {
        let prefix = &initial_buf[..n];
        if prefix.starts_with(b"GET /metrics") || prefix.starts_with(b"GET /api/stats") {
            let body = stats.render_prometheus();
            let resp = format!(
                "HTTP/1.1 200 OK\r\nContent-Type: text/plain; version=0.0.4; charset=utf-8\r\nContent-Length: {}\r\nConnection: close\r\n\r\n{}",
                body.len(),
                body
            );
            let _ = client_stream.write_all(resp.as_bytes()).await;
            let _ = client_stream.flush().await;
            return;
        }
        if prefix.starts_with(b"GET /gate_health") {
            let body = format!(r#"{{"status":"healthy","engine":"vector-smart-gate","uptime_sec":{}}}"#, stats.start_time.elapsed().as_secs());
            let resp = format!(
                "HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nContent-Length: {}\r\nConnection: close\r\n\r\n{}",
                body.len(),
                body
            );
            let _ = client_stream.write_all(resp.as_bytes()).await;
            let _ = client_stream.flush().await;
            return;
        }
    }

    let matched_route = match sniff_unified_route(&initial_buf[..n], &config.routes) {
        Some(r) => r,
        None => {
            eprintln!(
                "[WARN] No route matched for client {} ({} initial bytes read). Dropping connection.",
                peer_addr, n
            );
            return;
        }
    };

    stats.record(&matched_route.condition);

    let backend_addr = matched_route.target;
    let target_name = matched_route.name.as_str();

    let mut backend_stream = match connect_backend(backend_addr, peer_addr, config.transparent_ip).await {
        Ok(s) => s,
        Err(e) => {
            eprintln!(
                "[ERROR] Failed to connect to backend [{}] ({}) for client {}: {}",
                target_name, backend_addr, peer_addr, e
            );
            return;
        }
    };
    configure_robust_socket(&backend_stream);
    if config.tcp_nodelay {
        let _ = backend_stream.set_nodelay(true);
    }

    if n > 0 {
        if let Err(e) = backend_stream.write_all(&initial_buf[..n]).await {
            eprintln!("[ERROR] Failed to write initial buffer to backend: {}", e);
            return;
        }
    }

    // High performance Zero-Copy Linux splice(2) with graceful user-space fallback
    if config.zero_copy {
        match splice::zero_copy_splice_bidirectional(
            &mut client_stream,
            &mut backend_stream,
            config.pipe_buffer,
            config.pipe_adaptive,
        )
        .await
        {
            Ok(()) => {}
            Err(e) if e.kind() == std::io::ErrorKind::TimedOut => {
                // Post-Handshake Slowloris Idle Timeout (RSK-06) - cleanly drop connection and free resources
            }
            Err(_) => {
                let _ = tokio::io::copy_bidirectional(&mut client_stream, &mut backend_stream).await;
            }
        }
    } else {
        let _ = tokio::io::copy_bidirectional(&mut client_stream, &mut backend_stream).await;
    }
}

pub fn start_gate_engine(
    gate_name: &str,
    config: Arc<RuntimeConfig>,
    stats: Arc<Stats>,
    shutdown_rx: tokio::sync::watch::Receiver<bool>,
) {
    let num_cpus = std::thread::available_parallelism()
        .map(|n| n.get())
        .unwrap_or(4);

    let stats_reporter = Arc::clone(&stats);
    let mut stats_rx = shutdown_rx.clone();
    let g_name_stats = gate_name.to_string();
    tokio::spawn(async move {
        loop {
            tokio::select! {
                _ = tokio::time::sleep(Duration::from_secs(10)) => {
                    let total = stats_reporter.total_connections.load(Ordering::Relaxed);
                    if total > 0 {
                        println!(
                            "📊 [Vector Gate Stats - {}] Total: {} | Custom: {} | Syslog: {} | Beats: {} | Fluent: {} | Splunk: {} | Datadog: {} | Firehose: {} | Heroku: {} | PromRW: {} | PromPG: {} | OTel: {} | VectorNative: {} | StatsD: {} | dnstap: {} | HTTP: {} | Raw: {}",
                            g_name_stats,
                            total,
                            stats_reporter.custom_conns.load(Ordering::Relaxed),
                            stats_reporter.syslog_conns.load(Ordering::Relaxed),
                            stats_reporter.beats_conns.load(Ordering::Relaxed),
                            stats_reporter.fluent_conns.load(Ordering::Relaxed),
                            stats_reporter.splunk_conns.load(Ordering::Relaxed),
                            stats_reporter.datadog_conns.load(Ordering::Relaxed),
                            stats_reporter.aws_firehose_conns.load(Ordering::Relaxed),
                            stats_reporter.heroku_conns.load(Ordering::Relaxed),
                            stats_reporter.prom_rw_conns.load(Ordering::Relaxed),
                            stats_reporter.prom_pg_conns.load(Ordering::Relaxed),
                            stats_reporter.otel_conns.load(Ordering::Relaxed),
                            stats_reporter.vector_native_conns.load(Ordering::Relaxed),
                            stats_reporter.statsd_conns.load(Ordering::Relaxed),
                            stats_reporter.dnstap_conns.load(Ordering::Relaxed),
                            stats_reporter.http_conns.load(Ordering::Relaxed),
                            stats_reporter.raw_conns.load(Ordering::Relaxed),
                        );
                    }
                }
                _ = stats_rx.changed() => {
                    if *stats_rx.borrow() {
                        break;
                    }
                }
            }
        }
    });

    // Dedicated Prometheus HTTP Metrics Exporter on 0.0.0.0:9100
    let prom_stats = Arc::clone(&stats);
    let mut prom_shutdown = shutdown_rx.clone();
    tokio::spawn(async move {
        let prom_addr: SocketAddr = "0.0.0.0:9100".parse().unwrap();
        if let Ok(listener) = TcpListener::bind(prom_addr).await {
            println!("📈 [Vector Gate Telemetry] Dedicated Prometheus exporter listening on http://0.0.0.0:9100/metrics");
            loop {
                tokio::select! {
                    res = listener.accept() => {
                        if let Ok((mut stream, _)) = res {
                            let st = Arc::clone(&prom_stats);
                            tokio::spawn(async move {
                                let mut buf = [0u8; 1024];
                                if let Ok(n) = stream.read(&mut buf).await {
                                    if n > 0 {
                                        let body = st.render_prometheus();
                                        let resp = format!(
                                            "HTTP/1.1 200 OK\r\nContent-Type: text/plain; version=0.0.4; charset=utf-8\r\nContent-Length: {}\r\nConnection: close\r\n\r\n{}",
                                            body.len(),
                                            body
                                        );
                                        let _ = stream.write_all(resp.as_bytes()).await;
                                        let _ = stream.flush().await;
                                    }
                                }
                            });
                        }
                    }
                    _ = prom_shutdown.changed() => {
                        if *prom_shutdown.borrow() {
                            break;
                        }
                    }
                }
            }
        }
    });

    for worker_id in 0..num_cpus {
        let cfg = Arc::clone(&config);
        let st = Arc::clone(&stats);
        let bind_addr = config.bind;
        let mut rx = shutdown_rx.clone();
        let g_name_worker = gate_name.to_string();

        tokio::spawn(async move {
            let listener = match create_reuseport_listener(bind_addr, &cfg) {
                Ok(l) => l,
                Err(e) => {
                    eprintln!("[Worker {} - {}] Error creating SO_REUSEPORT listener: {}", worker_id, g_name_worker, e);
                    return;
                }
            };

            loop {
                tokio::select! {
                    accept_res = listener.accept() => {
                        match accept_res {
                            Ok((stream, addr)) => {
                                let c = Arc::clone(&cfg);
                                let s = Arc::clone(&st);
                                tokio::spawn(async move {
                                    handle_connection(stream, addr, c, s).await;
                                });
                            }
                            Err(e) => {
                                eprintln!("[Worker {}] Accept error: {}", worker_id, e);
                            }
                        }
                    }
                    _ = rx.changed() => {
                        if *rx.borrow() {
                            break;
                        }
                    }
                }
            }
        });
    }
}

fn scan_vrl_dirs(dirs: &[std::path::PathBuf]) -> Vec<(String, u128)> {
    let mut files = Vec::new();
    for dir in dirs {
        if dir.exists() && dir.is_dir() {
            scan_recursive_helper(dir, dir, &mut files);
        }
    }
    files.sort();
    files
}

fn scan_recursive_helper(root: &Path, current: &Path, files: &mut Vec<(String, u128)>) {
    if let Ok(entries) = std::fs::read_dir(current) {
        for entry in entries.filter_map(|e| e.ok()) {
            let p = entry.path();
            if p.is_dir() {
                scan_recursive_helper(root, &p, files);
            } else if p.extension().map_or(false, |ext| ext == "vrl") {
                let mtime_nano = entry.metadata().and_then(|m| m.modified()).map_or(0, |t| {
                    t.duration_since(std::time::UNIX_EPOCH).map_or(0, |d| d.as_nanos())
                });
                let rel = p.strip_prefix(root).unwrap_or(&p).to_string_lossy().to_string();
                files.push((rel, mtime_nano));
            }
        }
    }
}

fn spawn_vector_core(config_path: &Path) -> std::io::Result<tokio::process::Child> {
    println!("🚀 Launching Vector Core pipeline: vector --config {}", config_path.display());
    tokio::process::Command::new("vector")
        .arg("--config")
        .arg(config_path)
        .spawn()
}

async fn graceful_shutdown(child: &mut tokio::process::Child) {
    if let Some(pid) = child.id() {
        println!("⏳ Forwarding SIGTERM to Vector Core (PID: {}). Flushing on-disk buffers...", pid);
        unsafe {
            libc::kill(pid as i32, libc::SIGTERM);
        }
    }
    // Chờ tối đa 15 giây để Vector Core hoàn tất flush dữ liệu ra đĩa trước khi thoát
    let grace_period = Duration::from_secs(15);
    match tokio::time::timeout(grace_period, child.wait()).await {
        Ok(Ok(status)) => {
            println!("✅ Vector Core exited cleanly with status: {}", status);
        }
        Ok(Err(e)) => {
            eprintln!("❌ Vector Core wait error during graceful shutdown: {}", e);
        }
        Err(_) => {
            eprintln!("⚠️ Vector Core did not exit within 15s grace period. Forcing SIGKILL...");
            let _ = child.kill().await;
        }
    }
}

fn print_help() {
    println!("Vector Gate: Polymorphic Unified Declarative Ingress Multiplexer (type: any)");
    println!("Usage: vector-gate [COMMAND] [OPTIONS]");
    println!("\nCommands:");
    println!("  run                     Start Vector Gate and supervise Vector Core");
    println!("  validate                Validate vector configuration file including gate phase");
    println!("\nOptions:");
    println!("  -c, --config <PATH>     Path to vector.yaml configuration file");
    println!("  --bind <ADDR>           Standalone ingress listen address [default: 0.0.0.0:5000]");
    println!("  -h, --help              Print this help information");
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    // RSK-09: Background task to reap zombie child processes (PID 1 hygiene)
    tokio::spawn(async {
        loop {
            tokio::time::sleep(Duration::from_secs(5)).await;
            unsafe {
                let mut status = 0;
                while libc::waitpid(-1, &mut status, libc::WNOHANG) > 0 {}
            }
        }
    });

    let (shutdown_tx, shutdown_rx) = tokio::sync::watch::channel(false);
    let is_shutting_down = Arc::new(AtomicBool::new(false));
    let current_child_pid = Arc::new(AtomicI32::new(0));

    // RSK-08: Dual signal handlers for graceful shutdown (SIGTERM & SIGINT)
    let mut sigterm = signal(SignalKind::terminate()).expect("Failed to register SIGTERM handler");
    let mut sigint = signal(SignalKind::interrupt()).expect("Failed to register SIGINT handler");

    let args: Vec<String> = env::args().collect();

    let mut config_file: Option<String> = None;
    let mut validate_only = false;
    let mut standalone_cfg = RuntimeConfig::default();

    let mut i = 1;
    while i < args.len() {
        match args[i].as_str() {
            "-h" | "--help" => {
                print_help();
                std::process::exit(0);
            }
            "validate" => {
                validate_only = true;
            }
            "run" => {}
            "-c" | "--config" if i + 1 < args.len() => {
                config_file = Some(args[i + 1].clone());
                i += 1;
            }
            "--validate" if i + 1 < args.len() => {
                validate_only = true;
                config_file = Some(args[i + 1].clone());
                i += 1;
            }
            "--bind" if i + 1 < args.len() => {
                standalone_cfg.bind = args[i + 1].parse().expect("Invalid --bind address");
                i += 1;
            }
            "--transparent-ip" => {
                standalone_cfg.transparent_ip = true;
            }
            _ => {
                if !args[i].starts_with('-') && config_file.is_none() {
                    config_file = Some(args[i].clone());
                }
            }
        }
        i += 1;
    }

    // SCENARIO 1: Unified Config Mode with Vector Supervisor
    if let Some(ref path_str) = config_file {
        let path = Path::new(path_str);
        if !path.exists() {
            eprintln!("Error: Configuration file not found: {}", path.display());
            std::process::exit(1);
        }

        let unified_cfg = match UnifiedVectorConfig::load_from_file(path) {
            Ok(c) => c,
            Err(e) => {
                eprintln!("❌ Configuration Error in '{}': {}", path.display(), e);
                std::process::exit(1);
            }
        };

        let any_gate_enabled = unified_cfg.gates.values().any(|g| g.enabled);

        // Validation only mode
        if validate_only {
            println!("🔍 Validating unified configuration: {}", path.display());
            if any_gate_enabled {
                println!("✅ Gate Phase 0: Multi-Gate Engine (v2.5.0)");
                for (gate_name, gate) in &unified_cfg.gates {
                    if gate.enabled {
                        println!("  - Gate '{}' (type: '{}', address: {})", gate_name, gate.gate_type, gate.address);
                        let routes = gate.compile_routes()?;
                        println!("    Active Routes: {} configured", routes.len());
                        for (idx, r) in routes.iter().enumerate() {
                            match &r.condition {
                                RouteCondition::MagicBytes { bytes, offset } => {
                                    println!("      [{}] '{}.{}' (Magic: {:02X?}, Offset: {}) -> {}", idx + 1, gate_name, r.name, bytes, offset, r.target);
                                }
                                RouteCondition::Predefined(p) => {
                                    println!("      [{}] '{}.{}' (Predefined: {:?}) -> {}", idx + 1, gate_name, r.name, p, r.target);
                                }
                            }
                        }
                    } else {
                        println!("  - Gate '{}': Disabled (Bypass mode)", gate_name);
                    }
                }
            } else {
                println!("ℹ️ Gate Phase 0: All gates disabled or not defined (Bypass mode)");
            }

            if !unified_cfg.auto_remap_targets.is_empty() {
                println!("🧩 VRL Auto-Remap Transforms: {} configured", unified_cfg.auto_remap_targets.len());
                for (name, dir) in &unified_cfg.auto_remap_targets {
                    println!("  - Transform '{}' -> VRL directory: {}", name, dir.display());
                }
            }

            let sanitized = unified_cfg.sanitized_vector_yaml()?;
            let tmp_path = format!("/tmp/.vector_val_{}.yaml", std::process::id());
            std::fs::write(&tmp_path, &sanitized)?;

            let status = std::process::Command::new("vector")
                .arg("validate")
                .arg("--no-environment")
                .arg(&tmp_path)
                .status();

            let _ = std::fs::remove_file(&tmp_path);

            match status {
                Ok(s) if s.success() => {
                    println!("✅ Vector Core topology is valid!");
                    println!("🎉 All phases (Gate + Vector) validation PASSED successfully.");
                    std::process::exit(0);
                }
                Ok(s) => {
                    eprintln!("❌ Vector Core validation failed with code: {:?}", s.code());
                    std::process::exit(s.code().unwrap_or(1));
                }
                Err(e) => {
                    eprintln!("❌ Failed to execute vector validation: {}", e);
                    std::process::exit(1);
                }
            }
        }

        // Run mode with Supervisor
        let mut vector_config_path = path.to_path_buf();
        let mut tmp_file_to_clean: Option<PathBuf> = None;

        if any_gate_enabled {
            println!("============================================================");
            println!("🚪 [Vector Gate Phase 0: ACTIVE - MULTI-GATE ENGINE (v2.5.0)]");

            let any_transparent = unified_cfg.gates.values().any(|g| g.enabled && g.options.transparent_ip);
            if any_transparent {
                setup_transparent_ip_routing();
            }

            for (gate_name, gate) in &unified_cfg.gates {
                if !gate.enabled {
                    println!("ℹ️ Gate '{}': Disabled (Bypass mode)", gate_name);
                    continue;
                }
                let runtime_cfg = Arc::new(RuntimeConfig::from_gate_config(gate));
                let stats = Arc::new(Stats::default());

                println!("👉 Gate '{}' Ingress Endpoint: {}", gate_name, runtime_cfg.bind);
                println!("   Zero-Copy Splice Engine   : Enabled (Linux Kernel pipe2)");
                println!("   Multi-Queue SO_REUSEPORT  : Enabled");
                println!(
                    "   Transparent IP (TPROXY)   : {}",
                    if runtime_cfg.transparent_ip { "Enabled (L3/L4 Client IP Preservation)" } else { "Disabled" }
                );
                println!("   Active Routes:");
                for (idx, r) in runtime_cfg.routes.iter().enumerate() {
                    match &r.condition {
                        RouteCondition::MagicBytes { bytes, offset } => {
                            println!(
                                "     [{:02}] '{}.{}' (Base64 Magic: {:02X?}, Offset: {}) -> {}",
                                idx + 1, gate_name, r.name, bytes, offset, r.target
                            );
                        }
                        RouteCondition::Predefined(p) => {
                            println!(
                                "     [{:02}] '{}.{}' (Predefined: {:?}) -> {}",
                                idx + 1, gate_name, r.name, p, r.target
                            );
                        }
                    }
                }
                start_gate_engine(gate_name, runtime_cfg, stats, shutdown_rx.clone());
            }
            println!("============================================================");
        } else {
            println!("============================================================");
            println!("🚪 [Vector Gate Phase 0: BYPASS]");
            println!("ℹ️ All gates are disabled or none defined. Vector Core handles all traffic directly.");
            println!("============================================================");
        }

        // ALWAYS sanitize runtime YAML if 'gates:' block is present or 'auto_remap' was used,
        // ensuring Vector Core never encounters unknown fields even in Bypass Mode!
        let needs_sanitization = !unified_cfg.gates.is_empty() || !unified_cfg.auto_remap_targets.is_empty();
        if needs_sanitization {
            let sanitized = unified_cfg.sanitized_vector_yaml()?;
            let tmp_path = PathBuf::from(format!("/tmp/.vector_runtime_{}.yaml", std::process::id()));
            let tmp_atomic = format!("{}.tmp.{}", tmp_path.display(), std::process::id());
            std::fs::write(&tmp_atomic, &sanitized)?;
            std::fs::rename(&tmp_atomic, &tmp_path)?;
            vector_config_path = tmp_path.clone();
            tmp_file_to_clean = Some(tmp_path);
        }

        // Spawn VRL Watcher if auto_remap directories or vrl_dir is enabled
        let mut _watcher_handle = None;
        let vrl_watch_enabled = unified_cfg.gates.values().any(|g| g.options.vrl_watch);
        let vrl_dirs = unified_cfg.get_vrl_directories();

        if vrl_watch_enabled && !vrl_dirs.is_empty() {
            let vrl_dirs_clone = vrl_dirs.clone();
            let tmp_path_clone = vector_config_path.clone();
            let mut unified_cfg_clone = unified_cfg.clone();
            let initial_scan = scan_vrl_dirs(&vrl_dirs_clone);
            let child_pid_tracker = Arc::clone(&current_child_pid);
            let is_shutting_down_watcher = Arc::clone(&is_shutting_down);

            _watcher_handle = Some(tokio::spawn(async move {
                let mut last_scan = initial_scan;
                loop {
                    tokio::time::sleep(tokio::time::Duration::from_millis(500)).await;
                    if is_shutting_down_watcher.load(Ordering::Relaxed) {
                        break;
                    }
                    let current_scan = scan_vrl_dirs(&vrl_dirs_clone);
                    if current_scan != last_scan {
                        println!(
                            "✨ [Vector Gate VRL] Detected changes in VRL directories ({:?}). Debouncing for 2 seconds...",
                            vrl_dirs_clone
                        );

                        // RSK-05: Debounce 2 seconds before reloading to allow multi-file writes to settle
                        tokio::time::sleep(tokio::time::Duration::from_secs(2)).await;

                        // Re-scan after debounce to capture all settled changes
                        let settled_scan = scan_vrl_dirs(&vrl_dirs_clone);
                        last_scan = settled_scan;

                        println!(
                            "✨ [Vector Gate VRL] Applying settled VRL changes. Plugins: {} files. Re-synthesizing transforms...",
                            last_scan.len()
                        );

                        if let Err(e) = unified_cfg_clone.synthesize_vrl_transforms() {
                            eprintln!("❌ Failed to synthesize VRL transforms: {}", e);
                            continue;
                        }
                        match unified_cfg_clone.sanitized_vector_yaml() {
                            Ok(yaml) => {
                                // RSK-05: Atomic File Swap (Temp-and-Rename)
                                let tmp_atomic = format!("{}.tmp.{}", tmp_path_clone.display(), std::process::id());
                                if let Err(e) = std::fs::write(&tmp_atomic, &yaml) {
                                    eprintln!("❌ Failed to write temporary runtime config: {}", e);
                                } else if let Err(e) = std::fs::rename(&tmp_atomic, &tmp_path_clone) {
                                    eprintln!("❌ Atomic rename failed: {}", e);
                                    let _ = std::fs::remove_file(&tmp_atomic);
                                } else {
                                    let pid = child_pid_tracker.load(Ordering::Relaxed);
                                    if pid > 0 {
                                        println!("🔄 [Vector Gate VRL] Reloading Vector Core with SIGHUP (PID: {})...", pid);
                                        unsafe {
                                            libc::kill(pid, libc::SIGHUP);
                                        }
                                    }
                                }
                            }
                            Err(e) => eprintln!("❌ Failed to serialize updated YAML: {}", e),
                        }
                    }
                }
            }));
        }

        // RSK-09: Supervisor restart loop & RSK-08 Graceful Shutdown
        let mut restart_count = 0;
        while !is_shutting_down.load(Ordering::SeqCst) {
            let mut child = match spawn_vector_core(&vector_config_path) {
                Ok(c) => c,
                Err(e) => {
                    eprintln!("❌ Failed to spawn Vector Core: {}", e);
                    if is_shutting_down.load(Ordering::SeqCst) {
                        break;
                    }
                    tokio::time::sleep(Duration::from_millis(500)).await;
                    continue;
                }
            };

            let pid = child.id().unwrap_or(0) as i32;
            current_child_pid.store(pid, Ordering::SeqCst);

            tokio::select! {
                status = child.wait() => {
                    current_child_pid.store(0, Ordering::SeqCst);
                    if is_shutting_down.load(Ordering::SeqCst) {
                        match status {
                            Ok(st) => println!("Vector Core stopped: {}", st),
                            Err(e) => eprintln!("Vector Core wait error during shutdown: {}", e),
                        }
                        break;
                    }
                    restart_count += 1;
                    match status {
                        Ok(st) => eprintln!("⚠️ [Supervisor] Vector Core exited (status: {}). Restarting (#{})...", st, restart_count),
                        Err(e) => eprintln!("⚠️ [Supervisor] Vector Core error: {}. Restarting (#{})...", e, restart_count),
                    }
                    tokio::time::sleep(Duration::from_millis(500)).await;
                }
                _ = sigterm.recv() => {
                    println!("\n🛑 [Vector Gate] Received SIGTERM from Orchestrator. Initiating Graceful Shutdown...");
                    is_shutting_down.store(true, Ordering::SeqCst);
                    let _ = shutdown_tx.send(true);
                    graceful_shutdown(&mut child).await;
                    break;
                }
                _ = sigint.recv() => {
                    println!("\n🛑 [Vector Gate] Received SIGINT (Ctrl+C). Initiating Graceful Shutdown...");
                    is_shutting_down.store(true, Ordering::SeqCst);
                    let _ = shutdown_tx.send(true);
                    graceful_shutdown(&mut child).await;
                    break;
                }
            }
        }

        if let Some(tmp) = tmp_file_to_clean {
            let _ = std::fs::remove_file(tmp);
        }

        return Ok(());
    }

    // SCENARIO 2: Standalone Gate Server Mode
    if standalone_cfg.transparent_ip {
        setup_transparent_ip_routing();
    }
    println!("============================================================");
    println!("🦀 Vector Gate Standalone Engine (Unified Declarative Routing) v2.0.0");
    println!("👉 Ingress Single Port     : {}", standalone_cfg.bind);
    println!("🚀 Zero-Copy Kernel Splice : Enabled (pipe2)");
    println!(
        "🛡️ Transparent IP (TPROXY) : {}",
        if standalone_cfg.transparent_ip { "Enabled (L3/L4 Client IP Preservation)" } else { "Disabled" }
    );
    println!("============================================================");

    let stats = Arc::new(Stats::default());
    let cfg = Arc::new(standalone_cfg);
    start_gate_engine("standalone", cfg, stats, shutdown_rx);

    tokio::select! {
        _ = sigterm.recv() => {
            println!("\n🛑 Received SIGTERM. Shutting down standalone Vector Gate...");
            let _ = shutdown_tx.send(true);
        }
        _ = sigint.recv() => {
            println!("\n🛑 Received SIGINT (Ctrl+C). Shutting down standalone Vector Gate...");
            let _ = shutdown_tx.send(true);
        }
    }
    tokio::time::sleep(Duration::from_millis(200)).await;
    println!("Standalone Vector Gate shutdown complete.");

    Ok(())
}
