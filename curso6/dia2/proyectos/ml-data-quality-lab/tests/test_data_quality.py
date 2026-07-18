"""Tests for ETL integrity suite (patrón Great Expectations)."""

from __future__ import annotations

from src.data_quality import run_etl_suite, suite_passed
from src.generate_data import build_clean_current, build_current_with_issues, build_reference


def test_reference_dataset_passes_etl_suite():
    results = run_etl_suite(build_reference())
    assert suite_passed(results), [r for r in results if not r.success]


def test_clean_current_passes_etl_suite():
    results = run_etl_suite(build_clean_current())
    assert suite_passed(results), [r for r in results if not r.success]


def test_dirty_current_fails_etl_suite():
    results = run_etl_suite(build_current_with_issues())
    assert not suite_passed(results)
    failed = {r.expectation for r in results if not r.success}
    assert any("not_be_null" in name for name in failed)
    assert any("unique" in name for name in failed)
