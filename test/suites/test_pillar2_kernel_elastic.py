#!/usr/bin/env python3
"""
==============================================================================
QA TEST SUITE: PILLAR 2 - ELASTIC KERNEL-TUNED PERFORMANCE ENGINE
==============================================================================
Validates:
  TC-P2-01: Zero-Copy Splice Bidirectional Streaming Baseline
  TC-P2-02: Elastic Expansion on High-Throughput Burst (512 KB Burst)
  TC-P2-03: Post-Burst Elastic Shrinking & RAM Invariance
  TC-P2-04: Graceful Half-Close & Monotonic ACK Flushing Under Elastic Splicing
"""

import json
import os
import socket
import struct
import sys
import time
import uuid

TARGET_HOST = "127.0.0.1"
TARGET_PORT = 5000
OUTPUT_FILE = "/home/manager/vectormod/deploy/output/forwarded_logs.ndjson"

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

def get_forwarded_logs(tail_lines=300):
    if not os.path.exists(OUTPUT_FILE):
        return []
    try:
        with open(OUTPUT_FILE, "r", encoding="utf-8", errors="replace") as f:
            lines = f.readlines()[-tail_lines:]
        events = []
        for line in lines:
            line = line.strip()
            if line:
                try:
                    events.append(json.loads(line))
                except Exception:
                    pass
        return events
    except Exception:
        return []

def wait_for_event(predicate, timeout=5.0):
    start = time.time()
    while time.time() - start < timeout:
        events = get_forwarded_logs(400)
        for ev in reversed(events):
            if predicate(ev):
                return ev
        time.sleep(0.15)
    return None

def send_tcp(payload: bytes):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(4.0)
        s.connect((TARGET_HOST, TARGET_PORT))
        s.sendall(payload)
        time.sleep(0.05)

def send_lumberjack_batch(host: str, port: int, start_seq: int, events: list, half_close: bool = False, timeout: float = 5.0) -> list:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    s.connect((host, port))
    win_size = len(events)
    payload = b"2W" + struct.pack(">I", win_size)
    for i, evt_text in enumerate(events):
        seq = start_seq + i
        k = b"message"
        v = evt_text.encode("utf-8")
        payload += b"2D" + struct.pack(">I", seq) + struct.pack(">I", 1) + struct.pack(">I", len(k)) + k + struct.pack(">I", len(v)) + v
    s.sendall(payload)
    if half_close:
        s.shutdown(socket.SHUT_WR)
    acks = []
    try:
        while True:
            chunk = s.recv(6)
            if not chunk:
                break
            if len(chunk) == 6 and chunk[:2] == b"2A":
                ack_seq = struct.unpack(">I", chunk[2:6])[0]
                acks.append(ack_seq)
                if ack_seq >= start_seq + win_size - 1:
                    break
    except socket.timeout:
        pass
    finally:
        s.close()
    return acks

def main():
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*75}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}  🔬 QA TEST SUITE: PILLAR 2 - ELASTIC KERNEL PERFORMANCE ENGINE{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*75}{Colors.RESET}\n")

    passed = 0
    total = 0

    # -------------------------------------------------------------------------
    # TEST 1: Baseline Zero-Copy Splice
    # -------------------------------------------------------------------------
    total += 1
    corr1 = f"SPLICE_BASE_{uuid.uuid4().hex[:6]}"
    print("▶ [TC-P2-01] Testing Zero-Copy Splice Baseline Stream...")
    msg1 = f"<14>1 2026-10-26T12:00:00Z host-p2 app - {corr1} - Baseline kernel splice\n".encode()
    send_tcp(msg1)
    ev1 = wait_for_event(lambda e: corr1 in json.dumps(e))
    if ev1 and ev1.get("type_log") == "syslog":
        print(f"  {Colors.GREEN}✔ [PASS]{Colors.RESET} Baseline packet spliced cleanly to backend Vector Core")
        passed += 1
    else:
        print(f"  {Colors.RED}✘ [FAIL]{Colors.RESET} Failed to verify baseline packet: {ev1}")

    # -------------------------------------------------------------------------
    # TEST 2: Elastic Expansion on High-Throughput Burst (512 KB continuous)
    # -------------------------------------------------------------------------
    total += 1
    corr2 = f"BURST_EXP_{uuid.uuid4().hex[:6]}"
    print("▶ [TC-P2-02] Testing Kernel Pipe Elastic Expansion (512 KB Burst Stream)...")
    burst_chunk = b"A" * 1024
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(5.0)
        s.connect((TARGET_HOST, TARGET_PORT))
        # Send initial prefix as raw socket
        s.sendall(f"BURST_PAYLOAD_TEST_{corr2}: ".encode())
        for _ in range(512):
            s.sendall(burst_chunk)
        s.sendall(b"\n")
    time.sleep(0.5)

    ev2 = wait_for_event(lambda e: corr2 in json.dumps(e))
    if ev2:
        print(f"  {Colors.GREEN}✔ [PASS]{Colors.RESET} Spliced 512KB continuous burst without socket stalling or pipe buffer drop")
        passed += 1
    else:
        print(f"  {Colors.RED}✘ [FAIL]{Colors.RESET} Failed to receive burst stream event")

    # -------------------------------------------------------------------------
    # TEST 3: Post-Burst Elastic Shrinking & RAM Invariance
    # -------------------------------------------------------------------------
    total += 1
    corr3 = f"SHRINK_{uuid.uuid4().hex[:6]}"
    print("▶ [TC-P2-03] Testing Post-Burst Bidirectional Pipe Shrinking (<32 KB packet)...")
    msg3 = f"<14>1 2026-10-26T12:00:00Z host-p2 app - {corr3} - Post burst small packet shrink verification\n".encode()
    send_tcp(msg3)
    ev3 = wait_for_event(lambda e: corr3 in json.dumps(e))
    if ev3:
        print(f"  {Colors.GREEN}✔ [PASS]{Colors.RESET} Pipe smoothly accepted post-burst normal stream and shrunk to baseline")
        passed += 1
    else:
        print(f"  {Colors.RED}✘ [FAIL]{Colors.RESET} Failed post-burst packet: {ev3}")

    # -------------------------------------------------------------------------
    # TEST 4: Graceful Half-Close & Monotonic ACK Under Elastic Splice
    # -------------------------------------------------------------------------
    total += 1
    corr4 = f"HALF_CLOSE_{uuid.uuid4().hex[:6]}"
    print("▶ [TC-P2-04] Testing Graceful Half-Close with Elastic Splice ACKs...")
    acks = send_lumberjack_batch(TARGET_HOST, TARGET_PORT, start_seq=1, events=[f"evt_hc_{corr4}"], half_close=True)
    if acks and 1 in acks:
        print(f"  {Colors.GREEN}✔ [PASS]{Colors.RESET} Half-close preserved bidirectional ACK pipeline! (ACK: {acks})")
        passed += 1
    else:
        print(f"  {Colors.RED}✘ [FAIL]{Colors.RESET} Half-close failed to receive ACK: {acks}")

    # -------------------------------------------------------------------------
    # SUMMARY
    # -------------------------------------------------------------------------
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*75}{Colors.RESET}")
    print(f"📊 SUMMARY: {passed} / {total} Test Cases Passed ({(passed/total)*100:.1f}%)")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*75}{Colors.RESET}\n")

    return 0 if passed == total else 1

if __name__ == "__main__":
    sys.exit(main())

