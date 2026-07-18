"""Validación con Great Expectations (API ephemeral) sobre el dataset limpio."""

from __future__ import annotations

import pandas as pd
import pytest

from src.generate_data import build_clean_current

gx = pytest.importorskip("great_expectations")


def test_great_expectations_basic_suite():
    df = build_clean_current()
    context = gx.get_context(mode="ephemeral")
    data_source = context.data_sources.add_pandas("pandas_source")
    data_asset = data_source.add_dataframe_asset(name="customers")
    batch_definition = data_asset.add_batch_definition_whole_dataframe("whole")
    batch = batch_definition.get_batch(batch_parameters={"dataframe": df})

    suite = context.suites.add(gx.ExpectationSuite(name="customers_suite"))
    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToNotBeNull(column="customer_id")
    )
    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToBeUnique(column="customer_id")
    )
    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToBeBetween(
            column="age", min_value=18, max_value=100
        )
    )
    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToBeInSet(
            column="region",
            value_set=["north", "south", "east", "west"],
        )
    )

    validation = batch.validate(suite)
    assert validation.success is True
    assert isinstance(df, pd.DataFrame)
