# Vector Smart Gate - Production Deployment Package (v2.5.6)
**Official Docker Image:** `l1ghtg3m/vector-gate:2.5.6` | `l1ghtg3m/vector-gate:latest`

## 🚀 Hướng Dẫn Khởi Chạy Nhanh (Quick Start)

### 1. Tùy biến thông số môi trường (`.env`)
Nếu muốn thay đổi cổng, log level, hoặc giới hạn tài nguyên:
```bash
cp .env.example .env
nano .env
```
*(Mặc định: Cổng Ingress `5000`, Cổng Telemetry/Metrics `9100`, ulimit 1M file descriptors).*

### 2. Khởi chạy bằng Docker Compose
```bash
docker-compose up -d
```

### 3. Kiểm tra trạng thái hoạt động & Sức khỏe
```bash
# Kiểm tra container đang chạy:
docker ps -f name=vector-smart-gate

# Kiểm tra endpoint sức khỏe Gate:
curl -sf http://127.0.0.1:9100/gate_health

# Xem metrics Prometheus thời gian thực:
curl -s http://127.0.0.1:9100/metrics

# Xem log container:
docker-compose logs -f
```

### 4. Thử nghiệm đẩy log vào Ingress (Cổng 5000)
```bash
# Gửi 1 dòng Syslog RFC 5424:
echo '<14>1 2026-10-27T04:00:00Z web01 nginx 1234 - - Connection established' | nc -w 1 127.0.0.1 5000

# Gửi HTTP Webhook JSON:
curl -X POST http://127.0.0.1:5000/ -H "Content-Type: application/json" -d '{"event":"test","status":"ok"}'
```
Log được ghi vào thư mục `./output/forwarded_logs.ndjson`.
