#!/usr/bin/env python3
"""
Vector Smart Gate: Consolidated Sample Sender
Sends sample events for all 15 supported protocols through port 0.0.0.0:5000.
"""

import argparse
import json
import os
import socket
import struct
import time
import urllib.request

SAMPLES_JSON = os.path.join(os.path.dirname(__file__), "samples.json")

def send_tcp(host: str, port: int, payload: bytes, desc: str) -> bool:
    print(f"  [TCP] {desc:<35} ...", end=" ")
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        s.connect((host, port))
        s.sendall(payload)
        s.close()
        print("✅ SENT")
        return True
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False

def send_http(host: str, port: int, path: str, payload: str, headers: dict, desc: str) -> bool:
    url = f"http://{host}:{port}{path}"
    print(f"  [HTTP] {desc:<34} ...", end=" ")
    try:
        req = urllib.request.Request(url, data=payload.encode("utf-8"), headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=5) as resp:
            print(f"✅ HTTP {resp.getcode()}")
            return True
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False

def send_beats_lumberjack(host: str, port: int) -> bool:
    print(f"  [BEATS] Lumberjack v2 Protocol            ...", end=" ")
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        s.connect((host, port))
        payload_json = b'{"message":"Lumberjack Beats event"}'
        frame = bytearray([0x32, 0x4A]) + struct.pack(">I", 1) + struct.pack(">I", len(payload_json)) + payload_json
        s.sendall(frame)
        s.close()
        print("✅ SENT")
        return True
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False

def send_fluent_msgpack(host: str, port: int) -> bool:
    print(f"  [FLUENT] MessagePack Protocol             ...", end=" ")
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        s.connect((host, port))
        tag = b"app.fluent"
        record = b'{"log":"Fluent test"}'
        # Simplified msgpack array format [tag, timestamp, record]
        msgpack_frame = bytearray([0x93]) + bytearray([0xA0 + len(tag)]) + tag + struct.pack(">I", int(time.time())) + bytearray([0xDA, 0x00, len(record)]) + record
        s.sendall(msgpack_frame)
        s.close()
        print("✅ SENT")
        return True
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Vector Smart Gate Sample Sender")
    parser.add_argument("--host", default="127.0.0.1", help="Target host (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=5000, help="Target port (default: 5000)")
    parser.add_argument("--all", action="store_true", help="Send all sample payloads")
    parser.add_argument("--protocol", choices=["syslog", "http", "splunk", "datadog", "beats", "fluent", "raw"], help="Specific protocol to test")
    args = parser.parse_args()

    with open(SAMPLES_JSON, "r", encoding="utf-8") as f:
        samples = json.load(f)

    print("==================================================================")
    print(f"🚀 VECTOR SMART GATE SAMPLE DISPATCHER -> {args.host}:{args.port}")
    print("==================================================================")

    if args.protocol == "beats" or args.all:
        send_beats_lumberjack(args.host, args.port)
        time.sleep(0.1)

    if args.protocol == "fluent" or args.all:
        send_fluent_msgpack(args.host, args.port)
        time.sleep(0.1)

    for key, item in samples.items():
        proto = item["protocol"]
        payload = item["payload"]
        channel = item["channel"]

        if args.protocol == "syslog" and channel != "syslog":
            continue
        if args.protocol == "http" and channel != "http_server":
            continue
        if args.protocol == "splunk" and channel != "splunk_hec":
            continue
        if args.protocol == "datadog" and channel != "datadog_agent":
            continue
        if args.protocol == "raw" and channel != "socket":
            continue
        if not args.all and not args.protocol:
            continue

        if channel == "http_server":
            send_http(args.host, args.port, "/", payload, {"Content-Type": "application/json"}, proto)
        elif channel == "splunk_hec":
            send_http(args.host, args.port, "/services/collector/event", payload, {"Authorization": "Splunk token", "Content-Type": "application/json"}, proto)
        elif channel == "datadog_agent":
            send_http(args.host, args.port, "/v1/input", payload, {"DD-API-KEY": "key", "Content-Type": "application/json"}, proto)
        elif channel in ("syslog", "socket"):
            send_tcp(args.host, args.port, payload.encode("utf-8"), proto)

        time.sleep(0.1)

    print("==================================================================")
    print("✨ Hoàn tất lượt gửi mẫu!")

if __name__ == "__main__":
    main()
