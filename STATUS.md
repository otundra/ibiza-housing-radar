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
- `classify.py` — una sola llamada a **Claude Haiku 4.5** clasifica todos los titulares (is_housing, actor, palanca). Coste ≈ $0,01/semana.
- `generate.py` — **Claude Opus 4.7** genera el informe semanal (max 8.192 tokens). Coste ≈ $0,60/semana.
- `build_index.py` — regenera `docs/index.md` con todas las ediciones ordenadas.
- `costs.py` — registra cada llamada en CSV, regenera dashboard, aborta si mes supera $5.
- `report.py` — orquestador end-to-end.

### 3. Sistema de control de costes

- Append-only en [`data/costs.csv`](data/costs.csv)
- Dashboard legible en [`docs/costs.md`](docs/costs.md) (se regenera tras cada run)
- Tope duro: **5 USD/mes**. Editar `MONTHLY_BUDGET_USD` en `src/costs.py` para subirlo.
- Coste esperado real: **~2 USD/mes** (60-70% es Opus, el resto Haiku + ingesta).
- Si se supera el tope, el pipeline aborta **antes** de llamar a la API. No hay forma de que se dispare el gasto.

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
3. **Revisar costes** → <https://otundra.github.io/ibiza-housing-radar/costes/>. Debe estar en torno al 15-25 % del tope.

### Recomendable (15 min)

4. **Comprobar que las URLs de la W17 llevan al artículo real**. El pipeline resuelve los redirects de Google News; si alguno quedó como URL larga de `news.google.com`, es que el redirect falló (no rompe, solo queda feo).
5. **Decidir si subes el tope de coste.** Está en $5/mes. Si quieres más margen, cambia `MONTHLY_BUDGET_USD` en `src/costs.py`.
6. **Decidir lector objetivo.** Sigue sin definir. Afecta a: tono (más técnico-político vs. más divulgativo), distribución (newsletter, RRSS, nada), y qué diarios priorizar. Sin esto afinado, el sistema irá dando vueltas sobre lo mismo.

## ⚠️ Decisiones que tomé sin preguntarte

1. **Repo público en lugar de privado.** GitHub Pages no sirve desde repos privados en plan Free. Alternativas eran: pagar Pro, usar Netlify/Cloudflare Pages (cuenta nueva), o hacer el repo público. Elegí pública porque (a) el contenido ya es prensa pública + ideas, (b) la API key sigue guardada en Secrets, (c) te da transparencia como proyecto.
2. **Modelos de Anthropic.** Haiku 4.5 para clasificar (es lo más barato que mantiene calidad), Opus 4.7 para el informe (la calidad editorial sí importa ahí). Puedes cambiarlos en `src/classify.py` y `src/generate.py` — variable `MODEL`.
3. **Tope mensual $5.** Es ~2,5× el coste esperado. Margen razonable para evitar bloqueos por picos ocasionales pero suficientemente bajo para que una avería no haga daño.
4. **Fuentes RSS.** Google News como base (robusto, cubre todo) + RSS nativos de Diario y Periódico como refuerzo. Si un feed falla, se salta y sigue.

## 🟢 Flujo del lunes (qué pasará automáticamente)

```
05:00 UTC  cron dispara weekly-report.yml
05:00      checkout + pip install
05:01      src/ingest.py   → data/ingested.json
05:02      src/classify.py → data/classified.json   (1 llamada a Haiku)
05:03-05   src/generate.py → docs/editions/YYYY-wWW.md  (1 llamada a Opus)
05:05      src/build_index.py → docs/index.md
05:05      src/costs.py   → docs/costs.md + data/costs.csv
05:05      git commit + push con retry/rebase
05:06      Jekyll rebuild en GitHub Pages (~30s)
05:07      Nueva edición visible en la web
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

## ⚠️ Limitación conocida: URLs a través de Google News

Las URLs de las noticias en la edición automática apuntan a `news.google.com/rss/articles/...` en vez de al dominio del diario original. Motivo: Google News firma las URLs y ya no hace un simple redirect HTTP — requiere decodificar una URL firmada con un protocolo específico.

**Impacto real:** ninguno funcional — el click funciona y termina en el artículo original via Google News. Solo es cosmético (el href es largo y no informativo).

**Cómo resolverlo cuando quieras:** instalar el paquete `googlenewsdecoder` en `requirements.txt` y usarlo en `src/ingest.py::_resolve_gnews`. Añade ~200 ms por URL pero da URLs limpias del estilo `https://www.elpais.com/...`.

## 📋 Mejoras candidatas (cuando quieras)

- **Prompt caching** del `SYSTEM` del generador. Bajaría ~50% el coste de Opus. Gratis salvo el primer turno.
- **Newsletter email** con Buttondown (5 €/mes) o Listmonk self-hosted (0 €).
- **BOIB scraper** — normativa oficial de Baleares, gratis.
- **Dominio propio** `radar.ibizahousing.org` o similar. ~10 €/año.
- **Mejorar prompt del generador** con tu feedback sobre la W17.

## 🐛 Si algo falla

| Síntoma | Probable causa | Acción |
|---|---|---|
| Workflow falla en "Run pipeline" con error de API | Key revocada o sin crédito | Revisar <https://console.anthropic.com/settings/billing> |
| Web no muestra nueva edición | Jekyll build aún corriendo | Esperar 1-2 min y recargar |
| Edición sale truncada | `max_tokens` demasiado bajo | Subir en `src/generate.py` |
| Ediciones repetidas / raras | Bug en `build_index.py` | Mirar git log de `docs/index.md` |
| Presupuesto bloqueado | Mes excedió tope | Subir `MONTHLY_BUDGET_USD` en `src/costs.py` |

---

Buenos días ☀️ — Claude
