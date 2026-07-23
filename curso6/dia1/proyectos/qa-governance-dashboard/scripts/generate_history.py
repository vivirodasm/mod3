"""Generate ~3 days of OpenMetrics history for Prometheus backfill."""

from __future__ import annotations

import math
import random
from pathlib import Path

SERVICES = {
    "auth": {"flake": 0.04, "leakage": 0.08, "effectiveness": 0.92, "coverage": 78.0},
    "payments": {"flake": 0.11, "leakage": 0.16, "effectiveness": 0.82, "coverage": 68.0},
    "catalog": {"flake": 0.03, "leakage": 0.05, "effectiveness": 0.95, "coverage": 88.0},
    "notifications": {"flake": 0.14, "leakage": 0.19, "effectiveness": 0.80, "coverage": 62.0},
}

# Labels must match live scrape for continuous series in Grafana.
EXTRA_LABELS = 'env="lab",instance="exporter:8000",job="qa-governance-exporter"'

DAYS = 3
STEP_SECONDS = 300  # 5 minutos


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def main() -> None:
    rng = random.Random(42)
    out = Path(__file__).resolve().parents[1] / "prometheus" / "seed" / "history.om"
    out.parent.mkdir(parents=True, exist_ok=True)

    # promtool (v2.55) interpreta el timestamp de OpenMetrics como segundos unix
    # (aunque el spec hable de ms). Usamos segundos para obtener ~3 días reales.
    now_s = int(__import__("time").time())
    start_s = now_s - DAYS * 24 * 60 * 60
    step_s = STEP_SECONDS

    lines: list[str] = [
        "# HELP qa_flake_rate Proportion of flaky tests over total executed (0-1)",
        "# TYPE qa_flake_rate gauge",
        "# HELP qa_defect_leakage Defects found in production over total defects (0-1)",
        "# TYPE qa_defect_leakage gauge",
        "# HELP qa_test_effectiveness_ratio Defects caught in test over total defects (0-1)",
        "# TYPE qa_test_effectiveness_ratio gauge",
        "# HELP qa_coverage Automated test coverage percentage (0-100)",
        "# TYPE qa_coverage gauge",
    ]

    t = start_s
    point = 0
    while t <= now_s:
        # Ligera tendencia diaria para que el gráfico de 3 días se vea “vivo”
        day_wave = 0.01 * math.sin(point / 50.0)
        for service, base in SERVICES.items():
            flake = clamp(base["flake"] + day_wave + rng.uniform(-0.015, 0.02), 0.0, 1.0)
            leakage = clamp(base["leakage"] + day_wave + rng.uniform(-0.02, 0.03), 0.0, 1.0)
            effectiveness = clamp(
                base["effectiveness"] + rng.uniform(-0.015, 0.015), 0.0, 1.0
            )
            coverage = clamp(base["coverage"] + rng.uniform(-3.0, 3.0), 0.0, 100.0)
            labels = f'service="{service}",{EXTRA_LABELS}'
            lines.append(f"qa_flake_rate{{{labels}}} {flake:.6f} {t}")
            lines.append(f"qa_defect_leakage{{{labels}}} {leakage:.6f} {t}")
            lines.append(f"qa_test_effectiveness_ratio{{{labels}}} {effectiveness:.6f} {t}")
            lines.append(f"qa_coverage{{{labels}}} {coverage:.6f} {t}")
        t += step_s
        point += 1

    # OpenMetrics EOF marker required by promtool
    lines.append("# EOF")
    # LF only: promtool en Linux falla con CRLF de Windows.
    out.write_bytes(("\n".join(lines) + "\n").encode("utf-8"))
    print(f"Wrote {out} ({point} timestamps x {len(SERVICES)} services)")


if __name__ == "__main__":
    main()
