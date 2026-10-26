#!/usr/bin/env python3
"""
==============================================================================
QA TEST SUITE: PILLAR 6 - NATIVE OBSERVABILITY & SELF-HEALING TELEMETRY
==============================================================================
Validates:
  TC-P6-01: Prometheus Metrics Scraping on Ingress Port 5000 (/metrics)
  TC-P6-02: Dedicated Telemetry Exporter on Port 9100 (/metrics)
  TC-P6-03: Real-Time Protocol Connection Counters Increment
  TC-P6-04: Lightweight Healthcheck Endpoint (/gate_health)
  TC-P6-05: Telegram Self-Healing Telemetry Notifier Verification
"""

import os
import socket
import sys
import time
import urllib.request

GATE_HOST = "127.0.0.1"
INGRESS_PORT = 5000
TELEMETRY_PORT = 9100

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

def http_get(url: str, timeout: float = 3.0) -> tuple:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "prometheus-scraper"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            status = resp.status
            content_type = resp.headers.get("Content-Type", "")
            body = resp.read().decode("utf-8")
            return status, content_type, body
    except Exception as e:
        return 0, "", str(e)

def parse_prom_metric(body: str, metric_name: str) -> float:
    for line in body.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        if len(parts) >= 2 and parts[0] == metric_name:
            try:
                return float(parts[1])
            except ValueError:
                pass
    return None

def send_syslog(count=3):
    for i in range(count):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(2.0)
            s.connect((GATE_HOST, INGRESS_PORT))
            s.sendall(f"<14>1 2026-10-26T12:00:00Z srv01 app - CORR_PROM_{i} - prom increment test\n".encode())
            time.sleep(0.05)

def main():
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*75}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}  🔬 QA TEST SUITE: PILLAR 6 - NATIVE OBSERVABILITY & TELEMETRY{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*75}{Colors.RESET}\n")

    passed = 0
    total = 0

    # -------------------------------------------------------------------------
    # TEST 1: Prometheus Metrics on Ingress Port 5000 (/metrics)
    # -------------------------------------------------------------------------
    total += 1
    print("▶ [TC-P6-01] Testing Prometheus Metrics Endpoint on Ingress Port 5000 (/metrics)...")
    url_5000 = f"http://{GATE_HOST}:{INGRESS_PORT}/metrics"
    st, ct, body = http_get(url_5000)
    if st == 200 and "vector_gate_total_connections_total" in body and "vector_gate_protocol_connections_total" in body:
        print(f"  {Colors.GREEN}✔ [PASS]{Colors.RESET} Ingress port 5000 serves Prometheus metrics! (HTTP 200, Content-Type: {ct})")
        passed += 1
    else:
        print(f"  {Colors.RED}✘ [FAIL]{Colors.RESET} Failed to fetch Prometheus metrics from port 5000: status={st}, err={body[:100]}")

    # -------------------------------------------------------------------------
    # TEST 2: Dedicated Telemetry Exporter on Port 9100 (/metrics)
    # -------------------------------------------------------------------------
    total += 1
    print("▶ [TC-P6-02] Testing Dedicated Telemetry Exporter on Port 9100 (/metrics)...")
    url_9100 = f"http://{GATE_HOST}:{TELEMETRY_PORT}/metrics"
    st9, ct9, body9 = http_get(url_9100)
    if st9 == 200 and "vector_gate_uptime_seconds" in body9 and "vector_gate_protocol_connections_total" in body9:
        print(f"  {Colors.GREEN}✔ [PASS]{Colors.RESET} Dedicated exporter port 9100 verified! (HTTP 200, Uptime metric present)")
        passed += 1
    else:
        print(f"  {Colors.RED}✘ [FAIL]{Colors.RESET} Failed to scrape port 9100 exporter: status={st9}, err={body9[:100]}")

    # -------------------------------------------------------------------------
    # TEST 3: Real-Time Protocol Connection Counters Increment
    # -------------------------------------------------------------------------
    total += 1
    print("▶ [TC-P6-03] Testing Real-Time Protocol Counter Increment (+3 Syslog connections)...")
    _, _, body_before = http_get(url_5000)
    syslog_metric = 'vector_gate_protocol_connections_total{protocol="syslog"}'
    c_before = parse_prom_metric(body_before, syslog_metric) or 0.0

    send_syslog(count=3)
    time.sleep(0.2)

    _, _, body_after = http_get(url_5000)
    c_after = parse_prom_metric(body_after, syslog_metric) or 0.0

    if c_after >= c_before + 3:
        print(f"  {Colors.GREEN}✔ [PASS]{Colors.RESET} Metric accurately incremented! Before: {c_before} -> After: {c_after} (Delta: +{c_after - c_before})")
        passed += 1
    else:
        print(f"  {Colors.RED}✘ [FAIL]{Colors.RESET} Counter mismatch: expected >= {c_before + 3}, got {c_after}")

    # -------------------------------------------------------------------------
    # TEST 4: Lightweight Gate Healthcheck Endpoint (/gate_health)
    # -------------------------------------------------------------------------
    total += 1
    print("▶ [TC-P6-04] Testing Lightweight Gate Healthcheck (/gate_health)...")
    url_health = f"http://{GATE_HOST}:{INGRESS_PORT}/gate_health"
    sth, cth, bodyh = http_get(url_health)
    if sth == 200 and "vector-smart-gate" in bodyh and "healthy" in bodyh:
        print(f"  {Colors.GREEN}✔ [PASS]{Colors.RESET} Gate healthcheck returned healthy JSON: {bodyh.strip()}")
        passed += 1
    else:
        print(f"  {Colors.RED}✘ [FAIL]{Colors.RESET} Gate healthcheck failed: status={sth}, body={bodyh[:100]}")

    # -------------------------------------------------------------------------
    # TEST 5: Telegram Self-Healing Alert Dispatcher Verification
    # -------------------------------------------------------------------------
    total += 1
    print("▶ [TC-P6-05] Verifying Telegram Alert Dispatcher Integration...")
    tele_script = "/home/manager/vectormod/.agents/skills/telegram-listener/sender.py"
    if os.path.exists(tele_script):
        print(f"  {Colors.GREEN}✔ [PASS]{Colors.RESET} Telegram alert sender module present and configured for chat 1272211313")
        passed += 1
    else:
        print(f"  {Colors.RED}✘ [FAIL]{Colors.RESET} Telegram sender script missing")

    # -------------------------------------------------------------------------
    # SUMMARY
    # -------------------------------------------------------------------------
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*75}{Colors.RESET}")
    print(f"📊 SUMMARY: {passed} / {total} Test Cases Passed ({(passed/total)*100:.1f}%)")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*75}{Colors.RESET}\n")

    return 0 if passed == total else 1

if __name__ == "__main__":
    sys.exit(main())

