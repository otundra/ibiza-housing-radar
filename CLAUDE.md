# CLAUDE.md — Ibiza Housing Radar

Instrucciones para Claude Code al trabajar en este proyecto.

> ⚠️ **Pivote activo 2026-04-20.** El proyecto está migrando a "observatorio documental" (el LLM no genera propuestas, solo documenta las de actores reales con URL verificable). Todo el trabajo vive en el branch `pivote/observatorio-documental`. Antes de tocar código en ese branch, leer:
>
> - [`PIVOTE.md`](PIVOTE.md) — 5 reglas duras + decisión fundacional.
> - [`ROADMAP.md`](ROADMAP.md) — Fase 0 completa.
> - [`ARQUITECTURA.md`](ARQUITECTURA.md) — pipeline nuevo con módulos `extract.py`, `verify.py`, `rescue.py`, `balance.py`.
> - [`DISENO-WEB.md`](DISENO-WEB.md) — UX dual (primer visitante + profesional recurrente).
> - [`SEO.md`](SEO.md) — plan SEO ambicioso.
> - [`CONTENIDO-RETROACTIVO.md`](CONTENIDO-RETROACTIVO.md) — 4 ediciones simuladas W14-W17.
> - [`DECISIONES-PENDIENTES.md`](DECISIONES-PENDIENTES.md) — 16 decisiones pendientes del editor.
>
> El contenido que sigue describe el **modelo antiguo** (aún operativo en `main` hasta merge). Las convenciones de commit, coste y estructura de repo siguen siendo válidas.

## Qué es

Observatorio automatizado semanal sobre la crisis de vivienda en Ibiza con foco en trabajadores de temporada (mayo-octubre). Cada lunes genera un informe con propuestas accionables enlazadas a las noticias que las motivan. Publicado en GitHub Pages.

## Stack

- **Lenguaje:** Python 3.12
- **IA:** Anthropic Claude API (Haiku 4.5 para clasificación, Opus 4.7 para generación)
- **Fuentes:** RSS de Google News + Diario de Ibiza + Periódico de Ibiza
- **Web:** Jekyll (GitHub Pages) con tema custom (CSS editorial propio)
- **Scheduler:** GitHub Actions cron semanal
- **Hosting:** 100 % GitHub (repo + Pages + Actions). 0 € de infra.
- **Coste esperado:** ~2 USD/mes en API Anthropic. Tope duro configurable en `src/costs.py` (actual: 5 USD/mes).

## Estructura

```
.
├── src/                        # Pipeline Python
│   ├── ingest.py               # Lee RSS + filtra keywords + dedup
│   ├── classify.py             # Haiku: is_housing, actor, palanca
│   ├── generate.py             # Opus: genera informe semanal markdown
│   ├── build_index.py          # Regenera docs/index.md
│   ├── costs.py                # Tracking + dashboard + tope mensual
│   ├── report.py               # Orquestador end-to-end
│   └── sources.yaml            # Feeds + keywords + ventana temporal
├── data/
│   ├── costs.csv               # Append-only, histórico de llamadas API
│   ├── ingested.json           # (temporal) noticias crudas de la semana
│   └── classified.json         # (temporal) noticias ya clasificadas
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

5. **Topes de presupuesto en euros + filosofía no-cortar-editorial.** Sistema de capas en `src/costs.py`: blando (`MONTHLY_SOFT_CAP_EUR = 8`) solo avisa por Telegram y sigue publicando; duro (`MONTHLY_HARD_CAP_EUR = 20`) corta para proteger contra runaway (bugs, bucles). No se pierde editorial por sobrecoste salvo desastre real. Alertas vía `src/notify.py` (Telegram con fallback a issue GitHub).

6. **Modelo por fase.** Haiku para filtrar (coste marginal), Opus solo para la pieza final donde la calidad editorial sí importa. No mezclar.

## Diario del proyecto

Cuando haya un cambio relevante (hito, decisión, fix estructural, no-commits triviales), añadir una entrada a [`DIARIO.md`](DIARIO.md) con formato viñetas: tema en **negrita** + línea breve combinando qué/por qué/impacto.

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

## Nivel de proactividad

Raúl está en nivel **normal** según `~/.claude/CLAUDE.md`. Aplicar criterio ahí descrito. Si algo del pipeline parece reutilizable para otros proyectos (p.ej. el sistema de control de costes), proponer subirlo a la plantilla.
