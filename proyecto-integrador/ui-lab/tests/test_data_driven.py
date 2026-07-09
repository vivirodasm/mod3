"""Tests data-driven: datos cargados desde JSON y YAML.

Qué demuestra este archivo
--------------------------
1. Carga de JSON en tiempo de colección (parametrize + función de carga).
2. Uso de fixtures de datos (users, cart_scenarios) definidas en conftest.py.
3. Principio de separación de datos y lógica: agregar un nuevo caso de test
   es solo agregar una línea en el archivo JSON o YAML.

Diferencia entre los dos enfoques de parametrize
-------------------------------------------------
A) load_invalid_users() se llama en tiempo de colección (antes de que pytest
   inicie los navegadores). Útil cuando quieres ver los IDs de test en la
   salida sin arrancar ningún recurso pesado.

B) El fixture 'cart_scenarios' se inyecta en el test — los datos se resuelven
   justo antes de que el test comience. Útil para datos que dependen de otros
   fixtures o de estado externo.
"""

import json
import pytest
from pathlib import Path
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage

DATA_DIR = Path(__file__).parent.parent / "data"


# ── Enfoque A: carga en tiempo de colección ────────────────────────────────────

def _load_invalid_users():
    """Lee data/users.json y devuelve una lista de pytest.param para parametrize."""
    data = json.loads((DATA_DIR / "users.json").read_text(encoding="utf-8"))
    return [
        pytest.param(
            u["username"],
            u["password"],
            u["expected_error"],
            id=u["username"] or "username_vacio",
        )
        for u in data["invalid_users"]
    ]


@pytest.mark.parametrize("username,password,expected_error", _load_invalid_users())
def test_login_invalido_desde_json(page, username, password, expected_error):
    """Cada usuario inválido del JSON debe mostrar el error correcto."""
    login = LoginPage(page)
    login.go_to().login(username, password)
    assert expected_error in login.error_message()


# ── Enfoque B: escenarios de carrito desde YAML (via fixture) ──────────────────

@pytest.mark.parametrize("scenario_idx", [0, 1, 2])
def test_carrito_desde_yaml(authenticated_page, cart_scenarios, scenario_idx):
    """Verifica que la burbuja del carrito refleja el número correcto de productos.

    Se parametriza por índice para poder usar el fixture cart_scenarios
    (que se carga desde YAML en conftest.py) y al mismo tiempo tener
    tests nombrados individualmente en el reporte.
    """
    scenario = cart_scenarios[scenario_idx]
    inventory = InventoryPage(authenticated_page)

    for item_name in scenario["items"]:
        inventory.add_to_cart(item_name)

    assert inventory.cart_count() == scenario["count"], (
        f"Escenario '{scenario['description']}': "
        f"se esperaban {scenario['count']} ítems en el carrito."
    )
