# Sesión 3 — APIs y servicios web I: Postman + Newman

> **Objetivo:** al terminar esta sesión vas a poder probar una API (*Application Programming Interface*, interfaz de programación de aplicaciones) REST de punta a punta: entender sus verbos y códigos de estado, automatizar validaciones con Postman y correr todo desde la terminal con Newman — sin abrir ninguna interfaz gráfica.

**SUT (*System Under Test*, sistema bajo prueba):** [JSONPlaceholder](https://jsonplaceholder.typicode.com) — una API pública y gratuita de práctica que simula un blog (posts, comentarios, usuarios). No requiere cuenta ni token.

---

## Antes de empezar

1. **Instala Postman** (aplicación de escritorio): https://www.postman.com/downloads/ — la versión gratuita es suficiente.
2. **Verifica que tienes Node.js** (lo necesita Newman):

```bash
node --version   # cualquier versión 18+ sirve
```

3. **Clona/actualiza el repo y ubícate en el laboratorio:**

```bash
cd curso/proyecto-integrador/api-tests
```

4. **Prueba que Newman funciona** (se descarga solo la primera vez con `npx`):

```bash
npx --yes newman run postman/s3_crud_jsonplaceholder.postman_collection.json \
  --environment postman/jsonplaceholder.postman_environment.json
```

**Resultado esperado:** una tabla al final con `17 assertions | 0 failed`.

> **Atajo:** desde la raíz de `curso/` también puedes correr `task test:api:postman`.

---

## Agenda (3 horas)

| Bloque | Duración | Contenido |
|---|---|---|
| **A** | 45 min | Fundamentos REST: verbos, status codes, headers · Postman a fondo: variables, pre-request scripts, tests |
| Descanso | 15 min | ☕ |
| **B** | 45 min | Newman CLI: la colección corre en la terminal · integración conceptual con CI/CD |
| Descanso | 15 min | ☕ |
| **C** | 45 min | JSON Schema: contratos de API · **Reto: suite CRUD completa** |

---

## Bloque A — El ecosistema REST y Postman a fondo (45 min)

### 1. ¿Qué es una API REST?

**REST** (*Representational State Transfer*) es un estilo de arquitectura donde todo es un **recurso** con una URL, y las operaciones se expresan con **verbos HTTP** (*HyperText Transfer Protocol*):

| Verbo | Operación | Ejemplo en JSONPlaceholder | Analogía CRUD |
|---|---|---|---|
| `GET` | Leer | `GET /posts/1` | **R**ead |
| `POST` | Crear | `POST /posts` | **C**reate |
| `PUT` | Reemplazar completo | `PUT /posts/1` | **U**pdate |
| `PATCH` | Modificar parcial | `PATCH /posts/1` | **U**pdate |
| `DELETE` | Eliminar | `DELETE /posts/1` | **D**elete |

**CRUD** = *Create, Read, Update, Delete* — las 4 operaciones básicas sobre cualquier dato.

### 2. REST no está solo: SOAP y GraphQL

En el mundo real te vas a topar con tres estilos de API. Conviene saber ubicarlos:

| Estilo | Qué es | Cuándo te lo topas |
|---|---|---|
| **REST** | Recursos + verbos HTTP + JSON. El estándar de facto | La gran mayoría de las APIs modernas — es el que dominamos en el curso |
| **SOAP** (*Simple Object Access Protocol*) | Protocolo formal basado en XML (*Extensible Markup Language*), con contratos WSDL estrictos | Banca, seguros, gobierno — sistemas legados que no van a desaparecer |
| **GraphQL** | Un solo endpoint; el **cliente** decide qué campos pedir en la consulta | Apps con muchas vistas distintas (creado por Facebook/Meta) |

**Para QA lo esencial es:** los conceptos de hoy (status codes, validación de payload, contratos) aplican a los tres. Cambia el formato del mensaje, no la disciplina de prueba. Postman, de hecho, soporta los tres.

### 3. Códigos de estado (status codes) — el idioma de la API

| Familia | Significado | Los que más vas a ver |
|---|---|---|
| `2xx` | Todo bien | `200 OK`, `201 Created`, `204 No Content` |
| `3xx` | Redirección | `301 Moved`, `304 Not Modified` |
| `4xx` | Error **del cliente** | `400 Bad Request`, `401 Unauthorized`, `403 Forbidden`, `404 Not Found` |
| `5xx` | Error **del servidor** | `500 Internal Server Error`, `503 Service Unavailable` |

> **Regla de oro:** si te devuelve `4xx`, el problema está en tu request. Si es `5xx`, el problema está del otro lado.

### 4. Headers — los metadatos del mensaje

Los **headers** (cabeceras) viajan con cada request/response y describen el contenido:

- `Content-Type: application/json` → "te estoy mandando JSON (*JavaScript Object Notation*)"
- `Authorization: Bearer <token>` → "estas son mis credenciales"
- `Cache-Control` → "así se puede (o no) cachear esta respuesta"

### 5. Tu primer request en Postman

1. Abre Postman → botón **New** → **HTTP Request**.
2. Método: `GET` · URL: `https://jsonplaceholder.typicode.com/posts/1`
3. Presiona **Send** y observa: el **status** (200 OK), el **tiempo**, el **tamaño** y el **body** con el JSON.

### 6. Variables: nunca escribas la URL dos veces

En Postman hay variables de **entorno** (environment) y de **colección**. Nuestro environment define:

```
base_url = https://jsonplaceholder.typicode.com
```

Y desde ahí, toda URL se escribe como `{{base_url}}/posts/1`. Si mañana la API cambia de dominio, tocas **una sola línea**.

> Importa los dos archivos del repo en Postman: **Import** → arrastra `postman/s3_crud_jsonplaceholder.postman_collection.json` y `postman/jsonplaceholder.postman_environment.json`. Luego selecciona el environment "JSONPlaceholder · Curso QA" en el dropdown de arriba a la derecha.

### 7. Tests en Postman: JavaScript que valida la respuesta

Cada request puede llevar una pestaña **Scripts → Post-response** (antes llamada "Tests") con validaciones:

```javascript
pm.test('Status es 200 OK', function () {
    pm.response.to.have.status(200);
});

pm.test('Responde en menos de 2 segundos', function () {
    pm.expect(pm.response.responseTime).to.be.below(2000);
});

pm.test('El header Content-Type es JSON', function () {
    pm.expect(pm.response.headers.get('Content-Type')).to.include('application/json');
});
```

### 8. Pre-request scripts: código que corre ANTES de enviar

Sirven para preparar datos dinámicos. En nuestro `03 · POST Crear post`:

```javascript
// Genera un título único en cada ejecución
const titulo = 'Post QA ' + Date.now();
pm.collectionVariables.set('dynamic_title', titulo);
```

Y el body del request lo usa con `{{dynamic_title}}`. Así el test **nunca depende de datos quemados** (*hardcoded*).

### 9. Encadenar requests: el id creado se reutiliza

En el test del POST guardamos el `id` que devolvió la API:

```javascript
pm.collectionVariables.set('post_id', post.id);
```

Cualquier request posterior puede usar `{{post_id}}`. Esto convierte una colección en un **flujo**, no en requests sueltos.

---

## ☕ Descanso (15 min)

**Tarea opcional:** abre la colección importada y lee los tests del request `02 · GET Detalle de un post`. Hay algo ahí que veremos en el Bloque C… (spoiler: se llama JSON Schema).

---

## Bloque B — Newman: la colección sale de Postman y entra a la terminal (45 min)

### 1. ¿Por qué necesitamos salir de Postman?

Postman es excelente para **explorar** y **diseñar** tests, pero tiene un problema: alguien tiene que abrirlo y apretar botones. La automatización real vive en la terminal, porque la terminal es lo único que entiende un pipeline de **CI/CD** (*Continuous Integration / Continuous Delivery*, integración y entrega continuas).

**Newman** es el ejecutor oficial de colecciones Postman por línea de comandos. Es open source y no requiere cuenta.

> **Nota 2026:** Postman también ofrece **Postman CLI**, el sucesor oficial de Newman, pero requiere cuenta de Postman. En el curso usamos Newman porque funciona sin registro; los conceptos son idénticos.

### 2. Exportar una colección desde Postman

Si construiste una colección en la interfaz gráfica y la quieres versionar:

1. Clic derecho sobre la colección → **Export** → formato **Collection v2.1** → guarda el `.json`.
2. Lo mismo con el environment: ícono de ⚙️ → **Export**.
3. Esos `.json` se commitean a Git — **la colección es código**.

En el repo ya están exportados en `proyecto-integrador/api-tests/postman/`.

### 3. Correr la colección con Newman

```bash
cd curso/proyecto-integrador/api-tests

npx --yes newman run postman/s3_crud_jsonplaceholder.postman_collection.json \
  --environment postman/jsonplaceholder.postman_environment.json
```

**Qué hace cada parte:**
- `npx --yes newman` → descarga (si hace falta) y ejecuta Newman sin instalarlo globalmente.
- `run <colección>` → el archivo `.json` exportado.
- `--environment <env>` → de aquí sale `{{base_url}}`.

**Resultado esperado:**

```
┌─────────────────────────┬─────────────────────┬────────────────────┐
│                         │            executed │             failed │
│                requests │                   6 │                  0 │
│              assertions │                  17 │                  0 │
└─────────────────────────┴─────────────────────┴────────────────────┘
```

### 4. Opciones útiles de Newman

```bash
# Repetir la colección 3 veces (mini test de estabilidad)
npx newman run <colección> -e <env> --iteration-count 3

# Parar en el primer fallo
npx newman run <colección> -e <env> --bail

# Generar reporte HTML (requiere el reporter extra)
npx --yes newman run <colección> -e <env> \
  -r cli,htmlextra --reporter-htmlextra-export reporte.html
```

### 5. El atajo del curso: Taskfile

Desde la raíz de `curso/` ya quedó configurado:

```bash
task test:api:postman
```

### 6. ¿Y esto cómo se conecta con CI/CD?

El mismo comando que corriste a mano es el que correría GitHub Actions en cada push (lo haremos de verdad en la Sesión 5):

```yaml
# .github/workflows/api-tests.yml (adelanto conceptual — NO lo crees aún)
- name: Run API tests
  run: npx --yes newman run postman/s3_crud_jsonplaceholder.postman_collection.json \
    -e postman/jsonplaceholder.postman_environment.json
```

**La idea clave:** si Newman devuelve código de salida distinto de 0 (algún test falló), el pipeline se pone rojo y el release **no sale**. Eso es una puerta de calidad (*quality gate*).

---

## ☕ Descanso (15 min)

Sin tarea — llega fresco al reto del Bloque C. 💪

---

## Bloque C — Contratos con JSON Schema + Reto CRUD (45 min)

### 1. El problema: el test pasa, pero la API cambió

Imagina que el equipo de backend renombra `title` a `postTitle` en un refactor. Mira lo que pasa con la respuesta:

```
ANTES                                DESPUÉS del refactor
200 OK                               200 OK   ← para el server NO es un error
{ "id": 1, "title": "Hola" }         { "id": 1, "postTitle": "Hola" }
```

La cadena del desastre, paso a paso:

1. **El server sigue devolviendo 200** — renombrar un campo no es un error para él; responde un JSON válido, solo que con otro nombre.
2. **Tu test `pm.response.to.have.status(200)` sigue verde** — ese test solo mira la primera línea de la respuesta; nunca abre el body.
3. **La app que consume la API hace `respuesta.title`** — el campo ya no existe → `undefined` → pantalla vacía en producción. Y el release lo aprobó QA.

**Moraleja:** el status dice "el server respondió"; la estructura dice "respondió **lo que espero**". Necesitamos validar las dos cosas — y a eso se le llama **contrato**.

### 2. JSON Schema: el contrato de la respuesta

Un **JSON Schema** describe qué campos debe tener un JSON, de qué tipo son y cuáles son obligatorios:

```javascript
const postSchema = {
    type: 'object',
    required: ['userId', 'id', 'title', 'body'],   // si falta uno → falla
    properties: {
        userId: { type: 'integer' },
        id:     { type: 'integer' },
        title:  { type: 'string' },
        body:   { type: 'string' }
    }
};

pm.test('El post cumple el contrato (JSON Schema)', function () {
    pm.response.to.have.jsonSchema(postSchema);
});
```

Postman valida el schema internamente con **Ajv** (*Another JSON Schema Validator*), la librería estándar de la industria.

### 3. Pruébalo: rompe el contrato a propósito

1. En Postman, abre el request `02 · GET Detalle de un post`.
2. En el schema, cambia `title: { type: 'string' }` por `title: { type: 'integer' }`.
3. **Send** → el test falla con un mensaje de Ajv explicando exactamente qué campo no cumple.
4. Regrésalo a `string` y verifica que vuelve a pasar.

### 4. Validaciones de arrays completos

Para validar que **todos** los elementos de una lista cumplen el contrato:

```javascript
const listaSchema = {
    type: 'array',
    items: {                       // cada elemento del array…
        type: 'object',
        required: ['userId', 'id', 'title', 'body']
    }
};

pm.test('Los 100 posts cumplen el contrato', function () {
    pm.response.to.have.jsonSchema(listaSchema);
});
```

---

## 🏆 Reto de la sesión: tu propia suite CRUD

**Enunciado:** crea en Postman una colección nueva llamada `RETO_S3_<tu-nombre>` que valide el flujo CRUD completo del recurso **`/users`** de JSONPlaceholder, con **al menos 5 requests** y estas validaciones mínimas:

| # | Request | Validaciones requeridas |
|---|---|---|
| 1 | `GET {{base_url}}/users` | Status 200 · son 10 usuarios · tiempo < 2000 ms |
| 2 | `GET {{base_url}}/users/1` | Status 200 · **JSON Schema** con `id`, `name`, `username`, `email` obligatorios |
| 3 | `POST {{base_url}}/users` | Status 201 · el `name` enviado (generado en pre-request con `Date.now()`) coincide con el devuelto |
| 4 | `PUT {{base_url}}/users/1` | Status 200 · el campo actualizado coincide |
| 5 | `DELETE {{base_url}}/users/1` | Status 200 · body vacío `{}` |

**Bonus (nivel jefe):** agrega un 6.º request negativo (`GET /users/999999` → 404) y corre toda tu colección con Newman exportándola primero.

**Entrega:** el archivo `.json` exportado de tu colección. Se revisa corriéndolo con Newman: si sale `0 failed`, está aprobado.

---

## Errores comunes

| Síntoma | Causa | Solución |
|---|---|---|
| `{{base_url}}` aparece literal en la URL | No seleccionaste el environment | Dropdown superior derecho → "JSONPlaceholder · Curso QA" |
| `getaddrinfo ENOTFOUND` en Newman | Sin internet o URL mal escrita | Verifica conexión y revisa el environment |
| `newman: command not found` | Newman no está instalado globalmente | Usa `npx --yes newman run …` (como en esta guía) |
| El test del POST falla con título distinto | El pre-request script no corrió | Verifica que el script esté en la pestaña **Pre-request** del request, no en Tests |
| Todos los tests fallan con timeout | JSONPlaceholder lento o caído | Reintenta; si persiste, sube el límite de 2000 ms a 5000 ms |

---

## Resumen de comandos

```bash
# Correr la suite S3 completa (desde curso/proyecto-integrador/api-tests)
npx --yes newman run postman/s3_crud_jsonplaceholder.postman_collection.json \
  --environment postman/jsonplaceholder.postman_environment.json

# O con el atajo del Taskfile (desde curso/)
task test:api:postman
```

**Próxima sesión:** los mismos tests de API… pero en **Python puro** con `httpx` y `pytest`. Adiós interfaz gráfica, hola código. 🐍
