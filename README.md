# Vector Smart Gate

**High-Performance Multi-Gate Multiplexing Ingress & Unified Observability Pipeline**

Vector Smart Gate merges upstream **Timberio Vector (v0.58.0)** with the **Vector Smart Gate** high-performance zero-copy ingress multiplexer into a unified repository and application.

---

## 🌟 Key Architectural Capabilities

1. **Embedded Ingress Engine (`lib/vector-gate`)**:
   - **Linux Kernel Splice Turbo-Engine**: Uses `splice(2)` zero-copy pipe transfers for maximum throughput with minimal CPU overhead.
   - **Multi-Gate Declarative Routing**: Exposes multiple independent gates (e.g. `main_gate:5000`, `dmz_gate:5045`) concurrently.
   - **Protocol Auto-Recognition**: Automatic magic-byte inspection for Beats, Syslog (RFC3164/RFC5424), HTTP NDJSON, Generic JSON, CEF, Cisco ASA, and Fortigate.
   - **Dead-Letter Terminal**: Isolated per-gate fallback sink preventing head-of-line blocking on unknown payloads.

2. **Full Observability Data Pipeline (Vector Core)**:
   - 100+ native sources, transforms, and sinks (Elasticsearch, OpenSearch, ClickHouse, S3, Kafka, Datadog, Prometheus, etc.).
   - Ultra-fast Vector Remap Language (VRL) data transformation.

---

## 🚀 Unified Configuration (`vector.yaml`)

With Vector Smart Gate, you declare ingress gates directly inside your `vector.yaml`:

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

sources:
  gate_syslog:
    type: syslog
    mode: tcp
    address: 127.0.0.1:5140

  gate_beats:
    type: file
    # or native beats source

sinks:
  console_out:
    type: console
    inputs: ["gate_syslog"]
    encoding:
      codec: json
```

When Vector starts, if the `gates:` block is defined in the configuration, the embedded `vector-gate` engine automatically initializes, binds the gate sockets, and begins splicing incoming traffic to internal pipeline sources. If `gates:` is omitted, Vector runs in standard upstream mode.

---

## 🛠️ Building from Source

### Standalone Gate Binary (`vector-gate`)
To build only the lightweight high-performance ingress proxy binary:

```bash
cargo build -p vector-gate --release --bin vector-gate
```
Output: `target/release/vector-gate`

### Unified Vector Engine
To compile the complete unified Vector binary:

```bash
cargo build --release --bin vector
```
Output: `target/release/vector`

---

## 📁 Repository Structure

```
.
├── Cargo.toml               # Workspace manifest including lib/vector-gate
├── lib/
│   ├── vector-gate/         # Vector Smart Gate ingress crate (Splice, Multi-Gate, Magic Sniffer)
│   ├── vector-core/         # Core Vector pipeline data model and topologies
│   ├── vector-vrl/          # Vector Remap Language compiler & runtime
│   └── ...                  # Codecs, buffers, and protocol definitions
├── src/                     # Main Vector application entrypoint & runtime
└── config/                  # Configuration templates and examples
```

---

## 📄 License

Vector Smart Gate is licensed under the Mozilla Public License 2.0 (MPL-2.0). See [LICENSE](LICENSE) for details.
