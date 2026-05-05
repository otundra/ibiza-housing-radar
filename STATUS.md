# Estado operativo — actualizado 2026-05-05

> **Regla:** ≤ 100 líneas. Solo estado vigente. Lo histórico vive en [`DIARIO.md`](DIARIO.md); lo fundacional en [`CLAUDE.md`](CLAUDE.md) (sección *Reglas fundacionales*). Ver [D0](DECISIONES.md).

## 🧭 Marco de trabajo de la Fase 1 (desde 2026-04-23, [D6](DECISIONES.md))

Tres hitos grandes. El editor decide entrada y cierre de cada uno; el resto va en cola.

1. **Hito 1 · Auditor mínimo viable publicado con una edición real** ← activo.
2. **Hito 2 · Sistema de tiers cerrado e integrado** (en paralelo).
3. **Hito 3 · Titular legal resuelto** — diferido hasta antes del empuje público (decisión del editor 2026-04-28). No corre prisa mientras la web no se publique activamente; bloquea solo el lanzamiento, no el rodaje.

## 🟢 Activo

- **Pipeline documental semanal** en `main`. Cron lunes 05:00 UTC. Última edición: W19 (4-10 may 2026), corregida bajo régimen de rodaje ([D21](DECISIONES.md)) tras la sesión 2026-05-05 — cambios en metadata + etiquetas inline de fuente. Detalle en [`private/revisiones/2026-w19.md`](private/revisiones/2026-w19.md).
- **Sistema de auto-recuperación operativo** desde 2026-04-27 ([D16](DECISIONES.md)). Tres capas: reintentos automáticos del SDK (`max_retries=5`), workflow `auto-retry.yml` que relanza tras push de fix, y marca persistente `data/PIPELINE_FAILED.flag` que dispara aviso de recuperación al volver a publicar. Coste cero. Validación pendiente con el próximo incidente real.
- **Web live** → <https://otundra.github.io/ibiza-housing-radar/>
- **Control de costes operativo.** Topes blando 12 € / duro 50 €. Dashboard en [`private/costs.md`](private/costs.md).
- **Snapshot append-only** en `data/archive/YYYY-WNN/` desde W17.
- **Copia de seguridad en GitLab operativa** desde 2026-04-29. Pull mirroring nativo (gitlab.com/otundra/ibiza-housing-radar, privado). Actualización automática cada hora. Cero mantenimiento.
- **Nou Diari añadida como fuente RSS** desde 2026-04-29 (`src/sources.yaml`). Medio digital Eivissa/Formentera, 8-15 art/día, cobertura directa vivienda y temporada, sin paywall. Entra en el próximo cron.
- **Salud de fuentes operativa** desde 2026-04-25 (tarea OP2 de Revisión Fase 0.5). Módulo [`src/sources_health.py`](src/sources_health.py) + integración silenciosa en `ingest.py` + alerta consolidada vía Telegram con 4 reglas de detección (feed muerto, frecuencia caída, vacío inesperado, estructura cambiada).
- **Sistema de monitorización de decisiones operativo** desde 2026-04-24 ([D14](DECISIONES.md)). Aviso semanal por Telegram ([`src/decisions_watch.py`](src/decisions_watch.py)) + tablero interno ([`private/panel.md`](private/panel.md)) + refuerzo al arranque.
- **Sistema de aprendizaje semanal vivo** ([D17](DECISIONES.md), 2026-04-27): el revisor automático del lunes propone ajustes al generador, registro en [`APRENDIZAJES.md`](APRENDIZAJES.md). Loop cerrado por primera vez en sesión 2026-05-05 — 5 reglas nuevas al prompt del generador + sexta dimensión "trazabilidad" en el revisor ([D22](DECISIONES.md)).
- **Sistema de revisiones post-publicación** ([D23](DECISIONES.md), 2026-05-05): registro narrativo del razonamiento humano sobre las ediciones cuando dispara alerta o el editor pide lectura proactiva. Carpeta [`private/revisiones/`](private/revisiones/) + índice raíz [`REVISIONES.md`](REVISIONES.md). Primera revisión: W19.
- **Sistema de auditorías sistémicas** ([D24](DECISIONES.md), 2026-05-05): freno al pozo de modificación infinita. Auditoría humana cada 3 meses o tras 5 decisiones nuevas + termómetro de salud sistémica en `private/panel.md` + regla 5 de gestión documental ("una mirada antes de añadir"). Carpeta [`private/auditorias/`](private/auditorias/) + índice raíz [`AUDITORIAS.md`](AUDITORIAS.md). Bootstrap cerrado 2026-05-05 con veredicto verde.

## ⏸ Pausado

- **Bloque B (web completa).** Prototipo HTML Paso 1 entregado y verificado 2026-04-21 pero **no cerrado** — falta visto bueno visual y responder 3 preguntas abiertas (wordmark V2 Split en cabecera real, apilado 6 chips en mobile, barra de progreso 8 estados vs aplicables). Ver memoria [`prototipo_paso1_en_pausa.md`](.claude/projects/-Users-raulserrano-Documents-GitHub-ibiza-housing-radar/memory/prototipo_paso1_en_pausa.md).
- **Resto del Bloque B** (~20 páginas) en espera de decisión de alcance del editor.

## 🟡 En curso

- **Revisión Fase 0.5** — auditoría fundacional abierta 2026-04-21. 16 tareas cerradas sobre 69 totales de la tabla de seguimiento. Sesión 2026-04-29: OP1, RT8, RT9 (parcial), RT13, ED1 (parcial), ED4, EX4, FU3. Ver [`REVISION-FASE-0.5.md`](REVISION-FASE-0.5.md).
- **Hito 1 — Auditor mínimo viable.** PI9 partido en MVP + iteración ([D1](DECISIONES.md)). Detalle en [`ESTUDIO-COSTES-AUDITOR.md §10.0`](ESTUDIO-COSTES-AUDITOR.md). Diseño del módulo cerrado 2026-04-24 en [`DISENO-AUDITOR-MVP.md`](DISENO-AUDITOR-MVP.md). **Construcción en marcha:** Fases 1, 2 y 3 cerradas 2026-04-25. **W19 publicada con auditor activo** (4-10 may 2026) — primera corrida limpia del cron con auditor live según [D20](DECISIONES.md). Coste acumulado validación previa: 0,042 €. **Fase 4 en curso:** observación en vivo durante 3-4 ediciones consecutivas (W19-W22) en lugar del backfill de W10. Cierre del Hito 1 previsto al evaluar las métricas tras W22. Sin calendario ni fecha ([D15](DECISIONES.md)).
- **Hito 2 — Re-estudio del sistema de tiers** ✅ **cerrado 2026-04-23** (RT15, RT26). [`ESTUDIO-TIERS.md`](ESTUDIO-TIERS.md) completo con 5 decisiones operativas en [D9](DECISIONES.md). Queda como pendiente de datos la medición empírica del sesgo por actor (RT25, post-backfill). Implementación de `src/tiers.py` + `data/tiers.yml` pasa a PI10 (sin bloquear auditor MVP).

## 🏷️ Identidad (provisional 2026-04-21)

- **Wordmark:** `radar))ibiza_vivienda` (JetBrains Mono). Logo gráfico descartado, identidad 100% tipográfica.
- **Dominio candidato:** `radaribiza.com` (compra pendiente).
- **Repo:** slug `ibiza-housing-radar` mantenido hasta decisión de dominio.

## 🎯 Próximos hitos

Sin calendario ni fecha de lanzamiento ([D15](DECISIONES.md)). El avance se organiza por hitos; los rangos de reloj solo aplican al cron semanal, que es automático.

> **Régimen actual: rodaje pre-lanzamiento** ([D21](DECISIONES.md), 2026-04-28). Las ediciones publicadas son revisables libremente (formato, contenido editorial, estructura) sin nota pública de corrección hasta que la web se empuje al público activamente. Tras el lanzamiento, vuelve a aplicar plena la regla 1 fundacional (contenido editorial inmutable, errores vía `/correcciones/`).

- **Próxima edición automática** — W20 (lunes 11 may 2026). Primera con las 5 reglas nuevas en el prompt del generador + 6ª dimensión "trazabilidad" en el revisor.
- **Hito 1 — Auditor MVP en observación en vivo.** Fases 1-3 cerradas 2026-04-25, primera corrida live en W19. Fase 4 en curso: observación durante W19-W22. Cierre del Hito al evaluar métricas tras W22 — ver [D20](DECISIONES.md). Detalle en [`DISENO-AUDITOR-MVP.md §9`](DISENO-AUDITOR-MVP.md).
- **Cierre de tensión `blocks_cited`** — vigilar W20: si el revisor reabre la queja sobre amplitud, asciende a warning recurrente. Apuntado en [`private/revisiones/2026-w19.md`](private/revisiones/2026-w19.md).
- **Claridad como dimensión muerta** — revisar tras W21 si sigue dando 9/10 sin warnings concretos. Apuntado en [`APRENDIZAJES.md`](APRENDIZAJES.md). Decisión asociada [D22](DECISIONES.md).
- **Antes de abrir al público** — revisar exposición legal de la página de correcciones (`/correcciones/`). El protocolo de 72 h queda publicado antes de tener buzón operativo; riesgo acotado mientras la web no tiene tráfico pero hay que cerrarlo antes de abrir al público. Anclado al Hito 3 legal. Detalle en [`DISENO-AUDITOR-MVP.md §7`](DISENO-AUDITOR-MVP.md).
- **Revisión del sistema de monitorización** ([D14](DECISIONES.md)) — tras 2-4 ediciones del sistema funcionando. Decidir si sumar aviso por patrón en autoevaluación + aviso por acumulación de 5 decisiones pequeñas autónomas del asistente sin resumen.
- **Próxima auditoría sistémica** ([D24](DECISIONES.md)) — al cumplir antes de los dos disparadores: 5 decisiones nuevas (D29) o 90 días (≈2026-08-03).

## 📍 Puntos de entrada al retomar

| Vengo a… | Abrir primero |
|---|---|
| Arrancar el auditor mínimo | [`DISENO-AUDITOR-MVP.md`](DISENO-AUDITOR-MVP.md) (plano de obra) + [`ESTUDIO-COSTES-AUDITOR.md §10.0`](ESTUDIO-COSTES-AUDITOR.md) + [D1](DECISIONES.md), [D2](DECISIONES.md), [D3](DECISIONES.md) |
| Implementar el sistema de tiers | [`ESTUDIO-TIERS.md`](ESTUDIO-TIERS.md) cerrado. Siguiente: `src/tiers.py` + `data/tiers.yml` con los valores de [D9](DECISIONES.md) + badge en Jekyll + `/metodologia/#tiers` (tarea PI10) |
| Retomar diseño visual | memoria `prototipo_paso1_en_pausa.md` + [`ESTUDIO-DISENO.md §10`](ESTUDIO-DISENO.md) + entradas DIARIO 2026-04-21 |
| Cerrar Revisión Fase 0.5 | [`REVISION-FASE-0.5.md`](REVISION-FASE-0.5.md) |
| Tocar pipeline | [`ARQUITECTURA.md`](ARQUITECTURA.md) + [`src/`](src/) |
| Ver decisiones vigentes | [`DECISIONES.md`](DECISIONES.md) + migración pendiente en D1-D13 de `ESTUDIO-DISENO.md` + 16 cerradas de `DECISIONES-PENDIENTES.md` |
| Reorganizar docs | **NO — diferido post-lanzamiento.** Ver [`ESTUDIO-GESTION-CONOCIMIENTO.md`](ESTUDIO-GESTION-CONOCIMIENTO.md). |

## 🧭 Modelo activo

Observatorio documental. LLM no genera propuestas: documenta las de actores con nombre, con URL verificable. Consolidado en `main` desde 2026-04-21. Docs de referencia en cabecera de [`CLAUDE.md`](CLAUDE.md).

## 🗂 Docs vivos en raíz (28)

Fundacionales: `CLAUDE.md`, `README.md`, `DECISIONES.md`, `COMANDOS.md`.
Planificación: `ROADMAP.md`, `REVISION-FASE-0.5.md`, `DECISIONES-PENDIENTES.md`, `DISENO-AUDITOR-MVP.md`.
Producto: `ARQUITECTURA.md`, `DISENO-WEB.md`, `SEO.md`, `CONTENIDO-RETROACTIVO.md`.
Estudios: `ESTUDIO-DISENO.md`, `ESTUDIO-COSTES-AUDITOR.md`, `ESTUDIO-TIERS.md`, `ESTUDIO-3-MODELOS.md`, `ESTUDIO-GESTION-CONOCIMIENTO.md`, `ESTUDIOS-PENDIENTES.md`, `EXPANSION-TEMATICA.md`, `REPORTE-BENCHMARK.md`.
Sistemas vivos (registros narrativos y aprendizajes): `APRENDIZAJES.md`, `REVISIONES.md` (D23, 2026-05-05), `AUDITORIAS.md` (D24, 2026-05-05).
Estado/memoria: `STATUS.md` (este), `DIARIO.md`, `PLAN.md` (histórico), `PIVOTE.md` (histórico).

## ⚠️ Avisos vigentes

- **No reorganizar docs todavía.** La auditoría completa está diferida; aplicar solo las tres reglas baratas de [D0](DECISIONES.md).
- **No tocar prototipo HTML** sin orden explícita del editor (pausa activa desde 2026-04-21).
- **No mezclar modelos** a mitad de ejecución del pipeline (rompe caché).
