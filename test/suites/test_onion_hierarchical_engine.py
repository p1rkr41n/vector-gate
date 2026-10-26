#!/usr/bin/env python3
"""
QA VERIFICATION SUITE: HIERARCHICAL VRL ONION PARSING ENGINE (v2.4.0)
Validates:
  TC-01: Nginx Combined Log via HTTP Ingress (Shared Payload Parser)
  TC-02: Nginx Combined Log via Syslog Ingress (Shared Payload Parser)
  TC-03: FortiGate Key-Value via Syslog Ingress (Scoped Syslog Parser)
  TC-04: Cisco ASA Regex via Syslog Ingress (Scoped Syslog Parser)
  TC-05: Unknown Network Device (Dead-Letter Discovery, Zero Loss)
  TC-06: Atomic Zero-Downtime Hot-Drop of New Vendor VRL Plugin
"""

import json
import os
import socket
import subprocess
import sys
import time
import urllib.request

GATE_HOST = "127.0.0.1"
GATE_PORT = 5000
FORWARDED_LOGS = "/var/log/vector/forwarded_logs.ndjson"
VRL_DIR = "/home/manager/vectormod/deploy/vrl"

def run_docker_exec(cmd: str) -> str:
    res = subprocess.run(f"docker exec vector-smart-gate {cmd}", shell=True, capture_output=True, text=True)
    return res.stdout.strip()

def truncate_logs():
    run_docker_exec(f"truncate -s 0 {FORWARDED_LOGS}")

def get_logs() -> list:
    out = run_docker_exec(f"cat {FORWARDED_LOGS}")
    lines = [l for l in out.splitlines() if l.strip()]
    events = []
    for l in lines:
        try:
            events.append(json.loads(l))
        except Exception:
            pass
    return events

def send_tcp(payload: bytes):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(3.0)
        s.connect((GATE_HOST, GATE_PORT))
        s.sendall(payload)
        time.sleep(0.1)

def send_http(body: str) -> str:
    req = urllib.request.Request(
        f"http://{GATE_HOST}:{GATE_PORT}/",
        data=body.encode("utf-8"),
        headers={"Content-Type": "text/plain", "User-Agent": "qa-tester"}
    )
    with urllib.request.urlopen(req, timeout=3.0) as resp:
        return resp.read().decode("utf-8")

def main():
    print("=" * 80)
    print("🧪 EXECUTING FULL QA TEST SUITE: HIERARCHICAL ONION VRL PARSING ENGINE v2.4.0")
    print("=" * 80)

    truncate_logs()
    time.sleep(0.5)

    # -------------------------------------------------------------------------
    # TC-01: Nginx via HTTP Ingress -> parsed by vrl/payload/01_nginx.vrl
    # -------------------------------------------------------------------------
    print("\n[TC-01] Testing Nginx Access Log via HTTP POST (Transport: HTTP)...")
    truncate_logs()
    nginx_payload = '192.168.1.100 - - [25/Oct/2026:12:00:00 +0000] "GET /api/v1/users HTTP/1.1" 200 452 "-" "Mozilla/5.0"'
    try:
        send_http(nginx_payload)
    except Exception as e:
        print(f"  [ERROR] HTTP POST failed: {e}")
        sys.exit(1)
    
    time.sleep(0.6)
    logs = get_logs()
    tc1_pass = False
    for ev in reversed(logs):
        if ev.get("type_log") == "http_server" and ev.get("parser_applied") == "payload/01_nginx.vrl":
            if ev.get("vendor") == "Nginx" and ev.get("parser_status") == "SUCCESS":
                tc1_pass = True
                print(f"  [PASS] TC-01: HTTP Nginx -> type_log: '{ev.get('type_log')}', parser: '{ev.get('parser_applied')}', vendor: '{ev.get('vendor')}', status: {ev.get('status')}")
                break
    if not tc1_pass:
        print(f"  [FAIL] TC-01: Expected HTTP Nginx parsed. Output: {logs[-1] if logs else 'EMPTY'}")
        sys.exit(1)

    # -------------------------------------------------------------------------
    # TC-02: Nginx via Syslog RFC 3164 -> parsed by vrl/payload/01_nginx.vrl!
    # -------------------------------------------------------------------------
    print("\n[TC-02] Testing Nginx Access Log via Syslog Ingress (Transport: Syslog)...")
    truncate_logs()
    syslog_nginx = b'<13>Oct 25 12:00:00 web01 nginx: 192.168.1.200 - - [25/Oct/2026:12:00:00 +0000] "POST /api/v1/orders HTTP/1.1" 201 128 "-" "Go-http-client/1.1"\n'
    send_tcp(syslog_nginx)
    time.sleep(0.6)
    logs = get_logs()
    tc2_pass = False
    for ev in reversed(logs):
        if ev.get("type_log") == "syslog" and ev.get("parser_applied") == "payload/01_nginx.vrl":
            if ev.get("vendor") == "Nginx" and ev.get("parser_status") == "SUCCESS":
                tc2_pass = True
                print(f"  [PASS] TC-02: Syslog Nginx -> type_log: '{ev.get('type_log')}', parser: '{ev.get('parser_applied')}', vendor: '{ev.get('vendor')}', status: {ev.get('status')}")
                print("         ⭐️ Proved: Single 'payload/01_nginx.vrl' parses BOTH HTTP & Syslog successfully!")
                break
    if not tc2_pass:
        print(f"  [FAIL] TC-02: Expected Syslog Nginx parsed by payload/01_nginx.vrl. Output: {logs[-1] if logs else 'EMPTY'}")
        sys.exit(1)

    # -------------------------------------------------------------------------
    # TC-03: FortiGate Firewall via Syslog -> parsed by vrl/syslog/01_fortigate.vrl
    # -------------------------------------------------------------------------
    print("\n[TC-03] Testing FortiGate Key-Value via Syslog Ingress...")
    truncate_logs()
    forti_payload = b'<189>Oct 25 12:00:00 fgt01 date=2026-10-25 time=12:00:00 devname="FGT60D" type="traffic" srcip=10.0.0.50 dstip=8.8.8.8 proto=6 action="accept"\n'
    send_tcp(forti_payload)
    time.sleep(0.6)
    logs = get_logs()
    tc3_pass = False
    for ev in reversed(logs):
        if ev.get("type_log") == "syslog" and ev.get("parser_applied") == "syslog/01_fortigate.vrl":
            if ev.get("vendor") == "Fortinet" and ev.get("devname") == "FGT60D" and ev.get("parser_status") == "SUCCESS":
                tc3_pass = True
                print(f"  [PASS] TC-03: FortiGate Syslog -> type_log: '{ev.get('type_log')}', devname: '{ev.get('devname')}', vendor: '{ev.get('vendor')}'")
                break
    if not tc3_pass:
        print(f"  [FAIL] TC-03: FortiGate parse failed. Output: {logs[-1] if logs else 'EMPTY'}")
        sys.exit(1)

    # -------------------------------------------------------------------------
    # TC-04: Cisco ASA Firewall via Syslog -> parsed by vrl/syslog/02_cisco_asa.vrl
    # -------------------------------------------------------------------------
    print("\n[TC-04] Testing Cisco ASA Firewall via Syslog Ingress...")
    truncate_logs()
    cisco_payload = b'<166>Oct 25 12:00:00 cisco-gw01: %ASA-6-302013: Built inbound TCP connection 998877 for outside:192.168.1.150/443\n'
    send_tcp(cisco_payload)
    time.sleep(0.6)
    logs = get_logs()
    tc4_pass = False
    for ev in reversed(logs):
        if ev.get("type_log") == "syslog" and ev.get("parser_applied") == "syslog/02_cisco_asa.vrl":
            if ev.get("vendor") == "Cisco" and ev.get("msg_id") == "302013" and ev.get("parser_status") == "SUCCESS":
                tc4_pass = True
                print(f"  [PASS] TC-04: Cisco ASA Syslog -> type_log: '{ev.get('type_log')}', msg_id: '{ev.get('msg_id')}', vendor: '{ev.get('vendor')}', src_ip: '{ev.get('src_ip')}'")
                break
    if not tc4_pass:
        print(f"  [FAIL] TC-04: Cisco ASA parse failed. Output: {logs[-1] if logs else 'EMPTY'}")
        sys.exit(1)

    # -------------------------------------------------------------------------
    # TC-05: Unknown Network Device (Dead-Letter Discovery, Zero Loss)
    # -------------------------------------------------------------------------
    print("\n[TC-05] Testing Unknown Network Device (Dead-Letter Schema Discovery)...")
    truncate_logs()
    unknown_payload = b'<14>Oct 25 12:00:00 sw01 RUIJIE-SWITCH: Interface GigabitEthernet0/1 changed state to UP\n'
    send_tcp(unknown_payload)
    time.sleep(0.6)
    logs = get_logs()
    tc5_pass = False
    for ev in reversed(logs):
        if ev.get("type_log") == "syslog" and ev.get("_parse_status") == "unmatched":
            if "_raw_signature" in ev and ev.get("parser_status") == "UNPARSED_RAW":
                tc5_pass = True
                print(f"  [PASS] TC-05: Dead-Letter Discovery -> _parse_status: '{ev.get('_parse_status')}', signature: '{ev.get('_raw_signature')}'")
                print("         ⭐️ Proved: Unknown log is NOT lost; tagged with discovery signature!")
                break
    if not tc5_pass:
        print(f"  [FAIL] TC-05: Dead-Letter handling failed. Output: {logs[-1] if logs else 'EMPTY'}")
        sys.exit(1)

    # -------------------------------------------------------------------------
    # TC-06: Hot-Drop of New Vendor VRL Plugin (Snort IDS)
    # -------------------------------------------------------------------------
    print("\n[TC-06] Testing Hot-Drop of New Vendor VRL Plugin (Live SIGHUP Reload)...")
    snort_vrl_path = os.path.join(VRL_DIR, "syslog", "04_snort.vrl")
    snort_content = """#---
# match_contains: "[SNORT]"
# scope: syslog
# vendor: Snort
# priority: 4
#---
parsed, err = parse_regex(.message, r'\\[SNORT\\] (?P<alert_id>\\d+): (?P<alert_msg>.*)')
if err == null {
    . = merge!(., parsed)
    .parsed = true
    .vendor = "Snort"
}
"""
    try:
        with open(snort_vrl_path, "w", encoding="utf-8") as f:
            f.write(snort_content)
        print(f"  [INFO] Dropped new plugin: {snort_vrl_path}")
        time.sleep(3.0) # Wait for watcher 2-second debounce + SIGHUP reload

        truncate_logs()
        snort_payload = b'<34>Oct 25 12:00:00 ids01 snort: [SNORT] 9901: Remote Code Execution Exploit Attempt\n'
        send_tcp(snort_payload)
        time.sleep(0.6)
        logs = get_logs()
        tc6_pass = False
        for ev in reversed(logs):
            if ev.get("type_log") == "syslog" and ev.get("parser_applied") == "syslog/04_snort.vrl":
                if ev.get("vendor") == "Snort" and ev.get("alert_id") == "9901" and ev.get("parser_status") == "SUCCESS":
                    tc6_pass = True
                    print(f"  [PASS] TC-06: Live Hot-Drop -> parser: '{ev.get('parser_applied')}', vendor: '{ev.get('vendor')}', alert_id: '{ev.get('alert_id')}'")
                    break
        if not tc6_pass:
            print(f"  [FAIL] TC-06: Hot-Drop Snort failed. Output: {logs[-1] if logs else 'EMPTY'}")
            sys.exit(1)
    finally:
        if os.path.exists(snort_vrl_path):
            os.remove(snort_vrl_path)
            time.sleep(1.0)
            print("  [CLEANUP] Removed temporary 04_snort.vrl")

    print("\n" + "=" * 80)
    print("🏆 ALL 6/6 QA ACCEPTANCE TEST SCENARIOS PASSED WITH 100% SUCCESS!")
    print("=" * 80)

if __name__ == "__main__":
    main()
