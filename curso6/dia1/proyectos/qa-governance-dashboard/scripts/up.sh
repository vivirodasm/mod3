#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if [[ ! -f prometheus/seed/history.om ]]; then
  python3 scripts/generate_history.py || python scripts/generate_history.py
fi

docker compose up -d --build

echo "Esperando servicios..."
for i in $(seq 1 30); do
  if curl -sf "http://127.0.0.1:8000/" >/dev/null \
    && curl -sf "http://127.0.0.1:9090/-/ready" >/dev/null; then
    echo "OK"
    echo "Exporter:  http://localhost:8000/metrics"
    echo "Prometheus: http://localhost:9090"
    echo "Grafana:    http://localhost:3000  (admin/admin)"
    exit 0
  fi
  sleep 2
done

echo "Timeout esperando servicios" >&2
exit 1
