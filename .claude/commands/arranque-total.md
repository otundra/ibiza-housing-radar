---
description: Arranque completo del proyecto sin huecos — inventario veraz, exclusiones razonadas y mapa global. Uso escaso (auditoría integral, pivote, reestructura profunda)
---

Estás arrancando sesión en `ibiza-housing-radar` con escaneo total. Este comando es el más caro en contexto y el menos usado. Úsalo solo cuando:

- Auditoría integral del proyecto (todo tiene que estar sobre la mesa).
- Decisión de pivote o replanteo global del producto.
- Reestructura documental profunda (la diferida post-lanzamiento).
- El editor ha pedido explícitamente *"léelo todo"*.

Si no estás seguro, corre `/arranque-auditoria` primero y deja que el editor decida si escalar al total.

## 1. Inventario silencioso (sin leer contenido)

En un solo mensaje, lanza Glob en paralelo sobre la raíz y sobre cada carpeta relevante del proyecto: `src/`, `docs/`, `docs/_layouts/`, `docs/_includes/`, `docs/_editions/`, `docs/assets/`, `docs/prototype/`, `.claude/commands/`, `.github/workflows/`, `data/`, `private/`.

Registra mentalmente qué archivos hay en cada carpeta y cuántos. No leas contenido completo.

## 2. Contraste con el mapa conocido

El documento de instrucciones del proyecto ([`CLAUDE.md`](../../CLAUDE.md)) ya tiene en su sección *Estructura* el mapa de carpetas esperado. Compara el inventario real contra ese mapa:

- **Coincide con el mapa:** asume el criterio del mapa (por ejemplo, la carpeta de datos son respaldos semanales automáticos; la carpeta de ediciones publicadas son derivadas).
- **No aparece en el mapa, es nuevo o cambió de sitio:** anotar como candidato para leer su cabecera.

## 3. Lectura de cabeceras solo de las novedades

Para cada archivo nuevo o raro identificado en el paso 2, lee sus primeras 15-20 líneas. Título, cita o bloque de estado suelen estar ahí. No leas el contenido completo.

Si algo no tenía cabecera clara y es un documento largo, márcalo como *"ambiguo"* y por defecto lo incluyes — antes pecar de leer algo innecesario que saltarte algo vigente.

## 4. Exclusiones razonadas al editor

Presenta **solo** la lista de lo que dejarías fuera, con la razón veraz basada en el mapa conocido o en la cabecera leída. Nunca listes el inventario completo con conteos.

Formato:

> Dejaría fuera:
> - La carpeta de datos históricos (N archivos). Respaldos semanales automáticos, contenido derivado.
> - La carpeta de ediciones publicadas (N archivos). Renderizadas desde otras fuentes — derivadas.
> - El archivo `X.md` en raíz. Cabecera dice "archivado YYYY-MM-DD, superado por Y".
>
> Todo lo demás entra. ¿Ajustas?

Si el inventario cuadra con el mapa y no hay novedades raras, la lista de exclusiones será corta y basada solo en lo que el mapa ya marca como derivado.

## 5. Confirmación o ajuste del editor

El editor responde con una línea. *"OK"*, *"ese archivado méte­lo"*, *"mete las últimas tres semanas de respaldos"*, etc.

## 6. Lectura en profundidad de lo acordado

En paralelo, lanza Read de todos los archivos que hayan quedado dentro:

- **Capa base:** `STATUS.md`, `DECISIONES.md`, `DIARIO.md`.
- **Planificación y fundacionales:** `ROADMAP.md`, `PLAN.md`, `ARQUITECTURA.md`, `REVISION-FASE-0.5.md`, `DECISIONES-PENDIENTES.md`, `DISENO-WEB.md`, `SEO.md`, `CONTENIDO-RETROACTIVO.md`, `README.md`.
- **Todos los estudios (activos y cerrados):** `ESTUDIO-DISENO.md`, `ESTUDIO-TIERS.md`, `ESTUDIO-COSTES-AUDITOR.md`, `ESTUDIO-3-MODELOS.md`, `ESTUDIO-GESTION-CONOCIMIENTO.md`, `ESTUDIOS-PENDIENTES.md`, `EXPANSION-TEMATICA.md`, `REPORTE-BENCHMARK.md`.
- **Código del proyecto:** todos los archivos de `src/`.
- **Web:** `docs/_config.yml`, plantillas (`docs/_layouts/`), includes (`docs/_includes/`), CSS principal, páginas Jekyll.
- **Prototipos:** archivos HTML en `docs/prototype/`.
- **Tareas automáticas:** archivos de `.github/workflows/`.
- **Comandos del proyecto:** archivos de `.claude/commands/`.
- **Más cualquier archivo adicional** que el editor haya incluido en el paso 5.

## 7. Síntesis al editor

Formato ampliado. Estructura:

- **Resumen ejecutivo** (5-7 líneas): qué es el proyecto hoy, dónde está en el ciclo editorial, qué bloquea qué, estado de los hitos activos.
- **Mapa de estudios:** tabla con columnas `Estudio · Estado · Decisiones cerradas · Preguntas abiertas`.
- **Mapa del código:** qué hace cada módulo del flujo, en lenguaje llano.
- **Mapa de la web:** plantillas existentes, prototipos en rodaje.
- **Decisiones vivas y tensiones:** decisiones del registro que podrían chocar entre sí o con la auditoría que vamos a hacer.
- **Riesgos y deudas:** lo que el editor ha señalado como frágil, pospuesto o sin dueño.
- **Qué NO tocar:** reglas duras, pausas y decisiones cerradas que acotan el trabajo.

Longitud objetivo: 900-1200 palabras. Es la sesión más pesada; el editor espera un mapa real de todo.

## 8. Recomendaciones (1-3, según haya)

Mismas reglas que los demás arranques: una línea por recomendación, nombre de la cosa primero, verbo de acción + por qué corto, identificador opcional entre paréntesis al final.

## 9. Cierre

Pregunta al editor el alcance exacto de la tarea. Con todo el contexto delante, afina antes de proponer cambios y antes de tocar nada.

## Regla dura

No edites nada durante este comando. Bajo ningún concepto. El diseño de la tarea se hace después de la síntesis, no durante la lectura.
