#!/usr/bin/env bash
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
mkdir -p "$DIR/output" "$DIR/data" "$DIR/logs"

echo "[1/2] Khởi động Vector Core..."
vector --config "$DIR/vector/vector_ingress.yaml" > "$DIR/logs/vector.log" 2>&1 &
VECTOR_PID=$!
echo $VECTOR_PID > "$DIR/vector.pid"
sleep 2

if ! kill -0 $VECTOR_PID 2>/dev/null; then
    echo "[ERROR] Vector không thể khởi động! Kiểm tra logs/vector.log"
    cat "$DIR/logs/vector.log"
    exit 1
fi
echo "√ Vector đang chạy (PID: $VECTOR_PID)"

echo "[2/2] Khởi động HAProxy Smart Ingress (0.0.0.0:5000)..."
haproxy -f "$DIR/haproxy/haproxy.cfg" > "$DIR/logs/haproxy.log" 2>&1 &
HAPROXY_PID=$!
echo $HAPROXY_PID > "$DIR/haproxy.pid"
sleep 1

if ! kill -0 $HAPROXY_PID 2>/dev/null; then
    echo "[ERROR] HAProxy không thể khởi động! Kiểm tra logs/haproxy.log"
    cat "$DIR/logs/haproxy.log"
    exit 1
fi
echo "√ HAProxy đang chạy (PID: $HAPROXY_PID)"
echo "--------------------------------------------------------"
echo "🌟 Hệ thống Gom Cổng Thông Minh HAProxy + Vector đã sẵn sàng!"
echo "👉 Cổng tiếp nhận duy nhất: 0.0.0.0:5000"
echo "👉 File log đầu ra: $DIR/output/all_forwarded_logs.jsonl"

