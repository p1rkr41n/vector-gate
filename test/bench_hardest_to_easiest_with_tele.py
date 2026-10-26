#!/usr/bin/env python3
"""
==============================================================================
VECTOR GATE: HIERARCHICAL BENCHMARK & QA AUDIT (HARDEST TO EASIEST)
WITH REAL-TIME TELEGRAM ALERTING ON FAILURE
==============================================================================
Ranks QA test suites from HARDEST to EASIEST according to ISO 25010,
ISO/IEC 29119, DAMA DMBOK, and CNCF Chaos Engineering Principles.

Any failed standard is immediately dispatched to Telegram chat 1272211313
without waiting for manual user intervention.
"""

import os
import sys
import time
import json
import datetime
import subprocess
import urllib.request
import urllib.parse

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SUITES_DIR = os.path.join(ROOT_DIR, "test", "suites")

TELE_TOKEN = "8735945052:AAFvEYN0vkBV5tJKu8xMyWbPOtoCY14x-Qg"
TELE_CHAT_ID = "1272211313"

class Colors:
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    CYAN = "\033[96m"
    MAGENTA = "\033[95m"
    BOLD = "\033[1m"
    RESET = "\033[0m"

# Hierarchy: Rank 1 (Khó nhất) -> Rank 8 (Dễ nhất)
TEST_HIERARCHY = [
    {
        "rank": 1,
        "id": "CHAOS_BEATS_100",
        "name": "Level 1 (Cực Khó): 100 Flaky Beats Nodes Churn & Half-Close ACK Race",
        "file": "chaos_beats_100_flaky_nodes.py",
        "standard": "ISO 8000 / DAMA Uniqueness, ISO 25010 Reliability (Fault Tolerance)",
        "desc": "100 node flaky simulation, silent connection drops, TCP half-close FIN timing race, deduplication idempotency",
        "cmd": [sys.executable, os.path.join(SUITES_DIR, "chaos_beats_100_flaky_nodes.py")]
    },
    {
        "rank": 2,
        "id": "CHAOS_ADVERSARIAL",
        "name": "Level 2 (Rất Khó): Adversarial Chaos, Slowloris Starvation & Malformed Fuzzing",
        "file": "test_chaos_resilience.py",
        "standard": "CNCF Principles of Chaos Engineering, ISO 25010 Fault Tolerance",
        "desc": "Slowloris (50 slow connections), 200 SYN burst storms, corrupt byte mutations, zero-stuck channel validation",
        "cmd": [sys.executable, os.path.join(SUITES_DIR, "test_chaos_resilience.py")]
    },
    {
        "rank": 3,
        "id": "CAPACITY_STRESS_100K",
        "name": "Level 3 (Khó): Extreme Throughput Capacity & Sub-Microsecond Latency SLA",
        "file": "test_stress_100k.py",
        "standard": "ISO 25010 Performance Efficiency (Capacity & Time Behavior)",
        "desc": "100,000 event multi-threaded burst injection, EPS > 1,500,000 target, zero-copy kernel splice latency SLA",
        "cmd": [sys.executable, os.path.join(SUITES_DIR, "test_stress_100k.py")]
    },
    {
        "rank": 4,
        "id": "BENCH_SPLICE_HOP_A",
        "name": "Level 3b (Khó): Zero-Copy Splice vs Vector Core Micro-Benchmark",
        "file": "bench_gate_vs_vector.py",
        "standard": "ISO 25010 Performance Efficiency (Resource Utilization & Throughput)",
        "desc": "Hop A (Gate Kernel Splice) vs Hop B (Vector Core VRL Disk Sink) performance ratio & nanosecond latency measurement",
        "cmd": [sys.executable, os.path.join(SUITES_DIR, "bench_gate_vs_vector.py")]
    },
    {
        "rank": 5,
        "id": "MULTI_GATE_ISOLATION",
        "name": "Level 4 (Trung Bình Khá): Multi-Gate Ingress, Isolated Fallbacks & Short-Syntax",
        "file": "test_multi_gate.py",
        "standard": "ISO 25010 Modularity & Co-existence, RFC Specification Compliance",
        "desc": "Multi-port concurrent listeners, isolated <gate>.other fallbacks, rejection of deprecated namespace, direct passthrough",
        "cmd": [sys.executable, os.path.join(SUITES_DIR, "test_multi_gate.py")]
    },
    {
        "rank": 6,
        "id": "DEEP_E2E_PERSISTENCE",
        "name": "Level 5 (Trung Bình): Deep E2E Integration, Auto-Wiring & Disk Persistence",
        "file": "test_deep_e2e_verification.py",
        "standard": "ISO/IEC 29119-2 Dynamic Test Process, ISO 25010 Recoverability",
        "desc": "27 acceptance criteria: Zero-port auto-wiring, persistence forward to disk, container memory <= 120MB ceiling",
        "cmd": [sys.executable, os.path.join(SUITES_DIR, "test_deep_e2e_verification.py")]
    },
    {
        "rank": 7,
        "id": "PROTOCOLS_DISAMBIGUATION",
        "name": "Level 6 (Trung Bình): 12-15 Ingress Push Protocols Disambiguation",
        "file": "validate_all_log_types_e2e.py",
        "standard": "ISO 25010 Interoperability & Transport Portability",
        "desc": "Disambiguation of Lumberjack Beats, Syslog, HTTP, Fluent MsgPack, Splunk HEC, Datadog, Heroku, Firehose on Port 5000",
        "cmd": [sys.executable, os.path.join(SUITES_DIR, "validate_all_log_types_e2e.py")]
    },
    {
        "rank": 8,
        "id": "ONION_VRL_HIERARCHICAL",
        "name": "Level 7 (Nhẹ): Hierarchical Onion VRL Parsing & Dynamic SIGHUP Hot-Drop",
        "file": "test_onion_hierarchical_engine.py",
        "standard": "DAMA DMBOK Validity (Schema Evolution & Dead-Letter Discovery)",
        "desc": "Vendor rules (Fortigate, Cisco ASA, Nginx, CEF), dead-letter schema tagging, 2s debounced SIGHUP reload without restart",
        "cmd": [sys.executable, os.path.join(SUITES_DIR, "test_onion_hierarchical_engine.py")]
    },
    {
        "rank": 9,
        "id": "MATRIX_CORE_NATIVE",
        "name": "Level 8 (Dễ Nhất): Vector Core Native Features Matrix & Bypass Mode",
        "file": "test_standard_vector_matrix.py",
        "standard": "ISO/IEC 29119-4 Equivalence Partitioning & Boundary Testing",
        "desc": "Native Remap, Filter, Route, Reduce, Sample, and pure bypass mode verification",
        "cmd": [sys.executable, os.path.join(SUITES_DIR, "test_standard_vector_matrix.py")]
    }
]

def send_telegram_alert(test_item, stdout, stderr, returncode):
    """Sends an immediate Telegram alert when a test fails."""
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    error_snippet = (stderr.strip() or stdout.strip())[-1500:] # Last 1500 chars

    html_msg = f"""🚨 <b>[QA BENCHMARK ALERT - TEST FAILED]</b> 🚨

<b>Cấp độ:</b> {test_item['name']}
<b>Tiêu chuẩn Quốc tế:</b> <code>{test_item['standard']}</code>
<b>Mô tả bài test:</b> {test_item['desc']}
<b>File thực thi:</b> <code>{test_item['file']}</code>
<b>Mã lỗi (Exit code):</b> <code>{returncode}</code>
<b>Thời gian:</b> {now_str}

<b>Chi tiết lỗi:</b>
<pre>{error_snippet}</pre>

⚠️ <i>Thông báo tự động từ Hệ thống Benchmark Vector Gate.</i>"""

    url = f"https://api.telegram.org/bot{TELE_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELE_CHAT_ID,
        "text": html_msg,
        "parse_mode": "HTML"
    }
    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            res_data = json.loads(resp.read().decode("utf-8"))
            if res_data.get("ok"):
                print(f"  {Colors.YELLOW}📡 [Telegram Sent]{Colors.RESET} Alert sent to chat {TELE_CHAT_ID}")
            else:
                print(f"  {Colors.RED}❌ [Telegram Failed]{Colors.RESET} {res_data}")
    except Exception as e:
        print(f"  {Colors.RED}❌ [Telegram Error]{Colors.RESET} {e}")

def main():
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}🎯 VECTOR GATE HIERARCHICAL QA BENCHMARK (HARDEST -> EASIEST){Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}   Standards: ISO/IEC/IEEE 29119, ISO 25010, DAMA DMBOK, CNCF Chaos{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.RESET}\n")

    results = []
    overall_start = time.perf_counter()

    for item in TEST_HIERARCHY:
        print(f"\n{Colors.BOLD}{Colors.MAGENTA}▶ [{item['rank']}/{len(TEST_HIERARCHY)}] {item['name']}{Colors.RESET}")
        print(f"   📜 Tiêu chuẩn : {Colors.CYAN}{item['standard']}{Colors.RESET}")
        print(f"   🔍 Chi tiết   : {item['desc']}")
        print(f"   📁 File       : suites/{item['file']}")
        print("-" * 80)

        t0 = time.perf_counter()
        proc = subprocess.run(
            item["cmd"],
            cwd=ROOT_DIR,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        duration = time.perf_counter() - t0

        is_passed = (proc.returncode == 0)
        
        if is_passed:
            print(f"  {Colors.GREEN}{Colors.BOLD}✔ PASS{Colors.RESET} in {duration:.2f}s | {item['id']}")
            results.append({
                "item": item,
                "passed": True,
                "duration": duration,
                "details": "All criteria met within specifications"
            })
        else:
            print(f"  {Colors.RED}{Colors.BOLD}✘ FAIL{Colors.RESET} in {duration:.2f}s | {item['id']} (code {proc.returncode})")
            results.append({
                "item": item,
                "passed": False,
                "duration": duration,
                "details": proc.stderr or proc.stdout
            })
            # GỬI QUA TELEGRAM NGAY LẬP TỨC (KHÔNG CHỜ PHẢN HỒI)
            send_telegram_alert(item, proc.stdout, proc.stderr, proc.returncode)

    total_time = time.perf_counter() - overall_start

    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.RESET}")
    print(f"{Colors.BOLD}📊 TỔNG HỢP KẾT QUẢ KIỂM THỬ TỪ KHÓ TỚI DỄ (AUDIT REPORT){Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.RESET}")
    print(f"{'Cấp':<4} | {'Độ Khó / Tên Bài Test':<45} | {'Thời gian':<10} | {'Kết Quả'}")
    print("-" * 80)

    all_passed = True
    for r in results:
        status_str = f"{Colors.GREEN}PASS{Colors.RESET}" if r["passed"] else f"{Colors.RED}FAIL{Colors.RESET}"
        print(f"#{r['item']['rank']:<3} | {r['item']['id']:<45} | {r['duration']:>7.2f}s  | {status_str}")
        if not r["passed"]:
            all_passed = False

    print("=" * 80)
    passed_cnt = sum(1 for r in results if r["passed"])
    print(f"Kết quả: {passed_cnt}/{len(results)} tiêu chuẩn đạt chuẩn (Tỷ lệ: {passed_cnt/len(results)*100:.1f}%) | Tổng thời gian: {total_time:.2f}s")
    print(f"{'='*80}\n")

    sys.exit(0 if all_passed else 1)

if __name__ == "__main__":
    main()
