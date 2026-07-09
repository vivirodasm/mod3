# Guía del Instructor — Sesión 2

> Este documento es de uso exclusivo del instructor. No compartir con estudiantes.
> Referencia las slides de `PPT_CONTENIDO.md` y el código en `proyecto-integrador/ui-lab/`.

---

## Preparación previa a la sesión

Haz esto antes de que lleguen los estudiantes:

```bash
cd proyecto-integrador/ui-lab
uv sync --group dev
uv run playwright install chromium
uv run pytest -v   # confirmar que los 13 tests pasan
```

Ten SauceDemo abierta en el navegador con las DevTools listas para mostrar los `data-test` attributes.
Prepara dos ventanas de VS Code: una con `pages/login_page.py` y otra con `tests/test_login_pom.py`.

---

## Bloque A — El problema y los patrones (45 min)

### Slide 1 — Portada (1 min)

Preséntate brevemente. Menciona que esta sesión es 80% código y 20% conceptos.
Di explícitamente: *"Al final de hoy van a tener un framework de UI funcional que pueden ejecutar ahora mismo."*

---

### Slide 2 — Agenda (2 min)

Muestra el mapa de la sesión. Énfasis en que los bloques tienen pausas reales.
Pregunta rápida al grupo: *"¿Alguien ya escribió tests de UI antes? ¿Selenium, Cypress, Playwright?"*
Usa las respuestas para calibrar la profundidad de la explicación del Bloque A.

---

### Slide 3 — El problema (8 min)

**Puntos clave a enfatizar:**
- El código espagueti no es un error de principiante — es lo que pasa naturalmente si no hay estructura.
- El problema real no es que el test sea largo, sino que **el mantenimiento escala mal**.
- Ejemplo real: *"En un proyecto real con 200 tests y una refactoring del equipo de front-end, vi 6 horas perdidas buscando y reemplazando selectores."*

**Demo en vivo (opcional pero recomendada):**
Abre SauceDemo en el navegador → F12 → muestra los atributos `data-test` en el input de username.
*"Este `data-test` es el locator. Si mañana el equipo de front-end lo renombra, ¿qué pasa con tus tests?"*

**Pregunta para el grupo:** *"¿Cuántas veces aparecería `[data-test="login-button"]` si tienes 40 tests de regresión?"*

---

### Slide 4 — POM concepto (5 min)

**Puntos clave:**
- POM no es una librería ni un framework — es una **convención de organización**.
- El prefijo underscore (`self._login_btn`) es una señal para el equipo: "este atributo es interno, no lo uses directamente desde el test."
- La **interfaz fluida** (`return self`) permite encadenar: `.go_to().login(...)` — más legible que dos líneas separadas.

**Pregunta para el grupo:** *"¿Por qué creen que los locators son privados y los métodos son públicos?"*
Respuesta esperada: porque el test no debería saber nada de la implementación interna de la pantalla.

---

### Slide 5 — Test con POM (5 min)

Abre `tests/test_login_pom.py` en vivo.
Señala que el test tiene **cero selectores CSS** — solo llama nombres de negocio.
*"Este test lo puede leer el Product Owner sin saber nada de Python."*

**Énfasis crítico:** el test describe el **qué** (login exitoso redirige al inventario), no el **cómo** (fill, click, goto). Esa separación es lo que hace el código mantenible.

---

### Slide 6 — Estructura de Pages (3 min)

Abre el explorador de archivos de VS Code y muestra la carpeta `pages/`.
*"Tres archivos, tres pantallas. Si la app tuviera 20 pantallas, tendríamos 20 Page Objects."*
Señala el patrón de naming: locators privados (`_`), acciones públicas, consultas de estado.

---

### Slide 7 — Screenplay concepto (8 min)

**Antes de mostrar código:**
*"Imaginen que tienen un test donde un admin configura algo y luego un usuario regular verifica que lo ve. Con POM, ¿cómo distinguen qué acciones hace el admin y cuáles el usuario?"*
Pausa para que el grupo piense. La respuesta natural es "con comentarios" — exactamente el problema que Screenplay resuelve estructuralmente.

**Énfasis:** Screenplay no reemplaza POM, lo usa. Las Tasks llaman internamente a los Page Objects.

---

### Slide 8 — Test con Screenplay (7 min)

Abre `tests/test_login_screenplay.py` en vivo.
Muestra los dos ejemplos lado a lado (usa split screen o dos archivos).

**Pregunta clave:** *"¿Cuál es más legible? ¿Cuál prefieren?"*
No hay respuesta incorrecta — el objetivo es que el equipo debate y lleguen a su propia conclusión.

**Abrir `screenplay/actor.py`:** muestra el método `attempts_to`. Es simple: un loop.
*"No hay magia. El patrón es simple; lo que añade es intención y estructura."*

---

### Slide 9 — POM vs Screenplay (3 min)

La tabla es clara. Énfasis: **no hay un ganador absoluto**.
En el proyecto integrador del curso usan POM como base y Screenplay en los flujos complejos de la Sesión 5 (CI/CD con múltiples actores).

---

### Slide 10 — DRY y KISS (3 min)

Estos principios aparecen en **todas** las sesiones del curso. Introdúcelos bien aquí.
- DRY: *"Si copiaste código, algo está mal — o falta una función, o falta un fixture, o falta un Page Object."*
- KISS: *"La complejidad tiene un costo. Agrégala solo cuando el beneficio es claro."*

**Ejemplo rápido:** ¿por qué usamos POM y no Screenplay en los ejercicios base? Porque POM es suficiente para flujos de un solo actor. KISS en acción.

---

## Descanso — 15 minutos

Antes del descanso, da una instrucción concreta:
*"Durante el descanso, abre `pages/login_page.py` y lee el docstring del archivo. Trae una pregunta cuando vuelvan."*

---

## Bloque B — Laboratorio guiado (45 min)

### Slide 11 — Fixtures (10 min)

**Antes de mostrar el código:** pregunta al grupo qué pasa si 10 tests necesitan una página autenticada.
*"¿Copiamos el login en cada test? ¿Hay otra forma?"*

Abre `conftest.py` en vivo. Señala el `yield` — es el separador setup/teardown.
*"Todo lo que va antes del yield es setup. Todo lo que va después (si pones algo) es teardown. pytest-playwright cierra el browser automáticamente."*

**Demostración del scope:**
```bash
uv run pytest tests/test_data_driven.py -v --setup-show
```
`--setup-show` muestra en qué momento se crean y destruyen los fixtures. Muy útil para que el grupo vea el scope en acción.

---

### Slide 12 — Scope de Fixtures (8 min)

Muestra la tabla. El error más común: usar `scope="session"` para un fixture de `page`.

**Error conceptual frecuente:** *"¿Por qué no hacemos el `page` fixture session-scoped para que sea más rápido?"*
Respuesta: los tests dejarían de ser independientes. El estado de un test contaminaría el siguiente. Siempre preferimos tests deterministas sobre tests rápidos.

---

### Slide 13 — Data-Driven JSON (12 min)

Abre `data/users.json` y `tests/test_data_driven.py` en split screen.

**Demo paso a paso:**
1. Corre `uv run pytest tests/test_data_driven.py::test_login_invalido_desde_json -v`
2. Señala que los IDs de test vienen del campo `username` del JSON.
3. Agrega en vivo un quinto usuario inválido al JSON (usuario con solo espacios, por ejemplo).
4. Corre el test de nuevo — aparece el quinto caso sin tocar el código Python.

*"Este es el poder del data-driven: el analista de QA puede agregar casos sin tocar el código."*

---

### Slide 14 — Data-Driven YAML (10 min)

Muestra el YAML y el test parametrizado por índice.

**Pregunta al grupo:** *"¿Por qué parametrizamos por índice (0,1,2) y no directamente con los escenarios?"*
Razón: el fixture `cart_scenarios` es session-scoped y no se puede combinar directamente con `parametrize` que se evalúa en tiempo de colección. El índice es el puente entre los dos momentos.

**Demo:**
```bash
uv run pytest tests/test_data_driven.py::test_carrito_desde_yaml -v --headed
```
Con `--headed` el grupo ve el navegador abrirse y el carrito actualizarse en tiempo real.

---

### Slide 15 — Ventaja del Data-Driven (5 min)

Cierra el bloque con el principio. Conecta con lo que verán en S3:
*"En la sesión de APIs, los datos de los requests y los responses esperados también vivirán en archivos externos. Es el mismo patrón, aplicado a una capa diferente."*

---

## Descanso — 15 minutos

---

## Bloque C — Ejercicios y Mini Reto (45 min)

### Slides 16-17 — Setup y estructura (5 min)

Muestra la estructura de carpetas rápidamente. Asegúrate de que todos tienen los tests corriendo:
```bash
uv run pytest -v
```
**Si algún estudiante tiene error de importación:** lo más probable es que no esté en `ui-lab/` o que `uv sync` no se ejecutó con `--group dev`.

---

### Slide 18 — Ejercicio 1: CheckoutPage (20 min)

Deja que los estudiantes trabajen solos los primeros 15 minutos.
A los 15 min, muestra un esqueleto en vivo si el grupo está atascado:

```python
class CheckoutPage:
    def __init__(self, page):
        self._first_name = page.locator('[data-test="firstName"]')
        # ... completar

    def fill_shipping(self, first, last, zip_code):
        # ... completar
        return self

    def has_error(self) -> bool:
        return page.locator('[data-test="error"]').is_visible()
```

**Pista adicional para dar si preguntan:** en SauceDemo, el botón de continuar tiene `data-test="continue"` y el error tiene `data-test="error"` — igual que en login.

**Error común:** olvidar hacer `proceed_to_checkout()` en CartPage antes de llegar al checkout. El test falla porque la URL es incorrecta. Pídeles que verifiquen `page.url` en el error.

---

### Slide 19 — Mini Reto (15 min)

El mini reto es directo: solo tocan el YAML y el parámetro del test.
Si un estudiante intenta modificar el Page Object, es la señal de que no entendió la separación de responsabilidades — usa ese momento para aclarar.

**Validación del reto:**
```bash
uv run pytest -v   # debe mostrar 14 tests passed
```

---

### Slide 20 — Resumen (5 min)

Cierra con la tabla de resumen. Pregunta final al grupo:
*"¿En su trabajo actual (o en el último proyecto que vieron), usaban POM? ¿Data-Driven? ¿Qué les hubiera salvado tiempo?"*

Esta conversación conecta los patrones con la realidad del estudiante y refuerza la retención.

---

## Notas adicionales

**Si el tiempo es limitado:** recorta el Ejercicio 2 (Task de Screenplay). Es el menos crítico; el Ejercicio 1 y el Mini Reto son obligatorios.

**Si hay preguntas sobre Selenium vs Playwright:** responde brevemente — Playwright tiene autowaiting nativo, API más moderna y soporte oficial de Microsoft. En el curso usamos Playwright porque reduce el ruido de configuración. La lógica de POM aplica igual a Selenium.

**Entregable de esta sesión para el proyecto integrador:** la carpeta `ui-lab/` con los tests pasando es la base de la Etapa 4 del flujo CI/CD que construyen en la Sesión 5.
