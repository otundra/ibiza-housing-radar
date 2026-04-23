# Estado operativo — actualizado 2026-04-23

> **Regla:** ≤ 100 líneas. Solo estado vigente. Lo histórico vive en [`DIARIO.md`](DIARIO.md); lo fundacional en [`CLAUDE.md`](CLAUDE.md) y [`PIVOTE.md`](PIVOTE.md). Ver [D0](DECISIONES.md).

## 🧭 Marco de trabajo de la Fase 1 (desde 2026-04-23, [D6](DECISIONES.md))

Tres hitos grandes. El editor decide entrada y cierre de cada uno; el resto va en cola.

1. **Hito 1 · Auditor mínimo viable publicado con una edición real** ← activo.
2. **Hito 2 · Sistema de tiers cerrado e integrado** (en paralelo).
3. **Hito 3 · Titular legal resuelto** (en paralelo, bloquea empuje público).

## 🟢 Activo

- **Pipeline documental semanal** en `main`. Cron lunes 05:00 UTC. Última edición: W17 (20-26 abril 2026).
- **Web live** → <https://otundra.github.io/ibiza-housing-radar/>
- **Control de costes operativo.** Topes blando 12 € / duro 50 €. Dashboard en [`private/costs.md`](private/costs.md).
- **Snapshot append-only** en `data/archive/YYYY-WNN/` desde W17.

## ⏸ Pausado

- **Bloque B (web completa).** Prototipo HTML Paso 1 entregado y verificado 2026-04-21 pero **no cerrado** — falta visto bueno visual y responder 3 preguntas abiertas (wordmark V2 Split en cabecera real, apilado 6 chips en mobile, barra de progreso 8 estados vs aplicables). Ver memoria [`prototipo_paso1_en_pausa.md`](.claude/projects/-Users-raulserrano-Documents-GitHub-ibiza-housing-radar/memory/prototipo_paso1_en_pausa.md).
- **Resto del Bloque B** (~20 páginas) en espera de decisión de alcance del editor.

## 🟡 En curso

- **Revisión Fase 0.5** — auditoría fundacional abierta 2026-04-21, 34 tareas. Ver [`REVISION-FASE-0.5.md`](REVISION-FASE-0.5.md) + memoria [`revision_fase_0_5.md`](.claude/projects/-Users-raulserrano-Documents-GitHub-ibiza-housing-radar/memory/revision_fase_0_5.md).
- **Hito 1 — Auditor mínimo viable** (2 sem). PI9 partido en MVP + iteración ([D1](DECISIONES.md)). Detalle en [`ESTUDIO-COSTES-AUDITOR.md §10.0`](ESTUDIO-COSTES-AUDITOR.md). Pendiente inmediato: diseño sobre papel del módulo + mockup estático de `/correcciones/` en el prototipo.
- **Hito 2 — Re-estudio del sistema de tiers** (RT15). En paralelo al auditor MVP ([D5](DECISIONES.md)).

## 🏷️ Identidad (provisional 2026-04-21)

- **Wordmark:** `radar))ibiza_vivienda` (JetBrains Mono). Logo gráfico descartado, identidad 100% tipográfica.
- **Dominio candidato:** `radaribiza.com` (compra pendiente).
- **Repo:** slug `ibiza-housing-radar` mantenido hasta decisión de dominio.

## 🎯 Próximos hitos

- **Lunes 27 abr 07:00 CEST** — próxima edición automática (W18).
- **Arranque Hito 1 — Auditor MVP:** diseño sobre papel → construcción 2 sem → prueba empírica sobre W10 (2-8 marzo 2026).

## 📍 Puntos de entrada al retomar

| Vengo a… | Abrir primero |
|---|---|
| Arrancar el auditor mínimo | [`ESTUDIO-COSTES-AUDITOR.md §10.0`](ESTUDIO-COSTES-AUDITOR.md) + [D1](DECISIONES.md), [D2](DECISIONES.md), [D3](DECISIONES.md) |
| Retomar diseño visual | memoria `prototipo_paso1_en_pausa.md` + [`ESTUDIO-DISENO.md §10`](ESTUDIO-DISENO.md) + entradas DIARIO 2026-04-21 |
| Cerrar Revisión Fase 0.5 | [`REVISION-FASE-0.5.md`](REVISION-FASE-0.5.md) |
| Tocar pipeline | [`ARQUITECTURA.md`](ARQUITECTURA.md) + [`src/`](src/) |
| Ver decisiones vigentes | [`DECISIONES.md`](DECISIONES.md) + migración pendiente en D1-D13 de `ESTUDIO-DISENO.md` + 16 cerradas de `DECISIONES-PENDIENTES.md` |
| Reorganizar docs | **NO — diferido post-lanzamiento.** Ver [`ESTUDIO-GESTION-CONOCIMIENTO.md`](ESTUDIO-GESTION-CONOCIMIENTO.md). |

## 🧭 Modelo activo

Observatorio documental. LLM no genera propuestas: documenta las de actores con nombre, con URL verificable. Consolidado en `main` desde 2026-04-21. Docs de referencia en cabecera de [`CLAUDE.md`](CLAUDE.md).

## 🗂 Docs vivos en raíz (20)

Fundacionales: `CLAUDE.md`, `PIVOTE.md`, `README.md`, `DECISIONES.md`.
Planificación: `ROADMAP.md`, `REVISION-FASE-0.5.md`, `DECISIONES-PENDIENTES.md`.
Producto: `ARQUITECTURA.md`, `DISENO-WEB.md`, `SEO.md`, `CONTENIDO-RETROACTIVO.md`.
Estudios: `ESTUDIO-DISENO.md`, `ESTUDIO-COSTES-AUDITOR.md`, `ESTUDIO-3-MODELOS.md`, `ESTUDIO-GESTION-CONOCIMIENTO.md`, `ESTUDIOS-PENDIENTES.md`, `EXPANSION-TEMATICA.md`, `REPORTE-BENCHMARK.md`.
Estado/memoria: `STATUS.md` (este), `DIARIO.md`, `PLAN.md` (histórico).

## ⚠️ Avisos vigentes

- **No reorganizar docs todavía.** La auditoría completa está diferida; aplicar solo las tres reglas baratas de [D0](DECISIONES.md).
- **No tocar prototipo HTML** sin orden explícita del editor (pausa activa desde 2026-04-21).
- **No mezclar modelos** a mitad de ejecución del pipeline (rompe caché).
