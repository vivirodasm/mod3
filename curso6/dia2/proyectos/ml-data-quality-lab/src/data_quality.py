"""Data quality checks inspired by Great Expectations patterns."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

ALLOWED_REGIONS = {"north", "south", "east", "west"}


@dataclass
class ExpectationResult:
    expectation: str
    success: bool
    details: str


def expect_column_values_not_null(df: pd.DataFrame, column: str) -> ExpectationResult:
    nulls = int(df[column].isna().sum())
    return ExpectationResult(
        expectation=f"expect_column_values_to_not_be_null:{column}",
        success=nulls == 0,
        details=f"null_count={nulls}",
    )


def expect_column_values_unique(df: pd.DataFrame, column: str) -> ExpectationResult:
    dupes = int(df[column].duplicated().sum())
    return ExpectationResult(
        expectation=f"expect_column_values_to_be_unique:{column}",
        success=dupes == 0,
        details=f"duplicate_count={dupes}",
    )


def expect_column_values_in_set(
    df: pd.DataFrame, column: str, allowed: set[str]
) -> ExpectationResult:
    invalid = sorted(set(df[column].dropna().astype(str)) - allowed)
    return ExpectationResult(
        expectation=f"expect_column_values_to_be_in_set:{column}",
        success=len(invalid) == 0,
        details=f"invalid={invalid}",
    )


def expect_column_values_between(
    df: pd.DataFrame, column: str, min_value: float, max_value: float
) -> ExpectationResult:
    series = pd.to_numeric(df[column], errors="coerce")
    out_of_range = int(((series < min_value) | (series > max_value)).sum())
    return ExpectationResult(
        expectation=f"expect_column_values_to_be_between:{column}",
        success=out_of_range == 0,
        details=f"out_of_range={out_of_range}",
    )


def expect_email_format(df: pd.DataFrame, column: str = "email") -> ExpectationResult:
    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    series = df[column].dropna().astype(str)
    bad = int((~series.str.match(pattern)).sum())
    return ExpectationResult(
        expectation=f"expect_column_values_to_match_regex:{column}",
        success=bad == 0,
        details=f"invalid_format={bad}",
    )


def run_etl_suite(df: pd.DataFrame) -> list[ExpectationResult]:
    """Suite de integridad ETL: nulos, duplicados, formatos y rangos."""
    return [
        expect_column_values_not_null(df, "customer_id"),
        expect_column_values_not_null(df, "age"),
        expect_column_values_not_null(df, "email"),
        expect_column_values_unique(df, "customer_id"),
        expect_column_values_in_set(df, "region", ALLOWED_REGIONS),
        expect_column_values_between(df, "age", 18, 100),
        expect_column_values_between(df, "income", 0, 500000),
        expect_email_format(df, "email"),
    ]


def suite_passed(results: list[ExpectationResult]) -> bool:
    return all(r.success for r in results)
