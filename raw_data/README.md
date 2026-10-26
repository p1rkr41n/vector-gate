# RAW DATA & PHÂN TÍCH HỆ THỐNG (ANALYSIS REPOSITORY)
### Thư Mục Lưu Trữ Dữ Liệu Thô, Danh Mục Nguồn, Phân Tích So Sánh & Vấn Đề Thượng Nguồn

Thư mục này tập trung toàn bộ dữ liệu thô và các tài liệu/dữ liệu phân tích kỹ thuật phục vụ quá trình nghiên cứu và phát triển Vector Smart Gate:

---

## 📂 DANH MỤC CÁC PHÂN HỆ DỮ LIỆU

### 1. [`vrl_upstream_issues/`](vrl_upstream_issues/)
- **Mục đích**: Kho lưu trữ toàn bộ **272 issues và PRs** kéo trực tiếp từ kho mã nguồn gốc `vectordotdev/vrl` và `vectordotdev/vector`.
- **Bao gồm**:
  - `issues/`: Các tệp Markdown chi tiết cho từng issue (tiêu đề, nhãn, người tạo, nội dung thảo luận).
  - `CATEGORY_REPORT.md`: Báo cáo phân loại lỗi (Type System, Runtime Errors, Coercion, Performance).
  - `SUMMARY_REPORT.md`: Báo cáo thống kê tổng thể trạng thái các vấn đề upstream.
  - `vrl_all_issues.json`: Dữ liệu thô JSON đầy đủ.

### 2. [`vector_sources/`](vector_sources/)
- **Mục đích**: Danh mục phân loại toàn diện tất cả các nguồn dữ liệu của Timberio Vector.
- **Bao gồm**:
  - `vector_sources.csv`: Bảng tra cứu 15 nguồn PUSH và đặc tả kết nối, giao thức.
  - `vector_sources_by_layer.csv`: Phân chia nguồn theo tầng (Network, Agent, Cloud/SaaS, File/OS).

### 3. [`haproxy_analysis/`](haproxy_analysis/)
- **Mục đích**: Dữ liệu nghiên cứu, phân tích mã nguồn và đo kiểm đối chuẩn (Benchmarking) giữa HAProxy 2.8 và RAproxy Turbo-Kernel.
- **Bao gồm**: Cấu hình mẫu, kết quả đo latency và throughput đối chứng.

### 4. [`evtx_samples/`](evtx_samples/)
- **Mục đích**: Tệp log nhị phân Windows Event Log thô (`large_sample_2gb.evtx`) quy mô 2GB+ (>5 triệu sự kiện) phục vụ đo kiểm hiệu năng đọc lô, nén ZSTD và chuyển đổi sang Parquet cho IR / DFIR.

### 5. [`ideation/`](ideation/)
- **Mục đích**: Các bản ghi chú thảo luận, phác thảo ý tưởng kiến trúc sơ khởi (`idea.md`) trước khi hợp nhất vào Master Specification.
