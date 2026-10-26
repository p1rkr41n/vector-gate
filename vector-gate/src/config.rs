use indexmap::IndexMap;
use serde::{Deserialize, Serialize};
use std::fs;
use std::net::SocketAddr;
use std::path::{Path, PathBuf};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct UnifiedVectorConfig {
    #[serde(default, alias = "gates")]
    pub gate: Option<GateConfig>,

    #[serde(skip)]
    pub auto_remap_targets: IndexMap<String, PathBuf>,

    #[serde(flatten)]
    pub vector_topology: serde_yaml::Value,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct GateConfig {
    #[serde(default = "default_false")]
    pub enabled: bool,

    #[serde(rename = "type", default = "default_gate_type")]
    pub gate_type: String,

    #[serde(default = "default_bind_addr")]
    pub address: SocketAddr,

    #[serde(default)]
    pub options: GateOptions,

    /// Unified declarative routes: Supports both Map (<id>: { type, target, ... }) and List format
    #[serde(default)]
    pub routes: Option<RoutesConfig>,

    // Backward-compatibility legacy fields
    #[serde(default)]
    pub routing: Option<GateRouting>,

    #[serde(default)]
    pub custom_rules: Vec<CustomRuleConfig>,
}

fn default_false() -> bool {
    false
}
fn default_true() -> bool {
    true
}
fn default_gate_type() -> String {
    "any".to_string()
}
fn default_bind_addr() -> SocketAddr {
    "0.0.0.0:5000".parse().unwrap()
}
fn default_timeout_ms() -> u64 {
    200
}
fn default_sniff_window() -> usize {
    512
}
fn default_zero() -> usize {
    0
}

fn default_pipe_buffer_pages() -> usize {
    16
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct GateOptions {
    #[serde(default = "default_true")]
    pub zero_copy: bool,

    #[serde(default = "default_true")]
    pub reuse_port: bool,

    #[serde(default = "default_true")]
    pub defer_accept: bool,

    #[serde(default = "default_true")]
    pub tcp_nodelay: bool,

    #[serde(default = "default_timeout_ms")]
    pub inspect_timeout_ms: u64,

    #[serde(default = "default_sniff_window")]
    pub sniff_window_bytes: usize,

    /// Linux Kernel pipe capacity in number of pages (1 - 256 pages, 1 page = 4KB).
    /// Default is 16 (16 pages = 64KB). If set to 0 or omitted, defaults to 16.
    /// Range: 1 to 256 (256 pages = 1MB max Linux unprivileged limit).
    #[serde(default = "default_pipe_buffer_pages", alias = "pipe_buffer_bytes")]
    pub pipe_buffer: usize,

    /// Whether to dynamically expand the kernel pipe buffer on-demand under high burst.
    #[serde(default = "default_true")]
    pub pipe_adaptive: bool,

    /// Directory containing drop-in VRL parsing scripts (*.vrl)
    #[serde(default)]
    pub vrl_dir: Option<PathBuf>,

    /// Whether to watch vrl_dir and auto-reload on changes
    #[serde(default = "default_true")]
    pub vrl_watch: bool,

    /// Base port for auto-allocated internal loopback routes (default: 17500)
    #[serde(default)]
    pub internal_port_base: Option<u16>,
}

impl GateOptions {
    /// Resolves the effective pipe capacity in number of 4KB pages.
    pub fn resolved_pipe_pages(&self) -> usize {
        if self.pipe_buffer == 0 {
            16
        } else if self.pipe_buffer > 256 {
            // Handle legacy byte configuration gracefully (e.g. 65536 or 262144 bytes)
            if self.pipe_buffer >= 4096 {
                (self.pipe_buffer / 4096).clamp(1, 256)
            } else {
                256
            }
        } else {
            self.pipe_buffer
        }
    }
}

impl Default for GateOptions {
    fn default() -> Self {
        Self {
            zero_copy: true,
            reuse_port: true,
            defer_accept: true,
            tcp_nodelay: true,
            inspect_timeout_ms: default_timeout_ms(),
            sniff_window_bytes: default_sniff_window(),
            pipe_buffer: 16,
            pipe_adaptive: true,
            vrl_dir: None,
            vrl_watch: true,
            internal_port_base: None,
        }
    }
}

/// Dual-syntax Routes Config:
/// Format 1 (Vector Ecosystem Map): <route_name>: { type: "...", target: "...", magic_base64: "...", offset: 0 }
/// Format 2 (Sequential List): - name: "...", type: "...", target: "..."
#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(untagged)]
pub enum RoutesConfig {
    Map(IndexMap<String, RouteItemConfig>),
    List(Vec<RouteRuleConfig>),
}

/// Route Item in Map format (mirrors Vector Sources UX)
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct RouteItemConfig {
    #[serde(rename = "type", default = "default_socket_type")]
    pub item_type: String,

    #[serde(default)]
    pub magic_base64: Option<String>,

    #[serde(default = "default_zero")]
    pub offset: usize,

    /// Optional target. If None, auto-wired to sources referencing `gates.<name>`
    #[serde(default)]
    pub target: Option<SocketAddr>,
}

fn default_socket_type() -> String {
    "socket".to_string()
}

/// Route Item in List format (backward compatibility)
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct RouteRuleConfig {
    #[serde(default)]
    pub name: Option<String>,

    #[serde(rename = "type", default)]
    pub route_type: Option<String>,

    #[serde(rename = "match", default)]
    pub protocol_match: Option<String>,

    #[serde(default)]
    pub magic_base64: Option<String>,

    #[serde(default = "default_zero")]
    pub offset: usize,

    #[serde(default)]
    pub target: Option<SocketAddr>,
}

/// 15 Predefined Push protocols corresponding 1:1 with vector_sources.csv
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum PredefinedProtocol {
    Syslog,                // 1. syslog (RFC 3164 / 5424)
    Beats,                 // 2. logstash / beats (Lumberjack v1/v2)
    Fluent,                // 3. fluent (Forward MessagePack)
    SplunkHec,             // 4. splunk_hec (HTTP)
    DatadogIntake,         // 5. datadog_agent (HTTP)
    AwsFirehose,           // 6. aws_kinesis_firehose (HTTP)
    HerokuLogs,            // 7. heroku_logs (HTTP)
    PrometheusRemoteWrite, // 8. prometheus_remote_write (HTTP Snappy Protobuf)
    PrometheusPushgateway, // 9. prometheus_pushgateway (HTTP)
    OpenTelemetry,         // 10. opentelemetry (OTLP HTTP/gRPC)
    VectorNative,          // 11. vector (Native gRPC HTTP/2)
    Statsd,                // 12. statsd (DogStatsD / StatsD metric lines)
    Dnstap,                // 13. dnstap (DNS Frame Streams)
    GenericHttp,           // 14. http_server (REST Webhooks)
    RawSocket,             // 15. socket (Raw TCP Stream Fallback)
}

impl PredefinedProtocol {
    pub fn parse(s: &str) -> Result<Self, String> {
        let clean = s.trim().to_lowercase();
        match clean.as_str() {
            "syslog" => Ok(Self::Syslog),
            "beats" | "logstash" | "lumberjack" => Ok(Self::Beats),
            "fluent" | "fluentd" | "msgpack" => Ok(Self::Fluent),
            "splunk" | "splunk_hec" | "hec" => Ok(Self::SplunkHec),
            "datadog" | "datadog_agent" | "dd" => Ok(Self::DatadogIntake),
            "aws_firehose" | "firehose" | "kinesis" | "aws_kinesis_firehose" => Ok(Self::AwsFirehose),
            "heroku" | "heroku_logs" | "logplex" => Ok(Self::HerokuLogs),
            "prom_remote_write" | "prometheus_remote_write" | "prom_rw" | "remote_write" => Ok(Self::PrometheusRemoteWrite),
            "prom_pushgateway" | "prometheus_pushgateway" | "pushgateway" => Ok(Self::PrometheusPushgateway),
            "opentelemetry" | "otel" | "otlp" => Ok(Self::OpenTelemetry),
            "vector" | "vector_native" | "grpc" => Ok(Self::VectorNative),
            "statsd" | "dogstatsd" => Ok(Self::Statsd),
            "dnstap" => Ok(Self::Dnstap),
            "http" | "generic_http" | "http_server" | "webhook" => Ok(Self::GenericHttp),
            "raw" | "socket" | "tcp" | "default" | "other" => Ok(Self::RawSocket),
            other => Err(format!(
                "Unknown protocol type '{}'. Supported types: syslog, beats (logstash), fluent, splunk_hec, datadog (datadog_agent), aws_firehose, heroku (heroku_logs), prom_remote_write, prom_pushgateway, opentelemetry, vector, statsd, dnstap, http (http_server), socket (raw/other), any (custom)",
                other
            )),
        }
    }

    pub fn name(&self) -> &'static str {
        match self {
            Self::Syslog => "syslog",
            Self::Beats => "beats",
            Self::Fluent => "fluent",
            Self::SplunkHec => "splunk_hec",
            Self::DatadogIntake => "datadog",
            Self::AwsFirehose => "aws_firehose",
            Self::HerokuLogs => "heroku",
            Self::PrometheusRemoteWrite => "prom_remote_write",
            Self::PrometheusPushgateway => "prom_pushgateway",
            Self::OpenTelemetry => "opentelemetry",
            Self::VectorNative => "vector",
            Self::Statsd => "statsd",
            Self::Dnstap => "dnstap",
            Self::GenericHttp => "http",
            Self::RawSocket => "raw",
        }
    }
}

/// Route condition: either matching arbitrary binary slice or predefined protocol
#[derive(Debug, Clone)]
pub enum RouteCondition {
    MagicBytes {
        bytes: Vec<u8>,
        offset: usize,
    },
    Predefined(PredefinedProtocol),
}

/// Compiled route ready for sub-nanosecond execution
#[derive(Debug, Clone)]
pub struct CompiledRoute {
    pub name: String,
    pub condition: RouteCondition,
    pub target: SocketAddr,
}

/// Legacy custom rule config (backward compatibility)
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CustomRuleConfig {
    pub name: String,
    pub magic_base64: String,
    #[serde(default = "default_zero")]
    pub offset: usize,
    pub target: SocketAddr,
}

/// Legacy 15-target routing configuration (backward compatibility)
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct GateRouting {
    #[serde(default = "def_syslog")]
    pub syslog_target: SocketAddr,
    #[serde(default = "def_beats")]
    pub beats_target: SocketAddr,
    #[serde(default = "def_fluent")]
    pub fluent_target: SocketAddr,
    #[serde(default = "def_splunk")]
    pub splunk_target: SocketAddr,
    #[serde(default = "def_datadog")]
    pub datadog_target: SocketAddr,
    #[serde(default = "def_aws_firehose")]
    pub aws_firehose_target: SocketAddr,
    #[serde(default = "def_heroku")]
    pub heroku_target: SocketAddr,
    #[serde(default = "def_prom_remote_write")]
    pub prom_remote_write_target: SocketAddr,
    #[serde(default = "def_prom_pushgateway")]
    pub prom_pushgateway_target: SocketAddr,
    #[serde(default = "def_opentelemetry")]
    pub opentelemetry_target: SocketAddr,
    #[serde(default = "def_vector_native")]
    pub vector_native_target: SocketAddr,
    #[serde(default = "def_statsd")]
    pub statsd_target: SocketAddr,
    #[serde(default = "def_dnstap")]
    pub dnstap_target: SocketAddr,
    #[serde(default = "def_http")]
    pub http_target: SocketAddr,
    #[serde(default = "def_raw")]
    pub raw_target: SocketAddr,
}

fn def_syslog() -> SocketAddr { "127.0.0.1:15514".parse().unwrap() }
fn def_beats() -> SocketAddr { "127.0.0.1:15044".parse().unwrap() }
fn def_fluent() -> SocketAddr { "127.0.0.1:24224".parse().unwrap() }
fn def_splunk() -> SocketAddr { "127.0.0.1:18088".parse().unwrap() }
fn def_datadog() -> SocketAddr { "127.0.0.1:18282".parse().unwrap() }
fn def_aws_firehose() -> SocketAddr { "127.0.0.1:18443".parse().unwrap() }
fn def_heroku() -> SocketAddr { "127.0.0.1:18084".parse().unwrap() }
fn def_prom_remote_write() -> SocketAddr { "127.0.0.1:19090".parse().unwrap() }
fn def_prom_pushgateway() -> SocketAddr { "127.0.0.1:19091".parse().unwrap() }
fn def_opentelemetry() -> SocketAddr { "127.0.0.1:14318".parse().unwrap() }
fn def_vector_native() -> SocketAddr { "127.0.0.1:16000".parse().unwrap() }
fn def_statsd() -> SocketAddr { "127.0.0.1:18125".parse().unwrap() }
fn def_dnstap() -> SocketAddr { "127.0.0.1:15516".parse().unwrap() }
fn def_http() -> SocketAddr { "127.0.0.1:18080".parse().unwrap() }
fn def_raw() -> SocketAddr { "127.0.0.1:15515".parse().unwrap() }

impl Default for GateRouting {
    fn default() -> Self {
        Self {
            syslog_target: def_syslog(),
            beats_target: def_beats(),
            fluent_target: def_fluent(),
            splunk_target: def_splunk(),
            datadog_target: def_datadog(),
            aws_firehose_target: def_aws_firehose(),
            heroku_target: def_heroku(),
            prom_remote_write_target: def_prom_remote_write(),
            prom_pushgateway_target: def_prom_pushgateway(),
            opentelemetry_target: def_opentelemetry(),
            vector_native_target: def_vector_native(),
            statsd_target: def_statsd(),
            dnstap_target: def_dnstap(),
            http_target: def_http(),
            raw_target: def_raw(),
        }
    }
}

/// Fast, zero-dependency RFC 4648 Base64 decoder supporting standard and URL-safe alphabets
pub fn decode_base64(input: &str) -> Result<Vec<u8>, String> {
    let clean = input.trim();
    let mut buffer: u32 = 0;
    let mut bits: u32 = 0;
    let mut output = Vec::with_capacity(clean.len() * 3 / 4);

    for &b in clean.as_bytes() {
        if b == b'=' {
            break;
        }
        let val = match b {
            b'A'..=b'Z' => b - b'A',
            b'a'..=b'z' => b - b'a' + 26,
            b'0'..=b'9' => b - b'0' + 52,
            b'+' | b'-' => 62,
            b'/' | b'_' => 63,
            b' ' | b'\r' | b'\n' | b'\t' => continue,
            _ => return Err(format!("Invalid base64 character: '{}'", b as char)),
        };
        buffer = (buffer << 6) | (val as u32);
        bits += 6;
        if bits >= 8 {
            bits -= 8;
            output.push(((buffer >> bits) & 0xFF) as u8);
        }
    }
    Ok(output)
}

impl GateConfig {
    /// Compiles all routes (supporting modern Vector Map format, List format, or legacy custom_rules + routing)
    pub fn compile_routes(&self) -> Result<Vec<CompiledRoute>, String> {
        let mut compiled = Vec::new();

        if let Some(ref routes_cfg) = self.routes {
            match routes_cfg {
                // FORMAT 1 (USER PREFERRED): Map of named routes with Vector-compatible `type`
                RoutesConfig::Map(map) => {
                    for (name, item) in map {
                        let target = item.target.ok_or_else(|| {
                            format!(
                                "Gate route '{}' has no target and no source in 'sources:' references it with 'address: gates.{}'",
                                name, name
                            )
                        })?;

                        let clean_type = item.item_type.trim().to_lowercase();
                        if clean_type == "any" || clean_type == "custom" {
                            let b64 = item.magic_base64.as_ref().ok_or_else(|| {
                                format!("Route '{}' has type '{}' but missing 'magic_base64'", name, item.item_type)
                            })?;
                            let bytes = decode_base64(b64)
                                .map_err(|e| format!("Route '{}': invalid base64 '{}': {}", name, b64, e))?;
                            if bytes.is_empty() {
                                return Err(format!("Route '{}': base64 decoded to empty bytes", name));
                            }
                            if bytes.len() > 64 {
                                return Err(format!("Route '{}': magic bytes length ({}) exceeds max 64 bytes", name, bytes.len()));
                            }
                            if item.offset > 256 {
                                return Err(format!("Route '{}': offset ({}) exceeds max 256 bytes", name, item.offset));
                            }
                            compiled.push(CompiledRoute {
                                name: name.clone(),
                                condition: RouteCondition::MagicBytes {
                                    bytes,
                                    offset: item.offset,
                                },
                                target,
                            });
                        } else {
                            let proto = PredefinedProtocol::parse(&item.item_type)
                                .map_err(|e| format!("Route '{}': {}", name, e))?;
                            compiled.push(CompiledRoute {
                                name: name.clone(),
                                condition: RouteCondition::Predefined(proto),
                                target,
                            });
                        }
                    }
                }

                // FORMAT 2: Sequential List format
                RoutesConfig::List(list) => {
                    for (idx, r) in list.iter().enumerate() {
                        let target = r.target.ok_or_else(|| {
                            let n = r.name.as_deref().unwrap_or("unnamed");
                            format!(
                                "Gate route '{}' (index #{}) has no target and no source references it with 'address: gates.{}'",
                                n, idx + 1, n
                            )
                        })?;

                        let type_str = r.route_type.as_deref().or(r.protocol_match.as_deref());
                        if let Some(t) = type_str {
                            let clean = t.trim().to_lowercase();
                            if clean == "any" || clean == "custom" {
                                let b64 = r.magic_base64.as_ref().ok_or_else(|| {
                                    format!("Route #{}: type '{}' requires 'magic_base64'", idx + 1, t)
                                })?;
                                let bytes = decode_base64(b64)
                                    .map_err(|e| format!("Route #{}: invalid base64 '{}': {}", idx + 1, b64, e))?;
                                let name = r.name.clone().unwrap_or_else(|| format!("custom_b64_{}", b64));
                                compiled.push(CompiledRoute {
                                    name,
                                    condition: RouteCondition::MagicBytes { bytes, offset: r.offset },
                                    target,
                                });
                            } else {
                                let proto = PredefinedProtocol::parse(t)
                                    .map_err(|e| format!("Route #{}: {}", idx + 1, e))?;
                                let name = r.name.clone().unwrap_or_else(|| proto.name().to_string());
                                compiled.push(CompiledRoute {
                                    name,
                                    condition: RouteCondition::Predefined(proto),
                                    target,
                                });
                            }
                        } else if let Some(ref b64) = r.magic_base64 {
                            let bytes = decode_base64(b64)
                                .map_err(|e| format!("Route #{}: invalid base64 '{}': {}", idx + 1, b64, e))?;
                            let name = r.name.clone().unwrap_or_else(|| format!("custom_b64_{}", b64));
                            compiled.push(CompiledRoute {
                                name,
                                condition: RouteCondition::MagicBytes { bytes, offset: r.offset },
                                target,
                            });
                        } else {
                            return Err(format!("Route #{}: either 'type', 'match', or 'magic_base64' must be specified", idx + 1));
                        }
                    }
                }
            }
        } else {
            // BACKWARD-COMPATIBILITY: Compile custom_rules + routing
            for (idx, r) in self.custom_rules.iter().enumerate() {
                let bytes = decode_base64(&r.magic_base64)
                    .map_err(|e| format!("Legacy custom rule '{}': invalid base64: {}", r.name, e))?;
                if bytes.is_empty() {
                    return Err(format!("Legacy custom rule '{}': decoded to empty bytes", r.name));
                }
                if bytes.len() > 64 {
                    return Err(format!("Legacy custom rule '{}': exceeds max 64 bytes", r.name));
                }
                if r.offset > 256 {
                    return Err(format!("Legacy custom rule '{}': offset exceeds max 256 bytes", r.name));
                }
                compiled.push(CompiledRoute {
                    name: if r.name.is_empty() { format!("custom_{}", idx + 1) } else { r.name.clone() },
                    condition: RouteCondition::MagicBytes {
                        bytes,
                        offset: r.offset,
                    },
                    target: r.target,
                });
            }

            let routing = self.routing.clone().unwrap_or_default();
            compiled.push(CompiledRoute { name: "syslog".into(), condition: RouteCondition::Predefined(PredefinedProtocol::Syslog), target: routing.syslog_target });
            compiled.push(CompiledRoute { name: "beats".into(), condition: RouteCondition::Predefined(PredefinedProtocol::Beats), target: routing.beats_target });
            compiled.push(CompiledRoute { name: "fluent".into(), condition: RouteCondition::Predefined(PredefinedProtocol::Fluent), target: routing.fluent_target });
            compiled.push(CompiledRoute { name: "vector".into(), condition: RouteCondition::Predefined(PredefinedProtocol::VectorNative), target: routing.vector_native_target });
            compiled.push(CompiledRoute { name: "dnstap".into(), condition: RouteCondition::Predefined(PredefinedProtocol::Dnstap), target: routing.dnstap_target });
            compiled.push(CompiledRoute { name: "splunk_hec".into(), condition: RouteCondition::Predefined(PredefinedProtocol::SplunkHec), target: routing.splunk_target });
            compiled.push(CompiledRoute { name: "datadog".into(), condition: RouteCondition::Predefined(PredefinedProtocol::DatadogIntake), target: routing.datadog_target });
            compiled.push(CompiledRoute { name: "aws_firehose".into(), condition: RouteCondition::Predefined(PredefinedProtocol::AwsFirehose), target: routing.aws_firehose_target });
            compiled.push(CompiledRoute { name: "heroku".into(), condition: RouteCondition::Predefined(PredefinedProtocol::HerokuLogs), target: routing.heroku_target });
            compiled.push(CompiledRoute { name: "prom_remote_write".into(), condition: RouteCondition::Predefined(PredefinedProtocol::PrometheusRemoteWrite), target: routing.prom_remote_write_target });
            compiled.push(CompiledRoute { name: "prom_pushgateway".into(), condition: RouteCondition::Predefined(PredefinedProtocol::PrometheusPushgateway), target: routing.prom_pushgateway_target });
            compiled.push(CompiledRoute { name: "opentelemetry".into(), condition: RouteCondition::Predefined(PredefinedProtocol::OpenTelemetry), target: routing.opentelemetry_target });
            compiled.push(CompiledRoute { name: "statsd".into(), condition: RouteCondition::Predefined(PredefinedProtocol::Statsd), target: routing.statsd_target });
            compiled.push(CompiledRoute { name: "http".into(), condition: RouteCondition::Predefined(PredefinedProtocol::GenericHttp), target: routing.http_target });
            compiled.push(CompiledRoute { name: "other".into(), condition: RouteCondition::Predefined(PredefinedProtocol::RawSocket), target: routing.raw_target });
        }

        Ok(compiled)
    }

    pub fn validate(&self) -> Result<(), String> {
        if self.enabled {
            if self.gate_type.trim().to_lowercase() != "any" {
                return Err(format!(
                    "Invalid gate type '{}'. Only gate type 'any' is supported (self-disambiguating multi-protocol ingress).",
                    self.gate_type
                ));
            }
            let routes = self.compile_routes()?;
            if routes.is_empty() {
                return Err("Gate is enabled but no routing targets or routes are configured".into());
            }
        }
        Ok(())
    }
}

#[derive(Debug, Clone)]
pub struct VrlPlugin {
    pub name: String,              // e.g. "syslog/01_fortigate.vrl"
    #[allow(dead_code)]
    pub filename: String,          // e.g. "01_fortigate.vrl"
    pub scope: String,             // "syslog", "http", "payload", "all"
    pub priority: i32,
    pub match_prefix: Option<String>,
    pub match_contains: Option<String>,
    pub vendor: Option<String>,
    pub raw_script: String,
}

fn parse_vrl_plugin(rel_path: &str, filename: &str, content: &str) -> VrlPlugin {
    let mut scope: Option<String> = None;
    let mut priority: Option<i32> = None;
    let mut match_prefix: Option<String> = None;
    let mut match_contains: Option<String> = None;
    let mut vendor: Option<String> = None;

    let lines: Vec<&str> = content.lines().collect();
    let mut body_start_idx = 0;

    // Frontmatter delimiter detection: #--- or --- or //--- or # ---
    if !lines.is_empty() {
        let first_trimmed = lines[0].trim();
        if first_trimmed == "#---" || first_trimmed == "---" || first_trimmed == "# ---" || first_trimmed == "//---" {
            let mut close_idx = None;
            for i in 1..lines.len() {
                let l_trimmed = lines[i].trim();
                if l_trimmed == "#---" || l_trimmed == "---" || l_trimmed == "# ---" || l_trimmed == "//---" {
                    close_idx = Some(i);
                    break;
                }
            }

            if let Some(end) = close_idx {
                body_start_idx = end + 1;
                for line in &lines[1..end] {
                    let mut l = line.trim();
                    if l.starts_with('#') {
                        l = l[1..].trim();
                    } else if l.starts_with("//") {
                        l = l[2..].trim();
                    }
                    if let Some((k, v)) = l.split_once(':') {
                        let key = k.trim().to_lowercase();
                        let val = v.trim().trim_matches('"').trim_matches('\'').trim().to_string();
                        match key.as_str() {
                            "scope" => scope = Some(val.to_lowercase()),
                            "priority" => priority = val.parse::<i32>().ok(),
                            "match_prefix" => match_prefix = Some(val),
                            "match_contains" => match_contains = Some(val),
                            "vendor" => vendor = Some(val),
                            _ => {}
                        }
                    }
                }
            }
        }
    }

    let norm_path = rel_path.replace('\\', "/");
    let inferred_scope = if let Some(s) = scope {
        s
    } else if norm_path.starts_with("syslog/") {
        "syslog".to_string()
    } else if norm_path.starts_with("http/") {
        "http".to_string()
    } else if norm_path.starts_with("payload/") || norm_path.starts_with("common/") {
        "payload".to_string()
    } else if filename.starts_with("99_") || filename.contains("fallback") || filename.contains("dead_letter") {
        "all".to_string()
    } else {
        "payload".to_string()
    };

    let inferred_priority = if let Some(p) = priority {
        p
    } else {
        let digits: String = filename.chars().take_while(|c| c.is_ascii_digit()).collect();
        if !digits.is_empty() {
            digits.parse::<i32>().unwrap_or(100)
        } else if filename.contains("fallback") || filename.contains("dead_letter") {
            9999
        } else {
            100
        }
    };

    let raw_script = lines[body_start_idx..].join("\n");

    VrlPlugin {
        name: norm_path,
        filename: filename.to_string(),
        scope: inferred_scope,
        priority: inferred_priority,
        match_prefix,
        match_contains,
        vendor,
        raw_script,
    }
}

fn scan_vrl_dir_recursive(root: &Path, current: &Path, plugins: &mut Vec<VrlPlugin>) -> Result<(), std::io::Error> {
    if let Ok(entries) = fs::read_dir(current) {
        for entry in entries.filter_map(|e| e.ok()) {
            let p = entry.path();
            if p.is_dir() {
                scan_vrl_dir_recursive(root, &p, plugins)?;
            } else if p.extension().map_or(false, |ext| ext == "vrl") {
                let rel_path = p.strip_prefix(root).unwrap_or(&p).to_string_lossy().to_string();
                let filename = entry.file_name().to_string_lossy().to_string();
                let content = fs::read_to_string(&p)?;
                let plugin = parse_vrl_plugin(&rel_path, &filename, &content);
                plugins.push(plugin);
            }
        }
    }
    Ok(())
}

fn format_plugin_block(plugin: &VrlPlugin, indent: &str) -> String {
    let mut block = String::new();
    let mut conditions = Vec::new();

    conditions.push(".parsed != true".to_string());

    if let Some(ref prefix) = plugin.match_prefix {
        conditions.push(format!("starts_with(__msg, {:?})", prefix));
    }
    if let Some(ref substr) = plugin.match_contains {
        conditions.push(format!("contains(__msg, {:?})", substr));
    }

    let combined_condition = conditions.join(" && ");
    block.push_str(&format!("{}# --- Begin Plugin: {} (Priority: {}) ---\n", indent, plugin.name, plugin.priority));
    block.push_str(&format!("{}if {} {{\n", indent, combined_condition));

    let inner_indent = format!("{}    ", indent);
    for line in plugin.raw_script.lines() {
        block.push_str(&format!("{}{}\n", inner_indent, line));
    }

    // Auto-sync parsed state and metadata if parsing succeeded
    block.push_str(&format!("{}if .parsed == true || ._parsed == true {{\n", inner_indent));
    block.push_str(&format!("{}    .parsed = true\n", inner_indent));
    block.push_str(&format!("{}    ._parsed = true\n", inner_indent));
    block.push_str(&format!("{}    .parser_applied = {:?}\n", inner_indent, plugin.name));
    if let Some(ref vendor) = plugin.vendor {
        block.push_str(&format!("{}    if !exists(.vendor) {{\n", inner_indent));
        block.push_str(&format!("{}        .vendor = {:?}\n", inner_indent, vendor));
        block.push_str(&format!("{}    }}\n", inner_indent));
    }
    block.push_str(&format!("{}}}\n", inner_indent));
    block.push_str(&format!("{}}}\n\n", indent));

    block
}

fn generate_decision_tree_vrl(plugins: &[VrlPlugin]) -> String {
    let mut code = String::from(
        "# === Generated by Vector Smart Gate Hierarchical Onion Parsing Engine v2.4.2 ===\n\
         .parsed = false\n\
         ._parsed = false\n\
         .parser_applied = \"none\"\n\
         .parser_status = \"UNPARSED_RAW\"\n\n\
         __msg = string(.message) ?? \"\"\n\n"
    );

    if plugins.is_empty() {
        code.push_str(".parser_status = \"UNPARSED_RAW\"\n");
        return code;
    }

    let syslog_plugins: Vec<_> = plugins.iter().filter(|p| p.scope == "syslog").collect();
    let http_plugins: Vec<_> = plugins.iter().filter(|p| p.scope == "http").collect();
    let payload_plugins: Vec<_> = plugins.iter().filter(|p| p.scope == "payload" || p.scope == "common").collect();
    let all_plugins: Vec<_> = plugins.iter().filter(|p| p.scope == "all" || p.scope == "fallback").collect();

    // Phase 2A: Scoped Ingress Dispatcher - Syslog
    if !syslog_plugins.is_empty() {
        code.push_str("# ==============================================================================\n");
        code.push_str("# PHASE 2A (Syslog Scope): Transport-Specific Syslog Parsers\n");
        code.push_str("# ==============================================================================\n");
        code.push_str("if .type_log == \"syslog\" {\n");
        for p in syslog_plugins {
            code.push_str(&format_plugin_block(p, "    "));
        }
        code.push_str("}\n\n");
    }

    // Phase 2A: Scoped Ingress Dispatcher - HTTP
    if !http_plugins.is_empty() {
        code.push_str("# ==============================================================================\n");
        code.push_str("# PHASE 2A (HTTP Scope): Transport-Specific HTTP Parsers\n");
        code.push_str("# ==============================================================================\n");
        code.push_str("if .type_log == \"http_server\" || .type_log == \"http\" {\n");
        for p in http_plugins {
            code.push_str(&format_plugin_block(p, "    "));
        }
        code.push_str("}\n\n");
    }

    // Phase 2B: Shared Payload Dispatcher (Content-Level Parsers)
    if !payload_plugins.is_empty() {
        code.push_str("# ==============================================================================\n");
        code.push_str("# PHASE 2B: SHARED PAYLOAD DISPATCHER (Common Content Parsers)\n");
        code.push_str("# ==============================================================================\n");
        code.push_str("if .parsed != true {\n");
        for p in payload_plugins {
            code.push_str(&format_plugin_block(p, "    "));
        }
        code.push_str("}\n\n");
    }

    // Phase 2C: Global & Dead-Letter Fallback
    if !all_plugins.is_empty() {
        code.push_str("# ==============================================================================\n");
        code.push_str("# PHASE 2C: GLOBAL & DEAD-LETTER FALLBACK\n");
        code.push_str("# ==============================================================================\n");
        code.push_str("if .parsed != true {\n");
        for p in all_plugins {
            code.push_str(&format_plugin_block(p, "    "));
        }
        code.push_str("}\n\n");
    }

    // Final Status Normalization
    code.push_str(
        "# ==============================================================================\n\
         # FINAL STATUS NORMALIZATION\n\
         # ==============================================================================\n\
         if .parsed == true || ._parsed == true {\n\
             .parsed = true\n\
             ._parsed = true\n\
             .parser_status = \"SUCCESS\"\n\
         } else {\n\
             .parser_status = \"UNPARSED_RAW\"\n\
         }\n"
    );

    code
}

impl UnifiedVectorConfig {
    /// Auto-wires `address: "gates.<route_name>"` in `sources:` to Gate routes, allocates internal ports,
    /// and ensures `gates.other` terminal fallback route always exists.
    pub fn auto_wire_routes(&mut self) -> Result<(), Box<dyn std::error::Error>> {
        if let Some(ref mut gate) = self.gate {
            if !gate.enabled {
                return Ok(());
            }

            let mut next_port = gate.options.internal_port_base.unwrap_or(17500u16);

            let allocate_free_internal_port = |port: &mut u16| -> SocketAddr {
                loop {
                    let candidate = *port;
                    *port = port.saturating_add(1);
                    if let Ok(listener) = std::net::TcpListener::bind(("127.0.0.1", candidate)) {
                        drop(listener);
                        return SocketAddr::from(([127, 0, 0, 1], candidate));
                    }
                }
            };

            // 1. Ensure `other` route exists as the default fallback terminal
            match gate.routes {
                Some(RoutesConfig::Map(ref mut map)) => {
                    if !map.contains_key("other") {
                        map.insert(
                            "other".to_string(),
                            RouteItemConfig {
                                item_type: "socket".to_string(),
                                magic_base64: None,
                                offset: 0,
                                target: None,
                            },
                        );
                    }
                }
                Some(RoutesConfig::List(ref mut list)) => {
                    if !list.iter().any(|r| r.name.as_deref() == Some("other")) {
                        list.push(RouteRuleConfig {
                            name: Some("other".to_string()),
                            route_type: Some("socket".to_string()),
                            protocol_match: None,
                            magic_base64: None,
                            offset: 0,
                            target: None,
                        });
                    }
                }
                None => {
                    let mut map = IndexMap::new();
                    map.insert(
                        "other".to_string(),
                        RouteItemConfig {
                            item_type: "socket".to_string(),
                            magic_base64: None,
                            offset: 0,
                            target: None,
                        },
                    );
                    gate.routes = Some(RoutesConfig::Map(map));
                }
            }

            // 2. Scan and wire `sources:`
            if let Some(sources) = self.vector_topology.get_mut("sources").and_then(|s| s.as_mapping_mut()) {
                for (source_id, source_val) in sources.iter_mut() {
                    let s_name = source_id.as_str().unwrap_or("unknown_source").to_string();

                    // Wire closure for a specific address field in YAML
                    let mut do_wire = |addr_val: &mut serde_yaml::Value, label: &str| -> Result<(), Box<dyn std::error::Error>> {
                        if let Some(addr_str) = addr_val.as_str() {
                            let clean = addr_str.trim();
                            let target_name = if clean == "gates" || clean == "gate" {
                                "other"
                            } else if let Some(stripped) = clean.strip_prefix("gates.") {
                                stripped.trim()
                            } else if let Some(stripped) = clean.strip_prefix("gate.") {
                                stripped.trim()
                            } else {
                                return Ok(()); // Normal address, e.g. "127.0.0.1:15514"
                            };

                            let mut allocated_addr_opt: Option<SocketAddr> = None;

                            if let Some(RoutesConfig::Map(ref mut map)) = gate.routes {
                                if let Some(route_item) = map.get_mut(target_name) {
                                    let addr = match route_item.target {
                                        Some(existing) => existing,
                                        None => {
                                            let new_addr = allocate_free_internal_port(&mut next_port);
                                            route_item.target = Some(new_addr);
                                            new_addr
                                        }
                                    };
                                    allocated_addr_opt = Some(addr);
                                } else {
                                    let available: Vec<String> = map.keys().cloned().collect();
                                    return Err(format!(
                                        "Source '{}' references undefined gate route '{}'. Available routes: {:?}",
                                        label, clean, available
                                    ).into());
                                }
                            } else if let Some(RoutesConfig::List(ref mut list)) = gate.routes {
                                if let Some(route_item) = list.iter_mut().find(|r| r.name.as_deref() == Some(target_name)) {
                                    let addr = match route_item.target {
                                        Some(existing) => existing,
                                        None => {
                                            let new_addr = allocate_free_internal_port(&mut next_port);
                                            route_item.target = Some(new_addr);
                                            new_addr
                                        }
                                    };
                                    allocated_addr_opt = Some(addr);
                                } else {
                                    let available: Vec<String> = list.iter().filter_map(|r| r.name.clone()).collect();
                                    return Err(format!(
                                        "Source '{}' references undefined gate route '{}'. Available routes: {:?}",
                                        label, clean, available
                                    ).into());
                                }
                            }

                            if let Some(allocated) = allocated_addr_opt {
                                *addr_val = serde_yaml::Value::String(allocated.to_string());
                            }
                        }
                        Ok(())
                    };

                    // Top-level address
                    if let Some(addr_val) = source_val.get_mut("address") {
                        do_wire(addr_val, &s_name)?;
                    }

                    // Nested opentelemetry http block
                    if let Some(http_block) = source_val.get_mut("http") {
                        if let Some(addr_val) = http_block.get_mut("address") {
                            do_wire(addr_val, &format!("{}.http", s_name))?;
                        }
                    }

                    // Nested opentelemetry grpc block
                    if let Some(grpc_block) = source_val.get_mut("grpc") {
                        if let Some(addr_val) = grpc_block.get_mut("address") {
                            do_wire(addr_val, &format!("{}.grpc", s_name))?;
                        }
                    }
                }
            }

            // 3. Default any remaining None targets
            if let Some(RoutesConfig::Map(ref mut map)) = gate.routes {
                for (name, item) in map.iter_mut() {
                    if item.target.is_none() {
                        if name == "other" {
                            let discard: SocketAddr = "127.0.0.1:17599".parse().unwrap();
                            item.target = Some(discard);
                        } else {
                            return Err(format!(
                                "Gate route '{}' has no target and no source in 'sources:' references it with 'address: gates.{}'",
                                name, name
                            ).into());
                        }
                    }
                }
            } else if let Some(RoutesConfig::List(ref mut list)) = gate.routes {
                for item in list.iter_mut() {
                    if item.target.is_none() {
                        if item.name.as_deref() == Some("other") {
                            let discard: SocketAddr = "127.0.0.1:17599".parse().unwrap();
                            item.target = Some(discard);
                        } else {
                            let n = item.name.as_deref().unwrap_or("unnamed");
                            return Err(format!(
                                "Gate route '{}' has no target and no source references it with 'address: gates.{}'",
                                n, n
                            ).into());
                        }
                    }
                }
            }
        }
        Ok(())
    }

    pub fn discover_auto_remap_transforms(&mut self, config_dir: Option<&Path>) -> Result<(), Box<dyn std::error::Error>> {
        self.auto_remap_targets.clear();
        if let Some(mapping) = self.vector_topology.as_mapping() {
            let transforms_key = serde_yaml::Value::String("transforms".to_string());
            if let Some(transforms) = mapping.get(&transforms_key).and_then(|v| v.as_mapping()) {
                for (name_val, trans_val) in transforms {
                    let transform_name = name_val.as_str().unwrap_or("unknown");
                    if let Some(trans_map) = trans_val.as_mapping() {
                        let type_key = serde_yaml::Value::String("type".to_string());
                        if let Some(type_val) = trans_map.get(&type_key).and_then(|v| v.as_str()) {
                            let clean_type = type_val.trim().to_lowercase();
                            if clean_type == "auto_remap" || clean_type == "autoremap" {
                                let dir_key = serde_yaml::Value::String("dir".to_string());
                                let vrl_dir_key = serde_yaml::Value::String("vrl_dir".to_string());
                                let dir_opt = trans_map.get(&dir_key)
                                    .or_else(|| trans_map.get(&vrl_dir_key))
                                    .and_then(|v| v.as_str());

                                match dir_opt {
                                    Some(d) if !d.trim().is_empty() => {
                                        let raw_path = PathBuf::from(d.trim());
                                        let resolved_path = if raw_path.exists() {
                                            raw_path
                                        } else if raw_path.is_relative() {
                                            if let Some(base) = config_dir {
                                                let candidate = base.join(&raw_path);
                                                if candidate.exists() {
                                                    candidate
                                                } else {
                                                    raw_path
                                                }
                                            } else {
                                                raw_path
                                            }
                                        } else if raw_path.starts_with("/etc/vector/") {
                                            // Graceful fallback for local host testing outside container
                                            let rel = raw_path.strip_prefix("/etc/vector/").unwrap();
                                            if let Some(base) = config_dir {
                                                let cand1 = base.join(rel);
                                                let cand2 = base.parent().unwrap_or(base).join(rel);
                                                if cand1.exists() {
                                                    cand1
                                                } else if cand2.exists() {
                                                    cand2
                                                } else {
                                                    raw_path
                                                }
                                            } else {
                                                raw_path
                                            }
                                        } else {
                                            raw_path
                                        };

                                        if !resolved_path.exists() {
                                            return Err(format!(
                                                "Directory '{}' specified in auto_remap transform '{}' does not exist.",
                                                d, transform_name
                                            ).into());
                                        }
                                        if !resolved_path.is_dir() {
                                            return Err(format!(
                                                "Path '{}' specified in auto_remap transform '{}' is not a directory.",
                                                d, transform_name
                                            ).into());
                                        }
                                        self.auto_remap_targets.insert(transform_name.to_string(), resolved_path);
                                    }
                                    _ => {
                                        return Err(format!(
                                            "Transform '{}' has type '{}' but is missing mandatory parameter 'dir' specifying parser directory.",
                                            transform_name, type_val
                                        ).into());
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        Ok(())
    }

    pub fn get_vrl_directories(&self) -> Vec<PathBuf> {
        let mut dirs = Vec::new();
        for dir in self.auto_remap_targets.values() {
            if !dirs.contains(dir) {
                dirs.push(dir.clone());
            }
        }
        if let Some(ref gate) = self.gate {
            if let Some(ref legacy_dir) = gate.options.vrl_dir {
                if !dirs.contains(legacy_dir) {
                    dirs.push(legacy_dir.clone());
                }
            }
        }
        dirs
    }

    pub fn synthesize_vrl_transforms(&mut self) -> Result<(), Box<dyn std::error::Error>> {
        if !self.auto_remap_targets.is_empty() {
            let targets = self.auto_remap_targets.clone();
            for (transform_name, dir_path) in targets {
                let mut plugins = Vec::new();
                if dir_path.exists() && dir_path.is_dir() {
                    scan_vrl_dir_recursive(&dir_path, &dir_path, &mut plugins)?;
                }
                plugins.sort_by(|a, b| a.priority.cmp(&b.priority).then_with(|| a.name.cmp(&b.name)));
                let code = generate_decision_tree_vrl(&plugins);

                if let Some(mapping) = self.vector_topology.as_mapping_mut() {
                    let transforms_key = serde_yaml::Value::String("transforms".to_string());
                    if let Some(transforms) = mapping.get_mut(&transforms_key).and_then(|v| v.as_mapping_mut()) {
                        let parser_key = serde_yaml::Value::String(transform_name.clone());
                        if let Some(parser) = transforms.get_mut(&parser_key).and_then(|v| v.as_mapping_mut()) {
                            let type_key = serde_yaml::Value::String("type".to_string());
                            parser.insert(type_key, serde_yaml::Value::String("remap".to_string()));

                            let dir_key = serde_yaml::Value::String("dir".to_string());
                            let vrl_dir_key = serde_yaml::Value::String("vrl_dir".to_string());
                            parser.remove(&dir_key);
                            parser.remove(&vrl_dir_key);

                            let source_key = serde_yaml::Value::String("source".to_string());
                            parser.insert(source_key, serde_yaml::Value::String(code));
                        }
                    }
                }
            }
        } else {
            // Backward-compatibility: Check if gate.options.vrl_dir is defined
            let vrl_dir_opt = self.gate.as_ref().and_then(|g| g.options.vrl_dir.clone());
            if let Some(vrl_dir) = vrl_dir_opt {
                let mut plugins = Vec::new();
                if vrl_dir.exists() && vrl_dir.is_dir() {
                    scan_vrl_dir_recursive(&vrl_dir, &vrl_dir, &mut plugins)?;
                }
                plugins.sort_by(|a, b| a.priority.cmp(&b.priority).then_with(|| a.name.cmp(&b.name)));
                let code = generate_decision_tree_vrl(&plugins);

                if let Some(mapping) = self.vector_topology.as_mapping_mut() {
                    let transforms_key = serde_yaml::Value::String("transforms".to_string());
                    if let Some(transforms) = mapping.get_mut(&transforms_key).and_then(|v| v.as_mapping_mut()) {
                        let parser_key = serde_yaml::Value::String("universal_parser".to_string());
                        if let Some(parser) = transforms.get_mut(&parser_key).and_then(|v| v.as_mapping_mut()) {
                            let source_key = serde_yaml::Value::String("source".to_string());
                            parser.insert(source_key, serde_yaml::Value::String(code));
                        }
                    }
                }
            }
        }
        Ok(())
    }

    pub fn load_from_file<P: AsRef<Path>>(path: P) -> Result<Self, Box<dyn std::error::Error>> {
        let path_ref = path.as_ref();
        let config_dir = path_ref.parent();
        let content = fs::read_to_string(path_ref)?;
        let mut config: UnifiedVectorConfig = serde_yaml::from_str(&content)?;
        config.auto_wire_routes()?;
        config.discover_auto_remap_transforms(config_dir)?;
        config.synthesize_vrl_transforms()?;
        if let Some(ref gate) = config.gate {
            if let Err(err) = gate.validate() {
                return Err(err.into());
            }
        }
        Ok(config)
    }

    /// Produce a sanitized YAML string without the `gate:` block suitable for passing to Vector Core
    pub fn sanitized_vector_yaml(&self) -> Result<String, Box<dyn std::error::Error>> {
        let sanitized = serde_yaml::to_string(&self.vector_topology)?;
        Ok(sanitized)
    }
}
