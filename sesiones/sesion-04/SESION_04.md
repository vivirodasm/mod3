# Sesión 4 — APIs II: automatización con Python (httpx + pytest)

> **Objetivo:** al terminar esta sesión vas a tener los tests de API de la Sesión 3… pero en código Python puro: un cliente propio siguiendo **KISS** (*Keep It Simple, Stupid* — mantenlo simple), fixtures de pytest aplicando **DRY** (*Don't Repeat Yourself* — no te repitas) y casos alimentados desde archivos JSON/YAML (Data-Driven Testing).

**SUT (*System Under Test*):** [JSONPlaceholder](https://jsonplaceholder.typicode.com) — el mismo de la Sesión 3, para que compares Postman vs Python request por request.

---

## Antes de empezar

```bash
# 1. Entra al laboratorio
cd curso/proyecto-integrador/api-lab

# 2. Instala dependencias (solo la primera vez)
uv sync --group dev

# 3. Verifica que todo corre
uv run pytest -v
```

**Resultado esperado:** `17 passed`.

> **Atajos** desde la raíz de `curso/`: `task setup:api` y `task test:api`.

---

## Agenda (3 horas)

| Bloque | Duración | Contenido |
|---|---|---|
| **A** | 45 min | De Postman a Python: httpx directo · el cliente de API con KISS |
| Descanso | 15 min | ☕ |
| **B** | 45 min | pytest + fixtures: base URL, headers de autenticación, cliente compartido (DRY) |
| Descanso | 15 min | ☕ |
| **C** | 45 min | Data-Driven con JSON/YAML · **Reto: refactorizar tu suite de la S3 a Python** |

---

## Bloque A — De Postman a Python (45 min)

### 1. ¿Por qué salir de Postman si ya funcionaba?

Postman es excelente… hasta que necesitas: lógica compleja (reintentos, loops), compartir código con el equipo de desarrollo, versionar tests como código revisable línea por línea, o integrar los tests al mismo repo del producto. En ese momento quieres un **lenguaje de programación**.

**El mapa del ecosistema** (para que ubiques lo que verás en ofertas de trabajo):

| Herramienta | Lenguaje | Cuándo la eliges |
|---|---|---|
| **pytest + httpx/requests** | Python | Equipos Python-first — **la ruta de este curso** |
| **REST-assured** | Java | El producto y el equipo viven en Java/Spring |
| **Karate DSL** | Gherkin sobre JVM (*Java Virtual Machine*) | Equipos mixtos dev/QA en ecosistema Java que quieren tests legibles sin programar |

Las tres hacen lo mismo que aprenderás hoy: requests, validaciones, data-driven y paralelo. **El patrón es el que importa; la sintaxis se aprende en una semana.** Elegimos Python porque es el lenguaje base del curso y no requiere instalar la JVM.

### 2. httpx: el "Send" de Python

**httpx** es la librería HTTP moderna de Python (sucesora espiritual de `requests`, con la misma sintaxis y soporte async). Cada concepto de Postman tiene su equivalente directo:

| En Postman | En Python (httpx) |
|---|---|
| Método + URL + **Send** | `httpx.get(url)` |
| Status en pantalla | `respuesta.status_code` |
| Body (pestaña Pretty) | `respuesta.json()` |
| Headers de respuesta | `respuesta.headers["Content-Type"]` |
| Tiempo de respuesta | `respuesta.elapsed.total_seconds()` |
| `pm.test(...)` | `assert` |

### 3. Tu primer test de API en Python

Archivo: `tests/test_smoke_httpx.py`

```python
import httpx

BASE_URL = "https://jsonplaceholder.typicode.com"

def test_get_post_devuelve_200_y_el_recurso():
    respuesta = httpx.get(f"{BASE_URL}/posts/1")

    assert respuesta.status_code == 200
    post = respuesta.json()
    assert post["id"] == 1
```

Córrelo:

```bash
uv run pytest tests/test_smoke_httpx.py -v
```

Compara con Postman: son las MISMAS validaciones del request `02 · GET Detalle` de la S3, en 8 líneas.

### 4. El problema que ya huele mal

Mira `test_smoke_httpx.py` completo: la constante `BASE_URL` se repite en cada test, y si mañana la API pide un token, habría que tocar **todos** los archivos. En la S2 este mismo problema nos llevó al Page Object Model. Aquí nos lleva a…

### 5. El cliente de API — KISS en acción

Archivo: `client/api_client.py`

```python
class ApiClient:
    """Envoltorio delgado sobre httpx.Client para probar APIs REST."""

    def __init__(self, base_url, headers=None, timeout=10.0):
        self._http = httpx.Client(base_url=base_url, headers=headers or {}, timeout=timeout)

    def get(self, path, params=None):
        return self._http.get(path, params=params)

    def post(self, path, json=None):
        return self._http.post(path, json=json)
    # ... put() y delete() iguales de simples
```

**KISS aplicado:** una clase, cinco métodos, cero herencia, cero magia. La `base_url`, los headers y el timeout se configuran **una sola vez** y todos los tests los heredan:

```python
api = ApiClient("https://jsonplaceholder.typicode.com")
respuesta = api.get("/posts/1")     # la URL completa vive en UN lugar
```

> **¿Y `requests`?** Si en tu trabajo usan `requests`, el cliente es idéntico: cambia `httpx.Client` por `requests.Session`. Todo lo demás de la sesión aplica igual.

---

## ☕ Descanso (15 min)

**Tarea opcional:** abre `conftest.py` y cuenta cuántas veces aparece la palabra `fixture`. En el Bloque B te explico qué hace cada una.

---

## Bloque B — pytest + fixtures: la configuración vive en UN lugar (45 min)

### 1. El conftest.py: la caja de herramientas compartida

`conftest.py` es un archivo especial: pytest lo carga solo, y **todo lo que definas ahí está disponible en cualquier test sin importarlo**. Es donde aplicamos DRY a la configuración:

```python
BASE_URL = "https://jsonplaceholder.typicode.com"

@pytest.fixture(scope="session")
def auth_headers() -> dict:
    # JSONPlaceholder no exige token, pero el patrón es idéntico
    # al de una API real: el header viaja en TODOS los requests.
    return {"Authorization": "Bearer token-de-practica-curso-qa"}

@pytest.fixture(scope="session")
def api(base_url, auth_headers):
    """Cliente único para toda la corrida: se crea una vez, se cierra al final."""
    client = ApiClient(base_url, headers=auth_headers)
    yield client
    client.close()
```

**Tres cosas clave:**
- `scope="session"` → el cliente se crea **una vez** para todos los tests (no uno por test — más rápido).
- `yield` → lo que va después es el *teardown*: cerrar la conexión al terminar.
- Las fixtures se componen: `api` **pide** `base_url` y `auth_headers` como parámetros.

### 2. Los tests quedan limpios

Archivo: `tests/test_posts_crud.py` — el CRUD completo de la S3, refactorizado:

```python
def test_listar_posts_devuelve_100(api):     # ← pytest inyecta la fixture
    respuesta = api.get("/posts")

    assert respuesta.status_code == 200
    assert len(respuesta.json()) == 100
```

Ni URL, ni headers, ni timeouts: el test solo dice **qué valida**. Compáralo con la versión del Bloque A.

### 3. El "pre-request script" en Python

En la S3 generábamos un título único con `Date.now()`. El equivalente:

```python
def test_crear_post_devuelve_201_y_eco_del_payload(api):
    titulo = f"Post QA {time.time_ns()}"
    payload = {"title": titulo, "body": "Creado desde la Sesión 4", "userId": 1}

    respuesta = api.post("/posts", json=payload)

    assert respuesta.status_code == 201
    assert respuesta.json()["title"] == titulo
```

### 4. El "JSON Schema" en Python, versión KISS

```python
CONTRATO_POST = {"userId": int, "id": int, "title": str, "body": str}

def cumple_contrato(recurso: dict, contrato: dict) -> bool:
    return all(
        campo in recurso and isinstance(recurso[campo], tipo)
        for campo, tipo in contrato.items()
    )
```

Valida presencia y tipo de cada campo — el mismo concepto de contrato de la S3. (En proyectos grandes existe la librería `jsonschema`, que usa los mismos schemas que Postman.)

> **El siguiente nivel de los contratos — Pact:** lo que hicimos valida el contrato desde el lado del **consumidor**. Existe una disciplina completa llamada *contract testing* consumidor/proveedor, cuya herramienta estándar es **Pact**: el consumidor publica el contrato que espera y el proveedor lo verifica automáticamente en su propio CI antes de desplegar. Es el mecanismo profesional para que microservicios no se rompan entre sí. Quédate con el concepto — la base (validar estructura, no solo status) ya la dominas.

### 5. Corre el CRUD completo

```bash
uv run pytest tests/test_posts_crud.py -v
```

**Resultado esperado:** `6 passed` — los mismos 6 requests de la colección Postman, ahora en Python.

---

## ☕ Descanso (15 min)

Sin tarea — llega fresco al reto. 💪

---

## Bloque C — Data-Driven + Reto (45 min)

### 1. Los datos NO viven en el código

Ya lo hicimos en UI (S2); ahora en APIs. Los payloads viven en `data/`:

**`data/posts_payloads.json`** — 4 casos de creación:

```json
[
  { "caso": "post_normal",           "payload": { "title": "Reporte…", "body": "…", "userId": 1 } },
  { "caso": "titulo_largo",          "payload": { "title": "Un título muy largo…", "userId": 2 } },
  { "caso": "caracteres_especiales", "payload": { "title": "Áéíóú ñ 中文 🚀", "userId": 3 } },
  { "caso": "body_vacio",            "payload": { "title": "Post sin cuerpo", "body": "", "userId": 4 } }
]
```

**`data/update_cases.yaml`** — 3 casos de actualización (YAML es más legible para humanos).

### 2. parametrize: un test, N casos

```python
CASOS_POST = load_json("posts_payloads.json")

@pytest.mark.parametrize("caso", CASOS_POST, ids=[c["caso"] for c in CASOS_POST])
def test_crear_post_con_datos_externos(api, caso):
    respuesta = api.post("/posts", json=caso["payload"])

    assert respuesta.status_code == 201
    for campo, valor in caso["payload"].items():
        assert respuesta.json()[campo] == valor
```

```bash
uv run pytest tests/test_data_driven.py -v
```

**Resultado esperado:** `7 passed` — y en la salida cada caso aparece con su nombre: `[post_normal]`, `[titulo_largo]`…

**La regla de oro:** agregar un caso nuevo = agregar una entrada al JSON/YAML. **Cero código nuevo.**

---

## 🏆 Reto de la sesión: refactoriza tu suite de la S3 a Python

**Enunciado:** en la S3 creaste la colección `RETO_S3_<tu-nombre>` sobre `/users`. Hoy la conviertes a Python puro. Crea `tests/test_reto_users.py` con **al menos 5 tests**:

| # | Test | Validaciones requeridas |
|---|---|---|
| 1 | `test_listar_users` | Status 200 · son 10 usuarios |
| 2 | `test_detalle_cumple_contrato` | Status 200 · contrato con `id: int`, `name: str`, `username: str`, `email: str` |
| 3 | `test_crear_user` | Status 201 · `name` único generado con `time.time_ns()` y verificado en el eco |
| 4 | `test_actualizar_user` | Status 200 · el campo actualizado coincide |
| 5 | `test_eliminar_user` | Status 200 · body vacío `{}` |

**Reglas:**
- Todos los tests usan la fixture `api` — **prohibido** escribir la URL completa o crear clientes dentro del test.
- El contrato se valida reutilizando `cumple_contrato` (impórtalo o cópialo).

**Bonus (nivel jefe):** mueve los datos del `test_crear_user` a un archivo `data/users_payloads.json` con 3 casos y usa `parametrize`.

**Entrega:** tu `test_reto_users.py` (+ el JSON del bonus). Se revisa con `uv run pytest tests/test_reto_users.py -v`: todo en verde = aprobado.

---

## Errores comunes

| Síntoma | Causa | Solución |
|---|---|---|
| `ModuleNotFoundError: No module named 'client'` | Corriste pytest fuera de `api-lab` | `cd curso/proyecto-integrador/api-lab` primero |
| `fixture 'api' not found` | Tu test está fuera de la carpeta `tests/` o borraste `conftest.py` | El test debe vivir en `tests/` junto al `conftest.py` de la raíz del lab |
| `httpx.ConnectTimeout` | Internet lento o proxy | Reintenta; el timeout del cliente es 10 s |
| `assert 500 == 201` en PUT de users | JSONPlaceholder a veces responde 500 en `PUT /users/N` | Usa `PUT /users/1` con payload que incluya `"id": 1` |
| Los tests parametrizados no aparecen | El archivo de datos tiene un error de sintaxis | Valida el JSON/YAML (VS Code lo subraya en rojo) |

---

## Resumen de comandos

```bash
cd curso/proyecto-integrador/api-lab
uv sync --group dev              # primera vez
uv run pytest -v                 # toda la suite (17 tests)
uv run pytest tests/test_posts_crud.py -v    # solo el CRUD
uv run pytest -k "datos_externos" -v         # solo data-driven

# Atajos desde curso/
task setup:api
task test:api
```

**Próxima sesión:** CI/CD — GitHub Actions va a correr TODO lo que hemos construido (UI + Newman + pytest) en cada push. 🚀
