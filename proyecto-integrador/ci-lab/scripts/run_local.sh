#!/usr/bin/env bash
# Replica el job de CI en local con Docker (Mac / Linux / Git Bash).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "==> Build imagen CI (api-lab)"
docker compose build test

echo "==> Run pytest dentro de Docker"
docker compose run --rm --no-deps test

echo "OK — mismo criterio que el workflow de GitHub Actions"
