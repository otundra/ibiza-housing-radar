# Estado al despertar — 20 abr 2026

## 🎯 TL;DR

**Todo funciona.** La web está live, la primera edición publicada, el pipeline semanal automatizado y el control de costes operativo.

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
  - 🟡 4-6 €: Telegram FYI
  - 🟠 6-8 €: Telegram atención
  - 🔴 8-20 € (**tope blando**): Telegram urgente, **pipeline sigue publicando**. No se pierde editorial por sobrecoste.
  - 🚨 >20 € (**tope duro**): corte inmediato + alerta crítica. Protección runaway.
- Coste esperado real: **~2 €/mes** (~3,15 €/mes si se activa trilingüe). Los topes cubren ambos escenarios.

### 4. Theme Jekyll editorial custom

- Tipografía: Instrument Serif (titulares) + Inter (cuerpo) + JetBrains Mono (código)
- Paleta terracota-atardecer (accent `#c14a2d`) sobre crema cálido (`#f8f4ec`)
- Responsive, con `prefers-color-scheme: dark` completo
- Sticky header, hero con gradiente, cards para ediciones
- `_layouts/`: default, home, edition, page
- Plugins activos: jekyll-feed (RSS), jekyll-sitemap, jekyll-seo-tag

### 5. Primera edición publicada

- **W16 (2026-04-20)** — escrita a mano durante el setup, con contenido real de noticias recientes. La tienes en [`/ediciones/2026-w16/`](https://otundra.github.io/ibiza-housing-radar/ediciones/2026-w16/).
- **W17** — generada automáticamente por el pipeline (contenido real, URLs resueltas al artículo original). En [`/ediciones/2026-w17/`](https://otundra.github.io/ibiza-housing-radar/ediciones/2026-w17/).

## 🔍 Qué revisar cuando despiertes

### Imprescindible (5 min)

1. **Abrir la web** → <https://otundra.github.io/ibiza-housing-radar/>
2. **Leer la W17 entera** → es el primer informe 100% generado por el pipeline. Si te sabe bien, el sistema funciona. Si hay frases raras, dime qué y retoco el system prompt del generador.
3. **Revisar costes** → abre `private/costs.md` en tu clon local o en GitHub. Debe estar bien por debajo del tope blando (8 €).

### Recomendable (15 min)

4. **Topes ya calibrados en €.** Blando 8 €, duro 20 €. Cubre trilingüe cuando se active. Solo tocar si hay razón concreta.
5. **Decidir lector objetivo.** Sigue sin definir. Afecta a: tono (más técnico-político vs. más divulgativo), distribución (newsletter, RRSS, nada), y qué diarios priorizar. Sin esto afinado, el sistema irá dando vueltas sobre lo mismo.

## ⚠️ Decisiones que tomé sin preguntarte

1. **Repo público en lugar de privado.** GitHub Pages no sirve desde repos privados en plan Free. Alternativas eran: pagar Pro, usar Netlify/Cloudflare Pages (cuenta nueva), o hacer el repo público. Elegí pública porque (a) el contenido ya es prensa pública + ideas, (b) la API key sigue guardada en Secrets, (c) te da transparencia como proyecto.
2. **Modelos de Anthropic.** Haiku 4.5 para clasificar (es lo más barato que mantiene calidad), Opus 4.7 para el informe (la calidad editorial sí importa ahí). Puedes cambiarlos en `src/classify.py` y `src/generate.py` — variable `MODEL`.
3. **Topes revisados en €** (20-abr-2026): blando 8 € (≈4× coste actual) avisa sin cortar, duro 20 € (≈10× actual) corta solo ante runaway. Cubre también el escenario trilingüe (~3,15 €/mes) sin retocar. Filosofía: no perder editorial por sobrecoste salvo desastre real.
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

## 📋 Plan de mejora

El roadmap vivo vive en [`PLAN.md`](PLAN.md): 4 fases (base, distribución, contenido diferencial, red) + deuda técnica puntual. **Principio económico: 0 € salvo IA** (~2 €/mes de la API ya en marcha). Dominio propio diferido hasta tracción.

**Prioridades próximas 4 semanas** (del PLAN, todas 0 €):

1. Analítica (GoatCounter) + identidad editorial + metodología pública (Fase 1).
2. Newsletter (Buttondown free) + envío directo a periodistas locales (Fase 2).
3. Observatorio de precios por agregación de fuentes oficiales + crowd-sourcing ciudadano (Fase 3).

**Deuda técnica recomendada en paralelo:** prompt caching en Opus (~50 % ahorro), resiliencia en `classify.py`, métricas de pipeline, notificación de fallo del cron.

## 🐛 Si algo falla

| Síntoma | Probable causa | Acción |
|---|---|---|
| Workflow falla en "Run pipeline" con error de API | Key revocada o sin crédito | Revisar <https://console.anthropic.com/settings/billing> |
| Web no muestra nueva edición | Jekyll build aún corriendo | Esperar 1-2 min y recargar |
| Edición sale truncada | `max_tokens` demasiado bajo | Subir en `src/generate.py` |
| Ediciones repetidas / raras | Bug en `build_index.py` | Mirar git log de `docs/index.md` |
| Pipeline cortado por tope duro | Mes excedió 20 € (runaway real o bug) | Abrir `private/costs.md`, identificar origen, subir `MONTHLY_HARD_CAP_EUR` en `src/costs.py` solo si hay razón legítima |
| Telegram no llega | Token rotado, bot bloqueado o red caída | Si es crítico llegará como issue en GitHub. Verificar `TELEGRAM_BOT_TOKEN` con `curl` a `api.telegram.org/bot<TOKEN>/getMe` |

---

Buenos días ☀️ — Claude
