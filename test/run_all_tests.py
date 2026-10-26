#!/usr/bin/env python3
"""
Vector Smart Gate: Unified Test Runner
Executes automated QA verification suites and reports aggregated pass/fail metrics.
"""

import argparse
import os
import subprocess
import sys
import time

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))

SUITES = {
    "matrix": {
        "file": "test_standard_vector_matrix.py",
        "desc": "Standard Vector Core Native Features & VRL Matrix",
        "requires_gate": False
    },
    "onion": {
        "file": "test_onion_hierarchical_engine.py",
        "desc": "Hierarchical Onion VRL & Fallback Verification",
        "requires_gate": False
    },
    "protocols": {
        "file": "validate_all_log_types_e2e.py",
        "desc": "12-15 Ingress Push Protocols Disambiguation E2E",
        "requires_gate": True
    },
    "chaos": {
        "file": "test_chaos_resilience.py",
        "desc": "Adversarial Chaos & Stress Resilience (Slowloris, Storms, Fuzzing)",
        "requires_gate": True
    },
    "beats_rsk": {
        "file": "test_beats_and_rsk_hardening.py",
        "desc": "Beats Sliding Window, Flaky Drop Churn & P0-P2 Risk Remediation",
        "requires_gate": True
    },
    "chaos_beats_100": {
        "file": "chaos_beats_100_flaky_nodes.py",
        "desc": "100-Node Beats Chaos Simulation (Silent Drops, Resend Churn, Dedupe)",
        "requires_gate": True
    },
    "deep_e2e": {
        "file": "test_deep_e2e_verification.py",
        "desc": "Deep End-to-End Declarative Routing & Zero-Port Auto-Wiring",
        "requires_gate": True
    },
    "multigate": {
        "file": "test_multi_gate.py",
        "desc": "Multi-Gate Ingress, Isolated Fallback Terminals & Short Syntax",
        "requires_gate": True
    },
    "transparent_ip": {
        "file": "test_transparent_ip.py",
        "desc": "Transparent IP Kernel TPROXY & Dual-Stack IP Preservation",
        "requires_gate": True
    },
    "pillar1": {
        "file": "test_pillar1_multi_protocol.py",
        "desc": "Pillar 1 - Universal Multi-Protocol Transport Ingress & RFC 6587",
        "requires_gate": True
    },
    "pillar2": {
        "file": "test_pillar2_kernel_elastic.py",
        "desc": "Pillar 2 - Elastic Kernel-Tuned Performance Engine & Bidirectional Splice",
        "requires_gate": True
    },
    "pillar4": {
        "file": "test_pillar4_onion_vrl.py",
        "desc": "Pillar 4 - Universal Onion VRL & Schema Auto-Discovery",
        "requires_gate": True
    },
    "pillar5": {
        "file": "test_pillar5_elastic_buffer.py",
        "desc": "Pillar 5 - Elastic Buffering & Universal Deduplication",
        "requires_gate": True
    },
    "pillar6": {
        "file": "test_pillar6_observability.py",
        "desc": "Pillar 6 - Native Observability & Self-Healing Telemetry",
        "requires_gate": True
    }
}

def run_suite(name: str, info: dict) -> bool:
    suites_dir = os.path.join(TESTS_DIR, "suites")
    fpath = os.path.join(suites_dir, info["file"])
    print("\n" + "=" * 70)
    print(f"🧪 RUNNING SUITE: [{name.upper()}] - {info['desc']}")
    print(f"📁 Target script: suites/{info['file']}")
    print("=" * 70)

    start = time.time()
    res = subprocess.run([sys.executable, fpath], cwd=suites_dir)
    dur = time.time() - start

    if res.returncode == 0:
        print(f"\n✅ SUITE [{name.upper()}] PASSED in {dur:.2f}s")
        return True
    else:
        print(f"\n❌ SUITE [{name.upper()}] FAILED (exit code: {res.returncode}) in {dur:.2f}s")
        return False

def main():
    parser = argparse.ArgumentParser(description="Vector Smart Gate Test Runner")
    parser.add_argument("--all", action="store_true", help="Run all available test suites")
    parser.add_argument("--suite", choices=list(SUITES.keys()), help="Run a specific test suite")
    parser.add_argument("--list", action="store_true", help="List all available test suites")
    args = parser.parse_args()

    if args.list:
        print("\n📋 Available Test Suites in tests/:")
        for k, v in SUITES.items():
            gate_req = "Requires live Gate" if v["requires_gate"] else "Self-contained"
            print(f"  • {k:<12}: {v['desc']:<55} ({gate_req})")
        return

    suites_to_run = []
    if args.suite:
        suites_to_run.append(args.suite)
    elif args.all:
        suites_to_run = list(SUITES.keys())
    else:
        # Default run self-contained offline suites
        suites_to_run = ["matrix", "onion"]

    print("==================================================================")
    print("🚀 VECTOR SMART GATE: UNIFIED QA TEST RUNNER")
    print(f"🎯 Selected suites: {', '.join(suites_to_run)}")
    print("==================================================================")

    results = {}
    for sname in suites_to_run:
        results[sname] = run_suite(sname, SUITES[sname])

    print("\n" + "=" * 70)
    print("📊 AGGREGATED TEST EXECUTION SUMMARY")
    print("=" * 70)
    all_passed = True
    for sname, success in results.items():
        status = "✅ PASSED" if success else "❌ FAILED"
        if not success:
            all_passed = False
        print(f"  • {sname:<15}: {status}")

    print("=" * 70)
    if all_passed:
        print("🎉 ALL TEST SUITES PASSED (100.0% SUCCESS RATE)")
        sys.exit(0)
    else:
        print("⚠️ SOME TEST SUITES FAILED")
        sys.exit(1)

if __name__ == "__main__":
    main()
