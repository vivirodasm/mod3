# Sesión 2 — Desarrollo de Scripts: POM, Screenplay y Data-Driven Testing

> **Duración:** 3 horas · **Ritmo:** Bloque A (45 min) → descanso 15 min → Bloque B (45 min) → descanso 15 min → Bloque C (45 min) → salida
> **Lo que vas a construir:** una suite de pruebas de interfaz de usuario sobre SauceDemo usando Page Object Model, Screenplay, fixtures avanzadas y datos externos en JSON y YAML.

---

## Antes de empezar

Necesitas tener instalado `uv` (lo vimos en la Sesión 1). Luego:

```bash
# Desde la raíz del curso
cd proyecto-integrador/ui-lab

# 1. Instala las dependencias Python del laboratorio
uv sync --group dev

# 2. Descarga el navegador Chromium (solo la primera vez; ~150 MB)
uv run playwright install chromium

# 3. Verifica que todo funciona
uv run pytest --collect-only
```

Deberías ver los 13 tests listados sin errores de importación.
Si algo falla aquí, detente y revisa el error antes de continuar.

---

## Bloque A — El problema del código espagueti (45 min)

### El punto de partida: qué pasa sin patrones

Imagina que escribes tu primer test de login sin ningún patrón. Funciona.
Luego escribes el segundo. Luego el tercero. Al cabo de una semana tienes esto:

```python
# ❌ Código espagueti — NO hagas esto
def test_login():
    page.goto("https://www.saucedemo.com")
    page.locator('[data-test="username"]').fill("standard_user")
    page.locator('[data-test="password"]').fill("secret_sauce")
    page.locator('[data-test="login-button"]').click()
    assert page.url == "https://www.saucedemo.com/inventory.html"

def test_agregar_producto():
    page.goto("https://www.saucedemo.com")
    page.locator('[data-test="username"]').fill("standard_user")   # copia
    page.locator('[data-test="password"]').fill("secret_sauce")    # copia
    page.locator('[data-test="login-button"]').click()             # copia
    page.locator('.inventory_item:has-text("Sauce Labs Backpack")').locator("button").click()
    assert page.locator('.shopping_cart_badge').inner_text() == "1"
```

Ahora SauceDemo cambia `data-test="login-button"` a `data-test="submit-btn"`.
Tienes que buscar ese string en **todos** tus archivos de test. Si tienes 40 tests… éxito.

---

### La solución: Page Object Model (POM)

**Idea central:** cada pantalla de la aplicación tiene un solo archivo Python
que conoce todos sus locators y acciones. Los tests solo llaman métodos.

Abre el archivo `pages/login_page.py`. Esto es lo que verás:

```python
class LoginPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self._username  = page.locator('[data-test="username"]')
        self._password  = page.locator('[data-test="password"]')
        self._login_btn = page.locator('[data-test="login-button"]')
        self._error_msg = page.locator('[data-test="error"]')

    def go_to(self) -> "LoginPage":
        self.page.goto("https://www.saucedemo.com")
        return self          # ← devuelve self para encadenar: .go_to().login(...)

    def login(self, username: str, password: str) -> "LoginPage":
        self._username.fill(username)
        self._password.fill(password)
        self._login_btn.click()
        return self

    def error_message(self) -> str:
        return self._error_msg.inner_text()
```

Ahora el test queda así:

```python
# ✅ Con POM: limpio, DRY, sin locators expuestos
def test_login_exitoso(page):
    LoginPage(page).go_to().login("standard_user", "secret_sauce")
    assert InventoryPage(page).is_loaded()
```

Si cambia el locator del botón → solo tocas `login_page.py`. Todos los tests se benefician.

**Abre también:** `pages/inventory_page.py` y `pages/cart_page.py`.
Sigue la misma estructura: locators privados, métodos públicos con nombres de negocio.

---

### Lleva el POM más lejos: Screenplay

POM resuelve el problema del mantenimiento de locators.
Screenplay resuelve el problema de la **legibilidad de intención**.

**El modelo mental de Screenplay:**

| Concepto | Qué es | Archivo |
|---|---|---|
| **Actor** | Quién realiza las acciones | `screenplay/actor.py` |
| **Ability** | Qué herramienta usa el Actor | `screenplay/abilities/browse_web.py` |
| **Task** | Qué intenta hacer (en términos de negocio) | `screenplay/tasks/login.py` |

Un test con Screenplay se lee así:

```python
def test_actor_inicia_sesion(page):
    carlos = Actor("Carlos").can(BrowseTheWeb.using(page))
    carlos.attempts_to(
        Login.as_user("standard_user", "secret_sauce"),
        AddToCart.the_item("Sauce Labs Backpack"),
    )
    assert InventoryPage(page).cart_count() == 1
```

Cada línea es una oración en español. Cualquier persona del equipo entiende qué hace este test sin saber nada de Playwright.

Abre `screenplay/actor.py` y lee el método `attempts_to`. Luego abre `screenplay/tasks/login.py` y observa cómo la Task usa el Page Object internamente — no duplica nada.

---

### DRY y KISS: los dos principios que unifican todo

- **DRY** (*Don't Repeat Yourself*): si escribes lo mismo dos veces, algo está mal. Los locators van en el Page Object una sola vez.
- **KISS** (*Keep It Simple, Stupid*): la solución más simple que funciona es la correcta. Si POM resuelve tu problema, no necesitas Screenplay.

**Regla práctica:**
- Suite pequeña con un solo rol de usuario → **POM es suficiente**.
- Suite con múltiples roles o flujos complejos de negocio → **Screenplay clarifica la intención**.

---

## Bloque B — Laboratorio guiado (45 min)

### Lab 1: corre los tests base y léelos

```bash
# Desde proyecto-integrador/ui-lab
uv run pytest tests/test_login_pom.py -v
```

Deberías ver 6 tests pasando. Mientras corren, abre `tests/test_login_pom.py` y sigue el flujo: el test llama `LoginPage`, que llama el locator, que interactúa con el navegador.

```bash
# Ahora los tests de Screenplay
uv run pytest tests/test_login_screenplay.py -v
```

Compara las dos versiones del mismo flujo de login. ¿Cuál te resulta más legible?

---

### Lab 2: explora los fixtures en conftest.py

Abre `conftest.py`. Hay tres tipos de fixture aquí:

**a) `authenticated_page` — scope function (default)**
```python
@pytest.fixture
def authenticated_page(page):
    LoginPage(page).go_to().login("standard_user", "secret_sauce")
    yield page
```
Cada test que use `authenticated_page` recibe una sesión fresca.
El `yield` separa el setup (antes) del teardown (después).
pytest-playwright se encarga de cerrar la página al terminar.

**b) `users` y `products` — scope session**
```python
@pytest.fixture(scope="session")
def users() -> dict:
    return json.loads((DATA_DIR / "users.json").read_text())
```
El archivo se lee **una sola vez** aunque 20 tests lo usen. Eficiente.

Corre esto y observa cuánto tarda:
```bash
uv run pytest tests/test_data_driven.py -v
```

---

### Lab 3: data-driven desde JSON y YAML

Abre `tests/test_data_driven.py`. Hay dos enfoques:

**Enfoque A — parametrize con función de carga (JSON):**
```python
def _load_invalid_users():
    data = json.loads((DATA_DIR / "users.json").read_text())
    return [
        pytest.param(u["username"], u["password"], u["expected_error"],
                     id=u["username"] or "username_vacio")
        for u in data["invalid_users"]
    ]

@pytest.mark.parametrize("username,password,expected_error", _load_invalid_users())
def test_login_invalido_desde_json(page, username, password, expected_error):
    ...
```

Los IDs de test vienen del JSON. Agregar un nuevo caso inválido = una línea en `data/users.json`.

**Enfoque B — fixture de datos (YAML):**
```python
@pytest.mark.parametrize("scenario_idx", [0, 1, 2])
def test_carrito_desde_yaml(authenticated_page, cart_scenarios, scenario_idx):
    scenario = cart_scenarios[scenario_idx]
    ...
```

El fixture `cart_scenarios` carga `data/products.yaml` una vez por sesión.
Agrega un nuevo escenario en el YAML → el test lo toma en la siguiente corrida.

---

## Bloque C — Ejercicios y Mini Reto (45 min)

### Ejercicio 1 — Page Object para el Checkout

SauceDemo tiene una pantalla de checkout en `/checkout-step-one.html`.
Crea el archivo `pages/checkout_page.py` con:

- Locators de los campos `first-name`, `last-name`, `postal-code` y el botón `continue`.
- Método `fill_shipping(first, last, zip_code)` que rellena los tres campos.
- Método `continue_to_overview()` que hace clic en continuar.
- Método `has_error()` que devuelve `True` si hay un mensaje de error visible.

Pista: inspecciona el HTML de SauceDemo con las DevTools del navegador y busca los atributos `data-test`. Todos los elementos interactivos los tienen.

Una vez creado, escribe un test rápido en `tests/test_checkout_pom.py`:
```python
def test_checkout_sin_nombre_muestra_error(authenticated_page):
    InventoryPage(authenticated_page).add_to_cart("Sauce Labs Backpack").go_to_cart()
    CartPage(authenticated_page).proceed_to_checkout()
    checkout = CheckoutPage(authenticated_page)
    checkout.fill_shipping("", "", "").continue_to_overview()
    assert checkout.has_error()
```

---

### Ejercicio 2 — Task de Screenplay: CompleteCheckout

Crea `screenplay/tasks/complete_checkout.py` con una Task que:
1. Navegue al carrito.
2. Haga clic en Checkout.
3. Rellene los datos de envío.
4. Haga clic en continuar.

Nómbrala `CompleteCheckout.with_info(first, last, zip_code)`.

---

### Mini Reto — Suite data-driven con YAML extendido

1. Abre `data/products.yaml` y agrega un cuarto escenario de carrito con 4 productos.
2. Actualiza `test_data_driven.py::test_carrito_desde_yaml` para que también pruebe el índice 3.
3. Corre la suite completa y asegúrate de que los 14 tests pasan:

```bash
uv run pytest -v
```

**Pista:** no toques el código de los Page Objects ni del conftest; solo los archivos de datos y el test parametrizado.

---

### Errores comunes

| Error | Causa | Solución |
|---|---|---|
| `ModuleNotFoundError: pages` | pytest no encuentra el módulo porque no está en `PYTHONPATH` | Verifica que `pythonpath = ["."]` está en `pyproject.toml` y que corriste desde `ui-lab/` |
| `playwright._impl._errors.TimeoutError` | El locator no existe o tarda en aparecer | Usa `page.wait_for_selector(...)` o revisa que el selector sea correcto con las DevTools |
| `KeyError: 'BrowseTheWeb'` | El Actor no tiene la Ability registrada | Asegúrate de llamar `actor.can(BrowseTheWeb.using(page))` antes de `attempts_to` |
| Tests pasan localmente pero fallan en CI | Diferencias de timing en modo headless | Agrega `--headed` para depurar localmente; en CI usa `--browser chromium` explícitamente |

---

### Para llevar

Después de esta sesión tienes:
- Un **framework de UI** funcional sobre SauceDemo con POM + Screenplay.
- **Datos desacoplados** del código en JSON y YAML.
- **Fixtures** que manejan setup/teardown automáticamente.
- La base de la **Etapa 4** del proyecto integrador (pruebas de UI en el flujo CI/CD).

En la **Sesión 3** conectamos esta suite con APIs REST usando Postman y Newman.
