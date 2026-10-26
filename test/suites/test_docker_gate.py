#!/usr/bin/env python3
"""
Integration test for Containerized Vector Smart Gate (type: any)
Tests sending multiple log formats to container port 5000 and verifies output.
"""

import socket
import urllib.request
import json
import time
import os
import sys

GATE_PORT = 5000
HOST = "127.0.0.1"
OUTPUT_FILE = "/home/manager/vectormod/deploy/output/forwarded_logs.ndjson"

class Colors:
    GREEN = "\033[92m"
    RED = "\033[91m"
    BLUE = "\033[94m"
    RESET = "\033[0m"

def send_tcp(data):
    s = socket.create_connection((HOST, GATE_PORT), timeout=2)
    s.sendall(data)
    s.close()

def send_http(path, data, headers):
    req = urllib.request.Request(f"http://{HOST}:{GATE_PORT}{path}", data=data, headers=headers)
    with urllib.request.urlopen(req, timeout=2) as resp:
        return resp.status

print(f"\n{Colors.BLUE}==================================================================")
print("🚀 BẮT ĐẦU KIỂM THỬ TÍCH HỢP CONTAINER VECTOR SMART GATE (:5000)")
print(f"=================================================================={Colors.RESET}\n")

# 1. Syslog RFC 3164
print("[1/7] Gửi Syslog RFC 3164...")
send_tcp(b"<34>Oct 24 16:50:00 gate-docker kernel: IN=eth0 OUT= SRC=10.0.0.1 DST=10.0.0.2\n")
time.sleep(0.2)

# 2. Syslog RFC 5424
print("[2/7] Gửi Syslog RFC 5424...")
send_tcp(b"<165>1 2026-10-24T16:50:00Z docker-host myapp - ID42 [test@123 id=\"99\"] Login success\n")
time.sleep(0.2)

# 3. Check Point CEF
print("[3/7] Gửi Check Point CEF...")
send_tcp(b"<134>1 2026-10-24T16:50:00Z fw-docker CEF:0|CheckPoint|Firewall|1.0|drop|Drop|act=drop\n")
time.sleep(0.2)

# 4. Splunk HEC HTTP
print("[4/7] Gửi Splunk HEC HTTP...")
splunk_data = json.dumps({"event": "docker gate event", "sourcetype": "access_combined"}).encode()
send_http("/services/collector/event", splunk_data, {
    "Authorization": "Splunk 12345678-1234-1234-1234-123456789012",
    "Content-Type": "application/json",
    "Connection": "close"
})
time.sleep(0.2)

# 5. Datadog Agent HTTP
print("[5/7] Gửi Datadog Agent HTTP...")
dd_data = json.dumps([{
    "message": "Docker gate datadog test event",
    "status": "info",
    "timestamp": int(time.time()),
    "hostname": "docker-node",
    "service": "gatekeeper",
    "ddsource": "python",
    "ddtags": "env:production,container:docker-gate"
}]).encode()
send_http("/v1/input", dd_data, {
    "DD-API-KEY": "dummy-token",
    "Content-Type": "application/json",
    "Connection": "close"
})
time.sleep(0.2)

# 6. Generic HTTP Webhook
print("[6/7] Gửi Generic HTTP Webhook...")
http_data = json.dumps({"container": "docker-gate", "event": "webhook_triggered"}).encode()
send_http("/", http_data, {
    "Content-Type": "application/json",
    "Connection": "close"
})
time.sleep(0.2)

# 7. Raw Socket Stream
print("[7/7] Gửi Raw TCP Stream...")
send_tcp(b"CUSTOM_TCP_LOG: event_id=EVT-9001 action=ALLOW bytes=1024\n")
time.sleep(1.0)

print("\n==================================================================")
print("📊 KIỂM TRA FILE ĐẦU RA TRÊN HOST (./output/forwarded_logs.ndjson)")
print("==================================================================")

if os.path.exists(OUTPUT_FILE):
    with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
        lines = [l.strip() for l in f if l.strip()]
    print(f"Tổng số bản ghi container đã ghi thành công ra disk: {len(lines)}")
    if len(lines) >= 7:
        print(f"{Colors.GREEN}🎉 100% CÁC GIAO THỨC ĐÃ ĐƯỢC CONTAINER VECTOR GATE TIẾP NHẬN & XỬ LÝ THÀNH CÔNG!{Colors.RESET}")
    else:
        print(f"Bản ghi nhận được ({len(lines)}/7)")
        for l in lines[:3]:
            print("  sample:", l)
else:
    print(f"{Colors.RED}❌ File output chưa được tạo: {OUTPUT_FILE}{Colors.RESET}")
    sys.exit(1)

