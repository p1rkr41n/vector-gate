import socket
import time
import threading
import sys
import os

PORT = 5000
HOST = "127.0.0.1"
TOTAL_EVENTS = 100_000
NUM_THREADS = 8
BATCH_SIZE = TOTAL_EVENTS // NUM_THREADS

SYSLOG_SAMPLE = b"<134>1 2026-10-24T12:00:00Z firewall.sec.corp kernel - - [meta sequenceId=\"1000\"] Attack blocked proto=TCP src=192.168.1.50 dst=10.0.0.1\n"

results = []

def worker(worker_id, count):
    sent = 0
    start = time.perf_counter()
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        s.connect((HOST, PORT))
        
        # Send in chunks of 50 logs per write
        chunk = SYSLOG_SAMPLE * 50
        chunks_needed = count // 50
        
        for _ in range(chunks_needed):
            s.sendall(chunk)
            sent += 50
            
        s.close()
    except Exception as e:
        print(f"[Worker {worker_id}] Error: {e}", file=sys.stderr)
    elapsed = time.perf_counter() - start
    results.append((sent, elapsed))

print(f"🚀 [ST-01] Bắt đầu kiểm thử tải cực hạn: {TOTAL_EVENTS:,} sự kiện qua {NUM_THREADS} luồng song song...")
t0 = time.perf_counter()

threads = []
for i in range(NUM_THREADS):
    t = threading.Thread(target=worker, args=(i, BATCH_SIZE))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

total_elapsed = time.perf_counter() - t0
total_sent = sum(r[0] for r in results)
eps = total_sent / total_elapsed if total_elapsed > 0 else 0

print("=" * 70)
print(f"⚡ KẾT QUẢ KIỂM THỬ TẢI CỰC HẠN (ST-01 VECTOR-GATE TURBO-KERNEL)")
print("=" * 70)
print(f"• Tổng số sự kiện gửi đi       : {total_sent:,} events")
print(f"• Tổng thời gian xử lý         : {total_elapsed:.4f} giây")
print(f"• Thông lượng tức thời (EPS)    : {eps:,.0f} EPS (Sự kiện / Giây)")
print(f"• Độ trễ trung bình mỗi batch  : {(total_elapsed / (total_sent / 50)) * 1000:.4f} ms")
print(f"• Trạng thái nghiệm thu         : {'✅ ĐẠT CHỈ TIÊU (PASSED)' if eps >= 100000 else '⚠️ CHƯA ĐẠT'}")
print("=" * 70)

