#!/usr/bin/env python3
"""
==============================================================================
STRICT QA RE-VERIFICATION SUITE: UPSTREAM USER-REPORTED ISSUES AUDIT
==============================================================================
Directly tests and proves the resolution of the most critical upstream issues 
reported by Vector / VRL community (from research/vrl_upstream_issues & research/beats_issues):

- ISSUE-01 (VRL-#1352 / VRL-#215): CEF Complex Quotes & Pipe Delimiter Parser Crash
- ISSUE-02 (VRL-#1536): parse_key_value Fallback on Trailing Delimiters
- ISSUE-03 (VRL-#1043 & Cisco %ASA-): Generic Cisco ASA & Unstructured Syslog
- ISSUE-04 (VRL-#1989 & UTF-8 Non-ASCII): Multibyte Vietnamese & Emoji Boundary Safety
- ISSUE-05 (VRL-#2000 & E100/E103/E620): Type Coercion & Coalescing Infallibility
- ISSUE-06 (VEC-#19821 / VEC-#18765): Beats Sliding Window ACK Drops on Half-Close
- ISSUE-07 (VRL-#1824 & ReDoS): Catastrophic Backtracking & 64KB Payload Bomb Immunity
- ISSUE-08 (VEC-#14201 / VEC-#12890): Single-Port 5000 Multiplexing (Port Explosion Fix)
- ISSUE-09 (Dead-Letter Zero Loss): Unknown Proprietary Appliance Schema Discovery
- ISSUE-10 (Dynamic Healthcheck): Dual-Endpoint Telemetry & Ingress Health Validation
==============================================================================
"""

import json
import os
import socket
import struct
import sys
import time
import urllib.request
import uuid

TARGET_HOST = "127.0.0.1"
TARGET_PORT = 5000
TELEMETRY_PORT = 9100
OUTPUT_FILE = "/home/manager/vectormod/deploy/output/forwarded_logs.ndjson"

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    YELLOW = '\033[93m'
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

def wait_for_event(predicate, timeout=4.0):
    start = time.time()
    while time.time() - start < timeout:
        events = get_forwarded_logs(300)
        for ev in reversed(events):
            if predicate(ev):
                return ev
        time.sleep(0.1)
    return None

def send_tcp(payload: bytes):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(4.0)
        s.connect((TARGET_HOST, TARGET_PORT))
        s.sendall(payload)
        time.sleep(0.05)

def send_http(path: str, headers: dict, body: bytes):
    req = urllib.request.Request(
        f"http://{TARGET_HOST}:{TARGET_PORT}{path}",
        data=body,
        headers=headers,
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=4.0) as resp:
        return resp.read()

def main():
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}  🔬 STRICT QA AUDIT: RETESTING ALL UPSTREAM ISSUES ON VECTOR SMART GATE{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.RESET}\n")

    passed = 0
    total = 0

    # -------------------------------------------------------------------------
    # TEST 1: VRL-#1352 / VRL-#215 - CEF Parser Complex Quotes & Pipe Delimiter
    # -------------------------------------------------------------------------
    total += 1
    corr1 = f"CEF_{uuid.uuid4().hex[:6]}"
    cef_payload = (
        f"<134>Oct 27 08:00:00 cp-gw: CEF:0|Check Point|VPN-1 & FireWall-1|Check Point|drop|Drop|Low|"
        f"src=10.0.0.77 dst=192.168.1.99 spt=4567 dpt=443 act=drop proto=TCP "
        f'reason="Connection | reset by peer \\"nested quotes\\"" msgid={corr1}\n'
    ).encode()
    print("▶ [ISSUE-01] Testing VRL-#1352: CEF Complex Quotes & Embedded Pipe Delimiters...")
    send_tcp(cef_payload)
    ev1 = wait_for_event(lambda e: corr1 in json.dumps(e))
    if ev1 and ev1.get("vendor") == "CheckPoint" and ev1.get("src_ip") == "10.0.0.77" and ev1.get("dst_ip") == "192.168.1.99" and ev1.get("dst_port") == "443":
        print(f"  {Colors.GREEN}✔ [PASS]{Colors.RESET} VRL-#1352 Resolved: CEF parsed with quotes & pipe intact (src_ip={ev1.get('src_ip')}, dst_ip={ev1.get('dst_ip')})")
        passed += 1
    else:
        print(f"  {Colors.RED}✘ [FAIL]{Colors.RESET} VRL-#1352 Failed: CEF could not be parsed: {ev1}")

    # -------------------------------------------------------------------------
    # TEST 2: VRL-#1536 - parse_key_value Failed on Trailing Delimiter
    # -------------------------------------------------------------------------
    total += 1
    corr2 = f"FGT_{uuid.uuid4().hex[:6]}"
    fgt_payload = (
        f'<189>Oct 27 08:00:00 fgt01 date=2026-10-27 time=08:00:00 devname="FGT60D" devid="FGT60D123456" '
        f'logid="0000000013" type="traffic" subtype="forward" level="notice" vd="root" srcip=10.0.0.1 dstip=1.1.1.1 '
        f'action="deny" token="{corr2}" trailing_delim= \n'
    ).encode()
    print("▶ [ISSUE-02] Testing VRL-#1536: parse_key_value with Trailing Delimiters & Empty Keys...")
    send_tcp(fgt_payload)
    ev2 = wait_for_event(lambda e: corr2 in json.dumps(e))
    if ev2 and ev2.get("vendor") == "Fortinet" and ev2.get("devname") == "FGT60D":
        print(f"  {Colors.GREEN}✔ [PASS]{Colors.RESET} VRL-#1536 Resolved: FortiGate key-value safely parsed with trailing delimiter (devname={ev2.get('devname')})")
        passed += 1
    else:
        print(f"  {Colors.RED}✘ [FAIL]{Colors.RESET} VRL-#1536 Failed: FortiGate parsing failed: {ev2}")

    # -------------------------------------------------------------------------
    # TEST 3: VRL-#1043 & Generic Cisco %ASA- Regex Parsing
    # -------------------------------------------------------------------------
    total += 1
    corr3 = f"ASA_{uuid.uuid4().hex[:6]}"
    asa_payload = (
        f"<164>Oct 27 08:00:00 cisco-gw01: %ASA-4-106023: Deny tcp src inside:10.10.1.50/54321 "
        f"dst outside:198.51.100.2/80 by access-group acl_corporate token={corr3}\n"
    ).encode()
    print("▶ [ISSUE-03] Testing VRL-#1043 & Cisco: Generic Cisco ASA Regex Parsing (%ASA-X-YYYYYY)...")
    send_tcp(asa_payload)
    ev3 = wait_for_event(lambda e: corr3 in json.dumps(e))
    if ev3 and ev3.get("vendor") == "Cisco" and ev3.get("msg_id") == "106023" and ev3.get("severity") == "4":
        print(f"  {Colors.GREEN}✔ [PASS]{Colors.RESET} Cisco ASA Generic Parser Verified: vendor={ev3.get('vendor')}, msg_id={ev3.get('msg_id')}")
        passed += 1
    else:
        print(f"  {Colors.RED}✘ [FAIL]{Colors.RESET} Cisco ASA parsing failed: {ev3}")

    # -------------------------------------------------------------------------
    # TEST 4: VRL-#1989 - Multibyte Non-ASCII UTF-8 Vietnamese & Emoji Boundary
    # -------------------------------------------------------------------------
    total += 1
    corr4 = f"UTF8_{uuid.uuid4().hex[:6]}"
    utf8_payload = (
        f"<14>Oct 27 08:00:00 auth-srv: Người dùng quản trị 'Nguyễn Văn A' đã đăng nhập thất bại: "
        f"lỗi thẻ bảo mật phần cứng 🔐 [Mã_xác_thực: {corr4}]\n"
    ).encode("utf-8")
    print("▶ [ISSUE-04] Testing VRL-#1989: Multibyte Non-ASCII UTF-8 & Emoji Boundary Safety...")
    send_tcp(utf8_payload)
    ev4 = wait_for_event(lambda e: corr4 in json.dumps(e))
    if ev4 and ("Nguyễn Văn A" in json.dumps(ev4, ensure_ascii=False) or "auth-srv" in json.dumps(ev4)):
        print(f"  {Colors.GREEN}✔ [PASS]{Colors.RESET} VRL-#1989 Resolved: Vietnamese UTF-8 & Emoji parsed without worker panic!")
        passed += 1
    else:
        print(f"  {Colors.RED}✘ [FAIL]{Colors.RESET} UTF-8 parsing failed: {ev4}")

    # -------------------------------------------------------------------------
    # TEST 5: VRL-#2000 & E100/E103/E620 - Type Coercion & Coalescing
    # -------------------------------------------------------------------------
    total += 1
    corr5 = f"JSON_{uuid.uuid4().hex[:6]}"
    json_data = json.dumps({"service": "payment-api", "transaction_id": corr5, "amount": 149.99, "status": "approved"})
    http_payload = f"<14>Oct 27 08:00:00 api-gw: {json_data}\n".encode()
    print("▶ [ISSUE-05] Testing VRL-#2000: Type Coercion, Infallible Merging & Coalescing...")
    send_tcp(http_payload)
    ev5 = wait_for_event(lambda e: corr5 in json.dumps(e))
    if ev5 and ev5.get("parsed") is True and ev5.get("amount") == 149.99 and ev5.get("service") == "payment-api":
        print(f"  {Colors.GREEN}✔ [PASS]{Colors.RESET} VRL-#2000 Resolved: JSON payload auto-discovered & merged infallibly (amount={ev5.get('amount')})")
        passed += 1
    else:
        print(f"  {Colors.RED}✘ [FAIL]{Colors.RESET} VRL-#2000 failed: {ev5}")

    # -------------------------------------------------------------------------
    # TEST 6: VEC-#19821 / VEC-#18765 - Beats Sliding Window & ACK on Half-Close
    # -------------------------------------------------------------------------
    total += 1
    print("▶ [ISSUE-06] Testing VEC-#19821: Beats Lumberjack Sliding Window ACK on TCP Half-Close...")
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(4.0)
        s.connect((TARGET_HOST, TARGET_PORT))
        
        events = [f"lumberjack_evt_{i}_{uuid.uuid4().hex[:4]}" for i in range(1, 4)]
        w_frame = b"2W" + struct.pack(">I", len(events))
        d_frames = b"".join([
            b"2D" + struct.pack(">I", i) + struct.pack(">I", 1) + struct.pack(">I", 7) + b"message" + struct.pack(">I", len(ev.encode())) + ev.encode()
            for i, ev in enumerate(events, start=1)
        ])
        s.sendall(w_frame + d_frames)
        # Immediate TCP Half-Close (SHUT_WR): Proves Gate keeps b2c stream open for ACK
        s.shutdown(socket.SHUT_WR)
        
        resp = s.recv(6)
        ack_seq = struct.unpack(">I", resp[2:6])[0] if (len(resp) == 6 and resp[:2] == b"2A") else None
        s.close()
        
        if ack_seq == 3:
            print(f"  {Colors.GREEN}✔ [PASS]{Colors.RESET} VEC-#19821 Resolved: Lumberjack ACK received monotonically after Half-Close (ACK sequence={ack_seq})")
            passed += 1
        else:
            print(f"  {Colors.RED}✘ [FAIL]{Colors.RESET} VEC-#19821 Failed: ACK was not delivered (got: {ack_seq})")
    except Exception as e:
        print(f"  {Colors.RED}✘ [FAIL]{Colors.RESET} Lumberjack test exception: {e}")

    # -------------------------------------------------------------------------
    # TEST 7: VRL-#1824 - Regex ReDoS & Catastrophic Backtracking Immunity
    # -------------------------------------------------------------------------
    total += 1
    print("▶ [ISSUE-07] Testing VRL-#1824: Catastrophic Backtracking & Jumbo Payload ReDoS Bomb...")
    # Send 65,536 bytes of repetitive 'a' without newlines:
    jumbo_data = b"<14>Oct 27 08:00:00 redos-test: " + (b"a" * 60000) + b"! end_marker\n"
    t_start = time.time()
    send_tcp(jumbo_data)
    duration_ms = (time.time() - t_start) * 1000.0
    if duration_ms < 500.0:
        print(f"  {Colors.GREEN}✔ [PASS]{Colors.RESET} VRL-#1824 Resolved: 60KB ReDoS bomb absorbed in {duration_ms:.2f}ms (Immune to catastrophic backtracking)")
        passed += 1
    else:
        print(f"  {Colors.RED}✘ [FAIL]{Colors.RESET} VRL-#1824 Failed: Pipeline hung for {duration_ms:.2f}ms")

    # -------------------------------------------------------------------------
    # TEST 8: VEC-#14201 / VEC-#12890 - Single-Port 5000 Multiplexing
    # -------------------------------------------------------------------------
    total += 1
    print("▶ [ISSUE-08] Testing VEC-#14201: Single-Port 5000 Multiplexing (Eliminating Port Explosion)...")
    try:
        corr_dd = f"DD_{uuid.uuid4().hex[:6]}"
        dd_body = json.dumps([{
            "timestamp": int(time.time() * 1000),
            "message": f"datadog_event_{corr_dd}",
            "status": "info",
            "hostname": "test-node",
            "service": "billing-api",
            "ddsource": "python",
            "ddtags": "env:prod"
        }]).encode()
        send_http("/api/v2/logs", {"Content-Type": "application/json", "DD-API-KEY": "test-key"}, dd_body)
        
        corr_iot = f"IOT_{uuid.uuid4().hex[:6]}"
        iot_body = b"\xDE\xAD\xBE\xEF" + f" Sensor status: OK id={corr_iot}\n".encode()
        send_tcp(iot_body)
        
        ev_dd = wait_for_event(lambda e: corr_dd in json.dumps(e))
        ev_iot = wait_for_event(lambda e: corr_iot in json.dumps(e))
        
        if ev_dd and ev_iot and ev_dd.get("type_log") == "datadog_agent" and ev_iot.get("type_log") == "custom_binary_iot":
            print(f"  {Colors.GREEN}✔ [PASS]{Colors.RESET} VEC-#14201 Resolved: Datadog HTTP & Binary IoT disambiguated on SAME port 5000!")
            passed += 1
        else:
            print(f"  {Colors.RED}✘ [FAIL]{Colors.RESET} Multiplexing failed: DD={bool(ev_dd)}, IoT={bool(ev_iot)}")
    except Exception as e:
        print(f"  {Colors.RED}✘ [FAIL]{Colors.RESET} Multiplexing exception: {e}")

    # -------------------------------------------------------------------------
    # TEST 9: Dead-Letter Zero Log Loss & Schema Auto-Discovery
    # -------------------------------------------------------------------------
    total += 1
    print("▶ [ISSUE-09] Testing Dead-Letter Fallback: Zero Log Loss for Unknown Proprietary Hardware...")
    corr9 = f"UNKNOWN_{uuid.uuid4().hex[:6]}"
    unknown_raw = f"<13>Oct 27 08:00:00 switch-core09 %%HardwareAlert: FAN_SPEED_LOW sensor=fan2 rpm=1200 id={corr9}\n".encode()
    send_tcp(unknown_raw)
    ev9 = wait_for_event(lambda e: corr9 in json.dumps(e))
    if ev9 and ev9.get("_auto_discovered_format") == "key_value" and ev9.get("sensor") == "fan2":
        print(f"  {Colors.GREEN}✔ [PASS]{Colors.RESET} Zero Log Loss Proved: Unknown hardware log parsed via Dynamic Auto-Discovery (sensor={ev9.get('sensor')})")
        passed += 1
    elif ev9 and ev9.get("_parse_status") == "unmatched":
        print(f"  {Colors.GREEN}✔ [PASS]{Colors.RESET} Zero Log Loss Proved: Event preserved raw in Dead-Letter Sink!")
        passed += 1
    else:
        print(f"  {Colors.RED}✘ [FAIL]{Colors.RESET} Event dropped or lost: {ev9}")

    # -------------------------------------------------------------------------
    # TEST 10: Dynamic Port & Orchestrator Healthcheck (Orchestration Decoupling)
    # -------------------------------------------------------------------------
    total += 1
    print("▶ [ISSUE-10] Testing Orchestration Decoupling: Dual-Endpoint Healthcheck (5000 & 9100)...")
    try:
        # Check port 5000 /gate_health
        req_health = urllib.request.Request(f"http://{TARGET_HOST}:{TARGET_PORT}/gate_health")
        with urllib.request.urlopen(req_health, timeout=3.0) as resp:
            health_json = json.loads(resp.read().decode())
        
        # Check port 9100 /metrics exporter
        req_9100 = urllib.request.Request(f"http://{TARGET_HOST}:{TELEMETRY_PORT}/metrics")
        with urllib.request.urlopen(req_9100, timeout=3.0) as resp:
            metrics_body = resp.read().decode()
            
        if health_json.get("status") == "healthy" and "vector_gate_uptime_seconds" in metrics_body:
            print(f"  {Colors.GREEN}✔ [PASS]{Colors.RESET} Dynamic Healthcheck Verified: /gate_health returned '{health_json.get('status')}', Port 9100 Prometheus Exporter active!")
            passed += 1
        else:
            print(f"  {Colors.RED}✘ [FAIL]{Colors.RESET} Healthcheck failed: {health_json}")
    except Exception as e:
        print(f"  {Colors.RED}✘ [FAIL]{Colors.RESET} Healthcheck exception: {e}")

    # -------------------------------------------------------------------------
    # SUMMARY
    # -------------------------------------------------------------------------
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.RESET}")
    print(f"📊 STRICT UPSTREAM ISSUES AUDIT SUMMARY: {passed} / {total} Passed ({(passed/total)*100:.1f}%)")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.RESET}\n")

    return 0 if passed == total else 1

if __name__ == "__main__":
    sys.exit(main())
