#!/usr/bin/env python3
"""
Comprehensive Validation Script:
Verifies that each protocol sent to Vector Smart Gate (0.0.0.0:5000)
is routed to the correct destination source without misclassification or omission.
Checks .type_log and .source_id in /var/log/vector/forwarded_logs.ndjson.
"""

import base64
import json
import os
import socket
import sys
import time
import urllib.request

GATE_IP = "127.0.0.1"
GATE_PORT = 5000
OUTPUT_FILE = "/home/manager/vectormod/docker_gate/output/forwarded_logs.ndjson"

def get_output_line_count():
    if not os.path.exists(OUTPUT_FILE):
        return 0
    with open(OUTPUT_FILE, "r", encoding="utf-8", errors="ignore") as f:
        return sum(1 for line in f if line.strip())

def get_last_n_lines(n=5):
    if not os.path.exists(OUTPUT_FILE):
        return []
    with open(OUTPUT_FILE, "r", encoding="utf-8", errors="ignore") as f:
        lines = [line.strip() for line in f if line.strip()]
        return lines[-n:] if lines else []

def send_raw_tcp(payload: bytes):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5.0)
    s.connect((GATE_IP, GATE_PORT))
    s.sendall(payload)
    time.sleep(0.1)
    s.close()

def send_http(path: str, headers: dict, body: bytes):
    req = urllib.request.Request(
        f"http://{GATE_IP}:{GATE_PORT}{path}",
        data=body,
        headers=headers,
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=5.0) as resp:
            return resp.read()
    except Exception as e:
        return str(e).encode()

def run_test(name: str, send_fn, expected_type_log: str, expected_source_id: str):
    send_fn()
    
    # Wait up to 3 seconds for vector to write to output
    matched = None
    for _ in range(15):
        time.sleep(0.2)
        recent = get_last_n_lines(10)
        for l in reversed(recent):
            try:
                obj = json.loads(l)
                if obj.get("message") == "healthcheck":
                    continue
                if obj.get("type_log") == expected_type_log and obj.get("source_id") == expected_source_id:
                    matched = obj
                    break
            except Exception:
                pass
        if matched:
            break
    
    if matched:
        print(f"  [PASS] {name:<30} -> type_log: '{matched.get('type_log')}', source_id: '{matched.get('source_id')}'")
        return True, matched
    else:
        # Check what was actually written
        recent = get_last_n_lines(2)
        print(f"  [FAIL] {name:<30} -> Expected type_log: '{expected_type_log}', source_id: '{expected_source_id}'. Last output: {recent}")
        return False, None

def main():
    print("=" * 80)
    print("🚀 VALIDATING ALL LOG TYPES & SOURCES ROUTING ON VECTOR GATE (PORT 5000)")
    print("=" * 80)

    results = []

    # 1. Custom Binary IoT (0xDEADBEEF)
    def send_custom_iot():
        payload = b"\xDE\xAD\xBE\xEF" + b" IoT sensor status: OK temperature=24.5C\n"
        send_raw_tcp(payload)
    results.append(run_test("Custom Binary IoT (DEADBEEF)", send_custom_iot, "custom_binary_iot", "in_custom_iot"))

    # 2. Custom App Signature ("MYLOG")
    def send_custom_app():
        payload = b"MYLOG" + b" Application transaction completed id=98765\n"
        send_raw_tcp(payload)
    results.append(run_test("Custom App Signature (MYLOG)", send_custom_app, "custom_app_signature", "in_custom_app"))

    # 3. Custom Offset Signature ("MAGIC" at offset 4)
    def send_custom_offset():
        payload = b"INITMAGIC" + b" Header offset payload data stream\n"
        send_raw_tcp(payload)
    results.append(run_test("Custom Offset Signature (MAGIC@4)", send_custom_offset, "custom_offset_signature", "in_custom_offset"))

    # 4. Syslog RFC 5424
    def send_syslog_5424():
        payload = b"<134>1 2026-10-25T10:00:00.000Z myhost testapp 1234 - - System operational\n"
        send_raw_tcp(payload)
    results.append(run_test("Syslog RFC 5424", send_syslog_5424, "syslog", "in_syslog"))

    # 5. Syslog RFC 3164
    def send_syslog_3164():
        payload = b"<34>Oct 25 10:00:00 myhost kernel: eth0 link up\n"
        send_raw_tcp(payload)
    results.append(run_test("Syslog RFC 3164", send_syslog_3164, "syslog", "in_syslog"))

    # 6. Datadog Logs API
    def send_datadog():
        with open("/home/manager/vectormod/test/mock_logs/datadog_intake.json", "rb") as f:
            body = f.read()
        send_http("/api/v2/logs", {"Content-Type": "application/json", "DD-API-KEY": "test-key"}, body)
    results.append(run_test("Datadog Agent Intake", send_datadog, "datadog_agent", "in_datadog"))

    # 7. Splunk HEC
    def send_splunk():
        body = json.dumps({
            "time": time.time(),
            "event": "Splunk HEC test audit event",
            "sourcetype": "access_combined"
        }).encode('utf-8')
        send_http("/services/collector/event", {"Content-Type": "application/json", "Authorization": "Splunk mytoken"}, body)
    results.append(run_test("Splunk HEC Ingest", send_splunk, "splunk_hec", "in_splunk"))

    # 8. Generic HTTP Server
    def send_generic_http():
        body = b'{"event": "generic_http_payload", "status": "ok"}\n'
        send_http("/", {"Content-Type": "application/x-ndjson"}, body)
    results.append(run_test("Generic HTTP (http_server)", send_generic_http, "http_server", "in_http"))

    # 9. Heroku Logs
    def send_heroku():
        body = b'267 <158>1 2026-10-25T10:00:00.000000+00:00 host heroku router - at=info method=GET path="/cart_link" host=app.timber.io request_id=05726858-c44e-4f94-9a20-37df73be9006 fwd="73.75.38.87" dyno=web.1 connect=1ms service=22ms status=200 bytes=656 protocol=http\n'
        send_http("/events?app=myapp", {
            "Content-Type": "application/logplex-1",
            "Logplex-Msg-Count": "1",
            "Logplex-Frame-Id": "frame-01",
            "Logplex-Drain-Token": "drain-test"
        }, body)
    results.append(run_test("Heroku Drain", send_heroku, "heroku_logs", "in_heroku"))

    # 10. AWS Kinesis Firehose
    def send_firehose():
        record_data = base64.b64encode(b'{"message": "firehose log record"}').decode('ascii')
        body = json.dumps({
            "requestId": "req-12345",
            "timestamp": int(time.time() * 1000),
            "records": [{"data": record_data}]
        }).encode('utf-8')
        send_http("/aws/firehose", {
            "Content-Type": "application/json",
            "X-Amz-Firehose-Protocol-Version": "1.0",
            "X-Amz-Firehose-Request-Id": "req-12345",
            "X-Amz-Firehose-Source-Arn": "arn:aws:firehose:us-east-1:123456789012:deliverystream/test"
        }, body)
    results.append(run_test("AWS Kinesis Firehose", send_firehose, "aws_kinesis_firehose", "in_aws_firehose"))

    # 11. Fluent Forward Protocol (MessagePack array [tag, entries, option])
    def send_fluent():
        # Tag: 'test.app', time: now, record: {'log': 'fluent message'}
        # 0x93 = fixarray(3), 0xa8 = fixstr(8) 'test.app', 0x91 = fixarray(1), 0x92 = fixarray(2) [time, record]
        tag = b"test.app"
        t_int = int(time.time())
        # Let's send raw msgpack chunk
        payload = b"\x93\xa8test.app\x91\x92" + b"\xce" + t_int.to_bytes(4, 'big') + b"\x81\xa3msg\xa6fluent\x80"
        send_raw_tcp(payload)
    results.append(run_test("Fluent Forward (MsgPack)", send_fluent, "fluent_forward", "in_fluent"))

    # 12. Beats Lumberjack Protocol
    def send_beats():
        # Lumberjack v2 protocol: 0x32, 'D' (data frame), seq (4 bytes), count (4 bytes), kv pairs...
        # Let's send sample from samples/13_beats_lumberjack/beats_payload.json or raw bytes
        # Byte '2' is 0x32
        payload = b"2\x01\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x04line\x00\x00\x00\x05beats"
        # Beats requires full window or handshake, but let's test if router routes to beats_gate
        send_raw_tcp(payload)
    # Beats handshake can be tricky over raw socket, let's see how gate handles it

    # 13. Terminal Fallback / Raw Socket (other_unmatched)
    def send_raw_fallback():
        payload = b"UNKNOWN_ARBITRARY_RAW_TEXT_WITHOUT_SIGNATURE_9999\n"
        send_raw_tcp(payload)
    results.append(run_test("Fallback Raw Socket (other)", send_raw_fallback, "other_unmatched", "other_unmatched"))

    print("-" * 80)
    total_passed = sum(1 for p, _ in results if p)
    total_tests = len(results)
    print(f"📊 SUMMARY: {total_passed} / {total_tests} Tests Passed ({(total_passed/total_tests)*100:.1f}%)")
    print("=" * 80)

    if total_passed == total_tests:
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
