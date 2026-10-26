#!/usr/bin/env python3
"""
Comprehensive QA Matrix: Testing Standard Vector Core Features & Comparing with Vector Gate Wrapper
Tests 8 standard Vector features directly on upstream Vector and through Vector Gate wrapper.
Collects exact behaviors, discrepancies, and impacts on default logic.
"""

import json
import os
import shutil
import socket
import subprocess
import sys
import tempfile
import time

VECTOR_BIN = "/usr/local/bin/vector"
SUITE_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_ROOT = os.path.dirname(SUITE_DIR)
GATE_BIN = os.path.join(TEST_ROOT, "bin", "vector-gate")
if not os.path.exists(GATE_BIN):
    GATE_BIN = os.path.join(TEST_ROOT, "..", "vector-gate", "target", "release", "vector-gate")
WORKDIR = "/tmp/test_vector_matrix"

def setup():
    if os.path.exists(WORKDIR):
        shutil.rmtree(WORKDIR)
    os.makedirs(WORKDIR, exist_ok=True)

def get_free_port():
    s = socket.socket()
    s.bind(('127.0.0.1', 0))
    p = s.getsockname()[1]
    s.close()
    return p

def send_tcp(port, msg):
    s = socket.socket()
    s.connect(('127.0.0.1', port))
    if isinstance(msg, str):
        msg = (msg + "\n").encode()
    s.sendall(msg)
    s.close()

def run_test_case(name, config_yaml, send_fn, verify_fn, use_gate=False, timeout=4):
    out_file = os.path.join(WORKDIR, f"{name}_out.ndjson")
    cfg_file = os.path.join(WORKDIR, f"{name}.yaml")
    config_yaml = config_yaml.replace("{{OUT_FILE}}", out_file)
    with open(cfg_file, "w") as f:
        f.write(config_yaml)

    binary = GATE_BIN if use_gate else VECTOR_BIN
    cmd = [binary, "run", "-c", cfg_file] if use_gate else [binary, "--config", cfg_file]

    # Validate first
    val_cmd = [binary, "validate", "-c", cfg_file] if use_gate else [binary, "validate", "--no-environment", cfg_file]
    val_res = subprocess.run(val_cmd, capture_output=True, text=True)
    if val_res.returncode != 0:
        return {
            "name": name,
            "engine": "Gate" if use_gate else "Native Vector",
            "validation": False,
            "val_err": (val_res.stderr or val_res.stdout).strip(),
            "passed": False,
            "reason": "Validation failed"
        }

    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    time.sleep(1.2) # Allow bind

    try:
        if proc.poll() is not None:
            stdout, stderr = proc.communicate()
            return {
                "name": name,
                "engine": "Gate" if use_gate else "Native Vector",
                "validation": True,
                "passed": False,
                "reason": f"Process exited early with code {proc.returncode}: {stderr[:300]}"
            }

        send_fn()

        deadline = time.time() + timeout
        matched = False
        captured = []
        while time.time() < deadline:
            if os.path.exists(out_file):
                with open(out_file, "r") as f:
                    captured = [l.strip() for l in f if l.strip()]
                if verify_fn(captured):
                    matched = True
                    break
            time.sleep(0.2)

        return {
            "name": name,
            "engine": "Gate" if use_gate else "Native Vector",
            "validation": True,
            "passed": matched,
            "events_captured": len(captured),
            "reason": "OK" if matched else f"Output mismatch: {captured[:2]}"
        }
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=2)
        except Exception:
            proc.kill()

def main():
    setup()
    tests = []

    # 1. Standard VRL Remap (Arithmetic, String, Object mutations)
    port1 = get_free_port()
    cfg1 = f"""
data_dir: "{WORKDIR}/d1"
sources:
  in_raw:
    type: socket
    mode: tcp
    address: "127.0.0.1:{port1}"
transforms:
  vrl_step:
    type: remap
    inputs: ["in_raw"]
    source: |
      . = parse_json!(string!(.message))
      .val_doubled = to_int!(.val) * 2
      .user_upper = upcase(to_string!(.user))
      del(.secret)
sinks:
  out:
    type: file
    inputs: ["vrl_step"]
    path: "{{{{OUT_FILE}}}}"
    encoding:
      codec: json
"""
    tests.append(("STD-01: Native VRL Remap", cfg1, lambda: send_tcp(port1, '{"user": "alice", "val": 25, "secret": "shh"}'), 
                  lambda lines: len(lines) > 0 and json.loads(lines[-1]).get("val_doubled") == 50 and "secret" not in json.loads(lines[-1]), False))

    # 2. Standard Filter Transform (Conditional dropping)
    port2 = get_free_port()
    cfg2 = f"""
data_dir: "{WORKDIR}/d2"
sources:
  in_raw:
    type: socket
    mode: tcp
    address: "127.0.0.1:{port2}"
transforms:
  parse_json:
    type: remap
    inputs: ["in_raw"]
    source: |
      . = parse_json!(string!(.message))
  filter_errors:
    type: filter
    inputs: ["parse_json"]
    condition: "(to_int(.status) ?? 0) >= 400"
sinks:
  out:
    type: file
    inputs: ["filter_errors"]
    path: "{{{{OUT_FILE}}}}"
    encoding:
      codec: json
"""
    def send2():
        send_tcp(port2, '{"status": 200, "msg": "ok"}')
        time.sleep(0.1)
        send_tcp(port2, '{"status": 500, "msg": "server error"}')
        time.sleep(0.1)
        send_tcp(port2, '{"status": 404, "msg": "not found"}')

    tests.append(("STD-02: Native Filter (Condition Dropping)", cfg2, send2,
                  lambda lines: len(lines) == 2 and {json.loads(l)["status"] for l in lines} == {500, 404}, False))

    # 3. Standard Route Transform (Multi-Branch Split)
    port3 = get_free_port()
    cfg3 = f"""
data_dir: "{WORKDIR}/d3"
sources:
  in_raw:
    type: socket
    mode: tcp
    address: "127.0.0.1:{port3}"
transforms:
  parse_json:
    type: remap
    inputs: ["in_raw"]
    source: |
      . = parse_json!(string!(.message))
  route_events:
    type: route
    inputs: ["parse_json"]
    route:
      critical: '.severity == "critical"'
      info: '.severity == "info"'
  tag_crit:
    type: remap
    inputs: ["route_events.critical"]
    source: |
      .branch = "CRIT"
  tag_info:
    type: remap
    inputs: ["route_events.info"]
    source: |
      .branch = "INFO"
sinks:
  out:
    type: file
    inputs: ["tag_crit", "tag_info"]
    path: "{{{{OUT_FILE}}}}"
    encoding:
      codec: json
"""
    def send3():
        send_tcp(port3, '{"severity": "critical", "id": 1}')
        time.sleep(0.1)
        send_tcp(port3, '{"severity": "info", "id": 2}')

    tests.append(("STD-03: Native Route (Multi-Branch Routing)", cfg3, send3,
                  lambda lines: len(lines) == 2 and {json.loads(l)["branch"] for l in lines} == {"CRIT", "INFO"}, False))

    # 4. Standard Aggregate Transform (Event batching)
    port4 = get_free_port()
    cfg4 = f"""
data_dir: "{WORKDIR}/d4"
sources:
  in_raw:
    type: socket
    mode: tcp
    address: "127.0.0.1:{port4}"
transforms:
  parse_json:
    type: remap
    inputs: ["in_raw"]
    source: |
      . = parse_json!(string!(.message))
  red:
    type: reduce
    inputs: ["parse_json"]
    group_by: ["group"]
    expire_after_ms: 300
sinks:
  out:
    type: file
    inputs: ["red"]
    path: "{{{{OUT_FILE}}}}"
    encoding:
      codec: json
"""
    def send4():
        send_tcp(port4, '{"group": "g1", "val": 1}')
        send_tcp(port4, '{"group": "g1", "val": 2}')
        time.sleep(0.8)

    tests.append(("STD-04: Native Reduce (Log Aggregation)", cfg4, send4,
                  lambda lines: len(lines) >= 1, False, 5))

    # 5. Standard Sample Transform (Deterministic Sampling)
    port5 = get_free_port()
    cfg5 = f"""
data_dir: "{WORKDIR}/d5"
sources:
  in_raw:
    type: socket
    mode: tcp
    address: "127.0.0.1:{port5}"
transforms:
  parse_json:
    type: remap
    inputs: ["in_raw"]
    source: |
      . = parse_json!(string!(.message))
  sample_1_in_2:
    type: sample
    inputs: ["parse_json"]
    rate: 2
sinks:
  out:
    type: file
    inputs: ["sample_1_in_2"]
    path: "{{{{OUT_FILE}}}}"
    encoding:
      codec: json
"""
    def send5():
        for i in range(10):
            send_tcp(port5, f'{{"i": {i}}}')
            time.sleep(0.05)

    tests.append(("STD-05: Native Sample (Rate Limiting / Drop)", cfg5, send5,
                  lambda lines: 1 <= len(lines) <= 9, False))

    # 6. Now test the SAME features through Vector Gate wrapper
    # Gate with pure vector config (no gates: block)
    tests.append(("GATE-01: Pure Vector via Gate Wrapper (Remap)", cfg1, lambda: send_tcp(port1, '{"user": "alice", "val": 25, "secret": "shh"}'),
                  lambda lines: len(lines) > 0 and json.loads(lines[-1]).get("val_doubled") == 50, True))

    # Gate with gates.enabled: true + standard transforms
    port_gate = get_free_port()
    cfg_gate_active = f"""
data_dir: "{WORKDIR}/dg"
gates:
  main_gate:
    address: "127.0.0.1:{port_gate}"
    routes:
      other:
        type: "socket"
sources:
  other_unmatched:
    type: socket
    mode: tcp
    address: "main_gate.other"
transforms:
  std_remap:
    type: remap
    inputs: ["other_unmatched"]
    source: |
      . = parse_json!(string!(.message))
      .gate_passed = true
      .val_calc = to_int!(.val) * 10
sinks:
  out:
    type: file
    inputs: ["std_remap"]
    path: "{{{{OUT_FILE}}}}"
    encoding:
      codec: json
"""
    tests.append(("GATE-02: Active Gate + Standard Remap", cfg_gate_active, lambda: send_tcp(port_gate, '{"val": 5}'),
                  lambda lines: len(lines) > 0 and json.loads(lines[-1]).get("val_calc") == 50 and json.loads(lines[-1]).get("gate_passed") is True, True))

    # Gate with gates.enabled: false (Bypass mode)
    port_bypass = get_free_port()
    cfg_gate_disabled = f"""
data_dir: "{WORKDIR}/db"
gates:
  main_gate:
    enabled: false
sources:
  in_raw:
    type: socket
    mode: tcp
    address: "127.0.0.1:{port_bypass}"
transforms:
  std_remap:
    type: remap
    inputs: ["in_raw"]
    source: |
      .bypassed = true
sinks:
  out:
    type: file
    inputs: ["std_remap"]
    path: "{{{{OUT_FILE}}}}"
    encoding:
      codec: json
"""
    tests.append(("GATE-03: Gate Disabled (gates.enabled: false)", cfg_gate_disabled, lambda: send_tcp(port_bypass, 'hello'),
                  lambda lines: len(lines) > 0 and json.loads(lines[-1]).get("bypassed") is True, True))

    print(f"{'#':<3} | {'Test Name':<45} | {'Engine':<14} | {'Val':<5} | {'Status':<6} | {'Details'}")
    print("-" * 100)

    summary = []
    for idx, item in enumerate(tests, 1):
        tname, tcfg, tsend, tverify, tgate = item[0], item[1], item[2], item[3], item[4]
        tout = item[5] if len(item) > 5 else 4
        res = run_test_case(f"tc_{idx}", tcfg, tsend, tverify, use_gate=tgate, timeout=tout)
        status_str = "PASS" if res.get("passed") else "FAIL"
        val_str = "OK" if res.get("validation") else "ERR"
        engine_str = "Vector-Gate" if tgate else "Upstream-Vec"
        details = res.get("reason", "")
        if not res.get("validation"):
            details = res.get("val_err", "")[:40]
        print(f"{idx:<3} | {tname:<45} | {engine_str:<14} | {val_str:<5} | {status_str:<6} | {details}")
        summary.append(res)

    print("=" * 100)
    passed_cnt = sum(1 for r in summary if r.get("passed"))
    print(f"Total: {passed_cnt}/{len(summary)} passed.")

if __name__ == "__main__":
    main()
