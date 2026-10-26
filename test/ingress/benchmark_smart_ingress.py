#!/usr/bin/env python3
"""
Performance & Resource Benchmark: HAProxy + Vector Smart Ingress (:5000)
Pushes high volume across multiple protocols, tracks CPU & RAM in real-time, calculates EPS.
"""

import socket
import urllib.request
import time
import os
import sys
import threading
import json
import subprocess

TARGET_HOST = "127.0.0.1"
TARGET_PORT = 5000
OUTPUT_FILE = "/home/manager/vectormod/smart_ingress/output/all_forwarded_logs.jsonl"
RAPROXY_PID = 227337
VECTOR_PID = 224149

TOTAL_EVENTS_PER_WORKER = 10000
NUM_WORKERS = 5 # 5 parallel workers = 50,000 events total

benchmark_running = True
peak_haproxy_cpu = 0.0
peak_vector_cpu = 0.0
peak_haproxy_rss_mb = 0.0
peak_vector_rss_mb = 0.0

def monitor_resources():
    global benchmark_running, peak_haproxy_cpu, peak_vector_cpu, peak_haproxy_rss_mb, peak_vector_rss_mb
    while benchmark_running:
        try:
            out = subprocess.check_output(
                ["ps", "-p", f"{RAPROXY_PID},{VECTOR_PID}", "-o", "pid,%cpu,rss", "--no-headers"],
                text=True
            )
            for line in out.strip().splitlines():
                parts = line.split()
                if len(parts) >= 3:
                    pid, cpu, rss_kb = int(parts[0]), float(parts[1]), float(parts[2])
                    rss_mb = rss_kb / 1024.0
                    if pid == RAPROXY_PID:
                        peak_haproxy_cpu = max(peak_haproxy_cpu, cpu)
                        peak_haproxy_rss_mb = max(peak_haproxy_rss_mb, rss_mb)
                    elif pid == VECTOR_PID:
                        peak_vector_cpu = max(peak_vector_cpu, cpu)
                        peak_vector_rss_mb = max(peak_vector_rss_mb, rss_mb)
        except Exception:
            pass
        time.sleep(0.1)

def worker_syslog(worker_id, count):
    # Sends Syslog RFC 3164 in streaming TCP connection
    payload = b"<134>Oct 24 10:20:00 srv-app-01 sshd[28491]: Accepted publickey for manager from 192.168.1.100 port 54322 ssh2\n" * 50
    batches = count // 50
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TARGET_HOST, TARGET_PORT))
    for _ in range(batches):
        s.sendall(payload)
    s.close()

def worker_cef(worker_id, count):
    # Sends CEF over Syslog in streaming TCP connection
    payload = b"<134>Oct 24 10:20:01 fw-cp-01 CEF:0|Check Point|FireWall-1|Log|drop|act=drop src=203.0.113.45 dst=10.0.0.15\n" * 50
    batches = count // 50
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TARGET_HOST, TARGET_PORT))
    for _ in range(batches):
        s.sendall(payload)
    s.close()

def worker_raw(worker_id, count):
    # Sends Raw Socket stream
    payload = b'RAW_STREAM: event_type=audit user=root action=exec syscall=59 status=ok\n' * 50
    batches = count // 50
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TARGET_HOST, TARGET_PORT))
    for _ in range(batches):
        s.sendall(payload)
    s.close()

def worker_http_generic(worker_id, count):
    # Sends NDJSON batch over HTTP
    ndjson_body = '\n'.join([json.dumps({"app": "bench", "iter": i, "level": "info", "msg": "bench payload"}) for i in range(100)]) + '\n'
    batches = count // 100
    for _ in range(batches):
        req = urllib.request.Request(
            f"http://{TARGET_HOST}:{TARGET_PORT}/",
            data=ndjson_body.encode('utf-8'),
            headers={"Content-Type": "application/x-ndjson", "Connection": "close"},
            method="POST"
        )
        try:
            with urllib.request.urlopen(req, timeout=5) as resp:
                resp.read()
        except Exception:
            pass

def worker_splunk(worker_id, count):
    # Sends Splunk HEC batch
    splunk_body = '\n'.join([json.dumps({"event": {"metric": "cpu", "val": 42}, "host": "srv-bench"}) for i in range(100)]) + '\n'
    batches = count // 100
    for _ in range(batches):
        req = urllib.request.Request(
            f"http://{TARGET_HOST}:{TARGET_PORT}/services/collector/event",
            data=splunk_body.encode('utf-8'),
            headers={"Authorization": "Splunk test-token", "Content-Type": "application/json", "Connection": "close"},
            method="POST"
        )
        try:
            with urllib.request.urlopen(req, timeout=5) as resp:
                resp.read()
        except Exception:
            pass

def main():
    global benchmark_running
    print("==================================================================")
    print("⚡ BẮT ĐẦU BENCHMARK CHỊU TẢI & ĐO LƯỜNG TÀI NGUYÊN (50.000 EVENTS)")
    print("==================================================================")
    
    # Count initial lines in output file
    initial_count = 0
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            initial_count = sum(1 for line in f if line.strip())

    # Start resource monitor thread
    mon_thread = threading.Thread(target=monitor_resources, daemon=True)
    mon_thread.start()

    workers = [
        threading.Thread(target=worker_syslog, args=(1, TOTAL_EVENTS_PER_WORKER)),
        threading.Thread(target=worker_cef, args=(2, TOTAL_EVENTS_PER_WORKER)),
        threading.Thread(target=worker_raw, args=(3, TOTAL_EVENTS_PER_WORKER)),
        threading.Thread(target=worker_http_generic, args=(4, TOTAL_EVENTS_PER_WORKER)),
        threading.Thread(target=worker_splunk, args=(5, TOTAL_EVENTS_PER_WORKER)),
    ]

    start_time = time.time()
    for w in workers:
        w.start()

    for w in workers:
        w.join()

    duration = time.time() - start_time
    time.sleep(1) # wait for flush
    benchmark_running = False

    # Count final lines
    final_count = 0
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            final_count = sum(1 for line in f if line.strip())

    events_received = final_count - initial_count
    total_expected = TOTAL_EVENTS_PER_WORKER * len(workers)
    eps = events_received / duration if duration > 0 else 0

    print(f"• Tổng số sự kiện đẩy vào (5 luồng giao thức): {total_expected:,} events")
    print(f"• Số sự kiện Vector đã hứng và ghi đĩa:        {events_received:,} events")
    print(f"• Thời gian thực thi toàn bộ:                  {duration:.2f} giây")
    print(f"• Tốc độ thông lượng đạt được (EPS):           {eps:,.0f} EPS ⚡")
    print("------------------------------------------------------------------")
    print("📈 TIÊU HAO TÀI NGUYÊN HỆ THỐNG:")
    print(f" • RAproxy (PID {RAPROXY_PID}): CPU Peak: {peak_haproxy_cpu:.1f}%, RAM RSS: {peak_haproxy_rss_mb:.1f} MB")
    print(f" • Vector  (PID {VECTOR_PID}): CPU Peak: {peak_vector_cpu:.1f}%, RAM RSS: {peak_vector_rss_mb:.1f} MB")
    print(f" • Tổng tài nguyên RAM cả cụm (HA + Vector):   {peak_haproxy_rss_mb + peak_vector_rss_mb:.1f} MB")
    print("==================================================================")

if __name__ == "__main__":
    main()

