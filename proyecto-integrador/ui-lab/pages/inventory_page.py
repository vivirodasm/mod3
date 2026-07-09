"""Page Object de la pantalla de inventario de SauceDemo.

Esta página aparece justo después del login exitoso.
Permite agregar productos al carrito e ir al carrito.
"""

from __future__ import annotations
from playwright.sync_api import Page


class InventoryPage:
    """Representa https://www.saucedemo.com/inventory.html."""

    URL = "https://www.saucedemo.com/inventory.html"

    def __init__(self, page: Page) -> None:
        self.page = page
        self._cart_badge = page.locator('.shopping_cart_badge')
        self._cart_link  = page.locator('.shopping_cart_link')

    # ── Acciones ──────────────────────────────────────────────────────────

    def add_to_cart(self, item_name: str) -> "InventoryPage":
        """Agrega al carrito el producto cuyo nombre coincide con item_name."""
        # Locator contextual: busca el botón dentro del ítem que tiene ese nombre.
        item_card = self.page.locator(
            f'.inventory_item:has-text("{item_name}")'
        )
        item_card.locator("button").click()
        return self

    def go_to_cart(self) -> None:
        """Hace clic en el ícono del carrito."""
        self._cart_link.click()

    # ── Consultas ─────────────────────────────────────────────────────────

    def is_loaded(self) -> bool:
        """True si la URL actual es la del inventario."""
        return self.page.url == self.URL

    def cart_count(self) -> int:
        """Número en la burbuja del carrito; 0 si está vacío."""
        if self._cart_badge.is_visible():
            return int(self._cart_badge.inner_text())
        return 0

    def item_names(self) -> list[str]:
        """Lista de nombres de todos los productos visibles en la página."""
        return self.page.locator('.inventory_item_name').all_inner_texts()
