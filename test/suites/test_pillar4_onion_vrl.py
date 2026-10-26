#!/usr/bin/env python3
"""
==============================================================================
QA TEST SUITE: PILLAR 4 - UNIVERSAL ONION VRL & SCHEMA AUTO-DISCOVERY
==============================================================================
Validates:
  TC-P4-01: Universal Cisco ASA Generic Fallback (%ASA-X-YYYYYY)
  TC-P4-02: CheckPoint CEF Extension Deep Key-Value Extraction
  TC-P4-03: Zero-Day Dynamic Schema Auto-Discovery (JSON payload)
  TC-P4-04: Zero-Day Dynamic Schema Auto-Discovery (Key-Value payload)
"""

import json
import os
import socket
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
        s.settimeout(3.0)
        s.connect((TARGET_HOST, TARGET_PORT))
        s.sendall(payload)
        time.sleep(0.05)

def main():
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*75}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}  🔬 QA TEST SUITE: PILLAR 4 - UNIVERSAL ONION VRL & AUTO-DISCOVERY{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*75}{Colors.RESET}\n")

    passed = 0
    total = 0

    # -------------------------------------------------------------------------
    # TEST 1: Universal Cisco ASA Generic Fallback
    # -------------------------------------------------------------------------
    total += 1
    corr1 = f"ASA_{uuid.uuid4().hex[:6]}"
    asa_raw = f"<164>Oct 26 12:00:00 cisco-gw02: %ASA-4-106023: Deny tcp src inside:10.10.1.50/54321 dst outside:198.51.100.2/80 by access-group {corr1}\n".encode()
    print("▶ [TC-P4-01] Testing Universal Cisco ASA Generic Fallback (%ASA-4-106023)...")
    send_tcp(asa_raw)
    ev1 = wait_for_event(lambda e: corr1 in json.dumps(e))
    if ev1 and ev1.get("vendor") == "Cisco" and ev1.get("msg_id") == "106023" and ev1.get("severity") == "4":
        print(f"  {Colors.GREEN}✔ [PASS]{Colors.RESET} Generic Cisco ASA message parsed! vendor='{ev1.get('vendor')}', msg_id='{ev1.get('msg_id')}', severity='{ev1.get('severity')}'")
        passed += 1
    else:
        print(f"  {Colors.RED}✘ [FAIL]{Colors.RESET} Failed to parse generic Cisco ASA message: {ev1}")

    # -------------------------------------------------------------------------
    # TEST 2: CheckPoint CEF Extension Deep Key-Value Extraction
    # -------------------------------------------------------------------------
    total += 1
    corr2 = f"CEF_{uuid.uuid4().hex[:6]}"
    cef_raw = f"<134>Oct 26 12:00:00 cp-gw01: CEF:0|Check Point|VPN-1 & FireWall-1|Check Point|drop|Drop|Low|src=10.0.0.77 dst=192.168.1.99 spt=4567 dpt=443 act=drop proto=TCP msgid={corr2}\n".encode()
    print("▶ [TC-P4-02] Testing CheckPoint CEF Extension Deep Key-Value Extraction...")
    send_tcp(cef_raw)
    ev2 = wait_for_event(lambda e: corr2 in json.dumps(e))
    if ev2 and ev2.get("vendor") == "CheckPoint" and ev2.get("src_ip") == "10.0.0.77" and ev2.get("dst_ip") == "192.168.1.99" and ev2.get("dst_port") == "443":
        print(f"  {Colors.GREEN}✔ [PASS]{Colors.RESET} CEF extension fields extracted into SIEM schema: src_ip='{ev2.get('src_ip')}', dst_ip='{ev2.get('dst_ip')}', dst_port='{ev2.get('dst_port')}', action='{ev2.get('action')}'")
        passed += 1
    else:
        print(f"  {Colors.RED}✘ [FAIL]{Colors.RESET} Failed CEF extension extraction: {ev2}")

    # -------------------------------------------------------------------------
    # TEST 3: Zero-Day Dynamic Schema Auto-Discovery (JSON payload)
    # -------------------------------------------------------------------------
    total += 1
    corr3 = f"JSON_{uuid.uuid4().hex[:6]}"
    json_body = json.dumps({"service": "payment-api", "transaction_id": corr3, "amount": 99.50, "currency": "USD"})
    json_raw = f"<14>Oct 26 12:00:00 app-srv01 myapp: {json_body}\n".encode()
    print("▶ [TC-P4-03] Testing Zero-Day Dynamic Schema Auto-Discovery (JSON Syslog)...")
    send_tcp(json_raw)
    ev3 = wait_for_event(lambda e: corr3 in json.dumps(e))
    if ev3 and ev3.get("parsed") is True and ev3.get("service") == "payment-api" and ev3.get("amount") == 99.5:
        print(f"  {Colors.GREEN}✔ [PASS]{Colors.RESET} Auto-discovered/Parsed JSON schema: parser='{ev3.get('parser_applied')}', service='{ev3.get('service')}', amount={ev3.get('amount')}")
        passed += 1
    else:
        print(f"  {Colors.RED}✘ [FAIL]{Colors.RESET} Failed JSON auto-discovery: {ev3}")

    # -------------------------------------------------------------------------
    # TEST 4: Zero-Day Dynamic Schema Auto-Discovery (Key-Value payload)
    # -------------------------------------------------------------------------
    total += 1
    corr4 = f"KV_{uuid.uuid4().hex[:6]}"
    kv_raw = f"<14>Oct 26 12:00:00 router01 cluster=prod-us user=admin_sec status=blocked auth_token={corr4} reason=token_expired\n".encode()
    print("▶ [TC-P4-04] Testing Zero-Day Dynamic Schema Auto-Discovery (Key-Value Syslog)...")
    send_tcp(kv_raw)
    ev4 = wait_for_event(lambda e: corr4 in json.dumps(e))
    if ev4 and ev4.get("parsed") is True and ev4.get("_auto_discovered_format") == "key_value" and ev4.get("user") == "admin_sec":
        print(f"  {Colors.GREEN}✔ [PASS]{Colors.RESET} Auto-discovered Key-Value schema without prior vendor definition: user='{ev4.get('user')}', reason='{ev4.get('reason')}'")
        passed += 1
    else:
        print(f"  {Colors.RED}✘ [FAIL]{Colors.RESET} Failed Key-Value auto-discovery: {ev4}")

    # -------------------------------------------------------------------------
    # SUMMARY
    # -------------------------------------------------------------------------
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*75}{Colors.RESET}")
    print(f"📊 SUMMARY: {passed} / {total} Test Cases Passed ({(passed/total)*100:.1f}%)")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*75}{Colors.RESET}\n")

    return 0 if passed == total else 1

if __name__ == "__main__":
    sys.exit(main())
