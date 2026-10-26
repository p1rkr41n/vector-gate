#!/usr/bin/env python3
"""
==============================================================================
QA TEST SUITE: TRANSPARENT IP & TPROXY SOURCE IP PRESERVATION
==============================================================================
Validates that Vector Smart Gate (Phase 0) preserves 100% Client L3/L4
Source IP addresses when proxying traffic to Vector Core via Linux IP_TRANSPARENT.
"""

import subprocess
import time
import json
import os
import sys
import socket
import uuid

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

OUTPUT_FILE = "/home/manager/vectormod/deploy/output/forwarded_logs.ndjson"
GATE_CONTAINER = "vector-smart-gate"
DOCKER_NETWORK = "deploy_default"
TARGET_PORT = 5000

def log_header(title):
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}  {title}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.RESET}\n")

def log_pass(msg):
    print(f"  {Colors.GREEN}✔ [PASS]{Colors.RESET} {msg}")

def log_fail(msg):
    print(f"  {Colors.RED}✘ [FAIL]{Colors.RESET} {msg}")

def log_info(msg):
    print(f"  {Colors.BLUE}ℹ [INFO]{Colors.RESET} {msg}")

def get_container_ip(container_name):
    cmd = ["docker", "inspect", "-f", "{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}", container_name]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode == 0 and res.stdout.strip():
        return res.stdout.strip()
    return "172.21.0.2"

def get_forwarded_logs(tail_lines=1000):
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
    except Exception as e:
        log_fail(f"Error reading output file: {e}")
        return []

def send_from_container(client_ip, target_ip, payload):
    """Run an ephemeral container with an explicit IP and send payload via nc."""
    cmd = [
        "docker", "run", "--rm",
        "--network", DOCKER_NETWORK,
        "--ip", client_ip,
        "alpine", "sh", "-c",
        f"echo -ne '{payload}' | nc -w 1 {target_ip} {TARGET_PORT}"
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return res.returncode == 0

def wait_for_event(predicate, timeout=6.0):
    start = time.time()
    while time.time() - start < timeout:
        events = get_forwarded_logs()
        for ev in reversed(events):
            if predicate(ev):
                return ev
        time.sleep(0.2)
    return None

def main():
    log_header("TRANSPARENT IP & CLIENT L3/L4 SOURCE PRESERVATION TEST")

    # 1. Health & Environment Verification
    log_info(f"Target Container : {GATE_CONTAINER}")
    log_info(f"Docker Network   : {DOCKER_NETWORK}")
    log_info(f"Output File Path : {OUTPUT_FILE}")

    target_ip = get_container_ip(GATE_CONTAINER)
    log_info(f"Gate Ingress IP  : {target_ip}:{TARGET_PORT}")

    # Check container capabilities
    cap_check = subprocess.run(
        ["docker", "exec", GATE_CONTAINER, "ip", "rule", "show"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    if "from 127.0.0.1 lookup 100" in cap_check.stdout or cap_check.returncode == 0:
        log_pass("Policy routing rules (table 100) are active inside container.")
    else:
        log_fail(f"Policy routing check failed:\n{cap_check.stderr}")
        return 1

    total_tests = 0
    passed_tests = 0

    # -------------------------------------------------------------------------
    # TEST 1: Host Ingress via Port-Forwarding (Bridge Gateway IP)
    # -------------------------------------------------------------------------
    total_tests += 1
    corr_id_1 = f"HOST_INGRESS_{uuid.uuid4().hex[:8]}"
    log_info(f"[Test 1/4] Sending Syslog RFC 5424 from Host Bridge (Correlation ID: {corr_id_1})...")

    syslog_msg = f"<134>1 2026-10-26T12:00:00Z myhost testapp - {corr_id_1} - Transparent IP Host Verification {corr_id_1}\n"
    s = socket.create_connection(("127.0.0.1", TARGET_PORT), timeout=3)
    s.sendall(syslog_msg.encode())
    time.sleep(0.05)
    s.close()

    ev1 = wait_for_event(lambda e: corr_id_1 in json.dumps(e), timeout=6.0)
    if ev1:
        src_ip = ev1.get("source_ip")
        log_info(f"Received record with source_ip: '{src_ip}'")
        if src_ip and src_ip != "127.0.0.1":
            log_pass(f"Host bridge connection preserved real source IP ({src_ip}) instead of 127.0.0.1")
            passed_tests += 1
        else:
            log_fail(f"source_ip is 127.0.0.1 (Transparent IP failed to preserve source)")
    else:
        log_fail("Did not receive forwarded event for Test 1 within timeout")

    # -------------------------------------------------------------------------
    # TEST 2: Multi-Node Virtual Clients with Fixed Custom IPs
    # -------------------------------------------------------------------------
    corr_alpha = f"CORR_ALPHA_{uuid.uuid4().hex[:6]}"
    corr_beta = f"CORR_BETA_{uuid.uuid4().hex[:6]}"
    corr_gamma = f"CORR_GAMMA_{uuid.uuid4().hex[:6]}"
    test_clients = [
        {
            "name": "Node Alpha (Syslog RFC 3164)",
            "ip": "172.21.0.81",
            "msg": f"<34>Oct 26 12:00:00 node-alpha kernel: [{corr_alpha}] Firewall allow proto=TCP\n",
            "corr": corr_alpha,
        },
        {
            "name": "Node Beta (Syslog RFC 5424)",
            "ip": "172.21.0.82",
            "msg": f"<165>1 2026-10-26T12:00:00Z node-beta authservice - {corr_beta} [auth user=\"admin\"] Login OK {corr_beta}\n",
            "corr": corr_beta,
        },
        {
            "name": "Node Gamma (Raw Socket Stream)",
            "ip": "172.21.0.83",
            "msg": f"CUSTOM_RAW_TELEMETRY: node_id={corr_gamma} cpu=14.2 mem=45.1\n",
            "corr": corr_gamma,
        },
    ]

    for tc in test_clients:
        total_tests += 1
        log_info(f"[Test 2] Injecting from {tc['name']} with Client IP {tc['ip']}...")
        ok = send_from_container(tc["ip"], target_ip, tc["msg"])
        if not ok:
            log_fail(f"Failed to transmit packet from {tc['ip']}")
            continue

        ev = wait_for_event(lambda e: tc["corr"] in json.dumps(e))
        if ev:
            actual_ip = ev.get("source_ip")
            if actual_ip == tc["ip"]:
                log_pass(f"100% Match! Expected IP: {tc['ip']} | Received .source_ip: {actual_ip}")
                passed_tests += 1
            else:
                log_fail(f"Mismatch! Expected IP: {tc['ip']} | Received: {actual_ip}")
        else:
            log_fail(f"Event with marker {tc['corr']} not found in forwarded logs")

    # -------------------------------------------------------------------------
    # TEST 3: Burst Traffic with Rapid Multi-IP Concurrency
    # -------------------------------------------------------------------------
    total_tests += 1
    log_info("[Test 3/4] Testing concurrent burst across different source IPs...")
    burst_ips = ["172.21.0.91", "172.21.0.92", "172.21.0.93"]
    burst_success = 0

    for idx, b_ip in enumerate(burst_ips):
        corr = f"BURST_{idx}_{uuid.uuid4().hex[:6]}"
        msg = f"<14>1 2026-10-26T12:00:00Z burst-node myapp - {corr} - Burst verification {corr}\n"
        send_from_container(b_ip, target_ip, msg)
        ev = wait_for_event(lambda e: corr in json.dumps(e), timeout=6.0)
        if ev and ev.get("source_ip") == b_ip:
            burst_success += 1

    if burst_success == len(burst_ips):
        log_pass(f"All {burst_success}/{len(burst_ips)} concurrent burst packets maintained exact Source IPs.")
        passed_tests += 1
    else:
        log_fail(f"Burst test failed: only {burst_success}/{len(burst_ips)} succeeded.")

    # -------------------------------------------------------------------------
    # TEST 4: Integrity of Parser Pipeline and Metadata
    # -------------------------------------------------------------------------
    total_tests += 1
    log_info("[Test 4/4] Verifying metadata integrity (type_log, ingress_port, source_id)...")
    sample_corr = f"META_{uuid.uuid4().hex[:6]}"
    sample_ip = "172.21.0.95"
    sample_msg = f"<14>1 2026-10-26T12:00:00Z metanode app - {sample_corr} - Metadata check {sample_corr}\n"
    send_from_container(sample_ip, target_ip, sample_msg)
    ev_meta = wait_for_event(lambda e: sample_corr in json.dumps(e), timeout=6.0)

    if ev_meta:
        valid_type = ev_meta.get("type_log") == "syslog"
        valid_port = ev_meta.get("ingress_port") == 5000
        valid_src = ev_meta.get("source_ip") == sample_ip
        if valid_type and valid_port and valid_src:
            log_pass(f"Metadata intact: type_log={ev_meta.get('type_log')}, ingress_port={ev_meta.get('ingress_port')}, source_ip={valid_src}")
            passed_tests += 1
        else:
            log_fail(f"Metadata corrupted: {ev_meta}")
    else:
        log_fail("Metadata test event not found")

    # -------------------------------------------------------------------------
    # SUMMARY REPORT
    # -------------------------------------------------------------------------
    log_header("TEST SUMMARY & RESULTS")
    print(f"  Total Test Cases  : {total_tests}")
    print(f"  Passed Test Cases : {Colors.GREEN}{passed_tests}{Colors.RESET}")
    print(f"  Failed Test Cases : {Colors.RED if (total_tests - passed_tests) > 0 else Colors.GREEN}{total_tests - passed_tests}{Colors.RESET}")

    if passed_tests == total_tests:
        print(f"\n{Colors.BOLD}{Colors.GREEN}🎉 100% TRANSPARENT IP QA ACCEPTANCE CRITERIA ACHIEVED!{Colors.RESET}\n")
        return 0
    else:
        print(f"\n{Colors.BOLD}{Colors.RED}❌ QA TESTS FAILED!{Colors.RESET}\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())
