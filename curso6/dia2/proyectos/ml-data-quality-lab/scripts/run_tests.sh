#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if ! command -v uv >/dev/null 2>&1; then
  echo "Instala uv: https://docs.astral.sh/uv/getting-started/installation/" >&2
  exit 1
fi

uv sync
uv run pytest -v
uv run python -m src.run_pipeline
echo "Pipeline OK. Reporte: data/pipeline_report.json"
