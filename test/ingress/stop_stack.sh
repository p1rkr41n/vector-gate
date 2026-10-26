#!/usr/bin/env bash
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Dừng HAProxy và Vector..."
if [ -f "$DIR/haproxy.pid" ]; then
    HPID=$(cat "$DIR/haproxy.pid")
    kill $HPID 2>/dev/null || true
    rm -f "$DIR/haproxy.pid"
fi
killall haproxy 2>/dev/null || true

if [ -f "$DIR/vector.pid" ]; then
    VPID=$(cat "$DIR/vector.pid")
    kill $VPID 2>/dev/null || true
    rm -f "$DIR/vector.pid"
fi
pkill -f "vector_ingress.yaml" 2>/dev/null || true

echo "√ Đã dừng thành công!"

