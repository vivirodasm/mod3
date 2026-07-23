# Sesión 5 — CI/CD: control de calidad automático

> **Objetivo:** al terminar esta sesión vas a poder explicar CI en una frase, leer un workflow de GitHub Actions línea por línea y ejecutar la suite de APIs de la Sesión 4 **dentro de Docker**, exactamente como lo haría un pipeline.

**SUT (*System Under Test*):** la misma suite de `api-lab` de la Sesión 4 (17 tests sobre JSONPlaceholder). Hoy no escribes tests nuevos: aprendes a **correr los que ya tienes de forma automática**, en un entorno común para todo el equipo.

**Frase del día:** si un test solo pasa en tu máquina, no es un test de equipo.

---

## Antes de empezar

```bash
# 1. Verifica que Docker Desktop está corriendo
docker version

# 2. Entra al laboratorio de CI
cd proyecto-integrador/ci-lab
```

**Resultado esperado:** `docker version` imprime la versión del cliente y del servidor. Docker Desktop debe mostrar **Running**.

El `ci-lab` reutiliza la misma suite de `api-lab/`; no copia los tests, los corre dentro de un contenedor.

> **Atajo** desde la raíz de `curso/`: `task test:ci` corre los dos comandos del Bloque B de una sola vez.

---

## Agenda (3 horas)

| Bloque | Duración | Contenido |
|---|---|---|
| **A** | 45 min | Qué problema resuelve CI · qué significan CI y CD · leer un workflow de GitHub Actions completo |
| Descanso | 15 min | ☕ |
| **B** | 45 min | Correr la suite de la S4 dentro de Docker · comparar local vs contenedor · leer el workflow real |
| Descanso | 15 min | ☕ |
| **C** | 45 min | Filtro `-k smoke` · checklist · **adelanto de performance (S6)** |

---

## Bloque A — CI/CD paso a paso (45 min)

### 1. El problema que resuelve CI

Imagina esta secuencia, que pasa todos los días en cualquier equipo:

1. Ana corre los tests en su máquina → todo **verde**.
2. Sube el código al repositorio.
3. En la máquina de Luis (o en el servidor) → **rojo**.

Nadie mintió: los entornos son distintos (otra versión de Python, otra dependencia, otro sistema operativo). Falta un lugar **neutral y común** donde los tests corran igual para todos, cada vez que alguien sube un cambio. Eso es CI.

### 2. Qué significan CI y CD

| Sigla | En una frase |
|---|---|
| **CI** (*Continuous Integration*) | Cada cambio que subes se **verifica solo** en un entorno controlado |
| **CD** (*Continuous Delivery/Deployment*) | Además se **prepara o despliega** de forma automatizada |

Hoy trabajamos **solo la verificación automática (CI)**. Desplegar es otro tema, para más adelante.

### 3. El ecosistema de herramientas (no las instalas todas)

Todas hacen lo mismo: **un evento dispara una serie de pasos, y el resultado es verde o rojo.**

| Herramienta | Rol en este curso |
|---|---|
| **GitHub Actions** | La que usamos hoy — el workflow es un archivo YAML dentro del repo |
| Jenkins / GitLab CI / Azure Pipelines | Solo como referencia: mismo patrón, otro archivo de configuración |

**El patrón es el que importa; la sintaxis exacta se aprende en una semana.** Elegimos GitHub Actions porque vive en el mismo repositorio del producto y no necesitas instalar nada.

### 4. Anatomía de un workflow de GitHub Actions

Abre `proyecto-integrador/ci-lab/workflows/qa-api.yml`. Es una copia didáctica del workflow real. Este es el archivo completo:

```yaml
name: QA API Gate (plantilla Sesión 5)

on:
  push:
    paths:
      - "proyecto-integrador/api-lab/**"
      - "proyecto-integrador/ci-lab/**"
  pull_request:
    paths:
      - "proyecto-integrador/api-lab/**"
      - "proyecto-integrador/ci-lab/**"
  workflow_dispatch:

permissions:
  contents: read

concurrency:
  group: qa-api-${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  api-tests:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: proyecto-integrador/api-lab
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v5
        with:
          python-version: "3.12"
          enable-cache: true
      - run: uv sync --group dev
      - run: uv run pytest -v
      - run: uv run pytest -v -k smoke
```

No lo memorices; apréndete qué pregunta responde cada clave:

| Clave | Pregunta que responde |
|---|---|
| `on:` | ¿**Cuándo** corre? (al hacer `push`, al abrir un `pull_request`, o con el botón manual `workflow_dispatch`) |
| `paths:` | ¿Ante **qué cambios**? (solo si tocaste `api-lab` o `ci-lab`, para no gastar minutos de más) |
| `permissions:` | ¿Con **qué permisos**? (`contents: read` = los mínimos necesarios) |
| `concurrency:` | ¿Qué pasa si subes dos cambios seguidos? (cancela la corrida vieja del mismo PR) |
| `jobs:` | ¿**Qué trabajos** se ejecutan? (aquí uno: `api-tests`) |
| `runs-on:` | ¿En **qué máquina**? (`ubuntu-latest`, un runner que GitHub presta) |
| `steps:` / `run:` | ¿**Qué comandos**, en qué orden? (checkout → instalar uv → `uv sync` → pytest → smoke) |

Fíjate en los tres últimos `run:`: son **los mismos comandos que corres a mano** en `api-lab`. Ese es el punto de toda la sesión.

### 5. La regla de oro (y por qué usamos Docker)

> El comando en el que confías localmente debe ser exactamente el mismo que corre en CI.

Si en tu máquina corres `uv run pytest -v` y en CI corre otra cosa, cualquier diferencia te va a explotar cuando menos lo esperas. **Docker** resuelve esto: empaqueta Python, las dependencias y los tests en una imagen, así tu máquina se comporta igual que el runner de GitHub.

En workflows modernos (2026) también vas a ver:

- `permissions: contents: read` — menos privilegios por defecto (seguridad).
- `concurrency` — cancela ejecuciones viejas del mismo PR para no gastar minutos.
- Caché de dependencias (`enable-cache: true`) — la segunda corrida es mucho más rápida.

---

## ☕ Descanso (15 min)

**Tarea opcional:** vuelve a mirar el YAML y cuenta cuántos `run:` hay. En el Bloque B vas a correr esos mismos comandos, pero dentro de Docker.

---

## Bloque B — Laboratorio: la suite en Docker (45 min)

### 1. Corre la suite dentro de un contenedor

Este es el laboratorio obligatorio. Desde `proyecto-integrador/ci-lab`:

```bash
docker compose build test
docker compose run --rm --no-deps test
```

- `build test` construye la imagen (la primera vez tarda; después usa caché).
- `run --rm --no-deps test` corre la suite y borra el contenedor al terminar (`--rm`).

**Antes de dar Enter, predice:** ¿esperas verde o rojo? ¿por qué?
**Resultado esperado:** `17 passed` dentro del contenedor — los mismos 17 tests de la Sesión 4.

### 2. Qué hay dentro del contenedor

Por dentro, el `Dockerfile` copia la suite de `api-lab` e instala las dependencias con `uv`. Lo esencial:

```dockerfile
FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:0.6.14 /uv /usr/local/bin/uv
WORKDIR /app
COPY api-lab/pyproject.toml api-lab/uv.lock ./
COPY api-lab/client ./client
COPY api-lab/conftest.py ./
COPY api-lab/data ./data
COPY api-lab/tests ./tests
RUN uv sync --group dev --frozen
CMD ["uv", "run", "pytest", "-v"]
```

El `docker-compose.yml` solo le da nombre al servicio `test` y define la URL de la API como variable de entorno (`API_BASE_URL`), con JSONPlaceholder por defecto.

### 3. Compara local vs Docker (opcional)

Si tienes `uv` instalado y conexión, corre la misma suite fuera de Docker:

```bash
cd ../api-lab
uv run pytest -v
```

**Resultado esperado:** `17 passed` también. Mismo comando, mismo resultado, otro entorno: eso es la regla de oro en acción.

> Si JSONPlaceholder está lento o caído, sigue con Docker y la lectura del YAML (Plan B). El objetivo de hoy es el entorno común, no la API pública.

### 4. Lee el workflow real

Abre `.github/workflows/qa-api.yml` (el que sí corre en GitHub) y anota:

1. ¿Qué eventos disparan el pipeline?
2. ¿En qué carpeta corre pytest? (pista: `working-directory`)
3. ¿Dónde está el filtro `smoke`?

| Evento | Cuándo se dispara |
|---|---|
| `push` / `pull_request` | Ante cambios (aquí filtrados por `paths`) |
| `workflow_dispatch` | Con un botón manual en la pestaña Actions de GitHub |

> **Concepto (no está en este archivo):** un cuarto disparador común es `schedule` (un cron), útil para correr la suite completa de noche. Lo vas a ver en la Sesión 6.

**Lo que lograste:** viste la misma suite pasar en un entorno controlado, no en una revisión "a ojo" en tu máquina.

---

## ☕ Descanso (15 min)

Sin tarea — llega fresco al mini-reto. 💪

---

## Bloque C — Mini-reto y cierre (45 min)

### Mini-reto: corre solo los tests smoke

Un test **smoke** es una verificación rápida de "¿lo básico funciona?". En una suite grande, correr primero los smoke da una respuesta en segundos.

```bash
cd proyecto-integrador/api-lab
uv run pytest -v -k smoke
```

(Sin `uv`: ese mismo paso ya está en el YAML como el último `run:`. Léelo y explica con tus palabras qué hace.)

**Resultado esperado:** pasan solo los tests marcados como smoke, en una fracción del tiempo de la suite completa.

**Pregunta de cierre:** en un PR de 40 archivos, ¿por qué correr primero un job smoke le ahorra tiempo al equipo?

### Checklist

- [ ] Puedo explicar CI en **una** frase
- [ ] Sé señalar `on`, `jobs` y `steps` en un workflow
- [ ] Corrí la suite dentro de Docker (`ci-lab`) y vi `17 passed`
- [ ] Entiendo la regla: el comando local debe ser el mismo que el de CI

### Frase de cierre (30 s)

Completa: *"CI sirve para ___ porque ___."*

### Para llevar

Hoy sumaste la **etapa de CI** al proyecto integrador: la suite de APIs puede correr sola en cada cambio, en un entorno igual para todo el equipo.

---

## Errores comunes

| Síntoma | Causa | Solución |
|---|---|---|
| `Cannot connect to the Docker daemon` | Docker Desktop no está corriendo | Ábrelo y espera a que diga **Running** |
| La primera build tarda mucho | Está descargando la imagen base y las dependencias | Es normal; la segunda vez usa caché y es rápida |
| Tests rojos por la red | JSONPlaceholder lento o caído | Plan B: quédate con Docker (imagen ya construida) + lectura del YAML |
| `uv: command not found` | No tienes `uv` instalado | El laboratorio de Docker **no** lo necesita; solo la comparación opcional |
| `no such service: test` | Corriste el comando fuera de `ci-lab` | `cd proyecto-integrador/ci-lab` primero |

---

## Resumen de comandos

```bash
cd proyecto-integrador/ci-lab
docker compose build test                    # construye la imagen (primera vez)
docker compose run --rm --no-deps test        # corre la suite en Docker (17 passed)

# Comparar con local (opcional)
cd ../api-lab
uv run pytest -v                              # misma suite, fuera de Docker
uv run pytest -v -k smoke                     # solo los tests smoke

# Atajo desde curso/
task test:ci
```

**Próxima sesión (S6):** Performance con K6 — la verificación también falla (rojo) si la API responde demasiado lento. 🚀
