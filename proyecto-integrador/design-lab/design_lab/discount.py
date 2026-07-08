"""Regla de negocio de checkout (REQ-DSC-001..005).

Código simple: permite practicar EP, BVA y tablas de decisión sin depender de UI.
Trazable en proyecto-integrador/trazabilidad/matriz-trazabilidad.csv.
"""

VALID_CUSTOMER_TYPES = frozenset({"standard", "premium"})
MIN_ORDER_EXCLUSIVE = 0.0
MAX_ORDER_INCLUSIVE = 10_000.0
VOLUME_THRESHOLD = 1_000.0
DISCOUNT_CAP = 15.0


def calculate_discount(customer_type: str, order_total: float, has_coupon: bool) -> float:
    """Devuelve el porcentaje de descuento aplicable a un pedido.

    Reglas de negocio:
      REQ-DSC-001: premium → +10 ; standard → +0
      REQ-DSC-002: order_total >= 1000 → +5 (bono por volumen)
      REQ-DSC-003: has_coupon → +5
      REQ-DSC-004: el descuento total nunca excede 15
      REQ-DSC-005: 0 < order_total <= 10000; de lo contrario ValueError
    """
    if customer_type not in VALID_CUSTOMER_TYPES:
        raise ValueError(f"customer_type inválido: {customer_type!r}")
    if not MIN_ORDER_EXCLUSIVE < order_total <= MAX_ORDER_INCLUSIVE:
        raise ValueError(f"order_total fuera de rango (0; 10000]: {order_total}")

    discount = 10.0 if customer_type == "premium" else 0.0
    if order_total >= VOLUME_THRESHOLD:
        discount += 5.0
    if has_coupon:
        discount += 5.0
    return min(discount, DISCOUNT_CAP)
