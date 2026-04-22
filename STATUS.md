# Estado al despertar — 21 abr 2026

## ⏸ PAUSA ACTIVA (21-abr-2026 tarde) — Prototipo HTML entregado, diseño en hold

> **El editor pide parar el tema diseño/frontend para estudiar primero la arquitectura.** Nada que retocar del prototipo hasta nueva orden.
>
> **Prototipo visitable online** (noindex, no aparece en Google pero accesible con la URL): [home](https://otundra.github.io/ibiza-housing-radar/prototype/home.html) · [edition](https://otundra.github.io/ibiza-housing-radar/prototype/edition.html) · [actor](https://otundra.github.io/ibiza-housing-radar/prototype/actor.html) · [proposal](https://otundra.github.io/ibiza-housing-radar/prototype/proposal.html) · [preview logo](https://otundra.github.io/ibiza-housing-radar/prototype/logo/preview.html). Publicado vía Pages tras mover `prototype/` → `docs/prototype/`.
>
> **Qué está entregado:** Paso 1 del plan de prototipo (B34 del ROADMAP, §10 del estudio). 4 HTMLs estáticos en [`docs/prototype/`](docs/prototype/) + CSS + JS vanilla, datos reales de la edición del 20-26 abril 2026. Verificado en navegador, consola limpia, toggle tema persiste, a11y spot-checks OK. **B34 en revisión, no cerrado** — falta visto bueno visual y responder 3 preguntas abiertas.
>
> **Qué queda por revisar cuando se retome:** (1) lectura del wordmark V2 Split en cabecera real; (2) apilado de 6 chips de coalición en mobile; (3) si la barra de progreso muestra siempre los 8 estados o solo los aplicables.
>
> **Resto del Bloque B en espera.** ~20 páginas restantes del ROADMAP (política editorial, metodología, balance, radar, actores, propuestas, correcciones, glosario, estado, sistema, sin-dato, auditoría, costes, etc.) — pendiente de decisión del editor sobre alcance (shells vs estructura real vs completas).
>
> **Cómo recuperar el preview local:** `preview_start("prototype")` → `http://127.0.0.1:4100/home.html`. La config en [`.claude/launch.json`](.claude/launch.json) usa `/opt/homebrew/bin/python3` (el de Xcode está sandboxed).
>
> **Punto de entrada al retomar:** memoria [`prototipo_paso1_en_pausa.md`](../../.claude/projects/-Users-raulserrano-Documents-GitHub-ibiza-housing-radar/memory/prototipo_paso1_en_pausa.md) + [`DIARIO.md`](DIARIO.md) entradas 2026-04-21 + [`ESTUDIO-DISENO.md §10`](ESTUDIO-DISENO.md). No asumir aprobado.

## 🏷️ REBRANDING PROVISIONAL (21-abr-2026)

> Wordmark tipográfico cerrado 2026-04-21 noche: **`radar))ibiza_vivienda`** (formato `lugar_tema`, monospace). Logo SVG gráfico descartado; identidad 100% tipográfica. Dominio candidato `radaribiza.com` (compra pendiente según evolución del proyecto). Repo GitHub mantiene slug `ibiza-housing-radar`. Ver [DIARIO.md](DIARIO.md) entradas 2026-04-21.

## 🎨 ESTUDIO DE DISEÑO CERRADO (21-abr-2026)

> Entregable: [`ESTUDIO-DISENO.md`](ESTUDIO-DISENO.md) (14 secciones, ~700 líneas, benchmark con 13 referentes, 9 componentes especificados, plan de prototipo en 6 pasos).
>
> **13 decisiones (D1-D13) cerradas.** D1 cerrada con **V2 Split** (2026-04-21): wordmark en JetBrains Mono con `))` en terracota y resto en tinta. El orden del wordmark se fijó el mismo día en **`radar))ibiza_vivienda`** (formato `lugar_tema`). D2 resuelta con **favicon `))` vectorial** ([`docs/prototype/logo/favicon.svg`](docs/prototype/logo/favicon.svg)) — identidad 100% tipográfica. Preview vivo en [`docs/prototype/logo/preview.html`](docs/prototype/logo/preview.html).
>
> Dirección visual apuntada: **"mono + seams"** — mono tipográfico en más elementos + separadores tipo costura + iconografía Unicode (no emoji). Por formalizar al construir el prototipo HTML estático (Paso 1).
>
> Siguiente fase operativa: **Paso 1 del plan de prototipo** (B34 en ROADMAP) — HTML estático de 4 páginas con datos reales antes de migrar a Jekyll.

## 🧭 MODELO DOCUMENTAL ACTIVO (merge a `main` el 21-abr-2026)

> La transición al **modelo documental** está consolidada en `main` desde el 2026-04-21 mediodía (commit `b24a6ad`). Es el único modelo vigente. Origen: [estudio crítico](private/estudios/2026-04-20-propuestas.md) sobre el corpus W16-W17.
>
> **Expediente estratégico completo:**
>
> - [`PIVOTE.md`](PIVOTE.md) — decisión fundacional + 5 reglas duras.
> - [`ROADMAP.md`](ROADMAP.md) — Fase 0 de relanzamiento (pipeline + 15 páginas + contenido retroactivo + SEO + distribución) + fases siguientes.
> - [`ARQUITECTURA.md`](ARQUITECTURA.md) — pipeline nuevo con módulos `extract.py`, `verify.py`, `rescue.py`, `balance.py`.
> - [`DISENO-WEB.md`](DISENO-WEB.md) — UX dual (primer visitante + profesional recurrente), 15+ páginas nuevas.
> - [`ESTUDIO-DISENO.md`](ESTUDIO-DISENO.md) — sistema visual, benchmark editorial, 13 decisiones D1-D13 cerradas. **Nuevo 2026-04-21.**
> - [`SEO.md`](SEO.md) — plan ambicioso con long-tail, schema.org, OG dinámico, Search Console.
> - [`CONTENIDO-RETROACTIVO.md`](CONTENIDO-RETROACTIVO.md) — 8 ediciones simuladas W10-W17 bajo modelo nuevo.
> - [`DECISIONES-PENDIENTES.md`](DECISIONES-PENDIENTES.md) — 16 decisiones del editor resueltas.
>
> **Estado:** pipeline documental operativo en `main`. Bloque B (web) en pausa activa tras entrega del prototipo Paso 1. Revisión Fase 0.5 en curso antes de retomar diseño visual.

---

## 🎯 TL;DR operativo

**Todo funciona.** La web está live, el pipeline documental automatizado corre cada lunes y el control de costes está operativo. Snapshot append-only en `data/archive/YYYY-WNN/` desde la ejecución W17.

- 🌐 **Web:** <https://otundra.github.io/ibiza-housing-radar/>
- 📦 **Repo:** <https://github.com/otundra/ibiza-housing-radar> (público)
- ⏰ **Próxima edición automática:** lunes 27 abr 07:00 CEST

## ✅ Qué está hecho

### 1. Infraestructura (0 € de coste fijo)

- Repo GitHub público `otundra/ibiza-housing-radar`
- GitHub Pages sirviendo desde `/docs` rama `main`
- GitHub Actions con cron semanal lunes 05:00 UTC
- Secret `ANTHROPIC_API_KEY` validado contra la API real (HTTP 200 con Haiku)

### 2. Pipeline completo (`src/`)

- `ingest.py` — lee RSS de Google News (4 queries temáticas) + Diario de Ibiza + Periódico de Ibiza. Filtra por keywords, ventana de 10 días, deduplicación. Resuelve URLs de Google News al artículo original en paralelo.
- `classify.py` — una sola llamada a **Claude Haiku 4.5** clasifica todos los titulares (is_housing, actor, palanca). Coste ≈ 0,01 €/semana.
- `generate.py` — **Claude Opus 4.7** genera el informe semanal (max 8.192 tokens). Coste ≈ 0,55 €/semana.
- `build_index.py` — regenera `docs/index.md` con todas las ediciones ordenadas.
- `costs.py` — registra cada llamada en CSV (USD interno, euros para display), regenera dashboard privado, corta solo ante tope duro.
- `notify.py` — alertas Telegram con fallback a issue GitHub. Coste 0 €.
- `report.py` — orquestador end-to-end con resumen/alerta por Telegram al terminar (OK o fallo).

### 3. Sistema de control de costes en € con capas

- Append-only en [`data/costs.csv`](data/costs.csv) (USD internos para precisión).
- Dashboard **privado** en [`private/costs.md`](private/costs.md) — **no se sirve en la web**. Se regenera tras cada run.
- Topes en euros (editar `MONTHLY_SOFT_CAP_EUR` y `MONTHLY_HARD_CAP_EUR` en `src/costs.py`):
  - 🟢 <4 €: silencio
  - 🟢 <6 €: silencio
  - 🟡 6-9 €: Telegram FYI
  - 🟠 9-12 €: Telegram atención
  - 🔴 12-50 € (entre **tope blando** y **tope duro**): Telegram urgente, **pipeline sigue publicando**. No se pierde editorial por sobrecoste.
  - 🚨 >50 € (**tope duro**): corte inmediato + alerta crítica. Protección runaway.
- Coste esperado proyectado: **~6-7 €/mes** (pipeline + autoevaluación semanal + auditoría trimestral). Revisable cuando haya 3 meses de datos reales en `data/costs.csv`.

### 4. Theme Jekyll editorial custom

- Tipografía: Instrument Serif (titulares) + Inter (cuerpo) + JetBrains Mono (código)
- Paleta terracota-atardecer (accent `#c14a2d`) sobre crema cálido (`#f8f4ec`)
- Responsive, con `prefers-color-scheme: dark` completo
- Sticky header, hero con gradiente, cards para ediciones
- `_layouts/`: default, home, edition, page
- Plugins activos: jekyll-feed (RSS), jekyll-sitemap, jekyll-seo-tag

### 5. Primera edición publicada

- **W17 (20-26 abril 2026)** — primera edición generada 100% por el pipeline documental. Contenido real, URLs resueltas al artículo original, sin propuestas del observatorio. En [`/ediciones/2026-w17/`](https://otundra.github.io/ibiza-housing-radar/ediciones/2026-w17/). La W16 previa (modelo antiguo) se borró el 2026-04-21 para no contaminar el archivo público — sigue disponible en el histórico git.

## 🔍 Qué revisar cuando despiertes

### Imprescindible (5 min)

1. **Abrir la web** → <https://otundra.github.io/ibiza-housing-radar/>
2. **Leer la W17 entera** → es el primer informe 100% generado por el pipeline. Si te sabe bien, el sistema funciona. Si hay frases raras, dime qué y retoco el system prompt del generador.
3. **Revisar costes** → abre `private/costs.md` en tu clon local o en GitHub. Debe estar bien por debajo del tope blando (12 €).

### Recomendable (15 min)

4. **Topes ya calibrados en €.** Blando 12 €, duro 50 €. Cubre pipeline documental + autoevaluación + trilingüe cuando se active. Solo tocar si hay razón concreta.
5. **Decidir lector objetivo.** Sigue sin definir. Afecta a: tono (más técnico-político vs. más divulgativo), distribución (newsletter, RRSS, nada), y qué diarios priorizar. Sin esto afinado, el sistema irá dando vueltas sobre lo mismo.

## ⚠️ Decisiones que tomé sin preguntarte

1. **Repo público en lugar de privado.** GitHub Pages no sirve desde repos privados en plan Free. Alternativas eran: pagar Pro, usar Netlify/Cloudflare Pages (cuenta nueva), o hacer el repo público. Elegí pública porque (a) el contenido ya es prensa pública + ideas, (b) la API key sigue guardada en Secrets, (c) te da transparencia como proyecto.
2. **Modelos de Anthropic.** Haiku 4.5 para clasificar (es lo más barato que mantiene calidad), Opus 4.7 para el informe (la calidad editorial sí importa ahí). Puedes cambiarlos en `src/classify.py` y `src/generate.py` — variable `MODEL`.
3. **Topes revisados en €** (21-abr-2026): blando 12 € (absorbe pipeline documental + autoevaluación), duro 50 € (subido desde 20 € para absorber backfill 12 semanas + auditor IA sin bloqueos). Filosofía: no perder editorial por sobrecoste salvo desastre real.
4. **Fuentes RSS.** Google News como base (robusto, cubre todo) + RSS nativos de Diario y Periódico como refuerzo. Si un feed falla, se salta y sigue.

## 🟢 Flujo del lunes (qué pasará automáticamente)

```
05:00 UTC  cron dispara weekly-report.yml
05:00      checkout + pip install
05:01      src/ingest.py   → data/ingested.json
05:02      src/classify.py → data/classified.json   (1 llamada a Haiku)
05:03-05   src/generate.py → docs/_editions/YYYY-wWW.md  (1 llamada a Opus)
05:05      src/build_index.py → docs/index.md (panel de la última edición)
05:05      src/costs.py   → private/costs.md + data/costs.csv
05:05      src/report.py  → resumen OK a Telegram (o alerta crítica si falló)
05:05      git commit + push con retry/rebase
05:06      Jekyll rebuild en GitHub Pages (~30s)
05:07      Nueva edición visible en la web + aviso en tu Telegram
```

## 🛠 Comandos útiles

```bash
# Ver estado del repo
gh repo view otundra/ibiza-housing-radar --web

# Disparar manualmente una ejecución
gh workflow run weekly-report.yml -R otundra/ibiza-housing-radar

# Ver historial de ejecuciones
gh run list -R otundra/ibiza-housing-radar --workflow=weekly-report.yml

# Ejecutar pipeline en local (necesita ANTHROPIC_API_KEY)
cd ~/Documents/GitHub/ibiza-housing-radar
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...
python -m src.report
```

## 📋 Plan de mejora — modelo documental

El roadmap de trabajo activo vive en [`ROADMAP.md`](ROADMAP.md) (estructura V2 en 7 fases ejecutables). El [`PLAN.md`](PLAN.md) original se conserva como referencia histórica.

**Bloqueante antes de arrancar Fase 0:** confirmar las 16 decisiones en [`DECISIONES-PENDIENTES.md`](DECISIONES-PENDIENTES.md) (reescritura W16-W17, dominio propio, fecha relanzamiento, autoría, distribución, etc.).

**Fase 0 incluye:** pipeline nuevo (A **cerrado 2026-04-20**), 15+ páginas web (B pendiente), contenido retroactivo 8 ediciones (C pendiente), SEO masivo (D), analítica (E), distribución newsletter (F), utilidad pública diferida (G), legal y transparencia (H). Coste API proyectado ~6-7 €/mes dentro del tope blando 12 €.

## 🐛 Si algo falla

| Síntoma | Probable causa | Acción |
|---|---|---|
| Workflow falla en "Run pipeline" con error de API | Key revocada o sin crédito | Revisar <https://console.anthropic.com/settings/billing> |
| Web no muestra nueva edición | Jekyll build aún corriendo | Esperar 1-2 min y recargar |
| Edición sale truncada | `max_tokens` demasiado bajo | Subir en `src/generate.py` |
| Ediciones repetidas / raras | Bug en `build_index.py` | Mirar git log de `docs/index.md` |
| Pipeline cortado por tope duro | Mes excedió 50 € (runaway real o bug) | Abrir `private/costs.md`, identificar origen, subir `MONTHLY_HARD_CAP_EUR` en `src/costs.py` solo si hay razón legítima |
| Telegram no llega | Token rotado, bot bloqueado o red caída | Si es crítico llegará como issue en GitHub. Verificar `TELEGRAM_BOT_TOKEN` con `curl` a `api.telegram.org/bot<TOKEN>/getMe` |

---

Buenos días ☀️ — Claude
