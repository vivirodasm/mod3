"""End-to-end lab pipeline: generate data, validate ETL, evaluate model."""

from __future__ import annotations

import json
from pathlib import Path

from src.data_quality import run_etl_suite, suite_passed
from src.generate_data import build_clean_current, build_reference, main as generate_main
from src.model_checks import train_and_evaluate


def main() -> None:
    generate_main()
    root = Path(__file__).resolve().parents[1]
    data_dir = root / "data"

    reference = build_reference()
    current = build_clean_current()
    # Persist for GE-style inspection
    reference.to_csv(data_dir / "reference.csv", index=False)
    current.to_csv(data_dir / "current_clean.csv", index=False)

    etl_results = run_etl_suite(current)
    etl_ok = suite_passed(etl_results)
    report = train_and_evaluate(reference, current)

    summary = {
        "etl_passed": etl_ok,
        "etl_results": [r.__dict__ for r in etl_results],
        "model": {
            "precision": report.precision,
            "max_region_gap": report.max_region_gap,
            "income_drift_psi": report.income_drift_psi,
            "passed": report.passed,
        },
        "overall_passed": etl_ok and report.passed,
    }
    out = data_dir / "pipeline_report.json"
    out.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    if not summary["overall_passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
