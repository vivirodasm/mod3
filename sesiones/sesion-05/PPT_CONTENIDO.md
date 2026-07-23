# Sesión 5 — Contenido de diapositivas
## CI/CD: control de calidad automático

> ~20 slides · A: 1–7 · B: 8–14 · C: 15–20  
> Regla de slide: **1 idea + 1 acción** (evitar paredes de bullets)

---

### Slide 1 — Portada (2 min)
**Título:** CI/CD — control de calidad automático
- Sesión 5 · Certificación 3
- Frase: si solo pasa en tu máquina, no es un test de equipo

### Slide 2 — Al salir vas a poder (2 min)
- Explicar CI en una frase
- Leer un workflow YAML
- Correr pytest **en Docker**
- Ubicar Jenkins / GitLab / Azure entre las opciones

### Slide 3 — “En mi máquina sí pasa” (4 min)
- Ana verde · Luis rojo → entornos distintos
- Falta un **entorno neutral**
- Chat 10 s: ¿les ha pasado?

### Slide 4 — CI y CD en una frase (4 min)
- **CI:** solo verifica, en un entorno controlado
- **CD:** prepara o despliega de forma automatizada
- Hoy = solo la **verificación automática**

### Slide 5 — Herramientas (4 min)
- GitHub Actions = práctica en vivo
- Jenkins · GitLab · Azure = mismo patrón
- Evento → pasos → verde/rojo

### Slide 6 — Estructura del YAML (8 min)
- `on` ¿cuándo? · `jobs` ¿qué? · `runs-on` ¿dónde? · `steps` ¿cómo?
- Archivo: `ci-lab/workflows/qa-api.yml`
- Pausa 20 s: ¿qué hace `on`?

### Slide 7 — Regla de oro + 2026 (5 min)
- Mismo comando local ≈ CI
- Docker = tu máquina imita al runner
- Extra: `permissions` · `concurrency` · caché de `uv`
- Tras el café lo vemos en verde

---
**DESCANSO 15 MIN**
---

### Slide 8 — Arranque B (1 min)
**Título:** Lab — CI en tu máquina
- Misma suite api-lab (S4)

### Slide 9 — Predicción (3 min)
- Antes de correr: ¿verde o rojo?
- Escríbelo en el chat (5 s)

### Slide 10 — Lab Docker (12 min)
```bash
cd proyecto-integrador/ci-lab
docker compose run --rm --no-deps test
```
- Esperado: 17 passed
- Local con `uv` = opcional

### Slide 11 — ¿Qué ganamos? (4 min)
- Dependencias fijas · sistema fijo · menos “en mi máquina…”
- Se parece bastante al runner de Ubuntu

### Slide 12 — Disparadores (5 min)
- `push` · `pull_request` · `workflow_dispatch`
- `paths` = no gastar CI en cambios irrelevantes
- Smoke rápido en el PR · carga pesada después (idea de S6)

### Slide 13 — Workflow real (5 min)
- `.github/workflows/qa-api.yml`
- Señala: permissions · concurrency · working-directory · smoke
- ¿Quién ve el `working-directory`?

### Slide 14 — Logro del bloque (2 min)
- Verde en un entorno controlado, no en una revisión “a ojo” en tu máquina
- Tras el café: mini-reto smoke

---
**DESCANSO 15 MIN**
---

### Slide 15 — Arranque C (1 min)
**Título:** Mini-reto y cierre

### Slide 16 — Mini-reto `-k smoke` (10 min)
```bash
uv run pytest -v -k smoke
```
- ¿Para qué sirve un smoke en un PR grande?

### Slide 17 — Checklist (5 min)
- [ ] CI en una frase
- [ ] Leo `on` / `jobs` / `steps`
- [ ] Corrí Docker ci-lab
- [ ] Regla: mismo comando

### Slide 18 — Errores comunes (4 min)
- Docker apagado · primera build lenta · API pública caída · sin `uv` (Docker igual sirve)

### Slide 19 — Frase de cierre + adelanto de S6 (5 min)
- Completa: “CI es ___ porque ___.”
- Mañana: ¿la API es lo bastante rápida?

### Slide 20 — Gracias
- `sesiones/sesion-05/` + `proyecto-integrador/ci-lab/`
- Próxima: Performance con K6
