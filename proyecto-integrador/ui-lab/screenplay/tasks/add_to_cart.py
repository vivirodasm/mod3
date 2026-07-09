"""Task: AddToCart — agrega un producto al carrito desde el inventario."""

from __future__ import annotations
from screenplay.abilities.browse_web import BrowseTheWeb
from pages.inventory_page import InventoryPage


class AddToCart:
    """Tarea de alto nivel: agregar un producto al carrito de compras."""

    def __init__(self, item_name: str) -> None:
        self._item_name = item_name

    @classmethod
    def the_item(cls, item_name: str) -> "AddToCart":
        """Constructor expresivo: AddToCart.the_item('Sauce Labs Backpack')."""
        return cls(item_name)

    def perform_as(self, actor) -> None:
        page = actor.ability_to(BrowseTheWeb).page
        InventoryPage(page).add_to_cart(self._item_name)
