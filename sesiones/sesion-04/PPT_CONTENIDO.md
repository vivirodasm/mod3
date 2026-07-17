# Sesión 4 — Contenido de diapositivas
## APIs II: automatización con Python (httpx + pytest)

> 20 slides · Bloque A: slides 1-8 (45 min) · Bloque B: slides 9-14 (45 min) · Bloque C: slides 15-20 (45 min)

---

### Slide 1 — Portada (2 min)
**Título:** APIs II — de Postman a Python
- Sesión 4 de 10 · Curso QA Automation
- Hoy: los tests de la S3, en código Python puro
- Mismo SUT: JSONPlaceholder — para comparar request por request

### Slide 2 — ¿Por qué salir de Postman? (4 min)
- Postman brilla para **explorar** y **diseñar**
- Se queda corto cuando necesitas: lógica compleja, code review línea a línea, tests en el mismo repo del producto
- **No es Postman VS Python:** es Postman para explorar + Python para escalar
- El mapa del mercado: **pytest + httpx** (Python — nuestra ruta) · **REST-assured** (Java) · **Karate DSL** (Gherkin sobre JVM, equipos mixtos Java)
- El patrón es el mismo en las tres — la sintaxis se aprende en una semana

### Slide 3 — httpx: el "Send" de Python (5 min)
| Postman | Python (httpx) |
|---|---|
| Send | `httpx.get(url)` |
| Status | `respuesta.status_code` |
| Body Pretty | `respuesta.json()` |
| `pm.test()` | `assert` |
- httpx = sucesor moderno de `requests`, misma sintaxis (si tu empresa usa `requests`, todo aplica igual)

### Slide 4 — DEMO: primer test en Python (7 min)
```python
def test_get_post_devuelve_200_y_el_recurso():
    respuesta = httpx.get(f"{BASE_URL}/posts/1")
    assert respuesta.status_code == 200
    assert respuesta.json()["id"] == 1
```
- 8 líneas = el request `02 · GET Detalle` completo de la S3
- **DEMO:** `uv run pytest tests/test_smoke_httpx.py -v` → `4 passed`

### Slide 5 — Postman ↔ Python, mapa completo (5 min)
- Variables de environment → constante / fixture
- Pre-request script → líneas ANTES del request en el test
- Tests (pm.test) → `assert`
- Collection Runner → `pytest`
- Newman → `pytest` (¡ya no hace falta exportar nada!)

### Slide 6 — El código que huele mal (4 min)
- `BASE_URL` repetida en cada test 😬
- ¿Mañana piden token? → tocar TODOS los archivos
- En S2 este problema nos llevó al POM… aquí nos lleva al **cliente de API**

### Slide 7 — El cliente de API: KISS (8 min)
```python
class ApiClient:
    def __init__(self, base_url, headers=None, timeout=10.0):
        self._http = httpx.Client(base_url=base_url, headers=headers or {}, timeout=timeout)

    def get(self, path, params=None):
        return self._http.get(path, params=params)
```
- **KISS** (*Keep It Simple, Stupid*): una clase, 5 métodos, cero herencia
- base_url + headers + timeout se configuran **UNA vez**

### Slide 8 — DEMO: el cliente en acción (10 min)
- Abrir `client/api_client.py` → recorrerlo (cabe en una pantalla)
- `api.get("/posts/1")` — la URL completa vive en UN lugar
- Anticipo: "¿y quién crea el cliente? Eso es el Bloque B"

---
**☕ DESCANSO 15 MIN**
---

### Slide 9 — conftest.py: la caja compartida (6 min)
- pytest lo carga solo — sin imports en los tests
- Todo lo que definas ahí está disponible en cualquier test
- Es el lugar donde DRY se aplica a la **configuración**

### Slide 10 — Fixtures: anatomía (8 min)
```python
@pytest.fixture(scope="session")
def api(base_url, auth_headers):
    client = ApiClient(base_url, headers=auth_headers)
    yield client
    client.close()
```
- `scope="session"` → se crea UNA vez para todos los tests
- `yield` → lo que sigue es teardown (cerrar conexión)
- Las fixtures se **componen**: `api` pide `base_url` y `auth_headers`

### Slide 11 — Autenticación por fixture (6 min)
```python
@pytest.fixture(scope="session")
def auth_headers():
    return {"Authorization": "Bearer token-de-practica-curso-qa"}
```
- JSONPlaceholder no exige token, pero el patrón es el de una API real
- Mañana con token real: se cambia UNA fixture, cero tests

### Slide 12 — DEMO: el CRUD refactorizado (10 min)
```python
def test_listar_posts_devuelve_100(api):
    respuesta = api.get("/posts")
    assert respuesta.status_code == 200
    assert len(respuesta.json()) == 100
```
- Ni URL, ni headers: el test solo dice **qué valida**
- **DEMO:** `uv run pytest tests/test_posts_crud.py -v` → `6 passed`
- Son los 6 requests de la colección Postman de la S3

### Slide 13 — Pre-request y JSON Schema en Python (8 min)
- Título único: `f"Post QA {time.time_ns()}"` (el `Date.now()` de Python)
- Contrato KISS: `CONTRATO_POST = {"userId": int, "id": int, "title": str, "body": str}` + `cumple_contrato()`
- En proyectos grandes: librería `jsonschema` (mismos schemas que Postman)
- El siguiente nivel: **contract testing** consumidor/proveedor con **Pact** — el consumidor publica el contrato, el proveedor lo verifica en su CI (concepto, no lab)

### Slide 14 — MINI-LAB (7 min)
- Todos corren: `uv run pytest tests/test_posts_crud.py -v`
- Luego rompen un assert a propósito (`== 100` → `== 99`) y leen el error de pytest
- Objetivo: perderle el miedo al output rojo

---
**☕ DESCANSO 15 MIN**
---

### Slide 15 — Los datos NO viven en el código (5 min)
- Ya lo hicimos en UI (S2) — mismo principio en APIs
- `data/posts_payloads.json` → 4 casos de creación
- `data/update_cases.yaml` → 3 casos de PUT
- Agregar caso nuevo = editar el archivo. **Cero código.**

### Slide 16 — parametrize: un test, N casos (8 min)
```python
@pytest.mark.parametrize("caso", CASOS_POST, ids=[c["caso"] for c in CASOS_POST])
def test_crear_post_con_datos_externos(api, caso):
    respuesta = api.post("/posts", json=caso["payload"])
    assert respuesta.status_code == 201
```
- `ids=` → cada caso aparece con nombre en la salida: `[titulo_largo]`, `[caracteres_especiales]`

### Slide 17 — DEMO: data-driven corriendo (5 min)
- `uv run pytest tests/test_data_driven.py -v` → `7 passed`
- Agregar EN VIVO un caso al JSON → correr → `8 passed` sin tocar código

### Slide 18 — El reto: refactoriza tu S3 (20 min)
- Tu colección `RETO_S3` de `/users` → `tests/test_reto_users.py`
- Mínimo 5 tests · todos usan la fixture `api` · contrato con `cumple_contrato`
- **Prohibido:** URLs completas o clientes dentro del test
- Bonus: payloads en `data/users_payloads.json` + parametrize
- Aprobado = `uv run pytest tests/test_reto_users.py -v` todo verde

### Slide 19 — Errores comunes (4 min)
- `ModuleNotFoundError: client` → no estás en `api-lab`
- `fixture 'api' not found` → el test no está en `tests/`
- `PUT /users/N` a veces da 500 en JSONPlaceholder → usar id=1 con `"id": 1` en el payload

### Slide 20 — Cierre y próxima sesión (3 min)
- Balance: misma cobertura que la S3, ahora versionada, revisable y componible
- El proyecto integrador ya tiene: UI (S2) + Postman/Newman (S3) + pytest API (S4)
- **S5:** GitHub Actions corre TODO en cada push — nace el pipeline 🚀
