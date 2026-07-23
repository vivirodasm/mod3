"""Tests for precision, bias proxy and drift checks."""

from __future__ import annotations

from pathlib import Path

from src.generate_data import build_clean_current, build_reference
from src.model_checks import train_and_evaluate


def test_model_pipeline_passes_thresholds(tmp_path: Path):
    report = train_and_evaluate(
        build_reference(),
        build_clean_current(),
        tracking_uri=str(tmp_path / "mlruns"),
    )
    assert report.precision >= 0.70
    assert report.max_region_gap <= 0.25
    assert report.income_drift_psi <= 0.25
    assert report.passed is True
