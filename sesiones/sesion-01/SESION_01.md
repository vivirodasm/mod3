# Sesión 1 (Horas 1-3) — Diseño Técnico de Pruebas Automatizadas

> **Qué vas a lograr hoy:** convertir requisitos en casos de prueba usando cuatro técnicas concretas — partición de equivalencias (*Equivalence Partitioning*, EP), análisis de valores límite (*Boundary Value Analysis*, BVA), tablas de decisión y pruebas combinatorias por pares (*Pairwise Testing*). Al terminar tendrás un laboratorio corriendo en verde y la primera versión de tu matriz de trazabilidad, que conecta requerimientos, casos y defectos.

## Las herramientas que vamos a usar — y por qué

Antes de arrancar, hay que entender qué tenemos encima de la mesa. No necesitas memorizarlo todo ahora, solo ten claro para qué sirve cada cosa.

### `uv` — el gestor de entornos de Python

Python tiene un problema histórico: si instalas librerías directamente en tu sistema, tarde o temprano chocan entre sí. Un proyecto necesita la versión 1.x de algo, otro la 2.x, y el resultado son horas perdidas en errores que no tienen nada que ver con tu código.

`uv` resuelve eso. Crea una carpeta `.venv` por proyecto con solo las librerías que ese proyecto necesita, en las versiones exactas. Lo que instales ahí no toca nada más de tu máquina.

Por debajo hace tres cosas que importan:
- **Gestiona la versión de Python automáticamente.** Si no tienes la correcta, la descarga por ti.
- **Instala desde binarios pre-compilados.** Nada de compilar desde cero — detecta tu procesador (Intel, M1, M2, Windows) y descarga lo que corresponde.
- **Congela las versiones en `uv.lock`.** Ese archivo es una foto exacta de tus dependencias. Gracias a él, este laboratorio va a funcionar igual en tu máquina, en la de un compañero y en el servidor de integración continua.

### `Taskfile` — atajos para no escribir comandos largos

`Taskfile` no hace nada mágico. Agrupa comandos en alias cortos definidos en un archivo YAML. En lugar de escribir `cd proyecto-integrador/design-lab && uv run pytest -v --tb=short` cada vez, escribes `task test:design`.

A diferencia del clásico `Makefile`, funciona igual en macOS, Linux y Windows. Y como vive en el repo, también es documentación: cualquier persona que clone el proyecto sabe exactamente qué comandos existen y qué hacen.

**No es obligatorio.** Cada ejercicio incluye el comando equivalente por si no lo tienes instalado.

### `pytest` y `allpairspy` — el motor del laboratorio

`pytest` es el estándar de la industria para pruebas en Python. Lo usamos principalmente por la **parametrización**: escribes el código de un test una sola vez y lo ejecutas con decenas de combinaciones de datos. Agregar un caso nuevo es agregar una línea de datos, no duplicar código.

`allpairspy` implementa el algoritmo de pruebas por pares. Su trabajo es tomar una lista de parámetros con muchos valores posibles y calcular el subconjunto mínimo de combinaciones que garantiza que cada par de valores aparece al menos una vez junto.

### Git y Docker — lo que viene después

Hoy no los vas a usar, pero los vas a ver en el proyecto desde el principio:

- **Git** es el control de versiones. Toda la trazabilidad del código — quién cambió qué, cuándo y por qué — vive ahí. La revisión de trabajo mediante Pull Request (*PR*) es parte del flujo real que vamos a practicar.
- **Docker** aparece en sesiones posteriores. Permite levantar navegadores y bases de datos con un solo comando, tanto en tu máquina como en el servidor de automatización. El entorno es idéntico en ambos lados, sin sorpresas.

---

## Antes de empezar — prepara el entorno

Instala `uv` una sola vez (elige tu sistema):

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Verifica que quedó listo:

```bash
uv --version
```

Si vas a usar `task`, instálalo desde [taskfile.dev](https://taskfile.dev/installation/). Si no, sin problema — cada ejercicio tiene el comando completo.

Para inicializar el laboratorio de hoy:

```bash
cd proyecto-integrador/design-lab
uv sync
```

`uv sync` lee `pyproject.toml`, descarga todo lo necesario y lo deja listo en segundos.

---

# BLOQUE A (55 min) — Del requerimiento al caso de prueba

## A.1 El problema real (10 min)

Imagina este escenario: un equipo tiene 300 tests automatizados, la suite tarda 40 minutos en correr, todo pasa — y aun así producción se rompe con un pedido de exactamente $1,000.

¿Cómo es posible? Simple: **cantidad de tests no es lo mismo que cobertura de diseño**. Si nadie pensó en probar exactamente $1,000 — el límite entre "sin bono" y "con bono de volumen" — ese escenario no existe en la suite, no importa cuántos tests haya.

Los defectos no viven en los valores "cómodos" que uno elige al azar. Viven en los **límites** y en las **combinaciones de reglas** que nadie pensó de forma explícita.

El diseño técnico responde tres preguntas antes de escribir una sola línea de código:
1. **¿Qué probar?** → las técnicas de diseño (EP, BVA, tablas de decisión, pairwise) responden esto.
2. **¿Cuánto probar?** → la cobertura mínima suficiente, no exhaustiva.
3. **¿Cómo demostrar que está probado?** → la matriz de trazabilidad.

## A.2 Las técnicas — qué hace cada una (15 min)

**Partición de equivalencias (EP):** el sistema se comporta igual con todos los valores dentro de la misma clase. Por eso basta probar un valor representativo por clase, no todos. Regla fundamental: **incluir siempre las particiones inválidas** — ahí están los errores más frecuentes.

**Análisis de valores límite (BVA):** los errores se acumulan en las fronteras — en el `<` que debería ser `<=`, en el `>` que debería ser `>=`. Por cada límite se prueban el valor exacto y sus vecinos inmediatos.

**Tablas de decisión:** cuando hay N condiciones booleanas que interactúan, la tabla de 2^N reglas expone combinaciones que nadie habría pensado manualmente. Por ejemplo: ¿qué pasa cuando un cliente premium alcanza el umbral de volumen *y* encima tiene cupón? Sin la tabla, ese caso no existe en la suite.

**Pruebas combinatorias por pares (Pairwise Testing):** la mayoría de los defectos de interacción involucran como máximo 2 parámetros. Cubrir todos los *pares* posibles reduce 54 combinaciones a unas 12 filas sin perder casi nada en detección de defectos.

**Mantenibilidad — por diseño, no por accidente:**
- **Reusabilidad:** el caso parametrizado es la unidad reutilizable. Agregar un caso nuevo es agregar una línea de datos.
- **Desacoplamiento:** los datos viven en archivos YAML (*YAML Ain't Markup Language*) o CSV (*Comma-Separated Values*) fuera del código del test. Un analista puede modificarlos sin tocar Python.
- **Modulación:** un archivo por técnica. La lógica que se prueba vive separada de los tests.

## A.3 Trazabilidad — el contrato del conjunto de pruebas (10 min)

Tres identificadores son todo lo que necesitamos: `REQ` para requerimiento, `TC` para caso de prueba (*Test Case*) y `DEF` para defecto.

```
  REQUERIMIENTO            CASO DE PRUEBA              DEFECTO
 ┌──────────────┐  1..N  ┌─────────────────┐  0..N  ┌──────────┐
 │ REQ-DSC-002  │───────►│ TC-DSC-BVA-004  │───────►│ DEF-017  │
 │ "≥1000 → +5%"│        │ límite 1000.00  │        │ off-by-1 │
 └──────────────┘        └─────────────────┘        └──────────┘
        ▲                        │
        │   La matriz responde:  ▼
        │   "¿Qué REQ queda sin TC?"  → hueco de cobertura
        └── "¿Qué TC no mapea a REQ?" → test zombie (candidato a borrar)
```

La matriz vive en `proyecto-integrador/trazabilidad/matriz-trazabilidad.csv` y los identificadores de parametrización de pytest coinciden con los `tc_id` de esa matriz. La idea es tener **trazabilidad ejecutable** — no un Excel que nadie actualiza.

## A.4 Del ejemplo sencillo al mundo real (10 min)

**Primero, algo simple:** un campo "edad" que acepta valores entre 18 y 65.
- EP: `<18` (inválida), `18-65` (válida), `>65` (inválida), no numérico (inválida).
- BVA: `17, 18, 65, 66` → 4 tests que cubren toda la frontera.

**Ahora en el laboratorio.** Abre el archivo:

```
proyecto-integrador/design-lab/design_lab/discount.py
```

En las primeras líneas vas a encontrar las constantes y la función que usaremos durante toda la sesión:

```python
VOLUME_THRESHOLD = 1_000.0   # umbral de bono por volumen (REQ-DSC-002)
DISCOUNT_CAP     = 15.0      # tope máximo de descuento  (REQ-DSC-004)

def calculate_discount(customer_type: str, order_total: float, has_coupon: bool) -> float:
    """
    REQ-DSC-001: premium → +10 %; standard → +0 %
    REQ-DSC-002: order_total >= 1000 → +5 % (bono por volumen)
    REQ-DSC-003: has_coupon → +5 %
    REQ-DSC-004: el descuento total nunca excede 15 %
    REQ-DSC-005: 0 < order_total <= 10 000; de lo contrario lanza ValueError
    """
```

Los cinco requerimientos están en ese docstring. La implementación debajo es lo que vamos a probar. Los `REQ-DSC-*` son los mismos que aparecen en la matriz de trazabilidad:

```
proyecto-integrador/trazabilidad/matriz-trazabilidad.csv
```

Cuando alguien revisa tu trabajo en un Pull Request (PR), lo primero que valida no es el código del test, sino esto: "¿la parametrización cubre la tabla completa? ¿están los límites del REQ-DSC-002?". El código viene después.

## A.5 Demo — cómo se derivan los casos (10 min)

Vamos a derivar los casos directo desde los requerimientos que acabas de leer:

1. **REQ-DSC-005** dice `0 < order_total <= 10000`. De ahí salen tres particiones:
   - Inválida baja: cualquier valor `≤ 0` (por ejemplo, `0` o `-50`).
   - Válida: cualquier valor en `(0; 10000]` (por ejemplo, `500`).
   - Inválida alta: cualquier valor `> 10000` (por ejemplo, `10000.01`).

2. **BVA sobre ese rango:** los cuatro puntos que hay que probar son `0` (inválido, frontera exclusiva), `0.01` (el primer válido), `10000` (el último válido) y `10000.01` (inválido). Con esos cuatro valores queda cubierta toda la frontera.

3. **REQ-DSC-002** tiene su propio límite interno en `1000`: probar `999.99` (sin bono) y `1000.00` (con bono) captura el típico error de `<` donde debería ir `<=`.

4. **Condiciones que interactúan:** ¿es premium? / ¿total ≥ 1000? / ¿tiene cupón? → 2³ = 8 reglas. La regla R8 es `premium + volumen + cupón = 20 %`, pero el tope del REQ-DSC-004 lo recorta a `15 %`. Ese caso solo aparece cuando construyes la tabla completa — jamás lo encontrarías probando al azar.

5. Cada caso entra en `matriz-trazabilidad.csv` con su `tc_id` (por ejemplo `TC-DSC-BVA-004`) y la técnica usada.

> ☕ **Descanso 5 min**

---

# BLOQUE B (55 min) — Laboratorio guiado

## B.1 Estructura y primer arranque (15 min)

Así está organizado lo que vamos a usar hoy:

```
curso-automatizacion-apis-performance-seguridad/
├── Taskfile.yml                      ← atajos opcionales para ejecutar comandos del curso
├── proyecto-integrador/
│   ├── trazabilidad/matriz-trazabilidad.csv
│   └── design-lab/                   ← laboratorio práctico de hoy en Python
│       ├── pyproject.toml            ← dependencias declaradas del laboratorio
│       ├── design_lab/
│       │   ├── discount.py           ← regla de negocio que vamos a probar
│       │   └── pairwise_matrix.py    ← generación pairwise + análisis de huecos de cobertura
│       ├── data/decision_table.yaml  ← datos desacoplados de la lógica
│       └── tests/
│           ├── test_equivalence_boundary.py
│           ├── test_decision_table.py
│           └── test_pairwise.py
└── sesiones/sesion-01/SESION_01.md   ← este documento
```

Para correr la suite completa:

```bash
cd curso-automatizacion-apis-performance-seguridad
task setup          # instala las dependencias del laboratorio
task test:design    # corre todos los tests de la sesión
```

Sin `task`:

```bash
cd proyecto-integrador/design-lab
uv sync
uv run pytest -v
```

## B.2 EP + BVA ejecutables (15 min)

Abre el archivo:

```
proyecto-integrador/design-lab/tests/test_equivalence_boundary.py
```

Vas a encontrar tres bloques de parametrización. Léelos antes de ejecutar:

**Bloque 1 — particiones válidas** (`VALID_PARTITIONS`): cuatro filas, una por partición. El cuarto argumento es el resultado esperado y el `id` coincide exactamente con el `tc_id` de la matriz:

```python
pytest.param("standard", 500.0, False, 0.0,  id="TC-DSC-EP-001-standard-base"),
pytest.param("premium",  500.0, False, 10.0, id="TC-DSC-EP-002-premium-base"),
```

**Bloque 2 — valores límite** (`BOUNDARIES`): los cuatro puntos críticos del rango y del umbral de volumen. El test usa siempre `"standard"` sin cupón para aislar únicamente el efecto del monto:

```python
pytest.param(   0.01, 0.0, id="TC-DSC-BVA-001-minimo-valido"),
pytest.param( 999.99, 0.0, id="TC-DSC-BVA-003-justo-bajo-umbral-volumen"),
pytest.param(1000.00, 5.0, id="TC-DSC-BVA-004-umbral-volumen-exacto"),   # ← límite REQ-DSC-002
pytest.param(10_000.00, 5.0, id="TC-DSC-BVA-005-maximo-valido"),
```

**Bloque 3 — particiones inválidas** (`INVALID_PARTITIONS`): cuatro entradas que deben lanzar `ValueError`. El `pytest.raises(ValueError)` no es manejo de errores — es un **requerimiento ejecutable** (REQ-DSC-005). Si el código no lanza la excepción, el test falla.

> **Regla de oro:** agregar una partición nueva es agregar una línea de datos. El test no cambia.

## B.3 Tabla de decisión con datos externos (15 min)

Abre primero los datos:

```
proyecto-integrador/design-lab/data/decision_table.yaml
```

Vas a ver las 8 reglas (2³ condiciones: ¿premium? / ¿≥1000? / ¿cupón?). Busca la regla DT-R8:

```yaml
- id: DT-R8
  customer_type: premium
  order_total: 1500.0
  has_coupon: true
  expected: 15.0   # REQ-DSC-004: tope — sin la tabla, este caso nunca aparecería
```

`premium(10) + volumen(5) + cupón(5) = 20 %`, pero el tope del REQ-DSC-004 lo recorta a `15 %`. Este caso no aparece probando al azar. Solo la tabla completa lo expone.

Ahora abre el test:

```
proyecto-integrador/design-lab/tests/test_decision_table.py
```

Fíjate en dos cosas:
1. `load_rules()` lee el YAML y convierte cada fila en un `pytest.param`. Un analista puede editar las reglas **sin tocar Python** — eso es desacoplamiento real.
2. `test_decision_table_is_complete` cuenta las combinaciones únicas de condiciones y falla si hay menos de 8. Si alguien borra una regla por accidente, la suite lo detecta antes de que llegue a revisión.

## B.4 Pairwise + análisis de huecos de cobertura (10 min)

Abre el test:

```
proyecto-integrador/design-lab/tests/test_pairwise.py
```

El escenario: 3 navegadores × 3 sistemas operativos × 2 idiomas × 3 roles = **54 combinaciones**. Pairwise las reduce a ~10 filas cubriendo todos los pares.

Lee la restricción de negocio del archivo (líneas 24-28):

```python
def is_valid_combination(row: list) -> bool:
    """webkit (motor de Safari) solo corre en macOS."""
    if row[0] == "webkit" and row[1] != "macos":
        return False
    return True
```

**Hallazgo real que vas a ver documentado ahí:** con esa restricción, el algoritmo interno de `allpairspy` dejó fuera los pares `(chromium, macos)` y `(firefox, macos)` — huecos reales que no aparecen en la documentación de la herramienta.

Para resolverlo, abre:

```
proyecto-integrador/design-lab/design_lab/pairwise_matrix.py
```

El patrón tiene tres pasos: **generar → auditar los pares exigibles → completar los que faltan**. Un par es "exigible" solo si existe al menos una combinación válida completa que lo contenga. Los pares imposibles por la restricción no se exigen.

El test `test_pairwise_covers_every_achievable_pair` corre ese análisis y falla si quedan huecos. La moraleja: nunca asumas que una herramienta garantiza algo — demuéstralo con un test.

> ☕ **Descanso 5 min**

---

# BLOQUE C (60 min) — Tu turno

## C.1 Ejercicio individual (25 min) — Diseño del login de SauceDemo

Hoy solo diseñamos los casos. La automatización de la pantalla de login llega en la Sesión 2. Abre en el navegador:

```
https://www.saucedemo.com
```

Dedica 3 minutos a explorar la página antes de diseñar. Esto es lo que vas a observar:
- Hay 4 usuarios de prueba: `standard_user`, `locked_out_user`, `problem_user`, `performance_glitch_user`.
- Todos comparten la misma contraseña: `secret_sauce`.
- `locked_out_user` recibe un mensaje de error diferente al de credenciales incorrectas.
- Usuario o contraseña incorrectos muestran un mensaje de error genérico.
- Un login exitoso redirige a `/inventory.html`.

**Tu tarea** — edita el archivo:

```
proyecto-integrador/trazabilidad/matriz-trazabilidad.csv
```

Ya tiene encabezados y tres filas marcadas como `PENDIENTE` para `REQ-LOG-001`, `REQ-LOG-002` y `REQ-LOG-003`. Esto significa cada columna:

| Columna | Qué escribir |
|---|---|
| `req_id` | Identificador del requerimiento (ej. `REQ-LOG-001`) |
| `requerimiento` | Lo que observaste en la página, redactado como requerimiento |
| `tc_id` | Identificador del caso (ej. `TC-LOG-EP-001`) |
| `caso_de_prueba` | Qué entra y qué resultado se espera |
| `tecnica` | `Partición de equivalencias`, `Análisis de valores límite` o `Tabla de decisión` |
| `archivo_prueba` | Dejar vacío — se completa en la Sesión 2 cuando se automatice |
| `estado` | `DISEÑO` — el caso está definido pero aún no automatizado |
| `def_id` | Dejar vacío |

**Una fila ya completada del bloque de descuento, como referencia:**

```
REQ-DSC-002,Pedido >= 1000 suma 5% por volumen,TC-DSC-BVA-004,Límite exacto del umbral: 1000.00 → con bono de volumen,Análisis de valores límite,tests/test_equivalence_boundary.py,PASS,
```

**Cómo completar el ejercicio, paso a paso:**

1. **Escribe los requerimientos observables.** Por ejemplo:
   - `REQ-LOG-001`: "Credenciales válidas redirigen al inventario (`/inventory.html`)"
   - `REQ-LOG-002`: "El usuario bloqueado recibe un mensaje específico, diferente al de credenciales incorrectas"
   - `REQ-LOG-003`: "Campos vacíos o credenciales inválidas muestran un mensaje de error"

2. **Deriva las particiones de equivalencia** para los dos campos:
   - Usuario: válido activo / válido bloqueado / inexistente / vacío
   - Contraseña: correcta / incorrecta / vacía
   - Pregunta clave: ¿qué combinaciones producen el mismo resultado? Las que sí, colapsan en una sola partición.

3. **Construye la tabla de decisión** con tres condiciones: ¿el usuario existe? / ¿la contraseña es correcta? / ¿el usuario está bloqueado? → 2³ = 8 reglas posibles. Elimina las que son imposibles — no puede haber contraseña correcta si el usuario no existe.

4. Asigna un `tc_id` con prefijo `TC-LOG-*` a cada caso. Si identifies más requerimientos, agrega filas.

**¿Cómo saber si quedó bien?** Cada `REQ-LOG-*` tiene al menos un TC, cada TC declara su técnica, y hay al menos una partición inválida (campo vacío) y una regla de decisión con las 3 condiciones.

## C.2 Mini reto (20 min) — Pairwise para una matriz web

La matriz de compatibilidad del proyecto es: navegador `{chromium, firefox, webkit}` × tamaño de pantalla `{mobile, tablet, desktop}` × tema `{light, dark}` × rol `{admin, user}` = **36 combinaciones**.

1. En `tests/test_pairwise.py`, agrega una constante `PARAMETERS_LOGIN` con esos 4 parámetros.
2. Restricción de equipo: el rol `admin` no se prueba en pantalla `mobile`.
3. Genera la matriz pairwise y escribe un test que demuestre: (a) que el total es menor que 36, (b) que la restricción se respeta, y (c) que todos los pares `(tamaño de pantalla, tema)` están cubiertos.
4. **Justifica en 2 líneas** — en un comentario del Pull Request, no en el código: ¿qué tipo de defectos podrían escaparse con pairwise en vez del producto cartesiano y por qué ese intercambio vale la pena?

## C.3 Errores comunes — qué evitar y qué hacer (15 min)

| ❌ Error común | ✅ Práctica correcta |
|---|---|
| Probar solo el "camino feliz" con valores arbitrarios (`total=500`) | Cada valor de test viene de una técnica y es trazable a un REQ |
| Un test gigante con 15 asserts que mezcla particiones | Un caso parametrizado por diseño; el `id` es el `tc_id` de la matriz |
| Datos incrustados en el código del test | Datos en YAML o CSV versionados en `data/`, lógica en `tests/` |
| Matriz de trazabilidad en un Excel que nadie actualiza | CSV en el repo, revisado en el PR junto al código que traza |
| "Más tests = más calidad" → suites de 40 min con huecos de frontera | Cobertura mínima suficiente: EP + BVA + tabla + pairwise |
| Ignorar particiones inválidas ("eso nunca pasa") | `pytest.raises` como caso de primera clase (REQ-DSC-005) |
| Copiar y pegar el mismo test cambiando solo un número | `@parametrize`: agregar un caso = agregar una línea de datos |

**Lo que hiciste hoy en términos de código limpio:** nombres de test que describen comportamiento (`test_invalid_partitions_raise`), constantes de negocio con nombre propio (`VOLUME_THRESHOLD` en lugar del número `1000` suelto en el código), un archivo por técnica, y validaciones preventivas que protegen el diseño (`test_decision_table_is_complete`).

---

## ¿Quedó todo? — Lista de salida

- [ ] `task setup && task test:design` corre en verde: EP, BVA, tablas de decisión y pairwise.
- [ ] `matriz-trazabilidad.csv` con los REQ-DSC-* verificados y los REQ-LOG-* completados por ti.
- [ ] Mini reto pairwise implementado y pasando.
- [ ] Puedes explicar en 1 minuto por qué DT-R8 no existiría sin tabla de decisión.

**Próxima sesión (S2):** estos diseños se convierten en pruebas automatizadas de la interfaz de usuario (*User Interface*, UI) de SauceDemo, usando **Page Object Model**, **Screenplay** y el principio **Don't Repeat Yourself** (DRY), estados de prueba compartidos (*fixtures*) y datos externos en JSON (*JavaScript Object Notation*), YAML y CSV. La matriz de trazabilidad crece con los `TC-LOG-*` ya automatizados.
