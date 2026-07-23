#!/usr/bin/env bash
set -euo pipefail

echo "==> Exporter health"
curl -sf "http://127.0.0.1:8000/" | tee /dev/stderr
echo

echo "==> Metrics sample"
curl -sf "http://127.0.0.1:8000/metrics" | grep -E '^qa_(flake_rate|defect_leakage|test_effectiveness_ratio|coverage)' | head -n 20
echo

echo "==> Prometheus ready"
curl -sf "http://127.0.0.1:9090/-/ready"
echo

echo "==> Prometheus targets"
curl -sf "http://127.0.0.1:9090/api/v1/targets" | grep -o '"health":"[^"]*"' | head -n 5 || true
echo

echo "Verificación básica OK. Abre Grafana: http://localhost:3000"
