"""QA governance metrics exporter for Prometheus (course lab)."""

from __future__ import annotations

import os
import random
import threading
import time

from flask import Flask, Response
from prometheus_client import (
    CONTENT_TYPE_LATEST,
    Gauge,
    generate_latest,
)

SERVICES = ("auth", "payments", "catalog", "notifications")

FLAKE_RATE = Gauge(
    "qa_flake_rate",
    "Proportion of flaky tests over total executed (0-1)",
    ["service"],
)
DEFECT_LEAKAGE = Gauge(
    "qa_defect_leakage",
    "Defects found in production over total defects (0-1)",
    ["service"],
)
TEST_EFFECTIVENESS = Gauge(
    "qa_test_effectiveness_ratio",
    "Defects caught in test over total defects (0-1)",
    ["service"],
)
COVERAGE = Gauge(
    "qa_coverage",
    "Automated test coverage percentage (0-100)",
    ["service"],
)

# Seed values used for a stable first scrape; then they drift slightly.
# Valores pensados para que payments/notifications disparen alertas de forma estable.
BASELINES = {
    "auth": {"flake": 0.04, "leakage": 0.08, "effectiveness": 0.92, "coverage": 78.0},
    "payments": {"flake": 0.11, "leakage": 0.16, "effectiveness": 0.82, "coverage": 68.0},
    "catalog": {"flake": 0.03, "leakage": 0.05, "effectiveness": 0.95, "coverage": 88.0},
    "notifications": {"flake": 0.14, "leakage": 0.19, "effectiveness": 0.80, "coverage": 62.0},
}


def _clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def _refresh_metrics() -> None:
    for service in SERVICES:
        base = BASELINES[service]
        # Ruido acotado para que los servicios “rojos” no bajen del umbral por azar.
        flake = _clamp(base["flake"] + random.uniform(-0.005, 0.01), 0.0, 1.0)
        leakage = _clamp(base["leakage"] + random.uniform(-0.01, 0.015), 0.0, 1.0)
        effectiveness = _clamp(base["effectiveness"] + random.uniform(-0.01, 0.01), 0.0, 1.0)
        coverage = _clamp(base["coverage"] + random.uniform(-1.5, 1.5), 0.0, 100.0)

        FLAKE_RATE.labels(service=service).set(flake)
        DEFECT_LEAKAGE.labels(service=service).set(leakage)
        TEST_EFFECTIVENESS.labels(service=service).set(effectiveness)
        COVERAGE.labels(service=service).set(coverage)


def _metrics_loop(interval_seconds: float) -> None:
    while True:
        _refresh_metrics()
        time.sleep(interval_seconds)


app = Flask(__name__)


@app.get("/")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "qa-governance-exporter"}


@app.get("/metrics")
def metrics() -> Response:
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


def main() -> None:
    interval = float(os.getenv("METRICS_INTERVAL_SECONDS", "10"))
    host = os.getenv("EXPORTER_HOST", "0.0.0.0")
    port = int(os.getenv("EXPORTER_PORT", "8000"))

    _refresh_metrics()
    worker = threading.Thread(target=_metrics_loop, args=(interval,), daemon=True)
    worker.start()
    app.run(host=host, port=port, threaded=True)


if __name__ == "__main__":
    main()
