# VECTOR SMART GATE: MASTER SAMPLES CATALOG
### Bộ Dữ Liệu Mẫu Hợp Nhất & Lệnh Bắn Kiểm Thử 15 Giao Thức Chuẩn (Port `0.0.0.0:5000`)

Tất cả các định dạng log và gói tin dưới đây đều được gửi trực tiếp vào **DUY NHẤT một cổng `0.0.0.0:5000`** của Vector Smart Gate. Động cơ tự động phân tích byte đầu (Magic Bytes / Header sniffing) và chuyển tiếp tới đúng pipeline đích.

---

## 📊 BẢNG TRA CỨU NHANH 15 GIAO THỨC MẪU

| STT | Giao thức / Định dạng | Loại kết nối | Header / Magic Bytes | Kênh tiếp nhận nội bộ | Lệnh kiểm thử nhanh (1-Click) |
|:---:|:---|:---:|:---|:---:|:---|
| **01** | **Syslog RFC 3164 (BSD)** | TCP Socket | `<PRI>` (e.g. `<134>`) | `syslog` | `nc -w 1 127.0.0.1 5000 < samples/rfc3164.log` |
| **02** | **Syslog RFC 5424 (IETF)** | TCP Socket | `<PRI>1 ` | `syslog` | `nc -w 1 127.0.0.1 5000 < samples/rfc5424.log` |
| **03** | **Check Point CEF** | TCP Syslog | `CEF:0\|` | `syslog` | Netcat / Syslog socket |
| **04** | **Fortinet FortiGate KV** | TCP Syslog | `date=... devname=` | `syslog` | Netcat / Syslog socket |
| **05** | **Cisco ASA Firewall** | TCP Syslog | `%ASA-` | `syslog` | Netcat / Syslog socket |
| **06** | **Linux Kernel Auditd** | TCP Socket | `type=SYSCALL` | `socket` (raw) | Netcat TCP stream |
| **07** | **Suricata EVE JSON** | TCP Socket | `{"timestamp":...}` | `socket` (json) | Netcat TCP stream |
| **08** | **Zeek Network JSON** | TCP Socket | `{"ts":...}` | `socket` (json) | Netcat TCP stream |
| **09** | **Nginx Combined Access** | TCP Socket | `192.168... - [date]` | `socket` (text) | Netcat TCP stream |
| **10** | **Generic HTTP Webhook** | HTTP POST | `POST /` (JSON) | `http_server` | `curl -X POST http://127.0.0.1:5000/ -d @samples/...` |
| **11** | **Splunk HEC Event** | HTTP POST | `POST /services/collector` | `splunk_hec` | `curl -H 'Authorization: Splunk token' ...` |
| **12** | **Datadog Agent Intake** | HTTP POST | `POST /v1/input` | `datadog_agent` | `curl -H 'DD-API-KEY: key' ...` |
| **13** | **Elastic Beats (Filebeat)** | TCP Binary | Lumberjack v2 (`0x32 0x44`) | `logstash` | `python3 samples/send_samples.py --protocol beats` |
| **14** | **Fluent Forward** | TCP Binary | MessagePack (`0x92..0x94`) | `fluent` | `python3 samples/send_samples.py --protocol fluent` |
| **15** | **Raw Custom Socket** | TCP Socket | Bất kỳ chuỗi nhị phân/text | `socket` | Netcat TCP stream |

---

## 🚀 CÁCH SỬ DỤNG BỘ KIỂM THỬ MẪU (AUTOMATED RUNNER)

Bộ công cụ [`samples/send_samples.py`](send_samples.py) cho phép bắn kiểm thử toàn bộ hoặc từng giao thức đơn lẻ một cách dễ dàng:

```bash
# Bắn toàn bộ 15 giao thức mẫu qua cổng 5000
python3 samples/send_samples.py --all

# Bắn kiểm thử riêng giao thức Syslog
python3 samples/send_samples.py --protocol syslog

# Bắn kiểm thử riêng giao thức HTTP Webhook
python3 samples/send_samples.py --protocol http

# Bắn kiểm thử riêng Splunk HEC hoặc Datadog
python3 samples/send_samples.py --protocol splunk
python3 samples/send_samples.py --protocol datadog
```

Toàn bộ dữ liệu mẫu chi tiết dạng JSON có thể tích hợp vào các pipeline kiểm thử tự động tại [`samples/samples.json`](samples.json).
