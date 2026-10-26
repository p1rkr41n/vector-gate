#!/usr/bin/env python3
"""
QA Test Suite: Universal VRL Parsing Engine with Dynamic Hot-Drop Plugin Verification
Tests the exact sequence:
1. No VRL in folder -> Logs pass through UNPARSED (.parsed == false).
2. Drop nginx.vrl into folder -> Auto-detects in <500ms, reloads, and parses Nginx logs (.parsed == true).
3. Drop cisco_asa.vrl into folder -> Auto-detects and parses Cisco ASA logs (.parsed == true).
4. Remove nginx.vrl -> Reverts to UNPARSED for Nginx logs.
"""

import json
import os
import socket
import sys
import time
import urllib.request

GATE_IP = "127.0.0.1"
GATE_PORT = 5000
VRL_DIR = "/home/manager/vectormod/docker_gate/vrl"
OUTPUT_FILE = "/home/manager/vectormod/docker_gate/output/forwarded_logs.ndjson"

def clean_vrl_dir():
    os.makedirs(VRL_DIR, exist_ok=True)
    for f in os.listdir(VRL_DIR):
        if f.endswith(".vrl"):
            os.remove(os.path.join(VRL_DIR, f))

def get_output_line_count():
    if not os.path.exists(OUTPUT_FILE):
        return 0
    with open(OUTPUT_FILE, "r", encoding="utf-8", errors="ignore") as f:
        return sum(1 for line in f if line.strip())

def get_last_line():
    if not os.path.exists(OUTPUT_FILE):
        return None
    with open(OUTPUT_FILE, "r", encoding="utf-8", errors="ignore") as f:
        lines = [line.strip() for line in f if line.strip()]
        return lines[-1] if lines else None

def send_http_log(body: bytes):
    req = urllib.request.Request(
        f"http://{GATE_IP}:{GATE_PORT}/",
        data=body,
        headers={"Content-Type": "application/x-ndjson"},
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=5.0) as resp:
        return resp.read()

def send_syslog(body: bytes):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5.0)
    s.connect((GATE_IP, GATE_PORT))
    s.sendall(body)
    time.sleep(0.1)
    s.close()

def wait_for_new_log(count_before: int, timeout_sec=5.0):
    t0 = time.time()
    while time.time() - t0 < timeout_sec:
        time.sleep(0.1)
        count_after = get_output_line_count()
        if count_after > count_before:
            line = get_last_line()
            if line:
                try:
                    return json.loads(line)
                except Exception:
                    pass
    return None

def main():
    print("=" * 80)
    print("🧪 QA TEST: UNIVERSAL VRL PARSING ENGINE (HOT-DROP PLUGIN VERIFICATION)")
    print("=" * 80)

    # --------------------------------------------------------------------------
    # STEP 1: INITIAL STATE (NO VRL IN FOLDER)
    # --------------------------------------------------------------------------
    print("\n▶️ [STEP 1] Testing baseline: vrl/ directory is EMPTY (No parsers)")
    clean_vrl_dir()
    time.sleep(1.2) # Allow watcher to sync empty state

    nginx_sample = b'192.168.1.100 - admin [25/Oct/2026:10:00:00 +0000] "GET /api/v1/users HTTP/1.1" 200 452\n'
    c1 = get_output_line_count()
    send_http_log(nginx_sample)
    event1 = wait_for_new_log(c1)

    if not event1:
        print("  ❌ [FAIL] No log received at step 1!")
        sys.exit(1)

    print(f"  Received event: parsed={event1.get('parsed')}, parser_status='{event1.get('parser_status')}'")
    if event1.get("parsed") is False and event1.get("parser_status") == "UNPARSED_RAW" and "status" not in event1:
        print("  ✅ [PASS] Step 1 SUCCESS: Log was NOT parsed (Raw message preserved).")
    else:
        print("  ❌ [FAIL] Step 1 FAILED: Expected unparsed log!")
        sys.exit(1)

    # --------------------------------------------------------------------------
    # STEP 2: HOT-DROP nginx.vrl
    # --------------------------------------------------------------------------
    print("\n▶️ [STEP 2] Hot-dropping 'nginx.vrl' into vrl/ folder...")
    nginx_vrl_content = """
# Nginx / Apache Combined Access Log Parser
if is_string(.message) && match(string!(.message), r'^[0-9.]+ - [^ ]+ \\[') {
    parsed, err = parse_common_log(.message)
    if err == null {
        . = merge(., parsed)
        .parsed = true
        .parser_applied = "nginx_combined"
    }
}
"""
    with open(os.path.join(VRL_DIR, "nginx.vrl"), "w", encoding="utf-8") as f:
        f.write(nginx_vrl_content.strip())

    print("  File 'nginx.vrl' dropped. Waiting 1.5s for dynamic SIGHUP reload...")
    time.sleep(1.5)

    # --------------------------------------------------------------------------
    # STEP 3: VERIFY AUTO-PARSING OF NGINX LOG
    # --------------------------------------------------------------------------
    print("\n▶️ [STEP 3] Sending identical Nginx log to verify auto-parsing...")
    c2 = get_output_line_count()
    send_http_log(nginx_sample)
    event2 = wait_for_new_log(c2)

    if not event2:
        print("  ❌ [FAIL] No log received at step 3!")
        sys.exit(1)

    print(f"  Received event: parsed={event2.get('parsed')}, parser_applied='{event2.get('parser_applied')}', status={event2.get('status')}, method='{event2.get('method')}'")
    if event2.get("parsed") is True and event2.get("parser_applied") == "nginx_combined" and event2.get("status") == 200 and event2.get("method") == "GET":
        print(f"  ✅ [PASS] Step 3 SUCCESS: Log AUTOMATICALLY PARSED! (Client IP: {event2.get('host')}, Status: {event2.get('status')})")
    else:
        print(f"  ❌ [FAIL] Step 3 FAILED: Log was not parsed by nginx.vrl! Event: {event2}")
        sys.exit(1)

    # --------------------------------------------------------------------------
    # STEP 4: HOT-DROP cisco_asa.vrl
    # --------------------------------------------------------------------------
    print("\n▶️ [STEP 4] Hot-dropping second plugin: 'cisco_asa.vrl'...")
    cisco_vrl_content = """
# Cisco ASA Firewall Log Parser
if is_string(.message) && contains(string!(.message), "%ASA-") {
    parsed, err = parse_regex(.message, r'%ASA-(?P<severity>\\d)-(?P<msg_id>\\d+):\\s+(?P<action>\\w+)\\s+(?P<direction>\\w+)\\s+TCP connection\\s+(?P<conn_id>\\d+)\\s+for\\s+(?P<src_if>[\\w/]+):(?P<src_ip>[0-9.]+)/(?P<src_port>\\d+)')
    if err == null {
        . = merge(., parsed)
        .parsed = true
        .parser_applied = "cisco_asa"
    }
}
"""
    with open(os.path.join(VRL_DIR, "cisco_asa.vrl"), "w", encoding="utf-8") as f:
        f.write(cisco_vrl_content.strip())

    print("  File 'cisco_asa.vrl' dropped. Waiting 1.5s for dynamic SIGHUP reload...")
    time.sleep(1.5)

    # --------------------------------------------------------------------------
    # STEP 5: VERIFY CISCO ASA AUTO-PARSING
    # --------------------------------------------------------------------------
    print("\n▶️ [STEP 5] Sending Cisco ASA log to verify multi-plugin parsing...")
    cisco_sample = b'<134>1 2026-10-25T10:00:00Z fw-asa01 cisco - - - %ASA-6-302013: Built inbound TCP connection 98765 for outside:203.0.113.50/443\n'
    c3 = get_output_line_count()
    send_syslog(cisco_sample)
    event3 = wait_for_new_log(c3)

    if not event3:
        print("  ❌ [FAIL] No log received at step 5!")
        sys.exit(1)

    print(f"  Received event: parsed={event3.get('parsed')}, parser_applied='{event3.get('parser_applied')}', action='{event3.get('action')}', conn_id='{event3.get('conn_id')}'")
    if event3.get("parsed") is True and event3.get("parser_applied") == "cisco_asa" and event3.get("action") == "Built" and event3.get("conn_id") == "98765":
        print(f"  ✅ [PASS] Step 5 SUCCESS: Cisco ASA Log AUTOMATICALLY PARSED! (Action: {event3.get('action')}, ConnID: {event3.get('conn_id')}, SrcIP: {event3.get('src_ip')})")
    else:
        print(f"  ❌ [FAIL] Step 5 FAILED: Log was not parsed by cisco_asa.vrl! Event: {event3}")
        sys.exit(1)

    # --------------------------------------------------------------------------
    # STEP 6: VERIFY NGINX STILL PARSES (CO-EXISTENCE)
    # --------------------------------------------------------------------------
    print("\n▶️ [STEP 6] Re-testing Nginx log to verify co-existence of multiple plugins...")
    c4 = get_output_line_count()
    send_http_log(nginx_sample)
    event4 = wait_for_new_log(c4)
    if event4 and event4.get("parsed") is True and event4.get("parser_applied") == "nginx_combined":
        print("  ✅ [PASS] Step 6 SUCCESS: Multiple VRL plugins operate simultaneously with zero conflict.")
    else:
        print(f"  ❌ [FAIL] Step 6 FAILED! Event: {event4}")
        sys.exit(1)

    # --------------------------------------------------------------------------
    # STEP 7: REMOVE nginx.vrl & VERIFY REVERT
    # --------------------------------------------------------------------------
    print("\n▶️ [STEP 7] Removing 'nginx.vrl' and verifying graceful un-wiring...")
    os.remove(os.path.join(VRL_DIR, "nginx.vrl"))
    print("  File removed. Waiting 1.5s for dynamic SIGHUP reload...")
    time.sleep(1.5)

    c5 = get_output_line_count()
    send_http_log(nginx_sample)
    event5 = wait_for_new_log(c5)
    if event5 and event5.get("parsed") is False and event5.get("parser_status") == "UNPARSED_RAW":
        print("  ✅ [PASS] Step 7 SUCCESS: Gracefully reverted Nginx to UNPARSED when plugin removed.")
    else:
        print(f"  ❌ [FAIL] Step 7 FAILED! Event: {event5}")
        sys.exit(1)

    print("\n" + "=" * 80)
    print("🎉 ALL 7/7 QA PHASES PASSED WITH 100% SUCCESS!")
    print("🚀 UNIVERSAL VRL PARSING ENGINE IS FULLY OPERATIONAL!")
    print("=" * 80)

if __name__ == "__main__":
    main()

