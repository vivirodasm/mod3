"""Pruebas basadas en decisión — tabla completa cargada desde YAML.

Demuestra separación lógica/datos (mantenibilidad: desacoplamiento).
La tabla vive en data/decision_table.yaml; este archivo solo contiene lógica.
"""

from pathlib import Path

import pytest
import yaml

from design_lab.discount import calculate_discount

TABLE_PATH = Path(__file__).parent.parent / "data" / "decision_table.yaml"


def load_rules() -> list[pytest.param]:
    rules = yaml.safe_load(TABLE_PATH.read_text(encoding="utf-8"))["rules"]
    return [
        pytest.param(
            r["customer_type"], r["order_total"], r["has_coupon"], r["expected"], id=f"TC-{r['id']}"
        )
        for r in rules
    ]


@pytest.mark.parametrize(("customer_type", "order_total", "has_coupon", "expected"), load_rules())
def test_decision_table(customer_type: str, order_total: float, has_coupon: bool, expected: float) -> None:
    assert calculate_discount(customer_type, order_total, has_coupon) == expected


def test_decision_table_is_complete() -> None:
    """Guardrail: la tabla debe cubrir las 2^3 combinaciones de condiciones."""
    rules = yaml.safe_load(TABLE_PATH.read_text(encoding="utf-8"))["rules"]
    combos = {(r["customer_type"], r["order_total"] >= 1000, r["has_coupon"]) for r in rules}
    assert len(combos) == 8, "Faltan reglas en la tabla de decisión"
