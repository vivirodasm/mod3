"""Page Object de la pantalla de login de SauceDemo.

Por qué existe este archivo
---------------------------
Sin POM, cada test copia sus propios locators:
  page.locator('[data-test="username"]').fill("...")
  page.locator('[data-test="login-button"]').click()

Si SauceDemo cambia el atributo de ese botón, tienes que buscar y
reemplazar en TODOS los tests. Con este Page Object, lo cambias aquí
y todos los tests se benefician automáticamente.

Principio DRY en acción: un solo lugar de verdad por locator.
"""

from __future__ import annotations
from playwright.sync_api import Page


class LoginPage:
    """Representa la pantalla de login de https://www.saucedemo.com."""

    BASE_URL = "https://www.saucedemo.com"

    def __init__(self, page: Page) -> None:
        self.page = page

        # ── Locators: definidos UNA SOLA VEZ ──────────────────────────────
        # Usamos data-test porque son los atributos más estables de la app.
        # Si cambia el HTML pero no el atributo, el test sigue funcionando.
        self._username  = page.locator('[data-test="username"]')
        self._password  = page.locator('[data-test="password"]')
        self._login_btn = page.locator('[data-test="login-button"]')
        self._error_msg = page.locator('[data-test="error"]')

    # ── Acciones ──────────────────────────────────────────────────────────

    def go_to(self) -> "LoginPage":
        """Navega a la URL de login y devuelve self (interfaz fluida)."""
        self.page.goto(self.BASE_URL)
        return self

    def login(self, username: str, password: str) -> "LoginPage":
        """Rellena el formulario y hace clic en el botón de login."""
        self._username.fill(username)
        self._password.fill(password)
        self._login_btn.click()
        return self

    # ── Consultas (state) ─────────────────────────────────────────────────

    def error_message(self) -> str:
        """Texto del mensaje de error visible tras un login fallido."""
        return self._error_msg.inner_text()

    def has_error(self) -> bool:
        """True si hay un mensaje de error visible en pantalla."""
        return self._error_msg.is_visible()
