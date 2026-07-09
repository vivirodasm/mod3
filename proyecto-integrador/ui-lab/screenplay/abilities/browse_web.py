"""Ability: BrowseTheWeb — le da al Actor acceso al navegador (Playwright).

Una Ability encapsula UNA herramienta externa.
Si mañana cambiamos de Playwright a Selenium, solo tocamos este archivo;
el Actor y las Tasks no se enteran.
"""

from __future__ import annotations
from playwright.sync_api import Page


class BrowseTheWeb:
    """Capacidad de interactuar con un navegador web via Playwright."""

    def __init__(self, page: Page) -> None:
        self._page = page

    @classmethod
    def using(cls, page: Page) -> "BrowseTheWeb":
        """Constructor expresivo para usar con actor.can(BrowseTheWeb.using(page))."""
        return cls(page)

    @property
    def page(self) -> Page:
        """La instancia de Page de Playwright que usa el Actor."""
        return self._page
