# CLAUDE.md — Radar Vivienda Ibiza (provisional · repo: ibiza-housing-radar)

Instrucciones para Claude Code al trabajar en este proyecto.

> 🏷️ **Nombre 2026-04-21 (provisional).** Wordmark tipográfico cerrado: **`radar))ibiza_vivienda`** (formato `lugar_tema`, todo en `JetBrains Mono`, las `))` evocan ondas de radar). El editor cierra esta forma por lectura natural en español. Futuros verticales del mismo ecosistema: `radar))ibiza_turismo`, `radar))ibiza_medioambiente`, `radar))formentera_vivienda`.
>
> **Dominio:** `radaribiza.com` sigue siendo candidato principal. Compra pendiente según evolución del proyecto. Repo GitHub mantiene el slug `ibiza-housing-radar` hasta decisión de dominio. Tagline estable: *"Observatorio documental"*.
>
> **Logo gráfico descartado** 2026-04-21. Dirección visual elegida: **tipográfica pura**. Sin monograma SVG. El wordmark cumple la función de identidad completa. Preview vivo en [`docs/prototype/logo/preview.html`](docs/prototype/logo/preview.html) con 4 variantes (V1 mono plano · V2 split · V3 tri · V4 underline). Pendiente elección de variante.

> 🧭 **Modelo activo: observatorio documental.** Desde el 2026-04-21 (merge del modelo documental a `main`) es el único vigente. El LLM no genera propuestas; documenta las que actores con nombre formulan cada semana, con URL verificable. Documentos de referencia:
>
> - [`PIVOTE.md`](PIVOTE.md) — 5 reglas duras + decisión fundacional.
> - [`ROADMAP.md`](ROADMAP.md) — Fase 0 completa.
> - [`ARQUITECTURA.md`](ARQUITECTURA.md) — pipeline con módulos `extract.py`, `verify.py`, `rescue.py`, `balance.py`, `archive.py`, `self_review.py`.
> - [`DISENO-WEB.md`](DISENO-WEB.md) — UX dual (primer visitante + profesional recurrente).
> - [`ESTUDIO-DISENO.md`](ESTUDIO-DISENO.md) — sistema visual, benchmark editorial, 13 decisiones cerradas (D1-D13).
> - [`SEO.md`](SEO.md) — plan SEO ambicioso.
> - [`CONTENIDO-RETROACTIVO.md`](CONTENIDO-RETROACTIVO.md) — 12 ediciones retroactivas W06-W17 bajo modelo documental.
> - [`DECISIONES-PENDIENTES.md`](DECISIONES-PENDIENTES.md) — 16 decisiones resueltas del editor.
> - [`REVISION-FASE-0.5.md`](REVISION-FASE-0.5.md) — auditoría fundacional abierta 2026-04-21, pendiente antes de reanudar diseño visual.

## Qué es

Observatorio semanal documental sobre la crisis de vivienda en Ibiza con foco en trabajadores de temporada. Cada lunes mapea las propuestas que actores con nombre (instituciones, partidos, patronales, sindicatos, tercer sector, colectivos ciudadanos) formulan públicamente, con fuente verificable (URL). No genera propuestas propias.

El ciclo operativo se rige por el **calendario real de la isla**: de la *opening* de las clubs grandes (finales de abril) a la *closing* (mediados de octubre). En 2026: del 24 de abril al ~12 de octubre. Fuera de temporada (octubre → abril siguiente) el observatorio sigue publicando, cubriendo la *pre-temporada* del verano que viene. Etiquetas públicas: `Temporada YYYY` / `Pre-temporada YYYY` (sin "invierno", ambiguo). Fechas exactas de temporada en `data/temporadas.yml`, alimentado por la automatización anual `src/update_temporadas.py`.

Publicado en GitHub Pages.

## Stack

- **Lenguaje:** Python 3.12
- **IA:** Anthropic Claude API (Haiku 4.5 para clasificación, Sonnet 4.6 para extracción/verificación, Opus 4.7 para generación editorial).
- **Fuentes:** RSS de Google News + Diario de Ibiza + Periódico de Ibiza
- **Web:** Jekyll (GitHub Pages) con tema custom (CSS editorial propio).
- **OG images:** Puppeteer (Node.js en runner CI) renderiza plantilla HTML → PNG. Ver [ESTUDIO-DISENO.md §7](ESTUDIO-DISENO.md).
- **Scheduler:** GitHub Actions cron semanal + tarea anual para fechas de temporada.
- **Hosting:** 100 % GitHub (repo + Pages + Actions). 0 € de infra.
- **Coste esperado:** ~6-7 €/mes en API Anthropic (proyección, a revisar con 3 meses de datos reales). Capas de coste en `src/costs.py`: blando 12 €, duro 50 €. Ver [DIARIO.md 2026-04-21](DIARIO.md).

## Estructura

```
.
├── src/                        # Pipeline Python (modelo documental)
│   ├── ingest.py               # Lee RSS + filtra keywords + dedup
│   ├── classify.py             # Haiku: is_housing, actor, palanca, has_explicit_proposal
│   ├── extract.py              # Haiku + validador Sonnet: ficha estructurada por propuesta
│   ├── rescue.py               # Reglas: candidatas a rescate de ediciones previas
│   ├── generate.py             # Opus: compone la edición (no genera propuestas)
│   ├── verify.py               # URLs 200 + trazabilidad actor + verbos prohibidos
│   ├── balance.py              # Reparto de actores y bloques (30/90/180/365 días)
│   ├── self_review.py          # Sonnet: autoevaluación semanal tras publicar
│   ├── archive.py              # Snapshot append-only a data/archive/YYYY-WNN/
│   ├── build_index.py          # Regenera docs/index.md
│   ├── costs.py                # Tracking + dashboard + capas de tope mensual
│   ├── notify.py               # Alertas Telegram + fallback issue GitHub
│   ├── report.py               # Orquestador end-to-end
│   └── sources.yaml            # Feeds + keywords + ventana temporal
├── data/
│   ├── archive/YYYY-WNN/       # Snapshot append-only por ejecución (desde W17)
│   ├── proposals_history.json  # Propuestas extraídas, histórico acumulado
│   ├── costs.csv               # Append-only, histórico de llamadas API
│   ├── ingested.json           # Noticias crudas de la semana en curso
│   └── classified.json         # Noticias clasificadas de la semana en curso
├── docs/                       # Jekyll root (sirve como GitHub Pages)
│   ├── _config.yml
│   ├── _layouts/               # default, home, edition, page
│   ├── _includes/              # header, footer
│   ├── assets/css/main.css     # Theme custom (incluye dashboard de la home)
│   ├── assets/favicon.svg
│   ├── _editions/              # Ediciones semanales YYYY-wWW.md (colección Jekyll)
│   ├── index.md                # Regenerado por build_index.py (panel de la última edición)
│   ├── ediciones.md            # Página /ediciones/ con archivo completo
│   └── acerca.md
├── private/                    # Fuera de Jekyll, no servido por GitHub Pages
│   └── costs.md                # Dashboard privado de costes (regenerado por costs.py)
├── .github/workflows/
│   ├── weekly-report.yml       # Cron lunes 05:00 UTC
│   └── validate-key.yml        # Test manual de la API key
├── requirements.txt
├── DIARIO.md                   # Diario del proyecto (hitos, decisiones, cambios)
├── STATUS.md                   # Snapshot de estado actual (se actualiza a mano)
└── README.md
```

## Comandos típicos

```bash
# Ejecutar pipeline completo localmente (requiere ANTHROPIC_API_KEY)
export ANTHROPIC_API_KEY=sk-ant-...
python -m src.report

# Solo regenerar dashboard de costes (sin API)
python -m src.costs

# Solo reconstruir índice de home
python -m src.build_index

# Validar la API key contra Anthropic (sin consumir casi nada)
gh workflow run validate-key.yml
```

## Decisiones de arquitectura

1. **Google News como fuente base.** RSS nativos de diarios locales son frágiles (paywalls, cambios de feed). Google News está siempre online y cubre todos los diarios. Los RSS nativos se mantienen como refuerzo pero no son críticos.

2. **Clasificación en una sola llamada.** En lugar de una llamada a Haiku por titular (20 llamadas), se mandan todos en un único payload JSON. Misma precisión, coste dividido entre 20.

3. **Sin base de datos.** Todo el estado vive en el repo: ediciones como archivos Markdown, costes como CSV. Auditable, diffeable y sin infra externa.

4. **Commit-back desde Actions.** El workflow commitea la edición generada al mismo repo. Permite ver el histórico completo en GitHub sin servidor adicional.

5. **Topes de presupuesto en euros + filosofía no-cortar-editorial.** Sistema de capas en `src/costs.py` (actualizado 2026-04-20 para el modelo documental): blando `MONTHLY_SOFT_CAP_EUR = 12` solo avisa por Telegram y sigue publicando; duro `MONTHLY_HARD_CAP_EUR = 20` corta para proteger contra runaway (bugs, bucles). Capas: verde <6, amarilla 6-9, naranja 9-12, roja blanda 12-20, roja dura >20. No se pierde editorial por sobrecoste salvo desastre real. Alertas vía `src/notify.py` (Telegram con fallback a issue GitHub **solo en Actions**, no en ejecución local salvo level=critical).

6. **Modelo por fase.** Haiku para filtrar (coste marginal), Opus solo para la pieza final donde la calidad editorial sí importa. No mezclar.

## Reglas de gestión documental (desde 2026-04-23, ver [D0](DECISIONES.md))

Tres reglas baratas que frenan la entropía hasta la revisión profunda post-lanzamiento (ver [`ESTUDIO-GESTION-CONOCIMIENTO.md`](ESTUDIO-GESTION-CONOCIMIENTO.md)):

1. **DIARIO con fecha ISO + etiqueta temática.** Cada entrada nueva lleva cabecera `## YYYY-MM-DD [tema]`. Temas válidos: `[pipeline]`, `[diseno]`, `[editorial]`, `[arquitectura]`, `[docs]`, `[costes]`, `[legal]`, `[feedback]`, `[sesion]` (cierre general).
2. **DECISIONES.md fuente única.** Toda decisión nueva entra en [`DECISIONES.md`](DECISIONES.md) con ID `D{N}`. Otros docs referencian por ID (*"ver D7"*), no duplican contenido.
3. **STATUS.md ≤ 100 líneas.** Si crece, podar a DIARIO o borrar lo que ya viva en otro sitio.

## Slash commands del proyecto

Índice vivo en [`COMANDOS.md`](COMANDOS.md) (raíz). Si no aparece ahí, no existe. Al crear un comando nuevo en `.claude/commands/`, añadirlo a la tabla de `COMANDOS.md` en el mismo commit.

- **Arranque por defecto (sin comando, desde 2026-04-24).** Al empezar una sesión sin invocar ningún comando, leer en silencio `STATUS.md`, `DECISIONES.md` y las primeras 120 líneas de `DIARIO.md`, y **responder directo al prompt del editor sin sacar informe**. El informe ordenado + 1-3 recomendaciones + pregunta *"¿qué hacemos?"* solo se dispara cuando el editor escribe `/arranque` explícito.
- **Arranques con informe:** `/arranque` (ligero, ≈200 palabras), `/arranque-auditoria` (profundo, mapa de estudios + código, ≈700 palabras), `/arranque-total` (completo, todo el proyecto sin huecos, uso escaso). Criterio y qué lee cada uno en [`COMANDOS.md`](COMANDOS.md).
- **Ampliación transversal:** `/ampliar [área o descripción]` carga documentos de un área concreta del proyecto sin sacar informe. Usable tras cualquier arranque para subir de nivel de contexto sin repetir síntesis, o como carga puntual al empezar.
- **Cierre de sesión:** `/cierre` (ver [`.claude/commands/cierre.md`](.claude/commands/cierre.md)) con checklist fijo: auditoría de cambios, actualización dirigida de docs, commits atómicos, push y reporte de qué se tocó y qué no.

## Lenguaje en el chat del proyecto (desde 2026-04-24)

- **Un punto menos de lenguaje técnico.** Al hablar con el editor en el chat, traducir tecnicismos evitables al español común (flujo, registro, estructura, diferencias, envío…). La palabra técnica se mantiene en documentos internos de arquitectura, estudios y código; en la conversación se traduce. Alcance: solo este proyecto. Detalle en la memoria del asistente `feedback_lenguaje_llano_chat.md`.
- **Cero códigos sueltos en el chat.** Siempre empezar por el **nombre de la cosa**; el identificador (tipo `RT15`, `PI9`, `D11`, `W17`, `Q3`…) va entre paréntesis al final y solo si aporta trazabilidad. Nunca como etiqueta principal, nunca como primer elemento de una línea. 4 recaídas acumuladas a 2026-04-24 — próxima recaída = fallo grave. Excepción: siglas del dominio público del sector (BOIB, IBAVI, GOIB, CCOO, PIMEEF…) sí se usan sin glosar. Detalle en `feedback_referencias_con_contexto.md`.

## Diario del proyecto

Cuando haya un cambio relevante (hito, decisión, fix estructural, no-commits triviales), añadir una entrada a [`DIARIO.md`](DIARIO.md) con formato viñetas: tema en **negrita** + línea breve combinando qué/por qué/impacto. Cabecera obligatoria con fecha ISO + `[tema]` (regla 1).

## Convenciones de commits

Formato: `tipo(ámbito): descripción en español`.

Tipos usados:
- `report` — edición semanal generada
- `feat` — funcionalidad nueva del pipeline o web
- `fix` — corrección
- `docs` — documentación
- `chore` — scaffolding, CI, configs
- `refactor` — reorganización sin cambio de comportamiento
- `pipeline` — cambios al flujo de ingesta/clasificación/generación

Todos los commits generados por el bot llevan `Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>`.

## Roadmap

El plan de mejora estratégico vive en [`PLAN.md`](PLAN.md): 4 fases (base / distribución / contenido diferencial / red) + deuda técnica puntual + prioridades honestas + qué NO hacer. Al cerrar un punto, marcar estado en la tabla de seguimiento de `PLAN.md` y registrar entrada en [`DIARIO.md`](DIARIO.md).

## Qué NO hacer

- No escribir lógica de scraping HTML directo a diarios (frágil, legalmente gris). RSS solo.
- No cambiar modelos a mitad de ejecución (rompe caché y sube coste).
- No commitear `.env` ni claves. El `.gitignore` ya cubre `*.key` y `.env`.
- No publicar ediciones manuales con fechas futuras (el `permalink` se confunde).
- **No usar "W17" ni numeración de semana ISO en cara pública.** Solo como slug interno (archivos, logs, commits). En cara pública, URLs y etiquetas siempre con rango de fechas: `/ediciones/2026-04-20/`, `"Edición del 20-26 abril 2026"`.
- **No colorear partidos políticos con su color** (regla dura de imparcialidad visual). Todos los partidos van en gris neutro (`--actor-partido`). Ver [ESTUDIO-DISENO.md §5.1](ESTUDIO-DISENO.md).
- **No citar identificadores internos del proyecto al editor sin nombrar primero la cosa.** Regla dura tratada como sección propia arriba (*Lenguaje en el chat del proyecto*). Códigos tipo `RT15`, `PI9`, `D11`, `W17`, `Q3`, `B34`, `FU2`, `ED1`, `UX3` nunca van como etiqueta principal ni como primer elemento de una línea. 4 recaídas acumuladas a 2026-04-24 — próxima = fallo grave.

## Nivel de proactividad

Raúl está en nivel **normal** según `~/.claude/CLAUDE.md`. Aplicar criterio ahí descrito. Si algo del pipeline parece reutilizable para otros proyectos (p.ej. el sistema de control de costes), proponer subirlo a la plantilla.
