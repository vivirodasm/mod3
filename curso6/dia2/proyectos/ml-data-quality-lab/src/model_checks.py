"""Model validation: precision, bias/fairness proxy and data drift."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import mlflow
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

FEATURES = ["age", "income", "region"]
TARGET = "approved"


@dataclass
class ModelReport:
    precision: float
    max_region_gap: float
    income_drift_psi: float
    passed: bool


def _psi(expected: np.ndarray, actual: np.ndarray, buckets: int = 10) -> float:
    """Population Stability Index between two numeric distributions."""
    quantiles = np.linspace(0, 1, buckets + 1)
    breakpoints = np.unique(np.quantile(expected, quantiles))
    if len(breakpoints) < 3:
        return 0.0
    expected_counts = np.histogram(expected, bins=breakpoints)[0].astype(float)
    actual_counts = np.histogram(actual, bins=breakpoints)[0].astype(float)
    expected_perc = (expected_counts + 1e-6) / (expected_counts.sum() + 1e-6 * len(expected_counts))
    actual_perc = (actual_counts + 1e-6) / (actual_counts.sum() + 1e-6 * len(actual_counts))
    return float(np.sum((actual_perc - expected_perc) * np.log(actual_perc / expected_perc)))


def train_and_evaluate(
    reference: pd.DataFrame,
    current: pd.DataFrame,
    *,
    min_precision: float = 0.70,
    max_region_gap: float = 0.25,
    max_psi: float = 0.25,
    tracking_uri: str | None = None,
) -> ModelReport:
    x = reference[FEATURES]
    y = reference[TARGET]
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.25, random_state=42, stratify=y
    )

    preprocess = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), ["age", "income"]),
            ("cat", OneHotEncoder(handle_unknown="ignore"), ["region"]),
        ]
    )
    model = Pipeline(
        steps=[
            ("prep", preprocess),
            ("clf", LogisticRegression(max_iter=500)),
        ]
    )
    model.fit(x_train, y_train)
    preds = model.predict(x_test)
    precision = float(precision_score(y_test, preds, zero_division=0))

    # Fairness proxy: max gap in approval rate across regions on predictions
    eval_frame = x_test.copy()
    eval_frame["pred"] = preds
    rates = eval_frame.groupby("region")["pred"].mean()
    gap = float(rates.max() - rates.min()) if len(rates) else 0.0

    psi = _psi(reference["income"].to_numpy(), current["income"].to_numpy())

    passed = precision >= min_precision and gap <= max_region_gap and psi <= max_psi

    if tracking_uri is None:
        tracking_dir = Path(__file__).resolve().parents[1] / "mlruns"
    else:
        tracking_dir = Path(tracking_uri)
    tracking_dir.mkdir(parents=True, exist_ok=True)
    # sqlite backend is portable on Windows/macOS and supported by current MLflow
    db_path = (tracking_dir / "mlflow.db").resolve().as_posix()
    mlflow.set_tracking_uri(f"sqlite:///{db_path}")
    mlflow.set_experiment("curso6-ml-quality")
    with mlflow.start_run(run_name="credit-approval-lab"):
        mlflow.log_params(
            {
                "model": "LogisticRegression",
                "min_precision": min_precision,
                "max_region_gap": max_region_gap,
                "max_psi": max_psi,
            }
        )
        mlflow.log_metrics(
            {
                "precision": precision,
                "max_region_gap": gap,
                "income_drift_psi": psi,
                "passed": float(passed),
            }
        )

    return ModelReport(
        precision=precision,
        max_region_gap=gap,
        income_drift_psi=psi,
        passed=passed,
    )
