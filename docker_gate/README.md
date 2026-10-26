# VECTOR SMART GATE CONTAINER (v2.4.2)
## CẨM NANG VẬN HÀNH & HƯỚNG DẪN SỬ DỤNG TOÀN DIỆN
### "Mô Hình Củ Hành (Hierarchical VRL Onion Engine) — Khai Báo Rõ Ràng `type: auto_remap` Với Tham Số Bắt Buộc `dir:`"

---

## 1. TỔNG QUAN HỆ THỐNG
**Vector Smart Gate v2.4.2** giải quyết triệt để 3 bài toán lớn nhất của hạ tầng thu thập log:
1. **Cổng tiếp nhận duy nhất (Port 5000)**: Mọi log (Syslog, HTTP, Beats, Fluent, Splunk, Datadog...) đổ chung vào một cổng `5000:5000`. Gate tự động nhận diện chữ ký ở Tầng 4 bằng Linux Kernel `splice(2)` với tốc độ **8.48 triệu EPS**, độ trễ chỉ 118 ns.
2. **Khai báo `type: auto_remap` với tham số bắt buộc `dir:`**:
   - `type: auto_remap` (hoặc `type: autoremap`): Bắt buộc khai báo `dir: "<thư_mục_vrl>"`. RAPROXY sẽ tự động quét toàn bộ quy tắc VRL trong thư mục đó, biên dịch cây quyết định AST $O(1)$, và chuyển đổi sang chuẩn `type: remap` của Vector.
   - `type: remap`: Chuẩn remap gốc của Vector Core được giữ nguyên vẹn 100%, không bị can thiệp.
   - **Khả năng đa thể hiện (Multi-instance)**: Bạn có thể tạo nhiều transform `auto_remap` độc lập trỏ tới các thư mục khác nhau (VD: `network_rules`, `application_rules`).
   - **Tương thích thư mục phẳng (Flat) & phân cấp (Hierarchical)**: Thư mục `dir:` có thể chia thành các thư mục con `syslog/`, `http/`, `payload/`, hoặc để file phẳng kèm frontmatter `# scope:`.
3. **Mô hình Củ Hành (The Onion Peeler)**: Tách rời vỏ giao thức (Syslog/HTTP Header) khỏi ruột dữ liệu. Bạn chỉ cần viết **1 file VRL duy nhất** trong `payload/` (như `nginx.vrl`) là tự động phân giải thành công log bất kể log đó gửi qua HTTP POST hay Syslog!

---

## 2. BẢN ĐỒ THƯ MỤC
```text
docker_gate/
├── docker-compose.yml       # Khởi chạy dịch vụ container (image: l1ghtg3m/vector-gate:2.4.2)
├── Dockerfile               # Đóng gói image l1ghtg3m/vector-gate:2.4.2
├── config/
│   └── vector.yaml          # File cấu hình tổng (Gate, Sources, Transforms auto_remap, Sinks)
├── vrl/                     # THƯ MỤC QUY TẮC PARSE (CHỈ ĐỊNH TRONG dir:)
│   ├── syslog/              # Rule riêng cho Syslog (Fortinet, Cisco ASA, CEF...)
│   ├── http/                # Rule riêng cho Webhook qua HTTP POST
│   ├── payload/             # Rule DÙNG CHUNG cho cả HTTP lẫn Syslog (Nginx, JSON...)
│   └── 99_dead_letter_fallback.vrl # Chốt chặn bắt log lạ (Zero-loss)
├── bin/
│   └── vector-gate          # Binary thực thi Rust (RAPROXY Engine)
└── output/
    └── forwarded_logs.ndjson # File lưu trữ log sau khi bóc tách chuẩn hóa
```

---

## 3. CẤU HÌNH `auto_remap` TRONG `vector.yaml`
```yaml
transforms:
  # ============================================================================
  # 1. TRANSFORM AUTO-REMAP (BẮT BUỘC CÓ THUỘC TÍNH dir:)
  # ============================================================================
  universal_parser:
    type: auto_remap                  # Nhận diện tự động: auto_remap / autoremap
    inputs: ["tag_*"]                 # Nhận luồng từ các tag sources
    dir: "/etc/vector/vrl"            # [BẮT BUỘC] Thư mục chứa các script VRL!

  # ============================================================================
  # 2. TRANSFORM REMAP TIÊU CHUẨN CỦA VECTOR (GIỮ NGUYÊN 100%)
  # ============================================================================
  custom_tagger:
    type: remap                       # Vector standard remap (RAPROXY không can thiệp)
    inputs: ["universal_parser"]
    source: |
      .processed_at = now()
```

---

## 4. KHỞI CHẠY NHANH 3 BƯỚC

### Bước 1: Khởi động container
```bash
cd /home/manager/vectormod/docker_gate
docker compose up -d
# hoặc:
docker run -d --name vector-smart-gate -p 5000:5000 \
  -v ./config/vector.yaml:/etc/vector/vector.yaml:ro \
  -v ./vrl:/etc/vector/vrl \
  -v ./output:/var/log/vector \
  l1ghtg3m/vector-gate:2.4.2
```

### Bước 2: Bắn log thử nghiệm vào cổng 5000
```bash
# 1. Gửi log Nginx qua HTTP:
curl -X POST http://127.0.0.1:5000/ \
  -d '192.168.1.100 - - [25/Oct/2026:12:00:00 +0000] "GET /api/v1/users HTTP/1.1" 200 452'

# 2. Gửi log FortiGate qua Syslog (TCP):
echo '<189>Oct 25 12:00:00 fgt01 date=2026-10-25 time=12:00:00 devname="FGT60D" type="traffic" srcip=10.0.0.50 dstip=8.8.8.8 proto=6 action="accept"' | nc -w 1 127.0.0.1 5000

# 3. Gửi log Cisco ASA qua Syslog (TCP):
echo '<166>Oct 25 12:00:00 cisco-gw: %ASA-6-302013: Built inbound TCP connection 998877 for outside:192.168.1.150/443' | nc -w 1 127.0.0.1 5000
```

### Bước 3: Xem kết quả JSON đầu ra
```bash
tail -n 3 /home/manager/vectormod/docker_gate/output/forwarded_logs.ndjson | jq .
```

---

## 4. HƯỚNG DẪN THÊM THIẾT BỊ MỚI (DROP & PLAY TRONG 1 PHÚT)
**Không cần sửa file `vector.yaml`, không cần restart container!**
Chỉ cần tạo file `.vrl` ném vào `vrl/`:
- Nếu là Syslog $\rightarrow$ Đặt vào `vrl/syslog/`
- Nếu là HTTP $\rightarrow$ Đặt vào `vrl/http/`
- Nếu dùng chung cả hai $\rightarrow$ Đặt vào `vrl/payload/`

### Mẫu file `.vrl` chuẩn (5 dòng):
Tạo file: `docker_gate/vrl/syslog/04_snort.vrl`
```vrl
#---
# match_contains: "[SNORT]"
# scope: syslog
# vendor: Snort
# priority: 4
#---
parsed, err = parse_regex(.message, r'\[SNORT\] (?P<alert_id>\d+): (?P<alert_msg>.*)')
if err == null {
    . = merge!(., parsed)
    .parsed = true
}
```
*Lưu file xong, hệ thống tự phát hiện trong 0.5s và nạp nóng qua `SIGHUP` trong 15ms.*

---

## 5. BẢNG TRA CỨU METADATA (HIỂU LOG TRONG 5 GIÂY)
| Tên Trường | Ý Nghĩa Thực Tế |
| :--- | :--- |
| **`source_type`** | Được **Parse Tự Động** bởi bộ giải mã giao thức nào (`syslog`, `splunk_hec`...) |
| **`parser_applied`** | Được **Parse Thủ Công** bởi file VRL nào (`syslog/01_fortigate.vrl`...) |
| **`parser_applied: "none"`**| Chưa có file VRL thủ công nào xử lý phần ruột log này |
| **`parser_status`** | `"SUCCESS"` (đã parse thành công) hoặc `"UNPARSED_RAW"` (giữ nguyên gốc) |
| **`_parse_status: "unmatched"`**| Thiết bị lạ chưa có rule, rơi vào Dead-Letter Discovery (không bị mất log) |
| **`_raw_signature`** | Chuỗi gợi ý trích xuất sẵn để bạn copy ra tạo file VRL mới |

---

## 6. SỔ TAY CHẨN ĐOÁN & KIỂM THỬ
```bash
# 1. Kiểm tra tính toàn vẹn cú pháp:
/home/manager/vectormod/docker_gate/bin/vector-gate validate -c /home/manager/vectormod/docker_gate/config/vector.yaml

# 2. Chạy bộ test nghiệm thu 6 kịch bản VRL mới:
python3 /home/manager/vectormod/qa_test_onion_hierarchical_engine.py

# 3. Chạy bộ hồi quy 12 giao thức đẩy:
python3 /home/manager/vectormod/validate_all_log_types_e2e.py

# 4. Xem tài nguyên realtime:
docker stats vector-smart-gate --no-stream
```
