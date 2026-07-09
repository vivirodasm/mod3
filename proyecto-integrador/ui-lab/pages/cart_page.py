"""Page Object de la pantalla del carrito de SauceDemo."""

from __future__ import annotations
from playwright.sync_api import Page


class CartPage:
    """Representa https://www.saucedemo.com/cart.html."""

    URL = "https://www.saucedemo.com/cart.html"

    def __init__(self, page: Page) -> None:
        self.page = page
        self._items       = page.locator('.cart_item')
        self._checkout_btn = page.locator('[data-test="checkout"]')
        self._continue_btn = page.locator('[data-test="continue-shopping"]')

    # ── Acciones ──────────────────────────────────────────────────────────

    def proceed_to_checkout(self) -> None:
        """Hace clic en el botón 'Checkout'."""
        self._checkout_btn.click()

    def continue_shopping(self) -> None:
        """Regresa al inventario sin comprar."""
        self._continue_btn.click()

    # ── Consultas ─────────────────────────────────────────────────────────

    def is_loaded(self) -> bool:
        return self.page.url == self.URL

    def item_count(self) -> int:
        """Número de ítems distintos en el carrito."""
        return self._items.count()

    def item_names(self) -> list[str]:
        """Nombres de todos los productos en el carrito."""
        return self._items.locator('.inventory_item_name').all_inner_texts()

    def contains(self, item_name: str) -> bool:
        """True si el producto con ese nombre está en el carrito."""
        return item_name in self.item_names()
