# HƯỚNG DẪN CẤU HÌNH VÀ TƯƠNG TÁC TOÀN DIỆN (VECTOR SMART GATE v2.5.6)
**Tài liệu hướng dẫn người dùng vận hành, thiết lập định tuyến và kiểm thử tương tác**  
**Image Docker Hub:** `l1ghtg3m/vector-gate:2.5.6` (hoặc `l1ghtg3m/vector-gate:latest`)  
**Ingress Port duy nhất:** `0.0.0.0:5000` (TCP/UDP Multiplexing) & Telemetry Port `9100`  

---

## MỤC LỤC
1. [Giới thiệu tổng quan & Lợi ích kiến trúc](#1-giới-thiệu-tổng-quan--lợi-ích-kiến-trúc)
2. [Các khái niệm cốt lõi (Core Concepts)](#2-các-khái-niệm-cốt-lõi-core-concepts)
   - [Zero-Port Auto-Wiring (`address: "gates.<route>"`)](#21-zero-port-auto-wiring-address-gatesroute)
   - [Định tuyến tùy biến với Base64 Magic Bytes & Offset](#22-định-tuyến-tùy-biến-với-base64-magic-bytes--offset)
   - [Cầu chì chống nghẽn kênh (`gates.other` -> Blackhole Sink)](#23-cầu-chì-chống-nghẽn-kênh-gatesother---blackhole-sink)
   - [Danh mục 15 Giao thức Push dựng sẵn](#24-danh-mục-15-giao-thức-push-dựng-sẵn)
3. [Khởi chạy nhanh (Quick Start)](#3-khởi-chạy-nhanh-quick-start)
   - [Cách 1: Khởi chạy bằng Docker CLI](#31-cách-1-khởi-chạy-bằng-docker-cli)
   - [Cách 2: Khởi chạy bằng Docker Compose](#32-cách-2-khởi-chạy-bằng-docker-compose)
   - [Cách 3: Chạy trực tiếp Binary trên Linux](#33-cách-3-chạy-trực-tiếp-binary-trên-linux)
4. [Tài liệu đặc tả cấu hình (`vector.yaml`)](#4-tài-liệu-đặc-tả-cấu-hình-vectoryaml)
   - [Cấu hình mẫu tối giản (Minimal Configuration)](#41-cấu-hình-mẫu-tối-giản-minimal-configuration)
   - [Cấu hình mẫu đầy đủ chuẩn Production (15 Protocols + Custom)](#42-cấu-hình-mẫu-đầy-đủ-chuẩn-production)
5. [Hướng dẫn cấu hình Custom Base64 Magic Bytes](#5-hướng-dẫn-cấu-hình-custom-base64-magic-bytes)
6. [Sổ tay tương tác & Kiểm thử thực tế (Interactive Testing Playbook)](#6-sổ-tay-tương-tác--kiểm-thử-thực-tế-interactive-testing-playbook)
   - [Lệnh kiểm thử giao thức Syslog / CEF / KV Firewall](#61-giao-thức-syslog--firewall-cef-fortinet-cisco)
   - [Lệnh kiểm thử giao thức HTTP (Splunk, Datadog, OTel, Webhook)](#62-giao-thức-http-splunk-datadog-otel-webhook)
   - [Lệnh kiểm thử Beats, Fluent, dnstap, StatsD & Raw Socket](#63-giao-thức-beats-fluent-dnstap-statsd--raw-socket)
   - [Lệnh kiểm thử Chữ ký tùy biến (IoT Binary / Chuỗi App)](#64-chữ-ký-tùy-biến-iot-binary--chuỗi-app)
7. [Kiểm tra hợp lệ & Xử lý sự cố (Troubleshooting)](#7-kiểm-tra-hợp-lệ--xử-lý-sự-cố-troubleshooting)

---

## 1. GIỚI THIỆU TỔNG QUAN & LỢI ÍCH KIẾN TRÚC

### Vấn đề thực tế trong giám sát Log & SIEM
Trong hạ tầng SIEM/SOC và Cloud Observability, việc tiếp nhận dữ liệu từ hàng trăm thiết bị khác nhau (Server Linux, Windows, Firewall Fortinet, Cisco ASA, Kubernetes, Elastic Beats, Fluentbit, Splunk Forwarder, AWS CloudWatch, Datadog...) thường buộc quản trị viên phải:
* Mở hàng chục cổng Firewall khác nhau (`514` cho Syslog, `5044` cho Beats, `24224` cho Fluent, `8088` cho Splunk, `4318` cho OpenTelemetry, `8125` cho StatsD...).
* Phức tạp hóa Network Security Group (NSG), tăng nguy cơ lộ lọt cổng và khó khăn khi cấu hình NAT/Load Balancer.

### Giải pháp Vector Smart Gate v2.2.0
**Vector Smart Gate** tích hợp tầng Ingress thông minh vào trước Vector Core:
* **1 Cổng Ingress Duy Nhất (`5000:5000`)**: Thay thế toàn bộ các cổng riêng biệt. Mọi agent, máy chủ và thiết bị mạng chỉ cần trỏ log về đúng 1 cổng IP:5000.
* **Tự nhận diện giao thức (Polymorphic Disambiguation)**: Gate đọc vài byte đầu tiên của gói tin (Packet Sniffing trong bộ nhớ kernel) để phân loại giao thức chỉ trong $\approx 0.0001\text{ ms}$.
* **Zero-Copy Splice Turbo-Kernel**: Dữ liệu sau khi phân loại được đẩy thẳng qua cơ chế `splice(2)` của Linux Kernel trực tiếp giữa các socket, không sao chép dữ liệu qua User-Space buffer $\rightarrow$ Đạt thông lượng **> 5.3 Triệu Events/giây**.
* **Tài nguyên siêu nhẹ**: Toàn bộ tiến trình chỉ tiêu thụ **~23.7 MiB RAM** (bao gồm cả Gate + Vector Core bên trong).

---

## 2. CÁC KHÁI NIỆM CỐT LÕI (CORE CONCEPTS)

```
                            [ MỌI NGUỒN LOG & METRICS ]
               (Syslog, Beats, Splunk, Datadog, OTel, IoT, Webhook...)
                                        │
                                        ▼  (Gửi về duy nhất 1 cổng)
                          ┌───────────────────────────┐
                          │    0.0.0.0:5000 (Ingress) │
                          └─────────────┬─────────────┘
                                        │ (Zero-Copy Splice / First-Match-Wins)
                        ┌───────────────┴───────────────┐
                        │    VECTOR SMART GATE v2.2.0   │
                        └───────┬───────┬───────┬───────┘
            gates.custom_iot    │       │       │   gates.other
                    ┌───────────┘       │       └───────────┐
                    ▼                   ▼                   ▼
           ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
           │ in_custom_iot   │ │ in_syslog       │ │ other_unmatched │
           │ (127.0.0.1:auto)│ │ (127.0.0.1:auto)│ │ (127.0.0.1:auto)│
           └────────┬────────┘ └────────┬────────┘ └────────┬────────┘
                    │                   │                   │
                    ▼                   ▼                   ▼
           ┌─────────────────────────────────────┐ ┌─────────────────┐
           │  normalize_logs (VRL Transform)     │ │ blackhole_sink  │
           └──────────────────┬──────────────────┘ │ (Zero-Stuck)    │
                              ▼                    └─────────────────┘
           ┌─────────────────────────────────────┐
           │    Sinks (File, Elasticsearch, S3)  │
           └─────────────────────────────────────┘
```

### 2.1. Zero-Port Auto-Wiring (`address: "gates.<route>"`)
Trước đây, bạn phải tự tính toán và gán cổng nội bộ (loopback ports) như `127.0.0.1:15514`, `127.0.0.1:15044` cho từng route và source.  
Với **Zero-Port Auto-Wiring** trong v2.2.0:
1. Bạn chỉ cần đặt tên route trong `gates.routes`:
   ```yaml
   gates:
     routes:
       syslog_gate:
         type: "syslog"
   ```
2. Và trong `sources`, chỉ cần khai báo địa chỉ là `address: "gates.<tên_route>"`:
   ```yaml
   sources:
     in_syslog:
       type: syslog
       mode: tcp
       address: "gates.syslog_gate"    # <-- Không cần quan tâm số port!
   ```
*Vector Gate sẽ tự động cấp phát dải cổng loopback động ngầm (`127.0.0.1:17500+`) và ánh xạ hoàn toàn tự động trước khi Vector Core khởi động.*

### 2.2. Định tuyến tùy biến với Base64 Magic Bytes & Offset
Bạn có thể tự định nghĩa bất kỳ giao thức nhị phân hay chuỗi ký tự nào bằng Base64:
* `magic_base64`: Chuỗi Base64 mã hóa cho mảng bytes bạn muốn khớp.
* `offset`: Vị trí byte bắt đầu so khớp (mặc định là `0` - ngay đầu gói tin).
* `type: "any"`: Đánh dấu đây là quy tắc phân loại tùy biến.

### 2.3. Cầu chì chống nghẽn kênh (`gates.other` -> Blackhole Sink)
Khi thiết bị gửi dữ liệu rác, chuỗi nhị phân không xác định hoặc gói tin bị lỗi mạng:
- Thay vì từ chối hoặc làm treo kết nối TCP trên cổng 5000, Vector Gate sẽ tự động chuyển tiếp dữ liệu này vào route `gates.other`.
- Route `gates.other` được kết nối với `blackhole_sink` trong Vector để tiêu thụ an toàn gói tin rác mà không gây nghẽn đường ống (Zero-Stuck Channel Guarantee).

### 2.4. Danh mục 15 Giao thức Push dựng sẵn
Hệ thống nhận diện sẵn 15 loại giao thức chuẩn chỉ bằng khai báo `type:` trùng khớp với Vector Source:

| `type:` trong Route & Source | Giao thức tương ứng | Dấu hiệu nhận diện tự động (Signature Sniffing) |
| :--- | :--- | :--- |
| `syslog` | Syslog BSD, IETF, CEF, Firewall | Bắt đầu bằng `<PRI>` (ví dụ: `<34>Oct`, `<165>1`, `CEF:`, `%ASA-`) |
| `logstash` | Elastic Beats / Logstash | Byte Lumberjack v2 (`0x32 0x44` hoặc `0x32 0x43`) |
| `fluent` | Fluentd / Fluent-bit Forward | Header MessagePack (`0x93` hoặc `0x92`) |
| `splunk_hec` | Splunk HTTP Event Collector | HTTP Header `Authorization: Splunk ...` |
| `datadog_agent` | Datadog Agent HTTP Intake | HTTP Header `DD-API-KEY: ...` |
| `aws_kinesis_firehose`| AWS Kinesis Firehose HTTP | HTTP Header `X-Amz-Firehose-...` |
| `heroku_logs` | Heroku Logplex Drain | HTTP Header `Logplex-Drain-Token: ...` |
| `prometheus_remote_write`| Prometheus Remote Write | HTTP Path `/api/v1/write` hoặc header Protobuf RW |
| `prometheus_pushgateway` | Prometheus Pushgateway | HTTP Path `/metrics/job/...` |
| `opentelemetry` | OpenTelemetry OTLP HTTP/Protobuf | HTTP Path `/v1/logs`, `/v1/metrics`, `/v1/traces` |
| `vector` | Vector Native Protocol | HTTP/2 gRPC Preface (`PRI * HTTP/2.0\r\n\r\nSM\r\n\r\n`) |
| `statsd` | StatsD & DogStatsD | Cú pháp Metric text (`metric_name:val\|c`, `\|ms`, `\|g`) |
| `dnstap` | dnstap DNS FrameStreams | FrameStreams Control frame (`0x00...0x01...dnstap`) |
| `http_server` | Generic HTTP Webhook | Các request HTTP POST/PUT thông thường |
| `socket` | Raw TCP Socket (NDJSON stream) | Chuỗi JSON NDJSON (`{"key":"value"}\n`) hoặc text thuần |

---

## 3. KHỞI CHẠY NHANH (QUICK START)

### 3.1. Cách 1: Khởi chạy bằng Docker CLI (Đơn giản nhất)
Chỉ cần chạy lệnh sau để kéo Image chính thức từ Docker Hub và gắn file cấu hình của bạn:

```bash
docker run -d \
  --name vector-smart-gate \
  --restart unless-stopped \
  -p 5000:5000 \
  -v $(pwd)/deploy/config/vector.yaml:/etc/vector/vector.yaml:ro \
  -v $(pwd)/deploy/output:/var/log/vector \
  l1ghtg3m/vector-gate:2.2.0
```

Kiểm tra container đang chạy:
```bash
docker ps -f name=vector-smart-gate
# Xem tài nguyên tiêu thụ siêu nhẹ:
docker stats vector-smart-gate --no-stream
```

### 3.2. Cách 2: Khởi chạy bằng Docker Compose
Tạo file `docker-compose.yml`:
```yaml
version: "3.8"

services:
  vector-smart-gate:
    image: l1ghtg3m/vector-gate:2.2.0
    container_name: vector-smart-gate
    restart: unless-stopped
    ports:
      - "5000:5000"
    volumes:
      - ./config/vector.yaml:/etc/vector/vector.yaml:ro
      - ./output:/var/log/vector
    environment:
      - VECTOR_LOG=info
```

Khởi chạy dịch vụ:
```bash
docker compose up -d
# Xem log thời gian thực:
docker compose logs -f
```

### 3.3. Cách 3: Chạy trực tiếp Binary trên Linux
Nếu bạn chạy trên máy chủ Bare-metal hoặc VM Linux:
```bash
# Kiểm tra tính hợp lệ của cấu hình
vector-gate/target/release/vector-gate validate -c /path/to/vector.yaml

# Khởi chạy Gate kiêm Vector Supervisor
vector-gate/target/release/vector-gate run -c /path/to/vector.yaml
```

---

## 4. TÀI LIỆU ĐẶC TẢ CẤU HÌNH (`vector.yaml`)

### 4.1. Cấu hình mẫu tối giản (Minimal Configuration)
Nếu bạn chỉ cần tiếp nhận Syslog và một đường Webhook HTTP:
```yaml
data_dir: "/var/lib/vector"

gates:
  enabled: true
  type: "any"
  address: "0.0.0.0:5000"
  routes:
    my_syslog:
      type: "syslog"
    my_webhook:
      type: "http_server"
    other:
      type: "socket"

sources:
  in_syslog:
    type: syslog
    mode: tcp
    address: "gates.my_syslog"

  in_webhook:
    type: http_server
    address: "gates.my_webhook"

  other_unmatched:
    type: socket
    mode: tcp
    address: "gates.other"

transforms:
  normalize:
    type: remap
    inputs: ["in_*"]
    source: '.received_at = now()'

sinks:
  out_console:
    type: console
    inputs: ["normalize"]
    encoding:
      codec: json

  blackhole:
    type: blackhole
    inputs: ["other_unmatched"]
```

---

### 4.2. Cấu hình mẫu đầy đủ chuẩn Production
*(Trích từ cấu hình chuẩn `deploy/config/vector.yaml` hỗ trợ toàn diện 15 giao thức và 3 quy tắc tùy biến)*

```yaml
data_dir: "/var/lib/vector"

# ==============================================================================
# PHASE 0: GATE CONFIGURATION (TỰ ĐỘNG ĐẤU NỐI & TỰ ĐỘNG PHÂN LOẠI)
# ==============================================================================
gates:
  enabled: true
  type: "any"
  address: "0.0.0.0:5000"

  options:
    zero_copy: true             # Tăng tốc thông lượng qua Linux splice(2)
    reuse_port: true            # Tận dụng SO_REUSEPORT trên đa nhân CPU
    defer_accept: true          # Giảm chuyển đổi ngữ cảnh TCP
    tcp_nodelay: true           # Giảm độ trễ gói tin nhỏ
    inspect_timeout_ms: 200     # Chờ byte đầu tối đa 200ms
    sniff_window_bytes: 512     # Cửa sổ quan sát chữ ký gói tin
    pipe_buffer: 64             # Kích thước đường kính ống pipe theo số page (1 - 256 pages, 1 page = 4KB).
                                # Mặc định là 16 (64KB). Nếu set = 0 hoặc bỏ trống sẽ lấy mặc định 16.
                                # Các ngưỡng gợi ý: 16 (64KB), 64 (256KB), 128 (512KB), 256 (1MB max).
    pipe_adaptive: true         # Tự động co giãn đàn hồi kích thước pipe theo tải thực tế

  routes:
    # 1. Các quy tắc chữ ký tùy biến (First-Match-Wins)
    custom_binary_iot:
      type: "any"
      magic_base64: "3q2+7w=="        # Hex: 0xDEADBEEF (offset = 0)

    custom_app_signature:
      type: "any"
      magic_base64: "TVlMT0c="        # ASCII: "MYLOG" (offset = 0)

    custom_offset_signature:
      type: "any"
      magic_base64: "TUFHSUM="        # ASCII: "MAGIC" tại byte offset thứ 4
      offset: 4

    # 2. 15 Giao thức chuẩn Push (Tên route tương ứng với sources)
    syslog_gate:
      type: "syslog"

    beats_gate:
      type: "logstash"

    fluent_gate:
      type: "fluent"

    splunk_gate:
      type: "splunk_hec"

    datadog_gate:
      type: "datadog_agent"

    firehose_gate:
      type: "aws_kinesis_firehose"

    heroku_gate:
      type: "heroku_logs"

    prom_rw_gate:
      type: "prometheus_remote_write"

    prom_pg_gate:
      type: "prometheus_pushgateway"

    otel_gate:
      type: "opentelemetry"

    vector_gate:
      type: "vector"

    statsd_gate:
      type: "statsd"

    dnstap_gate:
      type: "dnstap"

    http_gate:
      type: "http_server"

    # 3. Cầu chì tự động chống nghẽn kênh
    other:
      type: "socket"

# ==============================================================================
# PHASE 1: VECTOR SOURCES (ĐẤU NỐI QUA CÚ PHÁP: address: "gates.<route>")
# ==============================================================================
sources:
  in_custom_iot:
    type: socket
    mode: tcp
    address: "gates.custom_binary_iot"
    decoding:
      codec: bytes

  in_custom_app:
    type: socket
    mode: tcp
    address: "gates.custom_app_signature"
    decoding:
      codec: bytes

  in_custom_offset:
    type: socket
    mode: tcp
    address: "gates.custom_offset_signature"
    decoding:
      codec: bytes

  in_syslog:
    type: syslog
    mode: tcp
    address: "gates.syslog_gate"

  in_beats:
    type: logstash
    address: "gates.beats_gate"

  in_fluent:
    type: fluent
    mode: tcp
    address: "gates.fluent_gate"

  in_splunk:
    type: splunk_hec
    address: "gates.splunk_gate"

  in_datadog:
    type: datadog_agent
    address: "gates.datadog_gate"

  in_aws_firehose:
    type: aws_kinesis_firehose
    address: "gates.firehose_gate"
    store_access_key: false

  in_heroku:
    type: heroku_logs
    address: "gates.heroku_gate"

  in_prom_rw:
    type: prometheus_remote_write
    address: "gates.prom_rw_gate"
    path: "/api/v1/write"

  in_prom_pg:
    type: prometheus_pushgateway
    address: "gates.prom_pg_gate"

  in_opentelemetry:
    type: opentelemetry
    grpc:
      address: "127.0.0.1:14317"
    http:
      address: "gates.otel_gate"

  in_vector_native:
    type: vector
    address: "gates.vector_gate"

  in_statsd:
    type: statsd
    mode: tcp
    address: "gates.statsd_gate"

  in_dnstap:
    type: dnstap
    mode: tcp
    address: "gates.dnstap_gate"

  in_http:
    type: http_server
    address: "gates.http_gate"
    decoding:
      codec: bytes

  # Terminal Fallback Source đón traffic rác/lạ
  other_unmatched:
    type: socket
    mode: tcp
    address: "gates.other"
    decoding:
      codec: bytes

# ==============================================================================
# PHASE 2 & 3: TRANSFORMS & SINKS
# ==============================================================================
transforms:
  normalize_logs:
    type: remap
    inputs: ["in_*"]
    source: |
      .container_ingest_ts = now()
      .gateway_phase = "gate_any_15_protocols"
      .ingress_port = 5000

sinks:
  # Ghi dữ liệu hợp lệ vào File lưu trữ
  file_output:
    type: file
    inputs: ["normalize_logs"]
    path: "/var/log/vector/forwarded_logs.ndjson"
    encoding:
      codec: json

  # Blackhole Sink: Tiêu thụ an toàn dữ liệu lạ, không nghẽn cổng 5000
  blackhole_sink:
    type: blackhole
    inputs: ["other_unmatched"]
```

---

## 5. HƯỚNG DẪN CẤU HÌNH CUSTOM BASE64 MAGIC BYTES

### Công cụ tạo chuỗi Base64 nhanh trên Linux / Terminal

#### Trường hợp 1: Chữ ký là chuỗi ký tự (ASCII Text)
Ví dụ bạn muốn nhận diện các log bắt đầu bằng `[PROD_LOG]` hoặc `BILLING_EVENT`:
```bash
echo -n "BILLING_EVENT" | base64
# Kết quả: QklMTElOR19FVkVOVA==
```
Cấu hình trong `vector.yaml`:
```yaml
gates:
  routes:
    billing_gate:
      type: "any"
      magic_base64: "QklMTElOR19FVkVOVA=="
```

#### Trường hợp 2: Chữ ký là mã nhị phân Hex (Binary Bytes)
Ví dụ thiết bị IoT gửi 4 bytes magic `0xCA 0xFE 0xBA 0xBE`:
```bash
echo -n -e "\xCA\xFE\xBA\xBE" | base64
# Kết quả: yv66vg==
```
Cấu hình trong `vector.yaml`:
```yaml
gates:
  routes:
    iot_gate:
      type: "any"
      magic_base64: "yv66vg=="
```

#### Trường hợp 3: Bỏ qua Header độ dài và so khớp tại Offset
Ví dụ giao thức ngân hàng có 4 bytes header độ dài gói tin, tiếp theo là mã chữ ký `ISO8583`:
```bash
echo -n "ISO8583" | base64
# Kết quả: SVNPODU4Mw==
```
Cấu hình trong `vector.yaml`:
```yaml
gates:
  routes:
    bank_gate:
      type: "any"
      magic_base64: "SVNPODU4Mw=="
      offset: 4                        # Bỏ qua 4 bytes đầu, bắt đầu khớp từ byte 4
```

---

## 6. SỔ TAY TƯƠNG TÁC & KIỂM THỬ THỰC TẾ (INTERACTIVE TESTING PLAYBOOK)

Tất cả các lệnh kiểm thử dưới đây đều gửi trực tiếp vào duy nhất cổng `127.0.0.1:5000`.

### 6.1. Giao thức Syslog & Firewall (CEF, Fortinet, Cisco)

* **Gửi Syslog RFC 3164 (BSD):**
  ```bash
  echo "<34>Oct 25 08:30:00 srv01 kernel: Out of memory test log" | nc -w 1 127.0.0.1 5000
  ```

* **Gửi Syslog RFC 5424 (IETF):**
  ```bash
  echo '<165>1 2026-10-25T08:30:00Z web01 nginx 1234 ID47 [exampleSDID@32473 iut="3"] User login success' | nc -w 1 127.0.0.1 5000
  ```

* **Gửi Check Point CEF:**
  ```bash
  echo "<134>1 2026-10-25T08:30:00Z fw01 CEF:0|Check Point|VPN-1|1.0|drop|Connection Dropped|act=drop src=10.0.0.1" | nc -w 1 127.0.0.1 5000
  ```

* **Gửi Fortinet FortiGate KV:**
  ```bash
  echo '<189>date=2026-10-25 time=08:30:00 devname="FGT-100D" logid="0001" type="traffic" action="deny"' | nc -w 1 127.0.0.1 5000
  ```

* **Gửi Cisco ASA Firewall:**
  ```bash
  echo "<166>Oct 25 2026 08:30:00: %ASA-6-302013: Built inbound TCP connection 9999 for outside:1.2.3.4/80" | nc -w 1 127.0.0.1 5000
  ```

---

### 6.2. Giao thức HTTP (Splunk, Datadog, OTel, Webhook)

* **Splunk HEC (HTTP Event Collector):**
  ```bash
  curl -s -X POST "http://127.0.0.1:5000/services/collector/event" \
    -H "Authorization: Splunk 12345678-1234-1234-1234-123456789012" \
    -H "Content-Type: application/json" \
    -d '{"event": "User logged out", "sourcetype": "access_combined"}'
  ```

* **Datadog Agent HTTP Intake:**
  ```bash
  curl -s -X POST "http://127.0.0.1:5000/v1/input" \
    -H "DD-API-KEY: my-datadog-key" \
    -H "Content-Type: application/json" \
    -d '[{"message": "Payment processed successfully", "service": "payment-api"}]'
  ```

* **AWS Kinesis Firehose HTTP:**
  ```bash
  curl -s -X POST "http://127.0.0.1:5000/" \
    -H "X-Amz-Firehose-Request-Id: req-001" \
    -H "X-Amz-Firehose-Protocol-Version: 1.0" \
    -H "Content-Type: application/json" \
    -d '{"requestId": "req-001", "records": [{"data": "SGVsbG8gRmlyZWhvc2U="}]}'
  ```

* **Heroku Logplex HTTPS Drain:**
  ```bash
  curl -s -X POST "http://127.0.0.1:5000/events" \
    -H "Logplex-Drain-Token: secret-token" \
    -H "Logplex-Msg-Count: 1" \
    -H "Content-Type: application/logplex-1" \
    -d '83 <40>1 2026-10-25T08:30:00+00:00 app web.1 - - Starting Puma web server\n'
  ```

* **OpenTelemetry OTLP HTTP:**
  ```bash
  curl -s -X POST "http://127.0.0.1:5000/v1/logs" \
    -H "Content-Type: application/x-protobuf" \
    --data-binary @/dev/null
  ```

* **Prometheus Pushgateway:**
  ```bash
  curl -s -X POST "http://127.0.0.1:5000/metrics/job/backup_job" \
    --data-binary $'# TYPE backup_duration_seconds gauge\nbackup_duration_seconds 42.5\n'
  ```

* **Generic HTTP Webhook:**
  ```bash
  curl -s -X POST "http://127.0.0.1:5000/" \
    -H "Content-Type: application/json" \
    -d '{"event": "github_push", "repository": "vector-gate", "commit": "v2.2.0"}'
  ```

---

### 6.3. Giao thức Beats, Fluent, dnstap, StatsD & Raw Socket

* **StatsD / DogStatsD Metrics:**
  ```bash
  echo "api.orders.total:1|c|#environment:production" | nc -w 1 127.0.0.1 5000
  ```

* **Raw TCP Socket (NDJSON log stream):**
  ```bash
  echo '{"user_id": 999, "action": "checkout", "total": 150.0}' | nc -w 1 127.0.0.1 5000
  ```

---

### 6.4. Chữ ký tùy biến (IoT Binary / Chuỗi App)

* **Gửi gói tin nhị phân IoT (`0xDEADBEEF`):**
  ```bash
  python3 -c "
  import socket
  s = socket.create_connection(('127.0.0.1', 5000))
  s.sendall(bytes([0xDE, 0xAD, 0xBE, 0xEF]) + b' iot_sensor_temp=32.5C\n')
  s.close()
  print('Đã gửi IoT binary packet thành công!')
  "
  ```

* **Gửi chuỗi chữ ký App (`MYLOG:`):**
  ```bash
  echo "MYLOG:2026-10-25:DB_BACKUP_COMPLETED" | nc -w 1 127.0.0.1 5000
  ```

* **Kiểm chứng dữ liệu đã lưu vào đĩa:**
  ```bash
  tail -n 10 /home/manager/vectormod/deploy/output/forwarded_logs.ndjson
  ```

---

## 7. KIỂM TRA HỢP LỆ & XỬ LÝ SỰ CỐ (TROUBLESHOOTING)

### 7.1. Lệnh kiểm tra cấu hình trước khi chạy (Syntax Validation)
Trước khi reload container, bạn có thể kiểm tra cú pháp cấu hình an toàn bằng lệnh:
```bash
docker exec -it vector-smart-gate vector-gate validate -c /etc/vector/vector.yaml
```
Kết quả thành công sẽ hiển thị danh sách tất cả các route đã được tự động đấu nối và thông báo:
```text
✅ Gate Phase 0: Enabled (type: 'any', address: 0.0.0.0:5000)
📋 Active Routes: 18 configured
...
✅ Vector Core topology is valid!
🎉 All phases (Gate + Vector) validation PASSED successfully.
```

### 7.2. Các lỗi thường gặp và cách khắc phục

| Hiện tượng | Nguyên nhân | Cách khắc phục |
| :--- | :--- | :--- |
| **Gửi gói tin lạ bị mất log** | Gói tin không khớp quy tắc nào và rơi vào `gates.other` | Đây là tính năng an toàn để chống nghẽn kênh. Nếu muốn lưu trữ gói tin này, bạn chỉ cần nối `other_unmatched` vào sink lưu trữ thay vì `blackhole_sink`. |
| **Port 5000 đã bị chiếm dụng** | Có tiến trình khác trên Host đang bind `5000` | Đổi port map bên ngoài: `-p 5001:5000` hoặc kiểm tra bằng `netstat -tlpn \| grep 5000`. |
| **Không nhận diện được Base64 Magic** | Mã hóa Base64 bị thừa ký tự newline (`\n`) | Luôn sử dụng flag `echo -n` khi encode Base64 trên shell terminal. |
| **OpenTelemetry báo 405 Method Not Allowed** | Endpoint không đúng | OpenTelemetry OTLP HTTP lắng nghe tại `/v1/logs`, `/v1/metrics`, `/v1/traces`. |

---
**Vector Smart Gate v2.2.0** — Thiết kế và tối ưu cho quy mô lớn, siêu nhẹ và an toàn tuyệt đối.



---

## 8. HƯỚNG DẪN CÁC TÍNH NĂNG MỚI (ENTERPRISE RELEASE v2.5.6)

### 8.1. Thu thập Prometheus Metrics thời gian thực (Native Exporter)
Vector Gate v2.5.6 tích hợp sẵn bộ phát sinh Prometheus Metrics dạng text format chuẩn OpenMetrics:

**Cách 1: Scrape trực tiếp qua cổng Ingress 5000**
```bash
curl http://127.0.0.1:5000/metrics
```
*Không cần mở thêm bất kỳ port nào trên firewall.*

**Cách 2: Scrape qua cổng Dedicated Telemetry 9100**
```bash
curl http://127.0.0.1:9100/metrics
```
*Cổng chuẩn để tích hợp trực tiếp vào Prometheus `scrape_configs` hoặc Datadog/Grafana Agent.*

**Mẫu kết quả trả về:**
```text
# HELP vector_gate_total_connections_total Total client TCP connections accepted by Vector Gate
# TYPE vector_gate_total_connections_total counter
vector_gate_total_connections_total 12840
# HELP vector_gate_protocol_connections_total Connections classified by protocol
# TYPE vector_gate_protocol_connections_total counter
vector_gate_protocol_connections_total{protocol="syslog"} 8512
vector_gate_protocol_connections_total{protocol="beats"} 3140
vector_gate_protocol_connections_total{protocol="http"} 1188
# HELP vector_gate_uptime_seconds Process uptime in seconds
# TYPE vector_gate_uptime_seconds gauge
vector_gate_uptime_seconds 43200
```

### 8.2. Kiểm tra sức khỏe Gate siêu tốc (`/gate_health`)
Dành cho Kubernetes Liveness/Readiness probe hoặc Docker healthcheck:
```bash
curl http://127.0.0.1:5000/gate_health
# Trả về: {"status":"healthy","engine":"vector-smart-gate","uptime_sec":43200}
```

### 8.3. Bật bảo toàn IP Nguồn (Transparent IP / Linux TPROXY)
Để Vector Core và SIEM nhận diện chính xác IP nguồn của client (thay vì `127.0.0.1`):
1. Trong file `deploy/docker-compose.yml`, bổ sung `cap_add: [NET_ADMIN]`.
2. Trong cấu hình `options:`, thiết lập `transparent_ip: true`:
   ```yaml
   gates:
     main_gate:
       address: "0.0.0.0:5000"
       options:
         transparent_ip: true
   ```

### 8.4. Gửi Syslog RFC 6587 (Octet-Counted Framing)
Hệ thống hỗ trợ chuẩn Syslog octet-counted framing theo RFC 6587:
```bash
echo -ne "105 <14>1 2026-10-26T12:00:00Z myhost myapp 1234 - - Event log message formatted via RFC 6587 octet counting\n" | nc 127.0.0.1 5000
```

### 8.5. Tự Động Khám Phá Lược Đồ Cho Thiết Bị Lạ (Schema Auto-Discovery)
Đối với các thiết bị mạng hoặc ứng dụng mới chưa có bộ giải mã (parser) riêng:
- Nếu log gửi đến là JSON (ví dụ: `{"app":"billing","amount":500}`), Gate sẽ tự động phân rã vào root và gán `_auto_discovered_format = "json"`.
- Nếu log gửi đến là Key-Value (ví dụ: `src=10.0.0.1 dst=8.8.8.8 action=drop`), Gate sẽ tự động phân rã thành các trường riêng biệt và gán `_auto_discovered_format = "key_value"`.
- Log hoàn toàn không bị mất mát hay rơi vào lỗi unparsed!

---
**Vector Smart Gate v2.5.6 Enterprise Release** — Nền tảng Log Gateway Toàn Năng, Hiệu Năng Tối Thượng và Thích Ứng Động Toàn Diện.
