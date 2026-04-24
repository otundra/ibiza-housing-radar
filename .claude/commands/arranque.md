---
description: Arranque ligero de sesión — panorámica de dónde estamos y qué no tocar (Tier 1, invocado explícitamente)
---

Estás arrancando sesión en `ibiza-housing-radar` con el comando explícito. Objetivo: sintetizar el estado del proyecto lo suficiente para trabajar con criterio, sin escanear nada más, y entregar 1-3 recomendaciones de siguiente paso antes de preguntar.

> **Nota:** si el editor no ha invocado este comando, el modo por defecto es **leer los tres docs en silencio y responder directo al prompt**, sin informe ni recomendaciones ni pregunta. Ver la regla de *arranque por defecto* en la sección *Slash commands del proyecto* de [`CLAUDE.md`](../../CLAUDE.md). Este comando es el modo "con informe", que se dispara solo cuando el editor lo pide.

## 1. Lectura en paralelo

En un solo mensaje, lanza Read a:

- [`STATUS.md`](../../STATUS.md) — completo (siempre ≤ 100 líneas por regla dura del registro de decisiones).
- [`DECISIONES.md`](../../DECISIONES.md) — completo.
- [`DIARIO.md`](../../DIARIO.md) — primeras 120 líneas (las más recientes; el diario va con lo nuevo arriba).

No leas nada más en este comando.

## 2. Síntesis al editor

Formato viñetas, sin adornos, máximo 200 palabras. Estructura:

- **Dónde estamos:** 1-2 frases (hito activo + fase).
- **Activo / en curso / pausado:** bullets con lo que refleja STATUS.
- **Últimos 3-5 cambios del diario:** una línea por entrada, con fecha y tema.
- **Decisiones que acotan trabajo inminente:** nombre de la cosa + título corto, solo si tocan. El código de la decisión va entre paréntesis al final si aporta trazabilidad; nunca como etiqueta principal.
- **Qué NO tocar:** pausas explícitas + reglas duras vigentes que limitan la sesión.
- **Señales ambiguas:** si STATUS, DIARIO y DECISIONES se contradicen, o hay algo abierto sin dueño claro, dilo en una línea.

## 3. Recomendaciones (1-3, según haya)

Tras la síntesis y antes de la pregunta de cierre, ofrece entre **1 y 3 recomendaciones** de siguiente paso concreto basadas en lo que has leído. No rellenes hasta tres si solo hay una o dos naturales — mejor poco y claro que forzado.

Regla de redacción para cada recomendación:

- **Una línea por recomendación.** Nombre de la cosa primero (nunca el código delante). Verbo de acción + por qué corto + trazabilidad opcional entre paréntesis al final.
- Ejemplo correcto: *"arrancar el diseño sobre papel del auditor mínimo — es el pendiente inmediato del hito 1 activo"*.
- Ejemplo incorrecto: *"RT26/Q1-Q5 ya listas por D9"* (todo códigos, cero contexto).

El editor puede elegir una, pedir otra, o contestar con algo distinto. La recomendación no compromete agenda; solo presenta opciones.

## 4. Cierre

Pregunta al editor: *"¿Qué vamos a hacer en esta sesión?"* — con las recomendaciones ya servidas, el editor elige. Con esa respuesta tienes criterio para decidir si la tarea cabe en Tier 1 o si conviene escalar.

## Cuándo escalar

Si el editor contesta con algo que toca:

- **Cambio de fase, arquitectura, estudio grande, o refactor del flujo** → sugiere `/arranque-fase` antes de ejecutar.
- **Auditoría estructural, decisión de pivote, o bloqueo por falta de mapa mental global** → sugiere `/arranque-auditoria`.
- **Resto** → sigue con lo que hay, ya es suficiente.

## Regla dura

No edites nada durante este comando. Es un arranque de contexto, no una sesión de trabajo. Las ediciones empiezan después de que el editor diga qué quiere hacer.
