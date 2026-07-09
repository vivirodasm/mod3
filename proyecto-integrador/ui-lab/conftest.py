"""conftest.py — Fixtures compartidas del laboratorio de UI.

Este archivo lo lee pytest automáticamente al arrancar.
Todo lo que defines aquí está disponible en TODOS los tests sin importar nada.

Qué hay aquí
------------
- authenticated_page : página con sesión ya iniciada (standard_user).
- users              : datos de usuarios cargados desde data/users.json.
- products           : datos de productos cargados desde data/products.yaml.
- cart_scenarios     : escenarios de carrito del mismo YAML.

Nota: los fixtures 'page', 'browser' y 'browser_context' los provee
pytest-playwright automáticamente — no hace falta redefinirlos.
"""

import json
import yaml
import pytest
from pathlib import Path
from pages.login_page import LoginPage

DATA_DIR = Path(__file__).parent / "data"


# ── Fixtures de dominio ────────────────────────────────────────────────────────

@pytest.fixture
def authenticated_page(page):
    """Fixture que devuelve una página con sesión iniciada como standard_user.

    Scope: 'function' (default) → cada test recibe una sesión fresca.
    Ventaja: los tests son independientes entre sí; uno no contamina al otro.
    """
    LoginPage(page).go_to().login("standard_user", "secret_sauce")
    yield page
    # pytest-playwright cierra el contexto/página después de yield.


# ── Fixtures de datos externos ─────────────────────────────────────────────────

@pytest.fixture(scope="session")
def users() -> dict:
    """Carga data/users.json una sola vez por sesión de pytest.

    Scope 'session': el archivo se lee una vez aunque lo usen 50 tests.
    Ideal para datos que no cambian entre tests.
    """
    return json.loads((DATA_DIR / "users.json").read_text(encoding="utf-8"))


@pytest.fixture(scope="session")
def products() -> list:
    """Carga la lista de productos desde data/products.yaml."""
    data = yaml.safe_load((DATA_DIR / "products.yaml").read_text(encoding="utf-8"))
    return data["products"]


@pytest.fixture(scope="session")
def cart_scenarios() -> list:
    """Carga los escenarios de carrito desde data/products.yaml."""
    data = yaml.safe_load((DATA_DIR / "products.yaml").read_text(encoding="utf-8"))
    return data["cart_scenarios"]
