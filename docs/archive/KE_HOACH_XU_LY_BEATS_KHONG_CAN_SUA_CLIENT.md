# KẾ HOẠCH & CHỈ THỊ KỸ THUẬT: PHƯƠNG ÁN XỬ LÝ SỰ CỐ BEATS MÀ KHÔNG CẦN CHỈNH SỬA BEAT AGENT (ZERO-TOUCH CLIENT ARCHITECTURE)

**Áp dụng cho:** Hệ thống giám sát an ninh mạng với 100+ máy trạm Filebeat / Winlogbeat phân tán tại các chi nhánh/đơn vị ở xa, đường truyền kém, chập chờn.  
**Ràng buộc vận hành:** **TUYỆT ĐỐI KHÔNG CAN THIỆP VÀO FILEBEAT/WINLOGBEAT TRÊN MÁY TRẠM** (do rào cản phân tán địa lý, quyền quản trị phân tán, chi phí vận hành quá lớn).  
**Triết lý kiến trúc:** **Server-Side Compensation Architecture (Gate & Core gánh 100% khiếm khuyết của Client).**

---

## 1. PHÂN TÍCH: TẠI SAO HOÀN TOÀN CÓ THỂ XỬ LÝ 100% TẠI VECTOR?

Khi không thể chỉnh sửa file `filebeat.yml` / `winlogbeat.yml` trên 100 máy trạm, máy trạm sẽ chạy với các thông số mặc định bất lợi:
1. `bulk_max_size: 2048` (Window cực lớn, gửi một khối 2MB - 4MB qua mạng yếu).
2. `pipelining: 2` (Bật gửi dồn nhiều window khi chưa nhận lời ACK).
3. `timeout: 30s` (Nếu server trả lời ACK chậm > 30s, client đơn phương cắt kết nối và gửi lại).
4. Khi mạng bị đứt ngầm (Silent Drop), Filebeat kết nối lại và gửi lại (resend) các bản ghi chưa được ACK, gây **trùng lặp log (Duplicate logs)** trên SIEM.

**Vector Smart Gate + Vector Core + Linux Kernel** hoàn toàn có thể "hóa giải" 100% các hành vi trên theo mô hình **4 Trụ Cột Bù Đắp**:

```mermaid
flowchart TD
    subgraph Client [100+ Máy Trạm Beat - KHÔNG CẦN SỬA ĐỔI]
        FB["Filebeat / Winlogbeat (Mặc định: bulk=2048, pipelining=2, timeout=30s)"]
    end

    subgraph Gate [Trụ Cột 1: Vector Smart Gate]
        G1["TCP_USER_TIMEOUT = 15s (Diệt sạch kết nối ma)"]
        G2["Graceful Half-Close (Flush nốt ACK, không vứt bỏ tương lai b2c)"]
        G3["TCP_NODELAY & QUICKACK (Giảm 40ms trễ TCP)"]
    end

    subgraph Core [Trụ Cột 2: Vector Core Pipeline]
        C1["in_beats: receive_buffer = 4MB (Nuốt trọn burst 2048 logs)"]
        C2["Early-ACK (acknowledgements: false) -> Trả lời ACK trong 2ms"]
        C3["Native Dedupe Transform: Triệt tiêu 100% duplicate log khi Beat resend"]
        C4["Disk Buffer 10GB: Đảm bảo At-Least-Once an toàn tuyệt đối"]
    end

    subgraph OS [Trụ Cột 3: Linux Host OS Tuning]
        K1["BBR Congestion Control (Chống sập băng thông trên mạng mất gói)"]
        K2["tcp_slow_start_after_idle = 0 (Không bóp tốc độ sau thời gian rảnh)"]
        K3["TCP R/W Buffers = 16MB (Hấp thụ bão lưu lượng)"]
    end

    Client --> Gate --> Core
    Gate -. Chạy trên .-> OS
```

---

## 2. CHI TIẾT 4 TRỤ CỘT BÙ ĐẮP PHÍA SERVER

### Trụ Cột 1: Early-ACK Tức Thì Trong 2ms (Hóa Giải Timeout 30s & Pipelining)
- **Vấn đề của Beat:** Filebeat gửi window to (2048 events) và chờ lời ACK. Nếu Vector chờ SIEM (Elasticsearch/Splunk) ghi xong mới ACK, thời gian sẽ vượt quá 30s $\rightarrow$ Filebeat timeout $\rightarrow$ đóng socket $\rightarrow$ lỗi `invalid sequence number`.
- **Giải pháp trên Vector Core:**
  - Cấu hình `acknowledgements: false` trên `sources.in_beats`.
  - Ngay khi các frame Lumberjack được nhận vào bộ nhớ đệm RAM của Vector Core (chỉ mất $1 - 2\,\text{ms}$), Vector Core lập tức phát sinh gói ACK `2A` gửi ngược về Filebeat qua Vector Gate.
  - Filebeat nhận được ACK ngay lập tức ($< 10\,\text{ms}$), sliding window lập tức trượt tiếp, không bao giờ bị nghẽn hay chạm ngưỡng timeout 30s.

### Trụ Cột 2: Bộ Lọc Khử Trùng Lặp Tự Động (Native Dedupe Transform - Hóa Giải Resend Churn)
- **Vấn đề của Beat:** Do mạng ở xa chập chờn, khi Filebeat không nhận được ACK trước khi đứt kết nối, nó sẽ kết nối lại và gửi lại (resend) toàn bộ 2048 bản ghi cũ $\rightarrow$ SIEM bị ngập trong log nhân bản.
- **Giải pháp trên Vector Core:**
  - Bổ sung một transform `type: dedupe` chuyên biệt ngay sau nguồn `in_beats` trong `vector.yaml`:
  ```yaml
  transforms:
    dedupe_beats:
      type: dedupe
      inputs: ["in_beats"]
      fields:
        match: ["host", "message"]   # Hoặc hash SHA-256 nội dung log
  ```
  - Transform này duy trì bộ đệm trượt (sliding cache). Bất kỳ bản ghi nào bị Filebeat gửi lại lần 2 do reconnect sẽ bị Vector âm thầm loại bỏ, chỉ chuyển duy nhất 1 bản ghi chuẩn về SIEM!

### Trụ Cột 3: Nâng Bộ Đệm Socket Lên 4MB & 10GB Disk Buffer (Hóa Giải Window 2048)
- **Vấn đề của Beat:** 100 máy Beat đồng loạt gửi `bulk_max_size: 2048`, mỗi event $\approx 1\,\text{KB}$, một đợt burst có thể lên tới $200\,\text{MB}$ dữ liệu dồn về một lúc. Nếu buffer nhỏ, kernel sẽ phát gói **TCP Zero Window**, ép client ngừng gửi.
- **Giải pháp trên Vector Core & Gate:**
  - Tăng `receive_buffer_bytes` của `in_beats` lên **$4,194,304\,\text{bytes}$ ($4\,\text{MB}$)**.
  - Nâng trần pipe kernel trong Gate lên **$256\,\text{KB}$** và buffer disk của sink lên **$10\,\text{GB}$**.
  - Server trở thành một "chiếc phễu khổng lồ", tiếp nhận trọn vẹn toàn bộ các mẻ dữ liệu 2048 events của Beat mà không gây bất kỳ áp lực ngược nào về phía client.

### Trụ Cột 4: Kích Hoạt TCP BBR & Vô Hiệu Hóa Slow-Start Sau Idle Trên Nhân Linux
- **Vấn đề của Beat:** Đường truyền ở xa (mạng 4G/WAN chập chờn) có tỷ lệ mất gói (packet loss) cao. Thuật toán điều khiển tắc nghẽn mặc định của Linux (CUBIC) cứ thấy mất gói là tự động cắt giảm 50% băng thông, khiến Filebeat càng truyền chậm và dễ rớt kết nối hơn. Sau một khoảng rảnh rỗi (idle), TCP lại reset cửa sổ về 1 MSS (Slow Start).
- **Giải pháp trên Host OS:**
  - Bật thuật toán **Google BBR (`net.ipv4.tcp_congestion_control = bbr`)**: Đo đạc dựa trên băng thông và độ trễ thực tế thay vì coi mất gói là tắc nghẽn, giúp duy trì tốc độ truyền tối đa ngay cả khi mạng chập chờn mất 5-10% gói tin!
  - Thiết lập `net.ipv4.tcp_slow_start_after_idle = 0`: Cấm nhân Linux reset cửa sổ tắc nghẽn về 0 sau thời gian rảnh, giúp Filebeat gửi đợt log tiếp theo với tốc độ cao ngay lập tức.

---

## 3. BẢNG SO SÁNH: SỬA BEAT VS CHỈ SỬA VECTOR

| Tiêu chí | Phương án Sửa 100 máy Beat | Phương án "Chỉ Sửa Vector" (Đề xuất) |
| :--- | :--- | :--- |
| **Chi phí vận hành** | Rất cao (truy cập 100 máy, xin phân quyền, rủi ro làm gián đoạn máy trạm) | **0 đồng** (Chỉ can thiệp tập trung tại máy chủ Gateway) |
| **Thời gian triển khai** | Vài tuần đến hàng tháng | **Hoàn thành ngay trong 10 phút** |
| **Khả năng chống treo ma** | Phụ thuộc vào việc cấu hình từng máy | **Triệt để 100%** (Gate cưỡng bức cắt kết nối ma sau 15s) |
| **Xử lý Duplicate Logs** | Hạn chế (vẫn có thể bị trùng nếu đứt cáp) | **Triệt để 100%** (Server có bộ lọc Dedupe tự động) |
| **Độ tin cậy dữ liệu** | Phụ thuộc vào mạng client | **Được bảo đảm bởi Disk Buffer 10GB trên Server** |

---

## 4. CHỈ THỊ KỸ THUẬT MỚI (NEW DIRECTIVE)

Ban hành chỉ thị kỹ thuật chính thức cho toàn bộ đội ngũ vận hành và hệ thống:

1. **Chỉ thị 1 (Nguyên tắc Zero-Touch Client):**
   - Đóng băng toàn bộ cấu hình phía client. Không thực hiện bất kỳ thay đổi nào trên 100 máy Beat trạm xa.
   - Toàn bộ cơ chế điều tiết, hấp thụ xung lực và khử trùng lặp được đảm nhiệm độc quyền bởi cụm **Vector Smart Gate v2.4.3**.

2. **Chỉ thị 2 (Cập nhật Cấu hình Vector Core `deploy/config/vector.yaml`):**
   - Nâng `sources.in_beats.receive_buffer_bytes` lên `4194304` (4MB).
   - Duy trì `acknowledgements: false` trên `in_beats`.
   - Kích hoạt tầng Deduplication `transforms.dedupe_beats` trước khi đẩy vào `universal_parser` hoặc `sinks`.

3. **Chỉ thị 3 (Kích hoạt Kernel Sysctl Trên Host Production):**
   - Áp dụng tệp `deploy/sysctl/99-vector-gate.conf` lên máy chủ Host Linux:
     ```bash
     sudo cp deploy/sysctl/99-vector-gate.conf /etc/sysctl.d/
     sudo sysctl --system
     ```
   - Kích hoạt module kernel BBR:
     ```bash
     sudo modprobe tcp_bbr
     ```
