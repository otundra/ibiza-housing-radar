# CLAUDE.md — Ibiza Housing Radar

Instrucciones para Claude Code al trabajar en este proyecto.

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
│   ├── assets/css/main.css     # Theme custom
│   ├── assets/favicon.svg
│   ├── editions/               # Ediciones semanales YYYY-wWW.md
│   ├── index.md                # Regenerado por build_index.py
│   ├── acerca.md
│   └── costs.md                # Regenerado por costs.py
├── .github/workflows/
│   ├── weekly-report.yml       # Cron lunes 05:00 UTC
│   └── validate-key.yml        # Test manual de la API key
├── requirements.txt
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

5. **Tope de presupuesto duro.** Antes de cualquier llamada a la API, el pipeline comprueba el gasto del mes en curso. Si el proyectado supera `MONTHLY_BUDGET_USD`, aborta. Protege contra bucles o escalada accidental.

6. **Modelo por fase.** Haiku para filtrar (coste marginal), Opus solo para la pieza final donde la calidad editorial sí importa. No mezclar.

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

## Próximas mejoras candidatas

- Añadir fuente de BOIB (convocatorias IBAVI, normativa autonómica).
- Detectar tendencias multi-semana (p.ej. evolución del precio medio de habitación).
- Newsletter por email vía Buttondown o similar (0-5 €/mes).
- Dominio propio `radar.ibizahousing.org` cuando tenga tracción.
- Caché de prompt (Anthropic prompt caching) sobre el SYSTEM prompt del generador para bajar el 50 % del coste del Opus.

## Qué NO hacer

- No escribir lógica de scraping HTML directo a diarios (frágil, legalmente gris). RSS solo.
- No cambiar modelos a mitad de ejecución (rompe caché y sube coste).
- No commitear `.env` ni claves. El `.gitignore` ya cubre `*.key` y `.env`.
- No publicar ediciones manuales con fechas futuras (el `permalink` se confunde).

## Nivel de proactividad

Raúl está en nivel **normal** según `~/.claude/CLAUDE.md`. Aplicar criterio ahí descrito. Si algo del pipeline parece reutilizable para otros proyectos (p.ej. el sistema de control de costes), proponer subirlo a la plantilla.
