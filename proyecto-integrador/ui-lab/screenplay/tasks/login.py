"""Task: Login — inicia sesión en SauceDemo usando el Page Object de login.

Las Tasks reutilizan los Page Objects: no duplican lógica,
solo orquestan los pasos desde la perspectiva del Actor.
"""

from __future__ import annotations
from screenplay.abilities.browse_web import BrowseTheWeb
from pages.login_page import LoginPage


class Login:
    """Tarea de alto nivel: iniciar sesión en la aplicación."""

    def __init__(self, username: str, password: str) -> None:
        self._username = username
        self._password = password

    @classmethod
    def as_user(cls, username: str, password: str) -> "Login":
        """Constructor expresivo: Login.as_user('standard_user', 'secret_sauce')."""
        return cls(username, password)

    def perform_as(self, actor) -> None:
        """Ejecuta la tarea usando las Abilities del Actor."""
        page = actor.ability_to(BrowseTheWeb).page
        LoginPage(page).go_to().login(self._username, self._password)
