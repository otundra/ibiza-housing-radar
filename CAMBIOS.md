# Diario de cambios — Ibiza Housing Radar

Registro cronológico de hitos, decisiones y cambios relevantes del proyecto.

Formato por entrada:
- **Qué cambió** (descripción breve)
- **Por qué** (motivación o problema que resolvía)
- **Impacto** (qué cambia para el usuario o el pipeline)

---

## 2026-04-20 — Día 1: montaje y primer informe

### Scaffold inicial

**Qué:** estructura completa del repo: `src/` (pipeline Python), `docs/` (Jekyll root), `.github/workflows/` (cron semanal + validación de key), `data/` (estado), `CLAUDE.md` + `README.md`.

**Por qué:** dejar todo el proyecto funcionando end-to-end en una sola sesión, sin intervención humana posterior.

**Impacto:** base para todo lo demás.

### Workflow de validación de key

**Qué:** `.github/workflows/validate-key.yml` con dispatch manual. Hace un ping mínimo a la API de Anthropic con Haiku.

**Por qué:** comprobar el secret `ANTHROPIC_API_KEY` sin consumir casi nada antes del primer run real.

**Impacto:** se confirma HTTP 200 con Haiku antes de lanzar el pipeline completo.

### Pipeline end-to-end + tema Jekyll

**Qué:** `ingest.py` + `classify.py` + `generate.py` + `build_index.py` + `costs.py` + `report.py`. Tema editorial custom (Instrument Serif + Inter + JetBrains Mono, paleta terracota-crema, dark mode). Primera edición W16 escrita a mano.

**Por qué:** necesitamos pipeline completo (ingesta → clasificación → generación → publicación) y que la web tenga identidad editorial desde el día 1.

**Impacto:** W16 publicada en `/ediciones/2026-w16/`.

### Fix: imports absolutos desde `src`

**Qué:** cambiar `from costs import ...` a `from src.costs import ...` en `classify.py` y `generate.py`.

**Por qué:** primer run del workflow falló con `ModuleNotFoundError: No module named 'costs'` al ejecutarse como `python -m src.report`.

**Impacto:** pipeline ejecutable correctamente desde la raíz del repo.

### Fix: `max_tokens=8192` en Opus + primer intento de resolución Google News

**Qué:** subir `max_tokens` de 4096 a 8192 en `generate.py`. Primer intento (fallido) de resolver URLs de Google News con `httpx.follow_redirects`.

**Por qué:** la W17 salió truncada exactamente a 4096 tokens. Y las URLs de Google News apuntaban a `news.google.com/rss/articles/...` en vez del diario original.

**Impacto:** ediciones completas. URLs seguían feas (Google firma las URLs, no es redirect HTTP simple).

### Fix: `build_index.py` formatea bien el slug `YYYY-wWW`

**Qué:** `{{ page.week | downcase }}.md` en lugar de `slice` concatenados.

**Por qué:** el link a "ver fuente en GitHub" rompía por mayúsculas/minúsculas.

**Impacto:** link correcto en cada edición.

### Jekyll: plugins SEO + feed + sitemap

**Qué:** habilitados `jekyll-feed`, `jekyll-sitemap`, `jekyll-seo-tag` en `_config.yml`.

**Por qué:** que el sitio sea indexable, tenga RSS propio y metadatos OG desde el inicio.

**Impacto:** `/feed.xml` y `/sitemap.xml` generados automáticamente.

### Fix: push con reintento + `pull --rebase` contra race conditions

**Qué:** loop de 3 intentos en el step "Commit edition and costs" del workflow. Si el push falla por non-fast-forward, hace `git pull --rebase` y reintenta.

**Por qué:** el run #3 falló porque se pushearon commits desde otro lado durante la ejecución.

**Impacto:** el workflow tolera que alguien pushee entre medias (humano u otro workflow).

### `STATUS.md`: resumen de despertar

**Qué:** documento con TL;DR, qué está hecho, qué revisar, decisiones tomadas sin preguntar, limitaciones conocidas, comandos útiles, tabla de troubleshooting.

**Por qué:** Raúl se acostó y pidió que al despertar tuviera todo claro en un solo sitio.

**Impacto:** punto de entrada único para reengancharse al proyecto.

### Fix definitivo: URLs de Google News con `googlenewsdecoder`

**Qué:** añadido `googlenewsdecoder>=0.1.7` a `requirements.txt`. Reescrita `_resolve_gnews` en `src/ingest.py` para usar la librería (decodifica el protocolo firmado de Google News) en lugar de seguir redirects HTTP.

**Por qué:** la limitación conocida de URLs largas `news.google.com/rss/articles/...` era cosmética pero fea. El paquete decodifica la URL firmada y devuelve el artículo original (`elpais.com/...`, `diariodeibiza.es/...`, etc.).

**Impacto:** W17 regenerada con 0 URLs de Google News. Todos los enlaces apuntan al dominio del diario original.

### Limpieza: sección de limitación conocida fuera de `STATUS.md`

**Qué:** eliminado el apartado "⚠️ Limitación conocida: URLs a través de Google News" y el punto 4 de "qué revisar" que lo acompañaba.

**Por qué:** ya no aplica, el fix está en producción.

**Impacto:** documentación consistente con el estado real.
