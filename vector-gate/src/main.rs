use std::env;
use std::net::SocketAddr;
use std::path::{Path, PathBuf};
use std::sync::atomic::{AtomicU64, Ordering};
use std::sync::Arc;
use std::time::Duration;
use tokio::io::{AsyncReadExt, AsyncWriteExt};
use tokio::net::{TcpListener, TcpStream};

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
        }
    }
}

#[derive(Default)]
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
}

impl Stats {
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
        PredefinedProtocol::Syslog => buf[0] == b'<',
        PredefinedProtocol::Beats => buf[0] == 0x32 || buf[0] == 0x31,
        PredefinedProtocol::Fluent => (0x92..=0x94).contains(&buf[0]),
        PredefinedProtocol::VectorNative => buf.starts_with(b"PRI * HTTP/2.0\r\n\r\nSM\r\n\r\n"),
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
        PredefinedProtocol::OpenTelemetry => check_http_details(buf, |path, _text| {
            path.starts_with("/v1/logs")
                || path.starts_with("/v1/traces")
                || path.starts_with("/v1/metrics")
                || path.starts_with("/opentelemetry")
        }),
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

async fn handle_connection(
    mut client_stream: TcpStream,
    peer_addr: SocketAddr,
    config: Arc<RuntimeConfig>,
    stats: Arc<Stats>,
) {
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

    let mut backend_stream = match TcpStream::connect(backend_addr).await {
        Ok(s) => s,
        Err(e) => {
            eprintln!(
                "[ERROR] Failed to connect to backend [{}] ({}) for client {}: {}",
                target_name, backend_addr, peer_addr, e
            );
            return;
        }
    };
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
        if let Err(_) = splice::zero_copy_splice_bidirectional(
            &mut client_stream,
            &mut backend_stream,
            config.pipe_buffer,
            config.pipe_adaptive,
        ).await {
            let _ = tokio::io::copy_bidirectional(&mut client_stream, &mut backend_stream).await;
        }
    } else {
        let _ = tokio::io::copy_bidirectional(&mut client_stream, &mut backend_stream).await;
    }
}

pub fn start_gate_engine(config: Arc<RuntimeConfig>, stats: Arc<Stats>) {
    let num_cpus = std::thread::available_parallelism()
        .map(|n| n.get())
        .unwrap_or(4);

    let stats_reporter = Arc::clone(&stats);
    tokio::spawn(async move {
        loop {
            tokio::time::sleep(Duration::from_secs(10)).await;
            let total = stats_reporter.total_connections.load(Ordering::Relaxed);
            if total > 0 {
                println!(
                    "📊 [Vector Gate Stats] Total: {} | Custom: {} | Syslog: {} | Beats: {} | Fluent: {} | Splunk: {} | Datadog: {} | Firehose: {} | Heroku: {} | PromRW: {} | PromPG: {} | OTel: {} | VectorNative: {} | StatsD: {} | dnstap: {} | HTTP: {} | Raw: {}",
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
    });

    for worker_id in 0..num_cpus {
        let cfg = Arc::clone(&config);
        let st = Arc::clone(&stats);
        let bind_addr = config.bind;

        tokio::spawn(async move {
            let listener = match create_reuseport_listener(bind_addr, &cfg) {
                Ok(l) => l,
                Err(e) => {
                    eprintln!("[Worker {}] Error creating SO_REUSEPORT listener: {}", worker_id, e);
                    return;
                }
            };

            loop {
                match listener.accept().await {
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
        });
    }
}

fn scan_vrl_dirs(dirs: &[std::path::PathBuf]) -> Vec<(String, u64)> {
    let mut files = Vec::new();
    for dir in dirs {
        if dir.exists() && dir.is_dir() {
            scan_recursive_helper(dir, dir, &mut files);
        }
    }
    files.sort();
    files
}

fn scan_recursive_helper(root: &Path, current: &Path, files: &mut Vec<(String, u64)>) {
    if let Ok(entries) = std::fs::read_dir(current) {
        for entry in entries.filter_map(|e| e.ok()) {
            let p = entry.path();
            if p.is_dir() {
                scan_recursive_helper(root, &p, files);
            } else if p.extension().map_or(false, |ext| ext == "vrl") {
                let mtime = entry.metadata().and_then(|m| m.modified()).map_or(0, |t| {
                    t.duration_since(std::time::UNIX_EPOCH).map_or(0, |d| d.as_secs())
                });
                let rel = p.strip_prefix(root).unwrap_or(&p).to_string_lossy().to_string();
                files.push((rel, mtime));
            }
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

        let gate_enabled = unified_cfg.gate.as_ref().map(|g| g.enabled).unwrap_or(false);

        // Validation only mode
        if validate_only {
            println!("🔍 Validating unified configuration: {}", path.display());
            if let Some(ref gate) = unified_cfg.gate {
                if gate.enabled {
                    println!("✅ Gate Phase 0: Enabled (type: '{}', address: {})", gate.gate_type, gate.address);
                    let routes = gate.compile_routes()?;
                    println!("📋 Active Routes: {} configured", routes.len());
                    for (idx, r) in routes.iter().enumerate() {
                        match &r.condition {
                            RouteCondition::MagicBytes { bytes, offset } => {
                                println!("  [{}] '{}' (Magic: {:02X?}, Offset: {}) -> {}", idx + 1, r.name, bytes, offset, r.target);
                            }
                            RouteCondition::Predefined(p) => {
                                println!("  [{}] '{}' (Predefined: {:?}) -> {}", idx + 1, r.name, p, r.target);
                            }
                        }
                    }
                } else {
                    println!("ℹ️ Gate Phase 0: Disabled (Bypass mode)");
                }
            } else {
                println!("ℹ️ Gate Phase 0: Not defined (Bypass mode)");
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

        if gate_enabled {
            let gate = unified_cfg.gate.as_ref().unwrap();
            let runtime_cfg = Arc::new(RuntimeConfig::from_gate_config(gate));
            let stats = Arc::new(Stats::default());

            println!("============================================================");
            println!("🚪 [Vector Gate Phase 0: ACTIVE - UNIFIED DECLARATIVE ENGINE]");
            println!("👉 Single Ingress Endpoint   : {}", runtime_cfg.bind);
            println!("🚀 Zero-Copy Splice Engine   : Enabled (Linux Kernel pipe2)");
            println!("⚡ Multi-Queue SO_REUSEPORT  : Enabled");
            println!("⏱️ Low-Latency Wakeup       : TCP_DEFER_ACCEPT & TCP_NODELAY");
            println!("🔗 Unified Declarative Routes (First-Match-Wins):");
            for (idx, r) in runtime_cfg.routes.iter().enumerate() {
                match &r.condition {
                    RouteCondition::MagicBytes { bytes, offset } => {
                        println!(
                            "  [{:02}] '{}' (Base64 Magic: {:02X?}, Offset: {}) -> {}",
                            idx + 1, r.name, bytes, offset, r.target
                        );
                    }
                    RouteCondition::Predefined(p) => {
                        println!(
                            "  [{:02}] '{}' (Predefined: {:?}) -> {}",
                            idx + 1, r.name, p, r.target
                        );
                    }
                }
            }
            println!("============================================================");

            start_gate_engine(runtime_cfg, stats);
        } else {
            println!("============================================================");
            println!("🚪 [Vector Gate Phase 0: BYPASS]");
            println!("ℹ️ Gate Phase 0 is disabled. Vector Core handles all traffic directly.");
            println!("============================================================");
        }

        // ALWAYS sanitize runtime YAML if 'gates:' block is present or 'auto_remap' was used,
        // ensuring Vector Core never encounters unknown fields even in Bypass Mode!
        let needs_sanitization = unified_cfg.gate.is_some() || !unified_cfg.auto_remap_targets.is_empty();
        if needs_sanitization {
            let sanitized = unified_cfg.sanitized_vector_yaml()?;
            let tmp_path = PathBuf::from(format!("/tmp/.vector_runtime_{}.yaml", std::process::id()));
            std::fs::write(&tmp_path, &sanitized)?;
            vector_config_path = tmp_path.clone();
            tmp_file_to_clean = Some(tmp_path);
        }

        println!("🚀 Launching Vector Core pipeline: vector --config {}", vector_config_path.display());

        let mut child = tokio::process::Command::new("vector")
            .arg("--config")
            .arg(&vector_config_path)
            .spawn()
            .expect("Failed to spawn Vector Core process");

        let child_pid = child.id();

        // Spawn VRL Watcher if auto_remap directories or vrl_dir is enabled
        let mut _watcher_handle = None;
        let vrl_watch_enabled = unified_cfg.gate.as_ref().map(|g| g.options.vrl_watch).unwrap_or(true);
        let vrl_dirs = unified_cfg.get_vrl_directories();

        if vrl_watch_enabled && !vrl_dirs.is_empty() {
            let vrl_dirs_clone = vrl_dirs.clone();
            let tmp_path_clone = vector_config_path.clone();
            let mut unified_cfg_clone = unified_cfg.clone();
            let initial_scan = scan_vrl_dirs(&vrl_dirs_clone);

            _watcher_handle = Some(tokio::spawn(async move {
                let mut last_scan = initial_scan;
                loop {
                    tokio::time::sleep(tokio::time::Duration::from_millis(500)).await;
                    let current_scan = scan_vrl_dirs(&vrl_dirs_clone);
                    if current_scan != last_scan {
                        println!("✨ [Vector Gate VRL] Detected changes in VRL directories ({:?}). Plugins: {} files. Re-synthesizing transforms...", vrl_dirs_clone, current_scan.len());
                        last_scan = current_scan;
                        if let Err(e) = unified_cfg_clone.synthesize_vrl_transforms() {
                            eprintln!("❌ Failed to synthesize VRL transforms: {}", e);
                            continue;
                        }
                        match unified_cfg_clone.sanitized_vector_yaml() {
                            Ok(yaml) => {
                                if let Err(e) = std::fs::write(&tmp_path_clone, yaml) {
                                    eprintln!("❌ Failed to write updated vector runtime config: {}", e);
                                } else if let Some(pid) = child_pid {
                                    println!("🔄 [Vector Gate VRL] Reloading Vector Core with SIGHUP (PID: {})...", pid);
                                    unsafe {
                                        libc::kill(pid as i32, libc::SIGHUP);
                                    }
                                }
                            }
                            Err(e) => eprintln!("❌ Failed to serialize updated YAML: {}", e),
                        }
                    }
                }
            }));
        }

        tokio::select! {
            res = child.wait() => {
                match res {
                    Ok(exit_status) => println!("Vector Core exited with status: {}", exit_status),
                    Err(e) => eprintln!("Vector Core error: {}", e),
                }
            }
            _ = tokio::signal::ctrl_c() => {
                println!("\nReceived shutdown signal. Stopping Vector Core and Gate gracefully...");
                let _ = child.kill().await;
            }
        }

        if let Some(tmp) = tmp_file_to_clean {
            let _ = std::fs::remove_file(tmp);
        }

        return Ok(());
    }

    // SCENARIO 2: Standalone Gate Server Mode
    println!("============================================================");
    println!("🦀 Vector Gate Standalone Engine (Unified Declarative Routing) v2.0.0");
    println!("👉 Ingress Single Port     : {}", standalone_cfg.bind);
    println!("🚀 Zero-Copy Kernel Splice : Enabled (pipe2)");
    println!("============================================================");

    let stats = Arc::new(Stats::default());
    let cfg = Arc::new(standalone_cfg);
    start_gate_engine(cfg, stats);

    tokio::signal::ctrl_c().await?;
    println!("Shutting down standalone Vector Gate.");

    Ok(())
}
