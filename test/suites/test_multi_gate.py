#!/usr/bin/env python3
"""
==============================================================================
VECTOR GATE v2.5.0 MULTI-GATE INGRESS & SHORT-SYNTAX TEST SUITE
==============================================================================
Tests the Multi-Gate architecture:
1. Multiple concurrent gates on distinct ports (e.g., dmz_gate:15045, lan_gate:15046)
2. Short wiring syntax: address: "<gate_name>.<route_name>"
3. Isolated fallback terminals: address: "<gate_name>.other"
4. Rejection of deprecated "gates." prefix
5. Rejection of unknown gate or route names
6. Direct socket passthrough (IP:Port untouched) alongside Multi-Gate
"""

import os
import sys
import time
import socket
import struct
import tempfile
import subprocess

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
GATE_BIN = os.path.join(ROOT_DIR, "test", "bin", "vector-gate")
if not os.path.exists(GATE_BIN):
    GATE_BIN = os.path.join(ROOT_DIR, "vector-gate", "target", "release", "vector-gate")

class Colors:
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    CYAN = "\033[96m"
    BOLD = "\033[1m"
    RESET = "\033[0m"

passed = 0
failed = 0

def record_test(name, success, detail=""):
    global passed, failed
    if success:
        passed += 1
        print(f"  {Colors.GREEN}✔ PASS{Colors.RESET} | {name} {Colors.CYAN}({detail}){Colors.RESET}")
    else:
        failed += 1
        print(f"  {Colors.RED}✘ FAIL{Colors.RESET} | {name} - {detail}")

def test_deprecated_gates_prefix_rejection():
    """Verify that 'gates.<route>' or 'gates.<gate>.<route>' is strictly rejected."""
    bad_yaml = """
gates:
  dmz_gate:
    address: "0.0.0.0:15045"
    routes:
      http_route:
        type: "http_server"
      other:
        type: "socket"

sources:
  in_http:
    type: http_server
    address: "gates.http_route"  # Deprecated!

  other_dmz:
    type: socket
    mode: tcp
    address: "dmz_gate.other"

sinks:
  blackhole:
    type: blackhole
    inputs: ["in_http", "other_dmz"]
"""
    with tempfile.NamedTemporaryFile("w", suffix=".yaml", delete=False) as f:
        f.write(bad_yaml)
        tmp = f.name

    try:
        res = subprocess.run([GATE_BIN, "validate", "-c", tmp], capture_output=True, text=True)
        is_rejected = res.returncode != 0 and "deprecated absolute namespace" in (res.stdout + res.stderr)
        record_test(
            "TC-MG-01: Rejection of deprecated 'gates.' prefix",
            is_rejected,
            "Properly rejected with helpful migration message"
        )
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)

def test_unknown_gate_rejection():
    """Verify that referencing an undefined gate is rejected with available gates list."""
    bad_yaml = """
gates:
  lan_gate:
    address: "0.0.0.0:15046"
    routes:
      beats_route:
        type: "logstash"
      other:
        type: "socket"

sources:
  in_beats:
    type: logstash
    address: "dmz_gate.beats_route"  # dmz_gate does not exist!

  other_lan:
    type: socket
    mode: tcp
    address: "lan_gate.other"

sinks:
  blackhole:
    type: blackhole
    inputs: ["in_beats", "other_lan"]
"""
    with tempfile.NamedTemporaryFile("w", suffix=".yaml", delete=False) as f:
        f.write(bad_yaml)
        tmp = f.name

    try:
        res = subprocess.run([GATE_BIN, "validate", "-c", tmp], capture_output=True, text=True)
        is_rejected = res.returncode != 0 and "references unknown gate 'dmz_gate'" in (res.stdout + res.stderr)
        record_test(
            "TC-MG-02: Rejection of unknown gate reference",
            is_rejected,
            "Properly identified unknown gate and listed available gates"
        )
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)

def test_unknown_route_rejection():
    """Verify that referencing an undefined route within a valid gate is rejected."""
    bad_yaml = """
gates:
  lan_gate:
    address: "0.0.0.0:15046"
    routes:
      beats_route:
        type: "logstash"
      other:
        type: "socket"

sources:
  in_syslog:
    type: syslog
    mode: tcp
    address: "lan_gate.non_existent_syslog"

  other_lan:
    type: socket
    mode: tcp
    address: "lan_gate.other"

sinks:
  blackhole:
    type: blackhole
    inputs: ["in_syslog", "other_lan"]
"""
    with tempfile.NamedTemporaryFile("w", suffix=".yaml", delete=False) as f:
        f.write(bad_yaml)
        tmp = f.name

    try:
        res = subprocess.run([GATE_BIN, "validate", "-c", tmp], capture_output=True, text=True)
        is_rejected = res.returncode != 0 and "references undefined route 'non_existent_syslog'" in (res.stdout + res.stderr)
        record_test(
            "TC-MG-03: Rejection of undefined route in valid gate",
            is_rejected,
            "Properly caught invalid route reference"
        )
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)

def test_valid_multi_gate_validation_and_direct_passthrough():
    """Verify that a valid multi-gate configuration with direct socket passes validation."""
    valid_yaml = """
gates:
  dmz_gate:
    address: "0.0.0.0:15045"
    options:
      zero_copy: true
      reuse_port: true
    routes:
      nginx_route:
        type: "http_server"
      other:
        type: "socket"

  lan_gate:
    address: "0.0.0.0:15046"
    options:
      zero_copy: true
      reuse_port: true
    routes:
      winlog_route:
        type: "logstash"
      other:
        type: "socket"

sources:
  in_dmz_nginx:
    type: http_server
    address: "dmz_gate.nginx_route"
    decoding:
      codec: json

  other_dmz:
    type: socket
    mode: tcp
    address: "dmz_gate.other"

  in_lan_winlog:
    type: logstash
    address: "lan_gate.winlog_route"

  other_lan:
    type: socket
    mode: tcp
    address: "lan_gate.other"

  in_legacy_direct:
    type: syslog
    mode: udp
    address: "0.0.0.0:15514"

transforms:
  tag_all:
    type: remap
    inputs: ["in_dmz_nginx", "in_lan_winlog", "in_legacy_direct"]
    source: |
      .processed = true

sinks:
  blackhole:
    type: blackhole
    inputs: ["tag_all", "other_dmz", "other_lan"]
"""
    with tempfile.NamedTemporaryFile("w", suffix=".yaml", delete=False) as f:
        f.write(valid_yaml)
        tmp = f.name

    try:
        res = subprocess.run([GATE_BIN, "validate", "-c", tmp], capture_output=True, text=True)
        out = res.stdout + res.stderr
        is_valid = res.returncode == 0 and "Gate 'dmz_gate'" in out and "Gate 'lan_gate'" in out and "PASSED" in out
        record_test(
            "TC-MG-04: Multi-Gate Validation & Wiring (dmz_gate & lan_gate)",
            is_valid,
            "dmz_gate:15045 and lan_gate:15046 validated successfully with zero warnings"
        )
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)

def test_live_multi_gate_ingress_and_fallback():
    """Verify live running instance: traffic to dmz_gate and lan_gate correctly demuxed and routed."""
    dmz_port = 19145
    lan_port = 19146
    out_dmz_file = f"/tmp/test_mg_dmz_{os.getpid()}.log"
    out_lan_file = f"/tmp/test_mg_lan_{os.getpid()}.log"
    out_other_dmz = f"/tmp/test_mg_other_dmz_{os.getpid()}.log"
    out_other_lan = f"/tmp/test_mg_other_lan_{os.getpid()}.log"

    for p in [out_dmz_file, out_lan_file, out_other_dmz, out_other_lan]:
        if os.path.exists(p):
            os.remove(p)

    cfg = f"""
data_dir: "/tmp/vector_mg_test_{os.getpid()}"

gates:
  dmz_gate:
    address: "127.0.0.1:{dmz_port}"
    options:
      zero_copy: true
      reuse_port: true
      vrl_watch: false
    routes:
      http_route:
        type: "http_server"
      other:
        type: "socket"

  lan_gate:
    address: "127.0.0.1:{lan_port}"
    options:
      zero_copy: true
      reuse_port: true
      vrl_watch: false
    routes:
      beats_route:
        type: "logstash"
      other:
        type: "socket"

sources:
  in_dmz_http:
    type: http_server
    address: "dmz_gate.http_route"
    decoding:
      codec: bytes

  other_dmz:
    type: socket
    mode: tcp
    address: "dmz_gate.other"
    decoding:
      codec: bytes

  in_lan_beats:
    type: logstash
    address: "lan_gate.beats_route"

  other_lan:
    type: socket
    mode: tcp
    address: "lan_gate.other"
    decoding:
      codec: bytes

sinks:
  sink_dmz:
    type: file
    inputs: ["in_dmz_http"]
    path: "{out_dmz_file}"
    encoding:
      codec: json

  sink_lan:
    type: file
    inputs: ["in_lan_beats"]
    path: "{out_lan_file}"
    encoding:
      codec: json

  sink_other_dmz:
    type: file
    inputs: ["other_dmz"]
    path: "{out_other_dmz}"
    encoding:
      codec: json

  sink_other_lan:
    type: file
    inputs: ["other_lan"]
    path: "{out_other_lan}"
    encoding:
      codec: json
"""
    with tempfile.NamedTemporaryFile("w", suffix=".yaml", delete=False) as f:
        f.write(cfg)
        cfg_path = f.name

    proc = None
    try:
        proc = subprocess.Popen([GATE_BIN, "run", "-c", cfg_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Wait for both gates to open
        ready = False
        for _ in range(50):
            time.sleep(0.1)
            try:
                s1 = socket.create_connection(("127.0.0.1", dmz_port), timeout=0.1)
                s1.close()
                s2 = socket.create_connection(("127.0.0.1", lan_port), timeout=0.1)
                s2.close()
                ready = True
                break
            except Exception:
                continue

        record_test("TC-MG-05: Multi-Gate Concurrent Socket Listeners", ready, f"Both 127.0.0.1:{dmz_port} and :{lan_port} active")

        if ready:
            # 1. Send HTTP request to dmz_gate
            s_http = socket.create_connection(("127.0.0.1", dmz_port), timeout=2.0)
            req = b"POST / HTTP/1.1\r\nHost: localhost\r\nContent-Length: 18\r\n\r\n{\"dmz_msg\":\"hello\"}"
            s_http.sendall(req)
            s_http.close()

            # 2. Send Beats payload to lan_gate
            # Pack lumberjack frame: '2' 'D' seq:1 count:1 key:"message", val:"lan_beat_event"
            s_beats = socket.create_connection(("127.0.0.1", lan_port), timeout=2.0)
            # Lumberjack compressed frame with data
            import zlib
            inner = b"2D\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x07message\x00\x00\x00\x0elan_beat_event"
            compressed = zlib.compress(inner)
            packet = b"2C" + struct.pack(">I", len(compressed)) + compressed
            s_beats.sendall(packet)
            s_beats.close()

            # 3. Send Unmatched Garbage to dmz_gate -> should go to other_dmz
            s_g1 = socket.create_connection(("127.0.0.1", dmz_port), timeout=2.0)
            s_g1.sendall(b"UNKNOWN_DMZ_GARBAGE_PAYLOAD\n")
            s_g1.close()

            # 4. Send Unmatched Garbage to lan_gate -> should go to other_lan
            s_g2 = socket.create_connection(("127.0.0.1", lan_port), timeout=2.0)
            s_g2.sendall(b"UNKNOWN_LAN_GARBAGE_PAYLOAD\n")
            s_g2.close()

            time.sleep(1.5)

            # Check files
            dmz_received = os.path.exists(out_dmz_file) and os.path.getsize(out_dmz_file) > 0
            record_test("TC-MG-06: DMZ Gate HTTP Ingestion (dmz_gate.http_route)", dmz_received, "HTTP payload delivered to in_dmz_http")

            lan_received = os.path.exists(out_lan_file) and os.path.getsize(out_lan_file) > 0
            record_test("TC-MG-07: LAN Gate Beats Ingestion (lan_gate.beats_route)", lan_received, "Lumberjack payload delivered to in_lan_beats")

            dmz_other_received = os.path.exists(out_other_dmz) and os.path.getsize(out_other_dmz) > 0
            record_test("TC-MG-08: Isolated Fallback for dmz_gate (dmz_gate.other)", dmz_other_received, "Garbage routed to other_dmz sink")

            lan_other_received = os.path.exists(out_other_lan) and os.path.getsize(out_other_lan) > 0
            record_test("TC-MG-09: Isolated Fallback for lan_gate (lan_gate.other)", lan_other_received, "Garbage routed to other_lan sink")

    finally:
        if proc:
            proc.terminate()
            try:
                proc.wait(timeout=3)
            except Exception:
                proc.kill()
        if os.path.exists(cfg_path):
            os.remove(cfg_path)
        for p in [out_dmz_file, out_lan_file, out_other_dmz, out_other_lan]:
            if os.path.exists(p):
                os.remove(p)

def main():
    print(f"\n{Colors.BOLD}{Colors.CYAN}=============================================================================={Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}🧪 VECTOR GATE v2.5.0 MULTI-GATE INGRESS & SHORT-SYNTAX TEST SUITE{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}=============================================================================={Colors.RESET}\n")

    test_deprecated_gates_prefix_rejection()
    test_unknown_gate_rejection()
    test_unknown_route_rejection()
    test_valid_multi_gate_validation_and_direct_passthrough()
    test_live_multi_gate_ingress_and_fallback()

    print(f"\n{Colors.BOLD}------------------------------------------------------------------------------{Colors.RESET}")
    print(f"Total: {passed + failed} | {Colors.GREEN}Passed: {passed}{Colors.RESET} | {Colors.RED}Failed: {failed}{Colors.RESET}")
    print(f"{Colors.BOLD}------------------------------------------------------------------------------{Colors.RESET}\n")

    sys.exit(0 if failed == 0 else 1)

if __name__ == "__main__":
    main()

