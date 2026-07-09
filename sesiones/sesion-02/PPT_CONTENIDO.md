# PPT — Sesión 2: POM, Screenplay y Data-Driven Testing

> Formato: cada slide tiene **título**, **cuerpo** (bullets o código) y una nota de contexto corta.
> Copiar y pegar directamente en PowerPoint/Google Slides.

---

## Slide 1 — Portada

**Título:** Sesión 2: Desarrollo de Scripts de Prueba

**Subtítulo:** Page Object Model · Screenplay · Fixtures · Data-Driven Testing

**Detalle:** `proyecto-integrador/ui-lab/` · SauceDemo como aplicación de práctica

---

## Slide 2 — Agenda

**Título:** ¿Qué vamos a construir hoy?

- 🔴 **Bloque A** (45 min) — El problema del código espagueti y cómo resolverlo
- ☕ Descanso — 15 min
- 🟡 **Bloque B** (45 min) — Laboratorio guiado: POM + fixtures + datos externos
- ☕ Descanso — 15 min
- 🟢 **Bloque C** (45 min) — Ejercicios individuales y mini reto → salida

**Al final de la sesión tendrás:** una suite de UI funcional lista para el flujo CI/CD

---

## Slide 3 — El Problema

**Título:** ¿Qué pasa si no usamos patrones?

```python
# En test_login.py
page.locator('[data-test="login-button"]').click()

# En test_checkout.py
page.locator('[data-test="login-button"]').click()  # ← copia

# En test_cart.py
page.locator('[data-test="login-button"]').click()  # ← copia x3
```

**Consecuencia:** SauceDemo cambia el atributo → 40 tests rotos → 2 horas de refactoring

---

## Slide 4 — La Solución: POM

**Título:** Page Object Model (POM)

> **Regla:** cada pantalla tiene un archivo Python. Los locators viven ahí, solo ahí.

```python
# pages/login_page.py
class LoginPage:
    def __init__(self, page):
        self._login_btn = page.locator('[data-test="login-button"]')

    def login(self, username, password):
        self._username.fill(username)
        self._password.fill(password)
        self._login_btn.click()
```

**Resultado:** cambias el locator en un lugar → todos los tests funcionan

---

## Slide 5 — Test con POM

**Título:** Cómo se ve el test con POM

```python
# tests/test_login_pom.py
def test_login_exitoso(page):
    LoginPage(page).go_to().login("standard_user", "secret_sauce")
    assert InventoryPage(page).is_loaded()
```

✅ El test describe **qué** sucede, no **cómo** lo hace el navegador
✅ Sin selectores CSS expuestos en el test
✅ Si cambia la UI → solo cambias el Page Object

---

## Slide 6 — Estructura de Pages

**Título:** Los tres Page Objects del laboratorio

```
pages/
├── login_page.py      ← /  (pantalla de login)
├── inventory_page.py  ← /inventory.html
└── cart_page.py       ← /cart.html
```

**Patrón en cada archivo:**
- Locators → privados (`self._btn`)
- Acciones → métodos públicos con nombre de negocio (`login`, `add_to_cart`)
- Consultas → métodos que devuelven estado (`is_loaded`, `cart_count`)

---

## Slide 7 — Más allá del POM: Screenplay

**Título:** Screenplay — tests que se leen como historias

**Los tres bloques de Screenplay:**

| Bloque | Pregunta | Ejemplo |
|---|---|---|
| **Actor** | ¿Quién? | `carlos = Actor("Carlos")` |
| **Ability** | ¿Con qué herramienta? | `.can(BrowseTheWeb.using(page))` |
| **Task** | ¿Qué intenta hacer? | `Login.as_user(...)` |

---

## Slide 8 — Test con Screenplay

**Título:** El mismo flujo, narrado diferente

```python
# POM
LoginPage(page).go_to().login("standard_user", "secret_sauce")
InventoryPage(page).add_to_cart("Sauce Labs Backpack")

# Screenplay
carlos = Actor("Carlos").can(BrowseTheWeb.using(page))
carlos.attempts_to(
    Login.as_user("standard_user", "secret_sauce"),
    AddToCart.the_item("Sauce Labs Backpack"),
)
```

**¿Cuál prefieres?** → depende del contexto del equipo

---

## Slide 9 — POM vs Screenplay

**Título:** ¿Cuándo usar cada uno?

| Situación | Recomendación |
|---|---|
| Suite pequeña, un solo rol | **POM** es suficiente |
| Múltiples roles en el mismo test | **Screenplay** clarifica quién hace qué |
| Equipo con Gherkin / BDD | **Screenplay** alinea el lenguaje |
| Empezando desde cero | **POM** primero, Screenplay si crece |

**Regla de oro:** usa el patrón más simple que resuelva tu problema (KISS)

---

## Slide 10 — DRY y KISS

**Título:** Los principios que unifican todo

**DRY** — *Don't Repeat Yourself*
- Si copias código, algo está mal
- Locators → Page Object · Setup → fixture · Datos → JSON/YAML

**KISS** — *Keep It Simple, Stupid*
- La solución más simple que funciona, es la correcta
- No añadas Screenplay si POM ya resuelve el problema

---

## Slide 11 — Fixtures en pytest

**Título:** Fixtures: setup reutilizable sin duplicar código

```python
# conftest.py — disponible para TODOS los tests sin importar nada

@pytest.fixture
def authenticated_page(page):
    LoginPage(page).go_to().login("standard_user", "secret_sauce")
    yield page   # ← setup antes / teardown después del yield
```

```python
# En el test — solo declara lo que necesita
def test_agregar_producto(authenticated_page):
    InventoryPage(authenticated_page).add_to_cart("Sauce Labs Backpack")
    assert InventoryPage(authenticated_page).cart_count() == 1
```

---

## Slide 12 — Scope de Fixtures

**Título:** Scope: cuántas veces se ejecuta cada fixture

| Scope | Se ejecuta | Cuándo usarlo |
|---|---|---|
| `function` (default) | Por cada test | Estado que no debe compartirse |
| `class` | Por clase de test | Tests agrupados que comparten contexto |
| `module` | Por archivo `.py` | Setup costoso que aplica a un módulo |
| `session` | Una vez por corrida | Datos estáticos, conexiones pesadas |

```python
@pytest.fixture(scope="session")
def users():
    return json.loads((DATA_DIR / "users.json").read_text())
```

---

## Slide 13 — Data-Driven: JSON

**Título:** Datos externos desde JSON

```python
# data/users.json
{
  "invalid_users": [
    {"username": "locked_out_user", "password": "secret_sauce",
     "expected_error": "Sorry, this user has been locked out."},
    {"username": "", "password": "secret_sauce",
     "expected_error": "Username is required"}
  ]
}
```

```python
# test_data_driven.py
@pytest.mark.parametrize("username,password,expected_error", _load_invalid_users())
def test_login_invalido(page, username, password, expected_error):
    login = LoginPage(page).go_to().login(username, password)
    assert expected_error in login.error_message()
```

---

## Slide 14 — Data-Driven: YAML

**Título:** Datos externos desde YAML

```yaml
# data/products.yaml
cart_scenarios:
  - description: "agregar un solo producto"
    items: ["Sauce Labs Backpack"]
    count: 1
  - description: "agregar dos productos"
    items: ["Sauce Labs Backpack", "Sauce Labs Bike Light"]
    count: 2
```

```python
@pytest.mark.parametrize("scenario_idx", [0, 1, 2])
def test_carrito_desde_yaml(authenticated_page, cart_scenarios, scenario_idx):
    scenario = cart_scenarios[scenario_idx]
    for item in scenario["items"]:
        InventoryPage(authenticated_page).add_to_cart(item)
    assert InventoryPage(authenticated_page).cart_count() == scenario["count"]
```

---

## Slide 15 — Ventaja del Data-Driven

**Título:** ¿Por qué separar datos del código?

❌ **Sin separación:**
- Agregar caso = modificar el test = riesgo de romper algo

✅ **Con separación:**
- Agregar caso = una línea en el JSON/YAML = cero riesgo en el código

**Regla:** si el test cambia solo porque los datos cambian, los datos están en el lugar equivocado

---

## Slide 16 — Estructura del laboratorio

**Título:** Lo que tienes en `proyecto-integrador/ui-lab/`

```
ui-lab/
├── conftest.py          ← fixtures compartidas
├── pages/               ← Page Objects (LoginPage, InventoryPage, CartPage)
├── screenplay/          ← Actor, Abilities, Tasks
│   ├── actor.py
│   ├── abilities/browse_web.py
│   └── tasks/ (login.py, add_to_cart.py)
├── data/
│   ├── users.json       ← datos de usuarios
│   └── products.yaml    ← catálogo + escenarios de carrito
└── tests/
    ├── test_login_pom.py
    ├── test_login_screenplay.py
    └── test_data_driven.py
```

---

## Slide 17 — Comandos del laboratorio

**Título:** Setup y ejecución

```bash
cd proyecto-integrador/ui-lab

# Primera vez
uv sync --group dev
uv run playwright install chromium

# Correr todos los tests
uv run pytest -v

# Solo un archivo
uv run pytest tests/test_login_pom.py -v

# Con navegador visible (para depurar)
uv run pytest --headed -v
```

---

## Slide 18 — Ejercicio Individual

**Título:** Tu turno — Bloque C

**Ejercicio 1:** Crea `pages/checkout_page.py` con:
- Locators de `first-name`, `last-name`, `postal-code`, botón `continue`
- Método `fill_shipping(first, last, zip_code)`
- Método `has_error() → bool`

**Ejercicio 2:** Crea `screenplay/tasks/complete_checkout.py`
- Task: `CompleteCheckout.with_info(first, last, zip_code)`

---

## Slide 19 — Mini Reto

**Título:** Mini Reto — Suite data-driven extendida

1. Agrega un **cuarto escenario** en `data/products.yaml` con 4 productos distintos
2. Actualiza `test_data_driven.py` para que también pruebe ese escenario
3. Corre la suite completa: todos los tests deben pasar

```bash
uv run pytest -v
```

**Restricción:** solo modificas el YAML y el test parametrizado. Los Page Objects y el conftest no se tocan.

---

## Slide 20 — Resumen

**Título:** Lo que aprendiste hoy

| Patrón / Herramienta | Para qué sirve |
|---|---|
| **POM** | Centralizar locators y eliminar duplicación |
| **Screenplay** | Narrar flujos complejos con múltiples roles |
| **DRY / KISS** | Guías de diseño que aplican a todo |
| **Fixtures (scope)** | Setup/teardown reutilizable y eficiente |
| **JSON / YAML** | Separar datos de la lógica de pruebas |

**Siguiente sesión:** APIs REST — Postman, Newman y validaciones de servicios web
