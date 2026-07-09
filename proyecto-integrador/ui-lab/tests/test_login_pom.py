"""Tests de login usando el patrón Page Object Model (POM).

Qué demuestra este archivo
--------------------------
1. POM en uso: LoginPage e InventoryPage son los únicos que conocen los locators.
2. DRY: el test no repite ningún selector; todo está en el Page Object.
3. Parametrize: varios casos de login inválido con una sola función de test.
4. Legibilidad: el test describe QUÉ pasa, no CÓMO lo hace el navegador.
"""

import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage


# ── Caso feliz ────────────────────────────────────────────────────────────────

def test_login_exitoso_redirige_al_inventario(page):
    """Un usuario válido debe llegar al inventario tras el login."""
    LoginPage(page).go_to().login("standard_user", "secret_sauce")
    assert InventoryPage(page).is_loaded(), (
        "Se esperaba estar en /inventory.html después del login exitoso."
    )


def test_inventario_muestra_productos(page):
    """El inventario debe listar al menos un producto tras el login."""
    LoginPage(page).go_to().login("standard_user", "secret_sauce")
    nombres = InventoryPage(page).item_names()
    assert len(nombres) > 0, "El inventario no debería estar vacío."


# ── Casos inválidos (parametrize) ─────────────────────────────────────────────

INVALID_LOGIN_CASES = [
    pytest.param(
        "locked_out_user", "secret_sauce",
        "Sorry, this user has been locked out.",
        id="usuario_bloqueado",
    ),
    pytest.param(
        "", "secret_sauce",
        "Username is required",
        id="username_vacio",
    ),
    pytest.param(
        "standard_user", "",
        "Password is required",
        id="password_vacio",
    ),
    pytest.param(
        "usuario_inventado", "clave_incorrecta",
        "Username and password do not match",
        id="credenciales_incorrectas",
    ),
]


@pytest.mark.parametrize("username,password,expected_error", INVALID_LOGIN_CASES)
def test_login_invalido_muestra_error(page, username, password, expected_error):
    """Cada credencial inválida debe mostrar el mensaje de error correcto."""
    login = LoginPage(page)
    login.go_to().login(username, password)

    assert login.has_error(), "Se esperaba un mensaje de error visible."
    assert expected_error in login.error_message(), (
        f"Error esperado: '{expected_error}'\n"
        f"Error obtenido: '{login.error_message()}'"
    )
