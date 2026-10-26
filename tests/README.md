# VECTOR SMART GATE: AUTOMATED TEST SUITES (TESTS/)
### Thư Mục Mã Nguồn Kiểm Thử Tự Động Hóa Tập Trung (Python QA Test Suites)

Toàn bộ các bài kiểm thử tự động, kiểm tra đối kháng (Chaos Engineering), đo kiểm tải cao (Stress Testing), và đối chuẩn hiệu năng (Benchmarking) của Vector Smart Gate được tập trung tại thư mục này.

---

## 📑 DANH MỤC CÁC BỘ KIỂM THỬ (TEST SUITES)

| Tệp Script | Nhóm kiểm thử | Mục tiêu xác minh | Điều kiện môi trường |
|:---|:---|:---|:---:|
| **[`run_all_tests.py`](run_all_tests.py)** | **Unified Test Runner** | Trình điều phối chạy tổng hợp toàn bộ hoặc từng bộ test suite | Python 3.10+ |
| **[`test_standard_vector_matrix.py`](test_standard_vector_matrix.py)** | **Standard Vector Matrix** | Đo kiểm 8 tính năng tiêu chuẩn của Vector Core (Remap, Filter, Route, Reduce, Sample, Fallback) | Độc lập (Tự tạo pipeline) |
| **[`test_onion_hierarchical_engine.py`](test_onion_hierarchical_engine.py)** | **Hierarchical Onion VRL** | Đo kiểm bóc tách phân tầng Syslog/Payload và cơ chế thả nóng Hot-Drop SIGHUP | Độc lập (Khởi chạy test core) |
| **[`validate_all_log_types_e2e.py`](validate_all_log_types_e2e.py)** | **15 Ingress Protocols** | Đo kiểm khả năng tự phân biệt (Disambiguation) 12-15 giao thức trên cổng 5000 | Cần container chạy cổng 5000 |
| **[`test_chaos_resilience.py`](test_chaos_resilience.py)** | **Chaos & Adversarial** | Kiểm tra khả năng chống chịu Slowloris, bão kết nối (10k conns), Fuzzing, OOM bombs | Cần container chạy cổng 5000 |
| **[`test_stress_100k.py`](test_stress_100k.py)** | **High-Throughput Stress** | Bơm 100,000 log liên tục để đo EPS duy trì và mức tiêu thụ RAM | Cần container chạy cổng 5000 |
| **[`bench_gate_vs_vector.py`](bench_gate_vs_vector.py)** | **Performance Benchmark** | Đo độ trễ nano-giây so sánh Hop A (Client -> Gate) vs Hop B (Gate -> Vector Core) | Cần môi trường Linux |
| **[`test_universal_vrl_hot_drop.py`](test_universal_vrl_hot_drop.py)** | **Hot-Drop Watcher** | Kiểm tra watcher phát hiện file mới và re-synthesize YAML động | Độc lập |

---

## 🚀 HƯỚNG DẪN CHẠY KIỂM THỬ

### 1. Chạy nhanh các bộ kiểm thử độc lập (Không cần bật Docker):
```bash
# Chạy bộ test matrix & onion tự động:
python3 tests/run_all_tests.py

# Hoặc chạy riêng từng bộ kiểm thử:
python3 tests/test_standard_vector_matrix.py
python3 tests/test_onion_hierarchical_engine.py
```

### 2. Chạy kiểm thử End-to-End toàn diện (Khi Vector Gate đang chạy cổng 5000):
```bash
# Khởi động Vector Gate:
docker compose up -d

# Chạy toàn bộ các bài test E2E & Chaos:
python3 tests/run_all_tests.py --all

# Hoặc chạy kiểm tra 15 giao thức:
python3 tests/validate_all_log_types_e2e.py

# Hoặc chạy kiểm tra độ ổn định kháng tấn công (Chaos Suite):
python3 tests/test_chaos_resilience.py
```
