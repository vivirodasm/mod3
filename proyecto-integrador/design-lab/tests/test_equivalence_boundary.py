"""Partición de equivalencias (Equivalence Partitioning, EP)
y análisis de valores límite (Boundary Value Analysis, BVA).

Cada id de parametrización coincide con la matriz de trazabilidad (TC-DSC-*).
"""

import pytest

from design_lab.discount import calculate_discount

# ── Particiones válidas (una muestra representativa por partición) ──────────

VALID_PARTITIONS = [
    pytest.param("standard", 500.0, False, 0.0, id="TC-DSC-EP-001-standard-base"),
    pytest.param("premium", 500.0, False, 10.0, id="TC-DSC-EP-002-premium-base"),
    pytest.param("standard", 500.0, True, 5.0, id="TC-DSC-EP-003-standard-cupon"),
    pytest.param("premium", 2000.0, False, 15.0, id="TC-DSC-EP-004-premium-volumen"),
]


@pytest.mark.parametrize(("customer_type", "order_total", "has_coupon", "expected"), VALID_PARTITIONS)
def test_valid_partitions(customer_type: str, order_total: float, has_coupon: bool, expected: float) -> None:
    assert calculate_discount(customer_type, order_total, has_coupon) == expected


# ── Valores límite del rango (0; 10000] y del umbral de volumen (1000) ──────

BOUNDARIES = [
    pytest.param(0.01, 0.0, id="TC-DSC-BVA-001-minimo-valido"),
    pytest.param(999.99, 0.0, id="TC-DSC-BVA-003-justo-bajo-umbral-volumen"),
    pytest.param(1000.00, 5.0, id="TC-DSC-BVA-004-umbral-volumen-exacto"),
    pytest.param(10_000.00, 5.0, id="TC-DSC-BVA-005-maximo-valido"),
]


@pytest.mark.parametrize(("order_total", "expected"), BOUNDARIES)
def test_boundary_values(order_total: float, expected: float) -> None:
    assert calculate_discount("standard", order_total, has_coupon=False) == expected


# ── Particiones inválidas (el código probado debe rechazarlas explícitamente) ─

INVALID_PARTITIONS = [
    pytest.param("standard", 0.0, id="TC-DSC-INV-001-total-cero"),
    pytest.param("standard", 10_000.01, id="TC-DSC-INV-002-sobre-maximo"),
    pytest.param("vip", 500.0, id="TC-DSC-INV-003-tipo-cliente-desconocido"),
    pytest.param("standard", -50.0, id="TC-DSC-INV-004-total-negativo"),
]


@pytest.mark.parametrize(("customer_type", "order_total"), INVALID_PARTITIONS)
def test_invalid_partitions_raise(customer_type: str, order_total: float) -> None:
    with pytest.raises(ValueError):
        calculate_discount(customer_type, order_total, has_coupon=False)
