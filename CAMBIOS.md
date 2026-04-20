# Diario de cambios — Ibiza Housing Radar

Registro cronológico de hitos, decisiones y cambios relevantes.

Formato: agrupar por fecha, cada cambio una viñeta con el tema en **negrita** y una línea breve (qué/por qué/impacto combinados).

Reglas:
- Más recientes arriba.
- Solo cambios con valor de memoria futura. No entradas para commits triviales.
- No duplicar lo que ya dice Git: aquí va el contexto, no el diff.
- Si un cambio altera arquitectura o stack, también actualizar `CLAUDE.md` y `README.md`.

---

## 2026-04-20 — Día 1: montaje y primer informe

- **Scaffold inicial** — estructura `src/` (pipeline Python) + `docs/` (Jekyll root) + `.github/workflows/` (cron semanal + validación de key) + `data/` (estado). Base para todo lo demás.
- **Workflow de validación de key** — `validate-key.yml` con dispatch manual hace ping mínimo a la API de Anthropic con Haiku. Confirma HTTP 200 antes del primer run real sin consumir presupuesto.
- **Pipeline end-to-end + tema Jekyll custom** — ingest → classify → generate → build_index → costs → report. Tema editorial (Instrument Serif + Inter + JetBrains Mono, paleta terracota-crema, dark mode). Primera edición W16 escrita a mano como semilla.
- **Fix imports absolutos desde `src`** — primer run falló con `ModuleNotFoundError: No module named 'costs'` al ejecutar con `python -m src.report`. Cambiado `from costs import …` → `from src.costs import …` en `classify.py` y `generate.py`.
- **`max_tokens=8192` en Opus** — la W17 salió truncada exactamente a 4096 tokens. Subido el límite para que no corte ediciones largas.
- **Fix slug del link a GitHub** — `build_index.py` generaba link mal por mayúsculas en el week (`2026-W16` vs `2026-w16`). Resuelto con `| downcase`.
- **Jekyll: plugins SEO + feed + sitemap** — habilitados `jekyll-feed`, `jekyll-sitemap`, `jekyll-seo-tag`. `/feed.xml` y `/sitemap.xml` disponibles desde el día 1.
- **Push con retry + rebase** — race condition: el workflow falló porque se pushearon commits en paralelo durante la ejecución. Loop de 3 intentos con `git pull --rebase` en el step de commit.
- **`STATUS.md` de despertar** — documento único con TL;DR, estado, qué revisar, decisiones tomadas sin preguntar y troubleshooting. Punto de entrada para reengancharse al proyecto.
- **Fix URLs de Google News** — los enlaces iban a `news.google.com/rss/articles/…` firmado. Instalado `googlenewsdecoder>=0.1.7`, decodifica el protocolo firmado y devuelve la URL original. Ahora los enlaces apuntan a `elpais.com`, `diariodeibiza.es`, etc.
- **Limpieza de limitación conocida** — eliminada sección en `STATUS.md` sobre URLs de Google News tras verificar el fix en producción. Documentación consistente con el estado real.
- **`CAMBIOS.md` del proyecto** — creado el diario con formato viñetas + enlaces desde `README.md` y `CLAUDE.md`. Norma: toda decisión o fix estructural se registra aquí.
