# ĐẶC TẢ PHÂN TÍCH NGHIỆP VỤ & THIẾT KẾ KỸ THUẬT (BA SPECIFICATION)
## DỰ ÁN: BẢNG ĐỊNH TUYẾN ĐA HÌNH HỢP NHẤT CHO VECTOR SMART GATE (UNIFIED DECLARATIVE ROUTING ENGINE)
### Tối Giản Hóa Cấu Hình YAML, Hợp Nhất Chữ Ký Base64 & 15 Giao Thức Chuẩn Trên Cổng `0.0.0.0:5000`

---

| **Thuộc tính** | **Giá trị chi tiết** |
|---|---|
| **Tên tài liệu** | Business Architecture & Technical Specification: Unified Declarative Routing Engine |
| **Mã dự án** | `VECTOR-GATE-UNIFIED-ROUTING` |
| **Phiên bản** | `v2.0 - Final Draft for Approval` |
| **Ngày lập** | 25/10/2026 |
| **Tác giả** | Antigravity AI Senior Architect (Pair-programming with @HelloKittyXamKinLung) |
| **Mục tiêu cốt lõi** | Xóa bỏ hoàn toàn sự phân mảnh cấu hình giữa `custom_rules` và `routing.xxx_target`, hợp nhất $100\%$ các quy tắc phân loại thành một bảng `routes:` duy nhất siêu tinh gọn, hỗ trợ song song **chuỗi Base64 tự định nghĩa** và **15 giao thức chuẩn dựng sẵn**, áp dụng quy tắc **First-Match-Wins** với **offset mặc định bằng 0**. |

---

## 1. TỔNG QUAN BỐI CẢNH & ĐỘNG LỰC CẢI TIẾN (EXECUTIVE SUMMARY)

### 1.1. Hiện Trạng & Vấn Đề (Pain Points of Current Architecture)
Trong phiên bản v1.1.0 hiện tại:
* Cấu hình Gate bị xé nhỏ thành 2 khối độc lập:
  ```yaml
  gate:
    custom_rules:      # Khối 1: Danh sách custom rule mảng động
      - name: "..."
        magic_base64: "..."
        offset: 0
        target: "..."
    routing:           # Khối 2: 15 trường cố định dạng phẳng
      syslog_target: "127.0.0.1:15514"
      beats_target:  "127.0.0.1:15044"
      ... (13 dòng tiếp theo)
  ```
* **Các điểm bất cập nghiêm trọng đối với người dùng (UX Debt)**:
  1. **Cực kỳ phức tạp và rườm rà**: Người dùng phải khai báo hoặc nhìn thấy danh sách 15 target ngay cả khi hệ thống của họ chỉ dùng 2-3 loại log.
  2. **Bất đối xứng về mặt tư duy (Mental Model Mismatch)**: Về bản chất, cả 15 giao thức dựng sẵn và các rule custom đều làm cùng một nhiệm vụ: *"Nếu dữ liệu có đặc điểm X $\rightarrow$ chuyển tiếp tới cổng Y"*. Việc tách thành 2 cấu trúc khác nhau làm tăng độ phức tạp không đáng có.
  3. **Không kiểm soát được thứ tự ưu tiên (Implicit vs Explicit Priority)**: Thứ tự so khớp giữa Custom Rules và các giao thức mặc định bị cố định trong mã nguồn Rust, người dùng không thể can thiệp thứ tự ưu tiên trực quan trên file cấu hình.

### 1.2. Mục Tiêu Cải Tiến Của Bản Thiết Kế v2.0
* **Hợp nhất thành một khối `routes:` duy nhất (Unified Array)**: Toàn bộ routing chỉ là một mảng tuần tự.
* **Đa hình (Polymorphic Match)**: Mỗi route có thể nhận diện qua:
  - `magic_base64`: Chuỗi Base64 nhị phân do người dùng nhập.
  - `match`: Từ khóa giao thức dựng sẵn (`"syslog"`, `"beats"`, `"splunk_hec"`, `"http"`, `"raw"`, ...).
* **Zero Boilerplate**:
  - `offset`: **Mặc định là 0** nếu không điền.
  - `name`: Tùy chọn (tự sinh tên nếu không đặt).
* **Khai báo theo nhu cầu (On-Demand Only)**: Dùng loại nào khai báo loại đó, không ép buộc khai báo thừa.
* **First-Match-Wins**: Thứ tự viết trong YAML chính là thứ tự Gate quét kiểm tra.

---

## 2. NGUYÊN TẮC THIẾT KẾ & ĐẶC TẢ CẤU HÌNH (SPECIFICATION SCHEMA)

### 2.1. Cấu Trúc Khai Báo Route Chi Tiết

Mỗi phần tử trong mảng `routes:` tuân thủ lược đồ sau:

```yaml
gate:
  enabled: true
  type: "any"
  address: "0.0.0.0:5000"

  routes:
    # Trường hợp A: Custom Rule qua chuỗi Base64 (offset tự hiểu là 0)
    - name: "my_iot_sensor"           # [Tùy chọn] Tên hiển thị
      magic_base64: "3q2+7w=="        # [Nhận diện A] 4 byte: 0xDEADBEEF
      target: "127.0.0.1:17001"       # [Bắt buộc] Địa chỉ backend đích

    # Trường hợp B: Custom Rule có Offset khác 0
    - name: "iso8583_banking"
      magic_base64: "TUFHSUM="        # [Nhận diện A] Chuỗi "MAGIC"
      offset: 4                       # [Tùy chọn] Bỏ qua 4 byte độ dài đầu
      target: "127.0.0.1:17002"

    # Trường hợp C: Giao thức dựng sẵn (Predefined Type)
    - match: "syslog"                 # [Nhận diện B] Từ khóa giao thức chuẩn
      target: "127.0.0.1:15514"

    # Trường hợp D: Fallback cho mọi kết nối TCP không xác định
    - match: "raw"                    # [Nhận diện B] Fallback catch-all
      target: "127.0.0.1:15515"
```

### 2.2. Danh Mục Từ Khóa Giao Thức Dựng Sẵn (`match: <keyword>`)

Hệ thống hỗ trợ sẵn 15 từ khóa tương ứng $1:1$ với toàn bộ danh mục PUSH trong `vector_sources.csv`:

| Từ khóa `match` | Tên nguồn Vector | Cơ chế nhận diện tự động trong Gate |
| :--- | :--- | :--- |
| `syslog` | `syslog` | Byte đầu là `<` (`0x3C`), bao gồm BSD (RFC 3164), IETF (RFC 5424), CEF, Fortinet KV, Cisco ASA. |
| `beats` (hoặc `logstash`) | `logstash` | Magic byte `0x32 0x44` (v2) hoặc `0x31` (v1) của Lumberjack. |
| `fluent` | `fluent` | Header MessagePack `0x92..=0x94`. |
| `splunk_hec` | `splunk_hec` | HTTP POST tới đường dẫn `/services/collector*` hoặc header `Splunk`. |
| `datadog` (hoặc `datadog_agent`) | `datadog_agent` | HTTP POST tới `/v1/input*`, `/api/v1/logs`, `/api/v2/logs` hoặc header `DD-API-KEY`. |
| `aws_firehose` | `aws_kinesis_firehose` | HTTP POST chứa header `X-Amz-Firehose-*` hoặc path `/aws/firehose`. |
| `heroku` (hoặc `heroku_logs`) | `heroku_logs` | HTTP POST tới `/events` hoặc chứa header `Logplex-Drain-Token`, User-Agent `Logplex`. |
| `prom_remote_write` | `prometheus_remote_write` | HTTP POST tới `/api/v1/write*` hoặc header `Content-Encoding: snappy`. |
| `prom_pushgateway` | `prometheus_pushgateway` | HTTP POST tới `/metrics/job/*`. |
| `opentelemetry` (hoặc `otel`) | `opentelemetry` | HTTP POST tới `/v1/logs`, `/v1/metrics`, `/v1/traces` hoặc header gRPC OTLP. |
| `vector` (hoặc `vector_native`) | `vector` | HTTP/2 gRPC Connection Preface (`PRI * HTTP/2.0\r\n\r\nSM\r\n\r\n`). |
| `statsd` | `statsd` | Cú pháp Metric dòng text chứa dấu `:` và các đuôi `\|c`, `\|g`, `\|ms`, `\|h`, `\|s`. |
| `dnstap` | `dnstap` | FrameStreams control frame bắt đầu bằng `0x00 0x00 0x00 0x00`. |
| `http` (hoặc `generic_http`) | `http_server` | Bất kỳ request HTTP/1.x nào khác (`POST /`, `GET /`, Webhooks REST). |
| `raw` (hoặc `socket`, `default`) | `socket` | Mọi luồng TCP stream thô còn lại (NDJSON, CSV, Auditd, Suricata, Zeek, Netcat). |

---

## 3. SO SÁNH TRỰC QUAN: BEFORE VS AFTER

```carousel
### ❌ TRƯỚC (v1.1.0): 35+ dòng, phân mảnh 2 khối
```yaml
gate:
  enabled: true
  type: "any"
  address: "0.0.0.0:5000"
  custom_rules:
    - name: "custom_binary_iot"
      magic_base64: "3q2+7w=="
      offset: 0
      target: "127.0.0.1:15515"
    - name: "custom_app_signature"
      magic_base64: "TVlMT0c="
      offset: 0
      target: "127.0.0.1:15515"
  routing:
    syslog_target: "127.0.0.1:15514"
    beats_target: "127.0.0.1:15044"
    fluent_target: "127.0.0.1:24224"
    splunk_target: "127.0.0.1:18088"
    datadog_target: "127.0.0.1:18282"
    aws_firehose_target: "127.0.0.1:18443"
    heroku_target: "127.0.0.1:18084"
    prom_remote_write_target: "127.0.0.1:19090"
    prom_pushgateway_target: "127.0.0.1:19091"
    opentelemetry_target: "127.0.0.1:14318"
    vector_native_target: "127.0.0.1:16000"
    statsd_target: "127.0.0.1:18125"
    dnstap_target: "127.0.0.1:15516"
    http_target: "127.0.0.1:18080"
    raw_target: "127.0.0.1:15515"
```
<!-- slide -->
### ✅ SAU (v2.0): Thống nhất 1 cụm, On-Demand, First-Match-Wins
```yaml
gate:
  enabled: true
  address: "0.0.0.0:5000"

  routes:
    # 1. Custom magic bytes (offset mặc định = 0)
    - name: "iot_payload"
      magic_base64: "3q2+7w=="
      target: "127.0.0.1:17001"

    # 2. Giao thức dựng sẵn (chỉ khai báo cái nào cần dùng)
    - match: "syslog"
      target: "127.0.0.1:15514"

    - match: "beats"
      target: "127.0.0.1:15044"

    - match: "http"
      target: "127.0.0.1:18080"

    # 3. Catch-all fallback
    - match: "raw"
      target: "127.0.0.1:15515"
```
````

---

## 4. KIẾN TRÚC THỰC THI TRONG RUST ENGINE (`raproxy`)

```mermaid
flowchart TD
    Client["Client / Agent Connection\n(Port 5000)"] --> Kernel["Linux Socket: SO_REUSEPORT + TCP_DEFER_ACCEPT"]
    Kernel --> Peek["Peek Buffer (First 512 bytes)"]
    
    subgraph Engine["UNIFIED ROUTE DISPATCHER (FIRST-MATCH-WINS)"]
        direction TB
        R1{"Route 1: Match?"}
        R2{"Route 2: Match?"}
        R3{"Route 3: Match?"}
        RN{"Route N: Match?"}
        
        R1 -->|No| R2
        R2 -->|No| R3
        R3 -->|No| RN
    end

    Peek --> R1
    
    R1 -->|Yes| T1["Target 1 (IP:Port)"]
    R2 -->|Yes| T2["Target 2 (IP:Port)"]
    R3 -->|Yes| T3["Target 3 (IP:Port)"]
    RN -->|Yes| TN["Target N (IP:Port)"]
    
    T1 & T2 & T3 & TN --> Pipe["Linux Zero-Copy splice(2) Pipe Bridge"]
    Pipe --> VectorBackend["Vector Internal Listeners / Sinks"]
```

### 4.1. Cơ Chế Khớp Lệnh (Matching Logic)
1. **Khởi tạo (Startup phase)**:
   - File cấu hình `vector.yaml` được nạp vào struct Rust:
     ```rust
     pub enum RouteCondition {
         MagicBytes {
             bytes: Vec<u8>,
             offset: usize,
         },
         Predefined(PredefinedProtocol),
     }

     pub struct UnifiedRoute {
         pub name: String,
         pub condition: RouteCondition,
         pub target: SocketAddr,
     }
     ```
   - Tất cả chuỗi `magic_base64` được giải mã sẵn ra `Vec<u8>` tại thời điểm nạp, kiểm tra tính hợp lệ (độ dài $1 \le n \le 64$ bytes, offset $\le 256$).
   - Nếu `offset` bị bỏ trống trong YAML, serde tự động gán mặc định `offset = 0`.
2. **Xử lý gói tin thời gian thực (Zero Latency Dispatch)**:
   - Khi có kết nối TCP đến, worker thread thực hiện duyệt tuần tự mảng `routes`:
     - Nếu route là `MagicBytes`: So sánh slice `&buf[offset .. offset + len] == &bytes[..]`. Tốn $\le 3\text{ ns}$ nhờ lệnh CPU SIMD.
     - Nếu route là `Predefined`: Gọi bộ sniffer tương ứng (ví dụ kiểm tra `<` cho Syslog, `0x32` cho Beats, method/path cho HTTP).
     - **Ngay khi tìm thấy route đầu tiên khớp $\rightarrow$ Dừng duyệt và chuyển tiếp ngay tới `target`!**
3. **Hiệu năng & Tài nguyên**:
   - Độ phức tạp thời gian: $O(K)$ với $K$ là số route được khai báo (thông thường $K \le 20$), tổng thời gian ra quyết định định tuyến $< 50\text{ nanoseconds}$.
   - Duy trì thông lượng đỉnh: **$\ge 7,000,000 \text{ EPS}$**.
   - Bộ nhớ RAM tiêu thụ: **$\le 5 \text{ MB}$** cho engine Gate.

---

## 5. KẾ HOẠCH TRIỂN KHAI & TIÊU CHÍ NGHIỆM THU (QA/QC ACCEPTANCE CRITERIA)

| Mã tiêu chí | Tên kịch bản kiểm thử | Kỳ vọng đạt được |
| :---: | :--- | :--- |
| **AC-01** | **Base64 không cần điền offset** | Cấu hình `magic_base64: "3q2+7w=="` không có offset, Gate tự hiểu offset = 0 và định tuyến chính xác. |
| **AC-02** | **Base64 có offset tùy biến** | Cấu hình `magic_base64: "TUFHSUM="`, `offset: 4`, Gate bỏ qua 4 byte đầu và match chính xác từ byte thứ 5. |
| **AC-03** | **Predefined Protocols** | Cấu hình các route `match: "syslog"`, `match: "beats"`, `match: "http"`, Gate tự động kích hoạt bộ sniffer tương ứng. |
| **AC-04** | **Thứ tự First-Match-Wins** | Đặt Custom Rule đè lên trước Syslog (ví dụ nhận diện log đặc biệt bắt đầu bằng `<CUSTOM>`), Gate phải chuyển vào target Custom thay vì target Syslog. |
| **AC-05** | **Cấu hình On-Demand rút gọn** | Khai báo file YAML chỉ có đúng 3 dòng route, Gate khởi động thành công, không đòi hỏi 15 target mặc định. |
| **AC-06** | **Tương thích ngược Vector Core** | Hàm `sanitized_vector_yaml()` tự động bóc tách sạch khối `gate:` mới, Vector Core khởi động trơn tru không lỗi schema. |
| **AC-07** | **Hiệu năng & Bền vững** | Bơm 20,000 logs liên tục, kiểm tra Zero-Copy Splice vẫn đạt $\ge 5,000,000 \text{ EPS}$ và RAM container $\le 25 \text{ MB}$. |

---

## 6. ĐỀ XUẤT HÀNH ĐỘNG TIẾP THEO (NEXT STEPS)

Sau khi bạn xem xét và phê duyệt bản đặc tả BA này, tôi sẽ thực hiện ngay:
1. **Refactor mã nguồn `raproxy`**: Chuyển đổi toàn bộ cấu trúc sang `UnifiedRoute` và mảng `routes:`.
2. **Cập nhật `vector.yaml`**: Viết lại cấu hình mới siêu tinh gọn theo chuẩn BA.
3. **Biên dịch Release & Đóng gói Docker Image v2.0.0**: Tag `l1ghtg3m/vector-gate:latest` và `2.0.0`.
4. **Chạy bộ kiểm thử QA toàn diện**: Đảm bảo $100\%$ Test Cases ĐẠT chuẩn.
5. **Đẩy image lên Docker Hub & Báo cáo kết quả trực tiếp qua Telegram**.

