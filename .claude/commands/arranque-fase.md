---
description: Arranque de fase — añade plan, arquitectura y estudio del área (Tier 2, al retomar tras pausa o cambiar de área)
---

Estás arrancando sesión en `ibiza-housing-radar` con contexto de fase. Usa este comando cuando:

- Han pasado más de una semana desde la última sesión.
- La sesión cambia de área (pipeline ↔ diseño ↔ editorial ↔ legal).
- El editor ha pedido explícitamente contexto más profundo.

Si no estás seguro de si aplica, corre `/arranque` primero y deja que el editor decida.

## 1. Capa base (igual que `/arranque`)

Lectura en paralelo en un solo mensaje:

- [`STATUS.md`](../../STATUS.md) — completo.
- [`DECISIONES.md`](../../DECISIONES.md) — completo.
- [`DIARIO.md`](../../DIARIO.md) — primeras 120 líneas.

## 2. Capa de fase

En un segundo mensaje con lecturas en paralelo:

- [`PLAN.md`](../../PLAN.md) — roadmap completo.
- [`ARQUITECTURA.md`](../../ARQUITECTURA.md) — módulos del pipeline y flujo.
- **Estudio del área.** Elige según el argumento que te haya pasado el editor o, si no lo hay, según el hito activo en STATUS:
  - **Pipeline / coste / auditor / tiers de confianza** → [`ESTUDIO-COSTES-AUDITOR.md`](../../ESTUDIO-COSTES-AUDITOR.md), [`ESTUDIO-TIERS.md`](../../ESTUDIO-TIERS.md), [`ESTUDIO-3-MODELOS.md`](../../ESTUDIO-3-MODELOS.md).
  - **Diseño web / identidad** → [`ESTUDIO-DISENO.md`](../../ESTUDIO-DISENO.md), [`DISENO-WEB.md`](../../DISENO-WEB.md).
  - **Editorial / contenido retroactivo / SEO** → [`CONTENIDO-RETROACTIVO.md`](../../CONTENIDO-RETROACTIVO.md), [`SEO.md`](../../SEO.md).
  - **Auditoría fundacional abierta** → [`REVISION-FASE-0.5.md`](../../REVISION-FASE-0.5.md).
  - **Gestión documental** → [`ESTUDIO-GESTION-CONOCIMIENTO.md`](../../ESTUDIO-GESTION-CONOCIMIENTO.md).

Si la tarea toca varias áreas, lee los estudios de todas ellas.

## 3. Síntesis al editor

Además de lo de `/arranque`, añade:

- **Fase y hito:** nombre del hito activo + los siguientes 2 hitos según PLAN o STATUS.
- **Mapa del estudio leído:** secciones cerradas, secciones abiertas, preguntas pendientes al editor.
- **Arquitectura tocada:** qué módulos del flujo entran en juego si la tarea los requiere (nombres con glosa, ej. *"módulo de extracción de propuestas (`extract.py`)"*).
- **Tareas abiertas en la auditoría fundacional** (si la sesión roza la revisión abierta el 21 de abril): resumen + estado.

Longitud objetivo: 350-450 palabras. Más denso que Tier 1, pero sigue sin ser una redacción.

## 4. Recomendaciones (1-3, según haya)

Con el mapa de fase delante, ofrece **1 a 3 recomendaciones** de siguiente paso concreto antes de la pregunta de cierre. No fuerces hasta tres si solo hay una o dos naturales.

Mismas reglas de redacción que en `/arranque`:

- Una línea por recomendación.
- Nombre de la cosa primero; el código va entre paréntesis al final y solo si aporta trazabilidad.
- Verbo de acción + por qué corto.

## 5. Cierre

Pregunta al editor qué vamos a hacer. Con la síntesis y las recomendaciones delante ya tiene un mapa ordenado para concretar.

## Regla dura

No edites nada durante este comando. Si detectas una inconsistencia o un doc desactualizado, regístralo en la síntesis como *"señal ambigua"* y deja que el editor decida si arreglarlo cae dentro de la sesión.
