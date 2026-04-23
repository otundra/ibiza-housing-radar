# Estudio — Arquitectura documental y gestión del conocimiento

> **Contexto.** Sesión 2026-04-23. Conversación con el editor sobre la tarea de roadmap *"Revisión profunda de arquitectura de archivos y gestión del conocimiento del proyecto"* (Fase 1, nuevo). Este documento congela las propuestas de esa sesión sin ejecutarlas completas: de momento solo se aplican **tres reglas baratas** y se crea `/cierre`. El resto queda aquí como plan de referencia.
>
> 🔁 **Revisión obligatoria post-lanzamiento.** Cuando el observatorio esté lanzado (evaluación 90 días, Fase 7 de ROADMAP) habrán cambiado docs, decisiones, volumen del DIARIO y estructura del repo. Este estudio debe revisarse antes de ejecutar la reorganización profunda: muchas cosas aquí descritas estarán obsoletas o ya resueltas por otras vías. Tarea emparejada añadida a ROADMAP en "Diferido con criterio claro".

## 1. Diagnóstico de la sesión

### 1.1 Dimensión del problema

- **20 documentos Markdown en raíz**, ~7.850 líneas, ~500 KB totales.
- **Tamaños relevantes:** DIARIO 100 KB / 533 líneas, REVISION-FASE-0.5 68 KB, ESTUDIO-DISENO 52 KB, ROADMAP 48 KB, PLAN 36 KB, ESTUDIO-COSTES-AUDITOR 36 KB, DISENO-WEB 32 KB, ARQUITECTURA 28 KB.
- **Leer "todo"** al arrancar una sesión ≈ 130k tokens. Inviable e innecesario.
- **Memoria en tres sitios simultáneos:** `~/.claude/CLAUDE.md` (global), `CLAUDE.md` del repo, `.claude/projects/.../memory/*.md` (10 entradas + MEMORY.md índice).

### 1.2 Patologías identificadas

1. **Duplicación de estado operativo.** STATUS.md, cabecera de CLAUDE.md, últimas entradas de DIARIO.md y memoria `prototipo_paso1_en_pausa.md` dicen casi lo mismo. Se desincronizan solas.
2. **Dualidad PLAN/ROADMAP.** Declarada (PLAN = histórico, ROADMAP = activo), pero ambos siguen pesando 80 KB juntos. Coste de lectura doble y riesgo de contradicciones.
3. **Tres registros paralelos de decisiones.** DECISIONES-PENDIENTES.md (16 resueltas), D1-D13 dentro de ESTUDIO-DISENO.md, y memorias sueltas en `.claude/memory/`. No hay fuente única.
4. **DIARIO monolítico y creciente.** 100 KB hoy, proyección ~500 KB en 6 meses si no se trocea. Sin resumen acumulado ni corte mensual/trimestral. A los 3 meses es inviable releer.
5. **Sin front-matter ni metadatos por doc.** No hay forma automática de saber si un doc está vivo, archivado, qué lo reemplaza o cuándo se revisó por última vez.
6. **Límites difusos entre ESTUDIO-* / REVISION / PIVOTE / ESTUDIOS-PENDIENTES / EXPANSION-TEMATICA.** Categorías no mutuamente excluyentes.
7. **Feedback del editor disperso.** 3 entradas en memoria `.claude`, acuerdos operativos también en CLAUDE.md del proyecto y viñetas en DIARIO. Imposible auditar "todos los acuerdos vigentes" rápido.
8. **Sin contrato de lectura de arranque.** No está escrito *"si vienes a X, lee Y y solo Y"*. Cada sesión se improvisa la exploración.

### 1.3 Lo que sí funciona (no tocar)

- **Memoria global `~/.claude/CLAUDE.md`** está bien calibrada.
- **MEMORY.md índice** es un patrón correcto: una línea por archivo con hook.
- **CLAUDE.md del proyecto** declara stack, estructura y convenciones sin duplicar decisiones estratégicas.
- **Commits con formato `tipo(ámbito): descripción`** son consistentes.

## 2. Propuesta estructural (tres capas)

| Capa | Contenido | Cuándo se lee | Tamaño objetivo |
|---|---|---|---|
| **Arranque** | `CLAUDE.md` + `STATUS.md` + `MEMORY.md` (auto-cargada) | Siempre, sin decisión | ≤ 400 líneas totales |
| **Navegación** | `INDEX.md` nuevo — mapa "intención → docs" | Siempre, auto | ≤ 100 líneas |
| **Profundidad** | ROADMAP, ARQUITECTURA, ESTUDIO-*, DIARIO, REVISION | Bajo demanda, dirigida por INDEX | sin tope, pero troceada |

**Meta:** sesiones normales se cierran con ~5-10k tokens de contexto sin perder profundidad, porque la profundidad se carga dirigida desde INDEX solo cuando toca.

## 3. Cambios estructurales propuestos

### 3.1 STATUS.md reducido y fijo

- **≤ 80-100 líneas.** Plantilla fija con campos: *activo / pausado / próximo hito / 3 enlaces clave*.
- Sin repetir contenido de DIARIO ni de CLAUDE.md.
- Regenerable a mano al cerrar sesión (`/cierre` lo chequea).

### 3.2 INDEX.md nuevo

- Matriz "intención → documentos a leer".
- Ejemplos de filas:
  - *"Vengo a tocar el pipeline"* → `ARQUITECTURA.md §X` + `src/costs.py` + última entrada DIARIO con tag `[pipeline]`.
  - *"Vengo a tocar diseño visual"* → `ESTUDIO-DISENO.md` + `DISENO-WEB.md` + prototipo en `docs/prototype/`.
  - *"Vengo a revisar estado"* → solo `STATUS.md` + `MEMORY.md`.
- Evita lecturas especulativas "por si acaso".

### 3.3 DIARIO troceado

- `DIARIO.md` conserva solo **las últimas 4 semanas**.
- Resto se mueve a `diario/2026-04.md`, `diario/2026-05.md`, etc.
- Al principio de `DIARIO.md`: resumen mensual de 10 líneas del histórico.
- Riesgo: rompe enlaces internos existentes. Requiere migración coordinada, no edición puntual.

### 3.4 DECISIONES.md como fuente única

- Append-only. Una decisión por fila.
- Formato tabla: `ID | fecha | tema | decisión | por qué | docs afectados | estado`.
- Migración: D1-D13 (de ESTUDIO-DISENO) + 16 decisiones cerradas de DECISIONES-PENDIENTES.md + decisiones sueltas en DIARIO → todas aquí.
- Resto de docs referencia por ID (`ver [D7 en DECISIONES.md]`).

### 3.5 Front-matter YAML en cada doc

Campos mínimos:

```yaml
---
estado: vivo | archivado | obsoleto
ultima_revision: 2026-04-23
reemplaza_a: [doc-anterior.md]  # opcional
leer_si: "vienes a tocar X"
---
```

Permite auditar qué está vivo, qué podar, y qué reemplaza a qué.

### 3.6 Carpeta `estudios/` consolidada

- Mover todos los `ESTUDIO-*.md` de raíz a `estudios/`.
- `ESTUDIOS-PENDIENTES.md` se convierte en índice de esa carpeta.
- Raíz queda limpia: solo docs de primer nivel (CLAUDE, STATUS, ROADMAP, ARQUITECTURA, DIARIO, DECISIONES, INDEX, PIVOTE, README).

### 3.7 Memoria `.claude` = solo feedback + punteros

- Nunca duplicar contenido que vive en el repo.
- Cada entrada de memoria incluye enlace al doc canónico.
- Entradas puras de feedback del editor (reglas de comportamiento) permanecen, son su sitio natural.

### 3.8 Contrato de arranque de sesión

Documentado en CLAUDE.md del proyecto:

> *"Al arrancar, leo STATUS.md + INDEX.md + MEMORY.md. Pido permiso antes de abrir docs largos (>300 líneas). Uso INDEX para decidir qué profundizar según la intención de la sesión."*

## 4. Ganancia estimada

- **Arranque óptimo:** hoy contexto auto ~5-8k tokens, pero exploración honesta requiere ~20-40k más. Con la estructura propuesta, sesiones normales se cierran en 5-10k tokens sin sacrificar profundidad.
- **Desincronización:** cae de 4 sitios a 1 por cada clase de información.
- **Acumulación útil:** feedback y decisiones pasan de "viñetas en DIARIO" a registros estructurados auditables.
- **Mantenimiento:** el coste del front-matter es recurrente pero bajo; se recupera la primera vez que evita una lectura de 2.000 líneas.

## 5. Riesgos y trade-offs

- **Disciplina recurrente.** Front-matter y DECISIONES.md solo funcionan si se cumplen. Si no, empeora (más estructura, misma entropía).
- **Churn si se hace ahora.** Con Revisión Fase 0.5 y prototipo abiertos, reorganizar introduce conflictos de merge documental y decisiones que luego hay que migrar. **Recomendado esperar a cerrar Revisión Fase 0.5.**
- **Troceo del DIARIO rompe enlaces.** Hay muchas referencias internas `DIARIO.md 2026-04-XX`. Hay que tratarlo como migración con buscar-y-reemplazar, no como edición.
- **Riesgo de sobre-ingeniería.** La estructura de 3 capas + INDEX + front-matter + DECISIONES puede ser overkill si el proyecto no crece. Revisar proporcionalidad antes de ejecutar todo.

## 6. Recomendación operativa de la sesión

**No abordar la reorganización completa ahora.** Tarea grande (1 sesión de arquitectura + 1 de migración) con frentes abiertos.

**Sí aplicar tres reglas baratas** que frenan la entropía hasta que toque la revisión profunda:

1. **DIARIO con fecha ISO y etiqueta temática.** Cada entrada nueva: `## 2026-04-23 [tema]` (ej. `[arquitectura]`, `[diseno]`, `[pipeline]`, `[feedback]`).
2. **DECISIONES.md como fuente única desde hoy.** Crearlo vacío con plantilla. Decisiones nuevas entran aquí primero; el resto referencia por ID. Migración histórica queda para la revisión profunda.
3. **STATUS.md ≤ 100 líneas.** Mover el exceso al DIARIO o borrar si ya vive en otro sitio.

**Plus:** comando `/cierre` con checklist fijo para no perder pasos al cerrar sesión (docs actualizados, DIARIO, commits atómicos, push, reporte).

## 7. Qué queda pendiente para la revisión profunda (post-lanzamiento)

Todo lo de la sección 3 excepto lo ya aplicado por reglas baratas:

- Creación de INDEX.md.
- DIARIO troceado por mes + resumen acumulado.
- Front-matter YAML en todos los docs.
- Consolidación de `estudios/` en carpeta.
- Migración histórica de decisiones a DECISIONES.md (D1-D13, DECISIONES-PENDIENTES).
- Revisión de la memoria `.claude/memory/` para eliminar duplicaciones con el repo.
- Contrato de arranque formalizado en CLAUDE.md.
- Auditoría PLAN.md vs ROADMAP.md (decidir si PLAN se archiva a `historia/` o se borra).

## 8. Cuándo revisar este documento

**Antes de ejecutar la reorganización profunda.** Condiciones:

- Observatorio lanzado (Fase 7 de ROADMAP iniciada).
- Primera evaluación de 90 días disponible.
- Revisión Fase 0.5 cerrada.

En ese momento: releer este estudio con ojo crítico, descartar lo que ya esté resuelto por otras vías, actualizar diagnóstico (probablemente DIARIO pese el doble y haya más estudios), y solo entonces planificar la migración.
