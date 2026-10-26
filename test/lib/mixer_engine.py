#!/usr/bin/env python3
"""
High-Speed In-Memory Event Mixer & Benchmark Streaming Engine
Zero external dependencies (uses Python standard library: socket, threading, time, json).
Pre-caches mock log templates into RAM, dynamically mutates timestamps/sequences,
and pumps data at line-rate through concurrent TCP/HTTP sockets.
"""

import argparse
import json
import os
import re
import socket
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from typing import List, Tuple, Dict, Any

# Regex patterns for fast in-memory timestamp mutation
ISO8601_REGEX = re.compile(rb'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{2}:\d{2})?')
RFC3164_REGEX = re.compile(rb'[A-Z][a-z]{2}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2}')
EPOCH_REGEX = re.compile(rb'"(time|timestamp)":\s*\d+(\.\d+)?')

def mutate_event_bytes(line: bytes, log_type: str, now: datetime, seq: int) -> bytes:
    """Mutate timestamp and sequence in-memory to ensure unique, non-deduplicated logs."""
    if log_type.startswith("syslog_rfc5424"):
        # Replace RFC5424 ISO8601 timestamp: 2026-10-25T10:00:00.123456Z
        ts_str = now.strftime('%Y-%m-%dT%H:%M:%S.%fZ').encode('ascii')
        return ISO8601_REGEX.sub(ts_str, line, count=1)
    elif log_type.startswith("syslog_rfc3164"):
        # Replace RFC3164 BSD timestamp: Oct 25 10:00:00
        ts_str = now.strftime('%b %e %H:%M:%S').encode('ascii')
        return RFC3164_REGEX.sub(ts_str, line, count=1)
    elif "json" in log_type or "datadog" in log_type or "splunk" in log_type or "suricata" in log_type:
        # JSON epoch or ISO timestamp
        epoch_str = f'"timestamp":{int(now.timestamp())}'.encode('ascii')
        return EPOCH_REGEX.sub(epoch_str, line, count=1)
    return line

def worker_tcp_stream(
    target_ip: str,
    target_port: int,
    events_to_send: int,
    sample_templates: List[bytes],
    log_type: str,
    batch_size: int,
    mutate: bool
) -> Dict[str, Any]:
    """Single worker thread streaming TCP payloads."""
    latencies = []
    total_bytes = 0
    events_sent = 0
    errors = 0
    num_samples = len(sample_templates)

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        s.settimeout(10.0)
        s.connect((target_ip, target_port))
    except Exception as e:
        return {
            "events_sent": 0,
            "total_bytes": 0,
            "errors": events_to_send,
            "latencies": [],
            "error_msg": str(e)
        }

    seq = 0
    while events_sent < events_to_send:
        batch_count = min(batch_size, events_to_send - events_sent)
        now = datetime.now(timezone.utc)
        
        # Pre-assemble batch in memory
        chunk_parts = []
        for i in range(batch_count):
            tpl = sample_templates[(seq + i) % num_samples]
            if mutate:
                tpl = mutate_event_bytes(tpl, log_type, now, seq + i)
            chunk_parts.append(tpl)
            if not tpl.endswith(b'\n'):
                chunk_parts.append(b'\n')
        
        batch_bytes = b"".join(chunk_parts)
        seq += batch_count

        t0 = time.perf_counter()
        try:
            s.sendall(batch_bytes)
            t1 = time.perf_counter()
            latencies.append((t1 - t0) * 1000.0) # ms
            total_bytes += len(batch_bytes)
            events_sent += batch_count
        except Exception as e:
            errors += batch_count
            break

    try:
        s.close()
    except Exception:
        pass

    return {
        "events_sent": events_sent,
        "total_bytes": total_bytes,
        "errors": errors,
        "latencies": latencies,
        "error_msg": None
    }

def worker_http_stream(
    target_ip: str,
    target_port: int,
    events_to_send: int,
    sample_templates: List[bytes],
    log_type: str,
    batch_size: int,
    mutate: bool
) -> Dict[str, Any]:
    """Single worker thread streaming HTTP requests with Keep-Alive."""
    latencies = []
    total_bytes = 0
    events_sent = 0
    errors = 0
    num_samples = len(sample_templates)

    endpoint_path = "/"
    headers_extra = ""
    if "datadog" in log_type:
        endpoint_path = "/api/v2/logs"
        headers_extra = "DD-API-KEY: test-key\r\nContent-Type: application/json\r\n"
    elif "splunk" in log_type:
        endpoint_path = "/services/collector/event"
        headers_extra = "Authorization: Splunk test-token\r\nContent-Type: application/json\r\n"
    else:
        endpoint_path = "/"
        headers_extra = "Content-Type: application/x-ndjson\r\n"

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        s.settimeout(10.0)
        s.connect((target_ip, target_port))
    except Exception as e:
        return {
            "events_sent": 0,
            "total_bytes": 0,
            "errors": events_to_send,
            "latencies": [],
            "error_msg": str(e)
        }

    seq = 0
    while events_sent < events_to_send:
        batch_count = min(batch_size, events_to_send - events_sent)
        now = datetime.now(timezone.utc)
        
        chunk_parts = []
        for i in range(batch_count):
            tpl = sample_templates[(seq + i) % num_samples]
            if mutate:
                tpl = mutate_event_bytes(tpl, log_type, now, seq + i)
            chunk_parts.append(tpl)
            if not tpl.endswith(b'\n'):
                chunk_parts.append(b'\n')
        
        body = b"".join(chunk_parts)
        seq += batch_count

        http_req = (
            f"POST {endpoint_path} HTTP/1.1\r\n"
            f"Host: {target_ip}:{target_port}\r\n"
            f"User-Agent: VectorBenchmark/1.0\r\n"
            f"Connection: keep-alive\r\n"
            f"Content-Length: {len(body)}\r\n"
            f"{headers_extra}\r\n"
        ).encode('ascii') + body

        t0 = time.perf_counter()
        try:
            s.sendall(http_req)
            # Read minimal HTTP response
            resp = s.recv(256)
            t1 = time.perf_counter()
            latencies.append((t1 - t0) * 1000.0)
            total_bytes += len(http_req)
            events_sent += batch_count
        except Exception as e:
            errors += batch_count
            break

    try:
        s.close()
    except Exception:
        pass

    return {
        "events_sent": events_sent,
        "total_bytes": total_bytes,
        "errors": errors,
        "latencies": latencies,
        "error_msg": None
    }

def run_benchmark(
    target_ip: str,
    target_port: int,
    log_file: str,
    log_type: str,
    total_events: int,
    concurrency: int,
    batch_size: int,
    mutate: bool
) -> Dict[str, Any]:
    """Execute the multi-threaded in-memory benchmark."""
    if not os.path.exists(log_file):
        raise FileNotFoundError(f"Mock log file not found: {log_file}")

    # 1. Read mock templates into RAM
    with open(log_file, "rb") as f:
        raw_lines = [line.strip() for line in f if line.strip()]

    if not raw_lines:
        raise ValueError(f"Mock log file {log_file} is empty!")

    base_samples_count = len(raw_lines)
    is_http = any(k in log_type.lower() for k in ["http", "datadog", "splunk", "nginx", "ndjson"])

    # 2. Distribute workload across concurrency workers
    events_per_worker = total_events // concurrency
    remainder = total_events % concurrency

    start_wall_time = time.time()
    t_start = time.perf_counter()

    worker_func = worker_http_stream if is_http else worker_tcp_stream

    with ThreadPoolExecutor(max_workers=concurrency) as executor:
        futures = []
        for i in range(concurrency):
            w_events = events_per_worker + (1 if i < remainder else 0)
            if w_events > 0:
                f = executor.submit(
                    worker_func,
                    target_ip,
                    target_port,
                    w_events,
                    raw_lines,
                    log_type,
                    batch_size,
                    mutate
                )
                futures.append(f)

        results = [f.result() for f in futures]

    t_end = time.perf_counter()
    elapsed = max(t_end - t_start, 0.000001)

    # 3. Aggregate metrics
    total_sent = sum(r["events_sent"] for r in results)
    total_bytes = sum(r["total_bytes"] for r in results)
    total_errors = sum(r["errors"] for r in results)
    all_latencies = []
    for r in results:
        all_latencies.extend(r["latencies"])

    all_latencies.sort()
    count_lat = len(all_latencies)

    p50 = all_latencies[int(count_lat * 0.50)] if count_lat > 0 else 0.0
    p90 = all_latencies[int(count_lat * 0.90)] if count_lat > 0 else 0.0
    p99 = all_latencies[int(count_lat * 0.99)] if count_lat > 0 else 0.0
    min_lat = all_latencies[0] if count_lat > 0 else 0.0
    max_lat = all_latencies[-1] if count_lat > 0 else 0.0

    eps = total_sent / elapsed
    mb_s = (total_bytes / (1024 * 1024)) / elapsed
    success_rate = (total_sent / total_events * 100.0) if total_events > 0 else 0.0

    return {
        "log_type": log_type,
        "target": f"{target_ip}:{target_port}",
        "protocol": "HTTP" if is_http else "TCP",
        "concurrency": concurrency,
        "batch_size": batch_size,
        "base_samples": base_samples_count,
        "total_events_requested": total_events,
        "total_events_sent": total_sent,
        "total_bytes": total_bytes,
        "total_errors": total_errors,
        "elapsed_seconds": round(elapsed, 4),
        "throughput_eps": round(eps, 2),
        "throughput_mb_s": round(mb_s, 2),
        "bandwidth_mbps": round(mb_s * 8, 2),
        "latency_min_ms": round(min_lat, 2),
        "latency_p50_ms": round(p50, 2),
        "latency_p90_ms": round(p90, 2),
        "latency_p99_ms": round(p99, 2),
        "latency_max_ms": round(max_lat, 2),
        "success_rate_percent": round(success_rate, 2),
        "status": "PASS" if total_sent == total_events else "PARTIAL_FAIL"
    }

def print_text_report(stats: Dict[str, Any]):
    """Print beautifully formatted ASCII report."""
    print("=" * 80)
    print("🚀 VECTOR STANDALONE INGESTION BENCHMARK REPORT")
    print("=" * 80)
    print(f"📌 THÔNG TIN KIỂM THỬ:")
    print(f"  • Log Protocol Type     : {stats['log_type']} ({stats['protocol']})")
    print(f"  • Target Destination    : {stats['target']}")
    print(f"  • Concurrency Workers   : {stats['concurrency']} Parallel Connections")
    print(f"  • Batch Size per Stream : {stats['batch_size']:,} events / frame")
    print("-" * 80)
    print(f"📊 KHỐI LƯỢNG & THỜI GIAN:")
    print(f"  • Target Events Count   : {stats['total_events_requested']:,} events")
    print(f"  • Base Mock Samples     : {stats['base_samples']:,} unique templates (In-Memory Mixed)")
    print(f"  • Total Data Ingested   : {stats['total_bytes'] / (1024*1024):.2f} MB ({stats['total_bytes']:,} bytes)")
    print(f"  • Total Execution Time  : {stats['elapsed_seconds']} seconds")
    print("-" * 80)
    print(f"⚡ HIỆU NĂNG ĐẠT ĐƯỢC (THROUGHPUT):")
    print(f"  • Ingest Rate (EPS)     : {stats['throughput_eps']:,.0f} EPS")
    print(f"  • Network Bandwidth     : {stats['throughput_mb_s']:.2f} MB/s ({stats['bandwidth_mbps']:.2f} Mbps)")
    print("-" * 80)
    print(f"⏱️ ĐỘ TRỄ MẠNG & XỬ LÝ (LATENCY):")
    print(f"  • Min Latency           : {stats['latency_min_ms']} ms")
    print(f"  • P50 (Trung vị)        : {stats['latency_p50_ms']} ms")
    print(f"  • P90                   : {stats['latency_p90_ms']} ms")
    print(f"  • P99                   : {stats['latency_p99_ms']} ms")
    print(f"  • Max Latency           : {stats['latency_max_ms']} ms")
    print("-" * 80)
    print(f"✅ ĐỘ TIN CẬY & TOÀN VẸN:")
    status_label = "THÀNH CÔNG HOÀN TOÀN" if stats['status'] == "PASS" else "MỘT PHẦN THẤT BẠI"
    print(f"  • Trạng thái            : {status_label} ({stats['success_rate_percent']}%)")
    print(f"  • Thành công            : {stats['total_events_sent']:,} / {stats['total_events_requested']:,} events")
    print(f"  • Thất bại / Bị drop    : {stats['total_errors']:,} events")
    print("=" * 80)

def main():
    parser = argparse.ArgumentParser(description="Vector High-Speed In-Memory Event Mixer")
    parser.add_argument("--target-ip", default="127.0.0.1", help="Target IP")
    parser.add_argument("--target-port", type=int, default=5000, help="Target Port")
    parser.add_argument("--log-file", required=True, help="Path to mock log file")
    parser.add_argument("--log-type", default="syslog_rfc5424", help="Log Protocol Type")
    parser.add_argument("--total-events", type=int, default=100000, help="Total events to send")
    parser.add_argument("--concurrency", type=int, default=8, help="Number of concurrent workers")
    parser.add_argument("--batch-size", type=int, default=500, help="Events per batch")
    parser.add_argument("--mutate", action="store_true", default=True, help="Enable in-memory mutation")
    parser.add_argument("--no-mutate", dest="mutate", action="store_false", help="Disable in-memory mutation")
    parser.add_argument("--json", action="store_true", help="Output JSON results")

    args = parser.parse_args()

    try:
        stats = run_benchmark(
            target_ip=args.target_ip,
            target_port=args.target_port,
            log_file=args.log_file,
            log_type=args.log_type,
            total_events=args.total_events,
            concurrency=args.concurrency,
            batch_size=args.batch_size,
            mutate=args.mutate
        )

        if args.json:
            print(json.dumps(stats, indent=2))
        else:
            print_text_report(stats)

        sys.exit(0 if stats["status"] == "PASS" else 1)
    except Exception as e:
        sys.stderr.write(f"Error during benchmark: {e}\n")
        sys.exit(2)

if __name__ == "__main__":
    main()
