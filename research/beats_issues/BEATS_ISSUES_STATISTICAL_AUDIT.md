# BÁO CÁO THỐNG KÊ LỊCH SỬ CÁC ISSUES GIAO THỨC BEATS TRÊN VECTOR
## PHẠM VI: ELASTIC BEATS (FILEBEAT, WINLOGBEAT, LUMBERJACK PROTOCOL) & VECTOR LOGSTASH SOURCE
**Chuyên mục:** Rà soát Thống kê Dữ liệu Thô (Chưa QA)  
**Nguồn dữ liệu:** Upstream Repository `vectordotdev/vector` (GitHub API Audit)  
**Thời gian rà soát:** 26/10/2026  

---

## 1. TỔNG QUAN ĐỊNH LƯỢNG (EXECUTIVE METRICS)

Trong hệ sinh thái **Vector**, giao thức **Elastic Beats** (Lumberjack v1 & v2 sử dụng trên các agent như Filebeat, Metricbeat, Winlogbeat) được hiện thực hóa thông qua module nguồn **`sources.logstash`** (lắng nghe mặc định trên cổng `5044`).

Qua quá trình quét tự động và bóc tách dữ liệu từ kho mã nguồn Vector Upstream, số lượng issues và pull requests liên quan được thống kê theo 2 tầng phạm vi:

| Phạm Vi Rà Soát | Tổng Số Items | Issues (Tổng) | Issues: Open | Issues: Closed | PRs (Fix / Feat) | PRs: Open | PRs: Closed |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Toàn cảnh tìm kiếm (Broad Scope)**<br/>*(Bao gồm thảo luận kiến trúc, so sánh Filebeat, issue người dùng)* | **125** | **102** | 31 *(30.4%)* | 71 *(69.6%)* | **23** | 2 | 21 |
| **Trọng tâm cốt lõi (Strict Beats / Lumberjack)**<br/>*(Trực tiếp module nguồn `logstash`, giải mã frame, ACK, TCP)* | **44** | **24** | 7 *(29.2%)* | 17 *(70.8%)* | **20** | 0 | 20 |

---

## 2. PHÂN LOẠI CÁC ISSUES THEO BẢN CHẤT KỸ THUẬT (44 ITEMS CỐT LÕI)

| Nhóm Chuyên Đề | Số Lượng Items | Tỷ Lệ % | Mô Tả Trọng Tâm Kỹ Thuật |
|:---|:---:|:---:|:---|
| **1. Cơ Chế Xác Thực ACK & Trượt Cửa Sổ (Windowing)** | **11** | 25.0% | Xử lý ACK boundary, lệch window Filebeat, duplicate logs, rớt kết nối giữa chừng (#25700, #25655, #25616, #25531, #23346, #22942, #13441, #10176, #492). |
| **2. An Ninh, Tấn Công DoS & Bùng Nổ Bộ Nhớ (ZipBomb)** | **4** | 9.1% | Lỗ hổng nén đệ quy ZipBomb qua zlib, remote OOM, cạn kiệt stack trace (#19087 [OPEN], #26129, #25818, #25825). |
| **3. Sập Luồng, Panic & Sai Lệch Khung Tin** | **5** | 11.4% | Worker thread panic khi nhận gói tin ngắn, đóng socket khi frame sai cú pháp, memory leak khi merge (#16273, #21286, #25664, #14197, #8004). |
| **4. Quản Lý Kết Nối TCP, Idle Starvation & Backpressure** | **5** | 11.4% | Kết nối Filebeat treo chiếm dụng slot RequestLimiter, kiểm soát hàng đợi backpressure (#26492 [OPEN], #8596). |
| **5. Ánh Xạ Siêu Dữ Liệu (Metadata, Schema & Namespaces)** | **6** | 13.6% | Ánh xạ trường namespace, định nghĩa schema, metadata mạng & client IP, timestamp parsing (#15026, #15290, #7308, #15657, #10346, #14422). |
| **6. Đề Xuất Tính Năng Mới, CI & Khởi Tạo Nguồn** | **13** | 29.5% | Khởi tạo nguồn logstash ban đầu, đề xuất logstash sink, dead letter queue, Docker CI tests (#420, #7857, #7598, #16397, #14854, #14971, #21918, #9578, #10544, #9576, #9540, #16191, #16055). |

---

## 3. DANH SÁCH CHI TIẾT CÁC ISSUES & PRS CỐT LÕI

*(Đã lưu trữ dữ liệu JSON thô tại `research/beats_issues/vector_upstream_beats_all.json`, `verified_beats_issues.json`, `verified_beats_prs.json`)*.

