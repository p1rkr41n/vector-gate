# Vector Smart Gate

High-Performance Multi-Gate Multiplexing Ingress Engine written in Rust.

`vector-gate` provides a zero-copy, low-latency TCP ingress proxy and magic protocol recognizer designed to demultiplex high-volume log streams into downstream ingestion pipelines (such as Timberio Vector).

## Key Features

- **Linux Zero-Copy Kernel Splice**: Uses `splice(2)` system calls with circular pipe buffers to achieve ultra-high throughput with minimal CPU and memory overhead.
- **Kernel Socket Optimizations**: Built-in support for `SO_REUSEPORT`, `TCP_DEFER_ACCEPT`, and `TCP_NODELAY`.
- **Intelligent Stream Recognition**: Inspects initial bytes (magic bytes/headers) within configurable timeouts to auto-route streams (Beats, Syslog RFC3164/RFC5424, HTTP/NDJSON, Splunk HEC, Datadog Intake, CEF, etc.).
- **Multi-Gate Architecture**: Supports multiple distinct gates running concurrently on separate network endpoints.
- **Fail-Safe Routing**: Dedicated dead-letter/fallback routing for unrecognized payloads to prevent ingestion head-of-line blocking.

## Requirements

- **OS**: Linux (kernel 4.x or later with `splice(2)` support)
- **Rust Toolchain**: Rust 2021 edition (`rustc` >= 1.70, `cargo`)

## Building from Source

```bash
cd vector-gate
cargo build --release
```

The compiled binary will be located at `vector-gate/target/release/vector-gate`.

## Configuration & Usage

`vector-gate` can parse configuration from a unified YAML configuration file:

```bash
./vector-gate/target/release/vector-gate [path/to/config.yaml]
```

### Configuration Example

```yaml
gates:
  main_gate:
    type: any
    address: 0.0.0.0:5000
    options:
      zero_copy: true
      reuse_port: true
      defer_accept: true
      inspect_timeout_ms: 200
    routing:
      syslog: 127.0.0.1:5140
      beats: 127.0.0.1:5044
      http: 127.0.0.1:8080
      other: 127.0.0.1:9999
```

## License

This project is licensed under the Mozilla Public License 2.0 (MPL-2.0). See [LICENSE](LICENSE) for details.
