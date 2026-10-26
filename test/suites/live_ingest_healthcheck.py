#!/usr/bin/env python3
"""
Live Data Ingestion Health & Stability Benchmark for Dockerized Vector Smart Gate
Runs stress load across concurrent connections and verifies data integrity on disk.
"""

import socket
import urllib.request
import json
import time
import threading
import subprocess
import os
import sys

GATE_PORT = 5000
HOST = "127.0.0.1"
OUTPUT_FILE = "/home/manager/vectormod/deploy/output/forwarded_logs.ndjson"

SYSLOG_SAMPLE = b"<134>1 2026-10-24T17:07:00Z firewall-gw kernel - - [audit@32473 action=\"ALLOW\"] Connection accepted src=192.168.1.10 dst=10.0.0.5 proto=TCP spt=49152 dpt=443\n"

def get_output_line_count():
    if not os.path.exists(OUTPUT_FILE):
        return 0
    with open(OUTPUT_FILE, "r", encoding="utf-8", errors="ignore") as f:
        return sum(1 for _ in f)

def get_container_stats():
    res = subprocess.run(
        ["docker", "stats", "vector-smart-gate", "--no-stream", "--format", "{{.MemUsage}} | {{.CPUPerc}}"],
        capture_output=True, text=True
    )
    return res.stdout.strip()

print("=" * 75)
print("🔍 BẮT ĐẦU ĐO KIỂM ĐỘ ỔN ĐỊNH & HIỆU NĂNG INGEST DỮ LIỆU CỦA DOCKER CONTAINER")
print("=" * 75)

init_lines = get_output_line_count()
init_stats = get_container_stats()
print(f"• Trạng thái ban đầu: {init_lines:,} bản ghi đã lưu")
print(f"• Tài nguyên ban đầu: {init_stats}")

# Benchmark 1: 50,000 Syslog RFC 5424 qua 8 luồng song song
TOTAL_SYSLOG = 50_000
THREADS = 8
PER_THREAD = TOTAL_SYSLOG // THREADS

results = []

def syslog_worker(w_id, count):
    sent = 0
    t0 = time.perf_counter()
    try:
        s = socket.create_connection((HOST, GATE_PORT), timeout=5)
        s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        chunk = SYSLOG_SAMPLE * 50
        for _ in range(count // 50):
            s.sendall(chunk)
            sent += 50
        s.close()
    except Exception as e:
        print(f"[Worker {w_id}] Lỗi: {e}", file=sys.stderr)
    elapsed = time.perf_counter() - t0
    results.append((sent, elapsed))

print(f"\n🚀 [Giai đoạn 1] Bắn xung {TOTAL_SYSLOG:,} sự kiện Syslog qua 8 luồng TCP đồng thời...")
t_start = time.perf_counter()
threads = [threading.Thread(target=syslog_worker, args=(i, PER_THREAD)) for i in range(THREADS)]
for t in threads: t.start()
for t in threads: t.join()
syslog_elapsed = time.perf_counter() - t_start
total_syslog_sent = sum(r[0] for r in results)
syslog_eps = total_syslog_sent / syslog_elapsed if syslog_elapsed > 0 else 0

print(f"  -> Hoàn tất trong: {syslog_elapsed:.4f} giây")
print(f"  -> Thông lượng tức thời: {syslog_eps:,.0f} EPS")

# Benchmark 2: Bắn HTTP Events (Splunk HEC + Datadog Agent)
print("\n🚀 [Giai đoạn 2] Bắn gói tin HTTP API (Splunk HEC + Datadog)...")
http_sent = 0
t_http = time.perf_counter()

# Splunk HEC
splunk_data = json.dumps({"event": "audit log record security test", "sourcetype": "security_audit"}).encode()
req_splunk = urllib.request.Request(
    f"http://{HOST}:{GATE_PORT}/services/collector/event",
    data=splunk_data,
    headers={"Authorization": "Splunk test-token", "Content-Type": "application/json", "Connection": "close"}
)
try:
    with urllib.request.urlopen(req_splunk, timeout=5) as r:
        if r.status == 200:
            http_sent += 1
except Exception as e:
    print(f"Lỗi Splunk: {e}", file=sys.stderr)

# Datadog Agent
dd_batch = json.dumps([{
    "message": "datadog agent event test",
    "status": "info",
    "timestamp": int(time.time()),
    "hostname": "prod-gateway",
    "service": "api",
    "ddsource": "python",
    "ddtags": "env:prod"
}]).encode()
req_dd = urllib.request.Request(
    f"http://{HOST}:{GATE_PORT}/v1/input",
    data=dd_batch,
    headers={"DD-API-KEY": "test-key", "Content-Type": "application/json", "Connection": "close"}
)
try:
    with urllib.request.urlopen(req_dd, timeout=5) as r:
        if r.status == 200:
            http_sent += 1
except Exception as e:
    print(f"Lỗi Datadog: {e}", file=sys.stderr)

http_elapsed = time.perf_counter() - t_http
print(f"  -> Đã gửi thành công {http_sent:,} sự kiện HTTP trong {http_elapsed:.4f}s")

# Chờ Vector flush dữ liệu hoàn tất ra disk
print("\n⏳ Đang đợi Vector flush dữ liệu hoàn tất ra disk (4 giây)...")
time.sleep(4.0)

final_lines = get_output_line_count()
final_stats = get_container_stats()
new_lines = final_lines - init_lines
expected_total = total_syslog_sent + http_sent

print("\n" + "=" * 75)
print("📊 BÁO CÁO TỔNG HỢP ĐỘ ỔN ĐỊNH VÀ TOÀN VẸN DỮ LIỆU (HEALTH REPORT)")
print("=" * 75)
print(f"• Tổng số sự kiện đẩy vào (Ingested)      : {expected_total:,} sự kiện")
print(f"• Số bản ghi ghi thành công (Written)     : {new_lines:,} sự kiện")
loss_rate = max(0.0, (1.0 - (new_lines / expected_total)) * 100) if expected_total > 0 else 0.0
print(f"• Tỷ lệ thất thoát dữ liệu (Packet Drop)  : {loss_rate:.2f}% ({'✅ KHÔNG RỚT BẢN GHI NÀO' if loss_rate == 0.0 else '⚠️ CÓ THẤT THOÁT'})")
print(f"• Thông lượng đỉnh Ingress (Peak EPS)     : {syslog_eps:,.0f} EPS")
print(f"• Tài nguyên Container sau tải            : {final_stats}")
print(f"• Trạng thái container                    : {'✅ HEALTHY & HOẠT ĐỘNG HOÀN HẢO' if loss_rate == 0.0 else '⚠️ CẦN KIỂM TRA'}")
print("=" * 75)

