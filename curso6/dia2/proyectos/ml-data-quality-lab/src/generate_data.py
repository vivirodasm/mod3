"""Generate synthetic ETL datasets for quality and drift labs."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = Path(__import__("os").environ.get("DATA_DIR", ROOT / "data"))


def build_reference(n: int = 400, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    ages = rng.integers(18, 70, size=n)
    incomes = rng.normal(45000, 12000, size=n).clip(15000, 120000)
    regions = rng.choice(["north", "south", "east", "west"], size=n)
    # Label: approve credit if income/age heuristic holds
    score = (incomes / 1000) - (ages * 0.2) + rng.normal(0, 2, size=n)
    approved = (score > 30).astype(int)
    return pd.DataFrame(
        {
            "customer_id": [f"C{i:05d}" for i in range(n)],
            "age": ages,
            "income": incomes.round(2),
            "region": regions,
            "email": [f"user{i}@example.com" for i in range(n)],
            "approved": approved,
        }
    )


def build_current_with_issues(n: int = 200, seed: int = 7) -> pd.DataFrame:
    """Current batch with nulls, duplicates and mild drift for demos."""
    rng = np.random.default_rng(seed)
    base = build_reference(n=n, seed=seed)
    # Drift: incomes shift upward
    base["income"] = (base["income"] * 1.15).round(2)
    # Inject quality issues
    dirty = base.copy()
    dirty.loc[0:4, "email"] = None
    dirty.loc[5:7, "age"] = None
    dirty = pd.concat([dirty, dirty.iloc[[10, 11]]], ignore_index=True)
    dirty.loc[12, "region"] = "unknown_zone"
    dirty.loc[13, "income"] = -100
    return dirty


def build_clean_current(n: int = 200, seed: int = 99) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    ages = rng.integers(18, 70, size=n)
    incomes = rng.normal(46000, 11000, size=n).clip(15000, 120000)
    regions = rng.choice(["north", "south", "east", "west"], size=n)
    score = (incomes / 1000) - (ages * 0.2) + rng.normal(0, 2, size=n)
    approved = (score > 30).astype(int)
    return pd.DataFrame(
        {
            "customer_id": [f"N{i:05d}" for i in range(n)],
            "age": ages,
            "income": incomes.round(2),
            "region": regions,
            "email": [f"new{i}@example.com" for i in range(n)],
            "approved": approved,
        }
    )


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    build_reference().to_csv(DATA_DIR / "reference.csv", index=False)
    build_clean_current().to_csv(DATA_DIR / "current_clean.csv", index=False)
    build_current_with_issues().to_csv(DATA_DIR / "current_dirty.csv", index=False)
    print(f"Datasets escritos en {DATA_DIR}")


if __name__ == "__main__":
    main()
