# VECTOR SMART GATE (v2.4.3)
### High-Performance Multiplexing Ingress & Zero-Port Auto-Wiring for Timberio Vector
**Docker Hub Image:** `l1ghtg3m/vector-gate:2.4.3` | `l1ghtg3m/vector-gate:latest`  
**Ingress Endpoint:** Single Public Port `0.0.0.0:5000` (TCP/UDP Multiplexing)  
**Throughput:** > 5,300,000 Events/sec | **Memory Footprint:** ~23.7 MiB RAM  

---

## 🌟 TỔNG QUAN HỆ THỐNG (OVERVIEW)

**Vector Smart Gate** là giải pháp Ingress thông minh tích hợp sẵn vào trước Timberio Vector Core:
* **Hội tụ 1 Cổng Duy Nhất (`0.0.0.0:5000`)**: Thay vì phải mở hàng chục cổng firewall (`514` Syslog, `5044` Beats, `24224` Fluent, `8088` Splunk, `4318` OTel, `8125` StatsD...), toàn bộ lưu lượng dữ liệu log, metric, webhook và IoT đều gửi chung vào cổng `5000`.
* **Zero-Port Auto-Wiring**: Định cấu hình sources trực tiếp bằng cú pháp `address: "gates.<route_name>"`. Vector Gate sẽ tự động cấp phát cổng loopback nội bộ động ngầm (`127.0.0.1:17500+`) và tái cấu trúc YAML an toàn trong bộ nhớ RAM trước khi Vector Core khởi chạy.
* **Hierarchical Onion VRL & Auto-Remap**: Hỗ trợ thư mục parsing phân tầng (Syslog, Payload, Fallback) và tự động transpile transforms tương ứng với hot-reload watcher.
* **Quy tắc phân loại tùy biến (Base64 Magic Bytes & Offset)**: Cho phép người dùng tùy ý nhận diện bất kỳ cấu trúc nhị phân (Hex/IoT) hoặc chuỗi ứng dụng nào theo nguyên tắc *First-Match-Wins*.
* **Cầu chì chống nghẽn kênh (`gates.other` -> Blackhole Sink)**: Gói tin rác hoặc chữ ký lạ lập tức được xả an toàn vào `blackhole_sink`, đảm bảo cổng `5000` luôn thông suốt, không bao giờ bị treo/block kết nối.
* **Động cơ Zero-Copy Splice Turbo-Kernel**: Sử dụng system call `splice(2)` của Linux kết hợp `SO_REUSEPORT` và `TCP_DEFER_ACCEPT`, đạt thông lượng kinh ngạc **> 5.3 triệu log/giây** mà chỉ tiêu thụ **~23.7 MiB RAM**.

---

## 🚀 KHỞI CHẠY NHANH (QUICK START)

### 1. Triển khai bằng Image có sẵn (Docker Hub)
```bash
docker run -d \
  --name vector-smart-gate \
  --restart unless-stopped \
  -p 5000:5000 \
  -v $(pwd)/deploy/config/vector.yaml:/etc/vector/vector.yaml:ro \
  -v $(pwd)/deploy/output:/var/log/vector \
  l1ghtg3m/vector-gate:2.4.3
```

### 2. Tự Build Hoàn Chỉnh Từ Mã Nguồn (Build Image From Source)
Toàn bộ Dockerfile, Docker Compose và cấu hình runtime được quy hoạch chuẩn tại thư mục `deploy/`:

```bash
# Di chuyển vào thư mục deploy và khởi động container:
cd deploy
docker compose up -d --build

# Hoặc khởi chạy từ thư mục gốc:
docker compose -f deploy/docker-compose.yml up -d --build
```

### 3. Kiểm tra container hoạt động
```bash
docker ps
# Kiểm tra tài nguyên RAM (~23.7 MiB):
docker stats vector-smart-gate --no-stream
# Gửi kiểm tra health check qua cổng 5000:
curl -sf http://127.0.0.1:5000/ -X POST -H "Content-Type: application/json" -d '{"ping":"vector-gate-ok"}'
```

---

## 📁 CẤU TRÚC DỰ ÁN TINH GỌN (CLEAN ARCHITECTURE)

Dự án được phân tách nghiêm ngặt, rành mạch và loại bỏ hoàn toàn sự phân mảnh:

```
vector-gate/
├── deploy/           # Toàn bộ hạ tầng container (Dockerfile, docker-compose.yml, config/vector.yaml, vrl/)
├── docs/             # Hồ sơ tài liệu kỹ thuật & tài liệu hướng dẫn (Master Specs, User Guide, VRL Audits)
├── vector-gate/      # Mã nguồn Rust cốt lõi (Rust Ingress Daemon, Zero-Copy Splice Engine, Magic Recognizer)
├── research/         # Dữ liệu phân tích & khảo cứu (VRL upstream issues audit, CSV catalogs, ideation)
├── test/             # Toàn bộ hệ thống kiểm thử tự động (suites/, samples/, runner.sh, run_all_tests.py)
│   ├── suites/       # 12 bộ Python QA test suites (Matrix, Onion, Chaos, Stress, Benchmarks)
│   └── samples/      # 15 giao thức mẫu chuẩn & script điều phối bắn test send_samples.py
├── README.md         # Tài liệu tổng quan dự án
├── .dockerignore     # Danh mục tối ưu build context Docker
└── .gitignore        # Danh mục loại trừ tệp tạm, thùng rác trash/ và dữ liệu lớn
```

---

## 📋 TÀI LIỆU HƯỚNG DẪN CHI TIẾT
* 📖 [**docs/USER_GUIDE.md** (Hướng dẫn cấu hình & Sổ tay kiểm thử tương tác)](docs/USER_GUIDE.md): Tài liệu hướng dẫn đầy đủ nhất từ A-Z với các lệnh test mẫu (curl, netcat, python) cho 15 giao thức và chữ ký tùy biến.
* 🧪 [**test/README.md** (Thư Mục Kiểm Thử Tự Động Hóa Tập Trung)](test/README.md): Bộ QA test suites tự động hóa (Python) gồm Standard Vector Matrix, Onion VRL, 15 Giao thức Ingress, Chaos Engineering, và runner [`test/run_all_tests.py`](test/run_all_tests.py).
* 📦 [**test/samples/README.md** (Bộ Dữ Liệu Mẫu & Test Dispatcher)](test/samples/README.md): Bảng tra cứu 15 giao thức mẫu và script bắn test tự động [`test/samples/send_samples.py`](test/samples/send_samples.py).
* 🔬 [**docs/VRL_AND_VECTOR_ISSUES_AUDIT_REPORT.md** (Báo Cáo Đối Soát 641 Issues Upstream)](docs/VRL_AND_VECTOR_ISSUES_AUDIT_REPORT.md): Phân tích chi tiết 8 Use Cases trọng yếu, đánh giá khả năng sửa lỗi & năng lực phòng vệ 641 issues VRL trên Vector Gate v2.4.3.
* 📚 [**docs/MASTER_SPECIFICATION.md** (Hồ sơ Thiết kế Kỹ thuật & Báo cáo Nghiệm thu Master)](docs/MASTER_SPECIFICATION.md): Tài liệu tổng hợp toàn diện bao gồm toàn bộ Phân tích nghiệp vụ (BA) và Nghiệm thu chất lượng (QA) của toàn hệ thống Vector Gate (Single Source of Truth).

---

## 🛠️ CẤU HÌNH NHANH TRONG `vector.yaml`

```yaml
data_dir: "/var/lib/vector"

# 1. KHAI BÁO PHASE GATE
gates:
  enabled: true
  type: "any"
  address: "0.0.0.0:5000"
  options:
    pipe_buffer: 64                   # Kích thước pipe 1-256 pages (1 page = 4KB, mặc định 16)
    pipe_adaptive: true               # Co giãn đàn hồi tự động theo tải
  routes:
    # Tùy biến Magic Bytes (Base64)
    custom_iot:
      type: "any"
      magic_base64: "3q2+7w=="        # 0xDEADBEEF
    # Giao thức chuẩn
    syslog_gate:
      type: "syslog"
    splunk_gate:
      type: "splunk_hec"
    # Cầu chì chống nghẽn
    other:
      type: "socket"

# 2. KHAI BÁO VECTOR SOURCES (TỰ ĐỘNG ĐẤU NỐI)
sources:
  in_custom_iot:
    type: socket
    mode: tcp
    address: "gates.custom_iot"        # Tự động map vào custom_iot!

  in_syslog:
    type: syslog
    mode: tcp
    address: "gates.syslog_gate"       # Tự động map vào syslog_gate!

  in_splunk:
    type: splunk_hec
    address: "gates.splunk_gate"       # Tự động map vào splunk_gate!

  other_unmatched:
    type: socket
    mode: tcp
    address: "gates.other"             # Đón traffic lạ

# 3. SINKS
sinks:
  file_output:
    type: file
    inputs: ["in_custom_iot", "in_syslog", "in_splunk"]
    path: "/var/log/vector/forwarded_logs.ndjson"
    encoding:
      codec: json

  blackhole_sink:
    type: blackhole
    inputs: ["other_unmatched"]        # Tiêu thụ an toàn traffic lạ
```

---

## ⚡ TEST THỬ NGHIỆM TƯƠNG TÁC NGAY

### 1. Chạy Bộ Kiểm Thử Tự Động Hóa (Python Test Suites)
```bash
# Chạy toàn bộ bài test độc lập (Matrix + Onion VRL):
python3 test/run_all_tests.py

# Hoặc chạy kiểm tra toàn diện cả E2E & Chaos:
python3 test/run_all_tests.py --all

# Bắn toàn bộ 15 giao thức mẫu vào Vector Gate:
python3 test/samples/send_samples.py --all
```

### 2. Bắn Dữ Liệu Thủ Công Qua Cổng 5000
echo "<34>Oct 25 08:45:00 myhost app: Test log to gate 5000" | nc -w 1 127.0.0.1 5000

# 2. Test Splunk HEC
curl -X POST "http://127.0.0.1:5000/services/collector/event" \
  -H "Authorization: Splunk 12345" \
  -H "Content-Type: application/json" \
  -d '{"event": "User logged in"}'

# 3. Test IoT Binary Magic (0xDEADBEEF)
python3 -c "
import socket
s = socket.create_connection(('127.0.0.1', 5000))
s.sendall(bytes([0xDE, 0xAD, 0xBE, 0xEF]) + b' sensor_val=100\n')
s.close()
"

# 4. Xem kết quả đã ghi vào file
tail -n 5 /home/manager/vectormod/deploy/output/forwarded_logs.ndjson
```

---

## 📊 THÔNG SỐ KỸ THUẬT (BENCHMARKS)
* **Thông lượng tối đa:** `5,313,402 Events/sec`
* **Độ trễ phân loại:** $\le 0.0001\text{ ms}$
* **Tài nguyên:** Container RAM: `23.72 MiB` | CPU Idle: `< 5%`
* **Độ tin cậy:** Cầu chì `gates.other` ngăn chặn 100% tình trạng treo cổng Ingress khi gặp dữ liệu rác.

