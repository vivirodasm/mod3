#!/bin/sh
set -eu

SEED_FILE="${SEED_FILE:-/seed/history.om}"
DATA_DIR="${DATA_DIR:-/prometheus}"
MARKER="${DATA_DIR}/.curso6_seeded"

if [ -f "$MARKER" ]; then
  echo "Seed ya aplicado, omitiendo."
  exit 0
fi

if [ ! -f "$SEED_FILE" ]; then
  echo "No existe $SEED_FILE" >&2
  exit 1
fi

echo "Creando bloques TSDB desde $SEED_FILE ..."
promtool tsdb create-blocks-from openmetrics "$SEED_FILE" "$DATA_DIR"

# Prometheus corre como nobody (65534); el seed corre como root.
chown -R 65534:65534 "$DATA_DIR" || true
touch "$MARKER"
chown 65534:65534 "$MARKER" || true

echo "Seed OK"
ls -la "$DATA_DIR" | head -n 30
