"""Matriz pairwise con análisis de huecos (gap analysis) — REQ-MTX-001.

Limitación conocida: allpairspy con filter_func poda filas con su algoritmo
greedy y puede SACRIFICAR pares válidos (ej. quedó sin cubrir (chromium, macos)
porque macOS ya apareció emparejado con webkit). El patrón aplicado:

    generar → auditar cobertura de pares → complementar filas faltantes

Un par (vi, vj) solo es exigible si existe al menos una fila completa válida
que lo contenga (los pares imposibles por restricción no cuentan).
"""

from itertools import combinations, product
from typing import Callable

from allpairspy import AllPairs

Row = list
Validator = Callable[[Row], bool]


def generate_pairwise_matrix(parameters: list[list], is_valid: Validator) -> list[Row]:
    """Genera la matriz pairwise y la complementa hasta cubrir todos los pares exigibles."""
    matrix = [list(row) for row in AllPairs(parameters, filter_func=is_valid)]
    for i, vi, j, vj in missing_pairs(parameters, is_valid, matrix):
        if (vi, vj) in {(r[i], r[j]) for r in matrix}:
            continue  # un complemento previo ya lo cubrió
        row = _row_containing_pair(parameters, is_valid, i, vi, j, vj)
        if row is not None:
            matrix.append(row)
    return matrix


def missing_pairs(
    parameters: list[list], is_valid: Validator, matrix: list[Row]
) -> list[tuple[int, object, int, object]]:
    """Pares exigibles (alcanzables por alguna fila válida) que la matriz no cubre."""
    missing = []
    for i, j in combinations(range(len(parameters)), 2):
        seen = {(row[i], row[j]) for row in matrix}
        for vi, vj in product(parameters[i], parameters[j]):
            if (vi, vj) in seen:
                continue
            if _row_containing_pair(parameters, is_valid, i, vi, j, vj) is not None:
                missing.append((i, vi, j, vj))
    return missing


def _row_containing_pair(
    parameters: list[list], is_valid: Validator, i: int, vi: object, j: int, vj: object
) -> Row | None:
    """Primera fila completa válida que contiene el par, o None si es imposible."""
    for combo in product(*parameters):
        row = list(combo)
        if row[i] == vi and row[j] == vj and is_valid(row):
            return row
    return None
