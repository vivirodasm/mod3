# Día 2 — Testing IA/ML, datos, RPA y madurez TMMi

> **Duración:** 4 horas · **Ritmo:** Bloque A (45) → descanso 15 → B (45) → descanso 15 → C (45) → descanso 15 → D (45)
> **Lo que vas a construir:** un plan de testing ejecutable para datos ETL + modelo ML (Great Expectations, precisión/sesgo/drift, MLflow) integrado a un pipeline CI de ejemplo.
> **Este día es autónomo:** no necesitás tener Docker ni el lab del Día 1 levantados.

---

## Antes de empezar

### Requisitos

| Herramienta | Windows | macOS |
|-------------|---------|-------|
| Python 3.11+ | [python.org](https://www.python.org/downloads/) o Store | `brew install python` |
| **uv** (recomendado) | Ver abajo | Ver abajo |
| Git | Opcional pero útil | Opcional pero útil |
| Editor | VS Code / Cursor | VS Code / Cursor |

### Instalar `uv`

**Windows (PowerShell):**

```powershell
irm https://astral.sh/uv/install.ps1 | iex
```

Cerrá y reabrí la terminal. Verificá:

```powershell
uv --version
```

**macOS:**

```bash
brew install uv
# o:
curl -LsSf https://astral.sh/uv/install.sh | sh
```

```bash
uv --version
```

### Arranque del laboratorio

```bash
# Desde la carpeta del Día 2
cd curso6/dia2/proyectos/ml-data-quality-lab

# 1) Instala dependencias en un entorno local del proyecto
uv sync

# 2) Corre la suite
uv run pytest -v
```

**Resultado esperado:** `5 passed`.

Si falla aquí, **paré** y mirá [Errores comunes](#errores-comunes).

---

## Agenda

| Bloque | Duración | Contenido |
|--------|----------|-----------|
| **A** | 45 min | Testing de IA/ML + pipelines de datos (ETL) |
| Descanso | 15 min | ☕ |
| **B** | 45 min | **Reto 2:** plan de testing ML/datos + CI |
| Descanso | 15 min | ☕ |
| **C** | 45 min | RPA · simulación de usuarios · gamificación |
| Descanso | 15 min | ☕ |
| **D** | 45 min | TMMi, estrategia de madurez y cierre |

Material de apoyo:
- Diapositivas: `ppt_contenido.md` / `dia2.pptx`
- Guion del instructor: `instructor_guide.md`

---

## Bloque A — Testing IA/ML y pipelines de datos (45 min)

### 1. Por qué testing de IA es distinto

En APIs un `assert status_code == 200` te salva mucho.  
En IA **no alcanza**:

- Un modelo puede “andar” y ser injusto (sesgo / fairness)  
- Puede quedar viejo por **drift** (los datos de hoy no se parecen a los de entrenamiento)  
- Si el **ETL** ensucia, el modelo hereda el bug con sonrisa de accuracy  

### 2. Validación de modelos (mapa del temario)

| Concepto | Pregunta que responde |
|----------|------------------------|
| Precisión | ¿Acertamos lo que importa? |
| Sesgo / fairness | ¿El error castiga a un grupo? |
| Drift | ¿Hoy ya no nos parecemos al entrenamiento? |

Herramientas del mapa oficial:

- **DeepChecks** — suites de validación de ML  
- **Amazon SageMaker Model Monitor** — drift en producción (concepto cloud)  
- **MLflow** — tracking de experimentos y métricas  
- **DVC** — versionado de datos/modelos  

### 3. Testing de pipelines ETL/ELT

Chequeos típicos:

- Nulos  
- Duplicados  
- Formatos (ej. email)  
- Rangos e integridad (valores permitidos)  

Herramientas del temario: **Great Expectations · Deequ · Soda Core · DBT**.

En el lab usamos **Great Expectations** + una suite estilo expectativas en Python.

### 4. Plan de testing (el que vas a ejecutar)

1. Validar datos de entrada (ETL)  
2. Entrenar / evaluar modelo  
3. Medir precisión  
4. Medir fairness (proxy por región)  
5. Medir drift vs referencia (PSI de income)  
6. Publicar resultado en CI + MLflow  

### 5. Preview de comandos del lab

```bash
cd curso6/dia2/proyectos/ml-data-quality-lab
uv sync
uv run pytest -v
uv run python -m src.run_pipeline
```

---

## Bloque B — Reto 2: plan de testing ML + datos (45 min)

### Enunciado

Diseñar y ejecutar un plan que valide:

- precisión  
- sesgo  
- drift de datos  
- integridad del pipeline ETL  

…integrando resultados en un pipeline CI/CD (workflow de ejemplo incluido).

Carpeta del lab: `proyectos/ml-data-quality-lab`

### Paso 1 — Entorno

```bash
cd curso6/dia2/proyectos/ml-data-quality-lab
uv sync
```

### Paso 2 — Suite ETL (patrón Great Expectations)

```bash
uv run pytest tests/test_data_quality.py -v
```

**Qué valida:** nulos, `customer_id` único, regiones permitidas, rangos age/income, formato email.

Abrí `src/data_quality.py` y leé los nombres de las expectativas (`expect_column_values_to_not_be_null`, etc.).

Dataset sucio (para ver fallos a propósito):

```bash
uv run python -c "from src.generate_data import build_current_with_issues; from src.data_quality import run_etl_suite, suite_passed; r=run_etl_suite(build_current_with_issues()); print(suite_passed(r)); print([x for x in r if not x.success])"
```

Debería imprimir `False` y listar expectations rotas.

### Paso 3 — Great Expectations (API real)

```bash
uv run pytest tests/test_gx_integration.py -v
```

Suite ephemeral sobre el dataset limpio. Contrato de datos ejecutable.

### Paso 4 — Modelo + MLflow

```bash
uv run pytest tests/test_model_checks.py -v
uv run python -m src.run_pipeline
```

**Resultado esperado del pipeline:** JSON con `"overall_passed": true` y archivo `data/pipeline_report.json`.

Umbrales del lab:

| Chequeo | Umbral |
|---------|--------|
| Precisión | ≥ 0.70 |
| Gap de fairness por región | ≤ 0.25 |
| PSI drift (income) | ≤ 0.25 |

Tracking MLflow: SQLite en `mlruns/mlflow.db` (se crea solo).

### Paso 5 — CI de ejemplo

Abrí `.github/workflows/quality.yml`.

Verás los mismos comandos que corriste en local (`uv sync`, `pytest`, `run_pipeline`).

Frase para llevarte: **si no corre en CI, no es gobernanza — es hobby.**

### Entregable / checklist del Reto 2

- [ ] `uv run pytest -v` → **5 passed**  
- [ ] `uv run python -m src.run_pipeline` → `overall_passed: true`  
- [ ] Entendés qué falla en el dataset sucio  
- [ ] Abriste el workflow de CI y reconocés los pasos  
- [ ] Podés explicar precisión vs fairness vs drift en una frase cada uno  

### Preguntas de cierre

1. ¿En tu empresa fallaría primero la calidad de **datos** o la del **modelo**?  
2. ¿Quién debería ser dueño del umbral de drift?  

---

## Bloque C — RPA, simulación de usuarios y gamificación (45 min)

### 1. RPA para validación de procesos

Bots que ejercitan procesos de negocio repetitivos (backoffice, altas, conciliaciones).

**No reemplaza** pruebas de API/UI bien hechas: **complementa** cuando el proceso completo es el sistema bajo prueba.

| Plataforma | Nota |
|------------|------|
| UiPath | Muy usado en empresa |
| Power Automate | Fuerte en ecosistema Microsoft |
| Automation Anywhere | Automatización de procesos a escala |

Criterio de selección: stack IT + licencias + observabilidad de resultados.

Casos de uso:

- Regresión de altas de cliente  
- Smoke de backoffice post-deploy  
- Verificación de reportes batch  

Evidencia mínima: capturas + logs + ID de transacción.

### 2. Simulación de usuarios reales con IA

Idea del temario:

- Modelar comportamiento (no solo scripts lineales)  
- Escenarios realistas (incluye reinforcement learning como concepto)  
- Pruebas basadas en patrones de uso reales  

```
Script fijo → caminos probables → política aprendida
```

Objetivo: encontrar bugs que el camino feliz no ve. Requiere telemetría ética.

### 3. Formación, simulación y gamificación

- Simuladores de entornos de testing  
- Retos con scoring automático  
- Plataformas: **Test Automation University**, **Codecademy**  

Los Retos 1 y 2 de este curso **son** gamificación seria: objetivo claro, score automático (tests/métricas), feedback inmediato.

### Mini-caso integrado (anotá tu respuesta)

Proceso de crédito:

1. RPA valida carga en backoffice  
2. Great Expectations valida dataset ETL  
3. Modelo ML decide aprobación  
4. Dashboard QA alerta leakage  

Si solo pudieras poner **un** control hoy, ¿dónde lo pondrías y por qué?

---

## Bloque D — TMMi y estrategia de madurez (45 min)

### 1. ¿Qué es TMMi?

**Test Management Maturity Model Integration**

No es una herramienta que se instala: es un **mapa de madurez** de la organización de testing (niveles + prácticas recomendadas).

### 2. Niveles (visión práctica)

```
Inicial → Gestionado → Definido → Medido → Optimizado
```

- Métricas + dashboards (Día 1) empujan hacia **Medido**  
- Retos en CI (Día 2) empujan hacia **Optimizado**  

Pregunta: del 1 al 5, ¿dónde está tu equipo hoy?

### 3. Estrategia sostenible (cadena completa)

1. Políticas (gobernanza)  
2. Métricas con umbral  
3. Observabilidad (Prometheus / Grafana / Kibana-Loki)  
4. Datos + ML validados  
5. Procesos RPA + aprendizaje gamificado  
6. Madurez TMMi  

### 4. Tablero de decisión

| Si duele… | Empezá por… |
|-----------|-------------|
| CI rojo por flake | bajar flake rate |
| Bugs en prod | leakage + alcance por riesgo |
| Modelo injusto | fairness + datos |
| Proceso manual frágil | RPA de validación |
| Nadie sabe el estado | dashboard de gobernanza |

### 5. Checklist final del curso (Certificación 6)

- [ ] Sé explicar flake, leakage y effectiveness  
- [ ] Levanté / usé el dashboard QA (Día 1) **o** entiendo el flujo  
- [ ] Corrí el lab de datos/ML (Día 2)  
- [ ] Ubico RPA, simulación y gamificación en la estrategia  
- [ ] Relaciono todo con un nivel TMMi  

### Dos pedidos para el lunes

1. Elegí **un umbral** y **un dueño**  
2. Publicá **al menos una métrica** donde todo el equipo la vea  

Madurez no es un certificado en la pared: es un hábito medible.

---

## Errores comunes

| Error / síntoma | Causa probable | Solución |
|-----------------|----------------|----------|
| `uv: command not found` | uv no instalado o PATH viejo | Reinstalá uv y **reabrí** la terminal |
| `python: command not found` | Python no en PATH | Windows: instalá Python marcando “Add to PATH”; Mac: `python3` |
| Falla `uv sync` por red/proxy | Restricción corporativa | Reintentá; si persiste, pedí al instructor el plan B (wheelhouse / mirror) |
| `ModuleNotFoundError: src` | Corrés fuera de la carpeta del lab | `cd` a `ml-data-quality-lab` y usá `uv run` |
| Test de GE falla con API distinta | Versión de Great Expectations | `uv sync` de nuevo (lockfile del repo) |
| MLflow error de file store | Backend viejo | El lab usa SQLite (`mlruns/mlflow.db`); no fuerces `./mlruns` a mano |
| pytest 4 passed / 1 failed | Modelo o datos drift | Corré `uv run python -m src.generate_data` vía pipeline; no edites umbrales sin entenderlos |
| Workflow CI no corre en GitHub | El YAML vive dentro del proyecto | Es un **ejemplo**; GitHub solo lee `.github/workflows` en la raíz del repo. Podés copiarlo allí si versionás el monorepo |

---

## Comandos útiles (atajo)

```bash
cd curso6/dia2/proyectos/ml-data-quality-lab

uv sync
uv run pytest -v
uv run pytest tests/test_data_quality.py -v
uv run pytest tests/test_gx_integration.py -v
uv run pytest tests/test_model_checks.py -v
uv run python -m src.run_pipeline

# Ver reporte
# macOS/Linux:  cat data/pipeline_report.json
# Windows:      Get-Content data/pipeline_report.json
```

Script opcional (macOS/Linux/Git Bash):

```bash
chmod +x scripts/run_tests.sh
./scripts/run_tests.sh
```

---

## Mapa de archivos del lab (orientación)

| Ruta | Para qué |
|------|----------|
| `src/generate_data.py` | Datasets sintéticos limpio / sucio / referencia |
| `src/data_quality.py` | Suite ETL estilo Great Expectations |
| `src/model_checks.py` | Precisión, fairness proxy, drift + MLflow |
| `src/run_pipeline.py` | Pipeline end-to-end |
| `tests/` | Tests automatizados del Reto 2 |
| `.github/workflows/quality.yml` | Ejemplo de CI |

---

## Para llevar

Después del Día 2 tenés:

- Plan de testing para datos + modelo (ejecutable)  
- Experiencia con Great Expectations + MLflow  
- Criterios para ubicar RPA y simulación de usuarios  
- Marco TMMi para hablar de madurez sin humo  

Junto con el Día 1: **gobernanza de punta a punta** (sistema de pruebas observable + datos/modelos validados en CI).
