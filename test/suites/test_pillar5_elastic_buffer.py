#!/usr/bin/env python3
"""
==============================================================================
QA TEST SUITE: PILLAR 5 - ELASTIC BUFFERING & DEDUPLICATION VERIFICATION
==============================================================================
Validates:
  TC-P5-01: Verification of Safe Buffer Mode ('when_full: drop_newest' vs deadlock)
  TC-P5-02: Universal Beats Sliding-Window Lumberjack Deduplication
  TC-P5-03: Disk Buffer Resilience & Max Capacity Configuration Check
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
CONFIG_FILE = "/home/manager/vectormod/deploy/config/vector.yaml"

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

def send_lumberjack_batch(host: str, port: int, start_seq: int, events: list, timeout: float = 5.0) -> list:
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
    print(f"{Colors.BOLD}{Colors.CYAN}  🔬 QA TEST SUITE: PILLAR 5 - ELASTIC BUFFERING & DEDUPE{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*75}{Colors.RESET}\n")

    passed = 0
    total = 0

    # -------------------------------------------------------------------------
    # TEST 1: Config Inspection for when_full: drop_newest
    # -------------------------------------------------------------------------
    total += 1
    print("▶ [TC-P5-01] Validating Safe Buffer Policy ('when_full: drop_newest')...")
    with open(CONFIG_FILE, "r") as f:
        content = f.read()

    if "when_full: drop_newest" in content and "when_full: block" not in content:
        print(f"  {Colors.GREEN}✔ [PASS]{Colors.RESET} File sink buffer verified: 'when_full: drop_newest' (Deadlock risk eliminated)")
        passed += 1
    else:
        print(f"  {Colors.RED}✘ [FAIL]{Colors.RESET} Unsafe 'when_full: block' still detected in configuration")

    # -------------------------------------------------------------------------
    # TEST 2: Sliding-Window Deduplication (Beats Lumberjack)
    # -------------------------------------------------------------------------
    total += 1
    corr_beats = f"DEDUPE_BEATS_{uuid.uuid4().hex[:6]}"
    beats_msg = f"Beats duplicate event {corr_beats}"

    print("▶ [TC-P5-02] Testing Beats Lumberjack Deduplication (Sending duplicate frames across 2 connections)...")
    acks1 = send_lumberjack_batch(TARGET_HOST, TARGET_PORT, start_seq=1, events=[beats_msg])
    time.sleep(0.2)
    acks2 = send_lumberjack_batch(TARGET_HOST, TARGET_PORT, start_seq=1, events=[beats_msg])
    time.sleep(1.0)

    events = get_forwarded_logs(300)
    matched_beats = [e for e in events if corr_beats in json.dumps(e)]

    if len(matched_beats) == 1:
        print(f"  {Colors.GREEN}✔ [PASS]{Colors.RESET} Duplicate Beats frame suppressed! Exactly 1 record written (matched: {len(matched_beats)})")
        passed += 1
    else:
        print(f"  {Colors.RED}✘ [FAIL]{Colors.RESET} Beats deduplication mismatch: expected 1 record, found {len(matched_beats)}")

    # -------------------------------------------------------------------------
    # TEST 3: Disk Buffer Capacity and Policy Integrity Check
    # -------------------------------------------------------------------------
    total += 1
    print("▶ [TC-P5-03] Checking Disk Buffer Capacity (10GB) and Persistence Specs...")
    if "max_size: 10737418240" in content and "type: disk" in content:
        print(f"  {Colors.GREEN}✔ [PASS]{Colors.RESET} Disk buffer capacity set to 10GB with persistent disk journal storage")
        passed += 1
    else:
        print(f"  {Colors.RED}✘ [FAIL]{Colors.RESET} Disk buffer capacity mismatch")

    # -------------------------------------------------------------------------
    # SUMMARY
    # -------------------------------------------------------------------------
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*75}{Colors.RESET}")
    print(f"📊 SUMMARY: {passed} / {total} Test Cases Passed ({(passed/total)*100:.1f}%)")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*75}{Colors.RESET}\n")

    return 0 if passed == total else 1

if __name__ == "__main__":
    sys.exit(main())
