"""Actor — núcleo del patrón Screenplay.

En Screenplay el "quién" y el "qué" están separados:
  - El Actor es QUIÉN realiza las acciones.
  - Las Abilities son LO QUE puede hacer (abrir el navegador, llamar una API…).
  - Las Tasks son CÓMO lo hace (pasos concretos compuestos de acciones).

Beneficio clave: los tests leen como especificaciones en inglés/español,
no como instrucciones de bajo nivel de la herramienta.

Comparación rápida:
  POM  → inventory.add_to_cart("Sauce Labs Backpack")
  Screenplay → carlos.attempts_to(AddToCart.the_item("Sauce Labs Backpack"))
"""

from __future__ import annotations
from typing import Any


class Actor:
    """Representa a un usuario en el sistema bajo prueba."""

    def __init__(self, name: str) -> None:
        self.name = name
        self._abilities: dict[str, Any] = {}

    # ── Construcción (fluent) ─────────────────────────────────────────────

    def can(self, ability: Any) -> "Actor":
        """Otorga una Ability al Actor. Retorna self para encadenar."""
        self._abilities[type(ability).__name__] = ability
        return self

    # ── Uso de Abilities ──────────────────────────────────────────────────

    def ability_to(self, ability_class: type) -> Any:
        """Recupera la Ability del tipo indicado.

        Lanza KeyError si el Actor no tiene esa Ability — señal de que
        falta un .can(...) en el setup del test.
        """
        key = ability_class.__name__
        if key not in self._abilities:
            raise KeyError(
                f"{self.name!r} no tiene la habilidad '{key}'. "
                f"¿Olvidaste actor.can({key}(...))?"
            )
        return self._abilities[key]

    # ── Ejecución de Tasks ────────────────────────────────────────────────

    def attempts_to(self, *tasks: Any) -> "Actor":
        """Ejecuta una o varias Tasks en orden. Retorna self."""
        for task in tasks:
            task.perform_as(self)
        return self

    def __repr__(self) -> str:
        abilities = list(self._abilities.keys())
        return f"Actor({self.name!r}, abilities={abilities})"
