"""Pruebas combinatorias — reducción pairwise de la matriz cross-browser.

Problema real: 3 navegadores × 3 SO × 2 idiomas × 3 roles = 54 combinaciones.
Pairwise cubre cada PAR de valores al menos una vez con una fracción del costo
(REQ-MTX-001).

Lección clave: allpairspy con restricciones NO garantiza todos los pares
(su poda greedy dejó fuera (chromium, macos) y (firefox, macos) en este mismo
dataset). Por eso el módulo design_lab.pairwise_matrix audita y complementa:
nunca asumas la garantía de la herramienta — demuéstrala con un test.
"""

from design_lab.pairwise_matrix import generate_pairwise_matrix, missing_pairs

BROWSERS = ["chromium", "firefox", "webkit"]
OPERATING_SYSTEMS = ["ubuntu", "windows", "macos"]
LANGUAGES = ["es", "en"]
ROLES = ["standard", "premium", "admin"]

PARAMETERS = [BROWSERS, OPERATING_SYSTEMS, LANGUAGES, ROLES]
FULL_CARTESIAN = 3 * 3 * 2 * 3  # 54


def is_valid_combination(row: list) -> bool:
    """Restricción de negocio: webkit (Safari engine) solo corre en macOS."""
    if len(row) >= 2 and row[0] == "webkit" and row[1] != "macos":
        return False
    return True


def test_pairwise_reduces_cartesian_product() -> None:
    matrix = generate_pairwise_matrix(PARAMETERS, is_valid_combination)
    assert 0 < len(matrix) < FULL_CARTESIAN


def test_pairwise_respects_constraints() -> None:
    for row in generate_pairwise_matrix(PARAMETERS, is_valid_combination):
        assert is_valid_combination(row), f"Combinación inválida generada: {row}"


def test_pairwise_covers_every_achievable_pair() -> None:
    """Gap analysis: tras complementar, no queda ningún par exigible sin cubrir."""
    matrix = generate_pairwise_matrix(PARAMETERS, is_valid_combination)
    gaps = missing_pairs(PARAMETERS, is_valid_combination, matrix)
    assert gaps == [], f"Pares sin cubrir: {gaps}"


def test_impossible_pairs_are_not_required() -> None:
    """(webkit, ubuntu) y (webkit, windows) son imposibles por restricción."""
    matrix = generate_pairwise_matrix(PARAMETERS, is_valid_combination)
    seen = {(row[0], row[1]) for row in matrix}
    assert ("webkit", "ubuntu") not in seen
    assert ("webkit", "windows") not in seen
