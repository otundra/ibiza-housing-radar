# Diario del proyecto — Ibiza Housing Radar

Registro cronológico de hitos, decisiones y cambios relevantes.

Formato: agrupar por fecha, cada cambio una viñeta con el tema en **negrita** y una línea breve (qué/por qué/impacto combinados).

Reglas:
- Más recientes arriba.
- Solo cambios con valor de memoria futura. No entradas para commits triviales.
- No duplicar lo que ya dice Git: aquí va el contexto, no el diff.
- Si un cambio altera arquitectura o stack, también actualizar `CLAUDE.md` y `README.md`.

---

## 2026-04-20 — Plan de mejora estratégico

- **Diagnóstico y plan de ruta** — auditoría completa del proyecto tras la primera edición automática. Conclusión: parte técnica sólida, pero impacto cero porque no hay distribución, ni tracking, ni feedback, ni fuente primaria propia. Creado [`PLAN.md`](PLAN.md) con 4 fases (base, distribución, contenido diferencial, red) + deuda técnica puntual + prioridades honestas + qué NO hacer. Documento vivo; cada punto cerrado se registra aquí.
- **Pivot a coste-cero salvo IA** — revisión del PLAN para que todo el roadmap sea 0 € directo. Único gasto aceptado: API Anthropic (~2 €/mes, ya en marcha). Dominio propio diferido hasta tracción (criterios explícitos en PLAN.md). Sustituciones clave: Plausible → GoatCounter, scraping Idealista → agregación de informes oficiales + crowd-sourcing ciudadano, evento pagado → co-organización con entidad local. Ahorro estimado: ~76 €/año sin pérdida relevante del 90 % del valor.
- **Sección de monetización añadida al PLAN** — estudio realista de 12 vías con rango de ingreso año 1 y año 3, esfuerzo, riesgo de misión. Techo honesto año 3-5: 5-20 k€/año combinados, nunca salario completo. Verdes: donaciones pasivas, grants periodísticos, consultoría institucional con transparencia, partnership institucional, charlas, libro anual, membership voluntario sin paywall del informe principal, licencia premium de dataset, servicios freelance derivados. Grises: merchandising simbólico en eventos. Rojas descartadas: publicidad, sponsored content, affiliate, paywall total, encargo del actor fiscalizado, ocultar financiación. Roadmap: 2026 Ko-fi pasivo + `/financiacion`; 2027 asociación + primer grant; 2028+ diversificación. Regla vinculante: transparencia radical publicando cada ingreso en `/financiacion`.
- **Observatorio de precios concretado y scraping descartado** — Fase 3.1 del PLAN detallada con Vía A (agregación de fuentes oficiales: Idealista/Fotocasa/INE/IBESTAT/Ministerio) + Vía B (formulario crowd-sourcing con cobertura de toda la isla, solo acuse automático, publicación en CSV anónimo, umbral mínimo de 10 respuestas por segmento para evitar reidentificación, sesgo muestral declarado). Scraping directo de portales descartado con justificación explícita (contradicción reputacional con la línea editorial, riesgo legal real por jurisprudencia Idealista, coste real de consulta legal 500-1.500 € vs los 80 € originalmente estimados, valor marginal sobre las vías limpias, mantenimiento frágil). Ruta de reserva vía API oficial condicionada a Fase 4.1 cerrada.

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
- **`DIARIO.md` del proyecto** — creado el diario con formato viñetas + enlaces desde `README.md` y `CLAUDE.md`. Norma: toda decisión o fix estructural se registra aquí.
- **Títulos de edición en lenguaje natural** — sustituido `"Semana 17 · 2026"` por `"Semana 4 - Abril 2026"` (número = posición del jueves ISO dentro de su mes). Helper `human_week_title()` en `generate.py`. Aplicado a W16/W17 y al template del system prompt para futuras ediciones.
- **Home con lectura completa** — la tarjeta de cada edición en la home ahora muestra, además del excerpt de una línea, toda la sección "Lectura" (2-3 frases con enlaces y negritas). `build_index.py` extrae la sección del markdown y la vuelca con `markdown="1"` para que kramdown procese el contenido. Nueva clase `.edition-lectura` en `main.css`.
