# SEO — Plan de ataque ambicioso

**Fecha:** 2026-04-20
**Origen:** [CLAUDE.md](CLAUDE.md#reglas-fundacionales), [DISENO-WEB.md](DISENO-WEB.md).
**Objetivo estratégico:** que cuando alguien en Ibiza escriba en Google cualquier pregunta sobre vivienda, alquiler, desahucio, temporeros o alquiler turístico, aparezcamos en la primera página. Y que cuando aparezca, el snippet vale un click.

---

## Principios

1. **SEO es pilar fundamental, no añadido.** Cada decisión de producto se evalúa por su impacto en descubribilidad.
2. **Contenido denso > contenido optimizado**. Google premia hoy el E-E-A-T (experiencia, pericia, autoridad, confianza). El modelo documental es exactamente lo que Google quiere.
3. **Long-tail antes que keywords amplias**. "Vivienda Ibiza" es impagable (empresas inmobiliarias, portales). "Qué es sa Joveria Ibiza" es ganable.
4. **Velocidad sí importa**. Jekyll estático ya es rápido; no romper eso añadiendo JS innecesario.
5. **Verificabilidad genera backlinks**. Cada propuesta documentada con URL es material citable. Los citadores nos enlazan.
6. **Sin dominio propio hasta tracción** (PLAN.md). SEO se hace en `otundra.github.io/ibiza-housing-radar` con plena consciencia de que limita ranking. Cuando se active el dominio propio, migración 301 completa.

---

## Keywords research — arranque

### Cabeza (alta competencia, baja conversión para nosotros)

- "vivienda ibiza" — dominado por inmobiliarias
- "alquiler ibiza" — dominado por idealista/fotocasa
- "pisos ibiza" — dominado por portales

No pelear por estas. Ranquear cuando se pueda sin optimizar específicamente.

### Cuerpo (competencia media, conversión alta)

- "crisis vivienda ibiza"
- "vivienda trabajadores ibiza"
- "alquiler temporeros ibiza"
- "alquiler temporada ibiza"
- "precio habitación ibiza"
- "habitación alquiler ibiza"
- "desahucio ibiza"
- "alquiler turístico ibiza legal"
- "hut ibiza"
- "ibavi ibiza ayudas"
- "vivienda formentera"
- "consell eivissa vivienda"

Objetivo: posicionamiento top-10 en 6 meses para la mayoría.

### Long-tail (baja competencia, conversión altísima)

- "qué es sa joveria ibiza"
- "asentamiento trabajadores ibiza"
- "desalojo sa joveria"
- "can misses asentamiento"
- "caravana temporeros ibiza"
- "precio habitación ibiza temporada 2026"
- "cuánto cuesta una habitación en ibiza 2026"
- "dónde viven los camareros en ibiza"
- "cómo alquilar legal en ibiza"
- "llei 5/2018 habitatge baleares resumen"
- "alquiler turístico ilegal ibiza multa"
- "viviendas vacías ibiza"
- "vpo ibiza sa penya"
- "7 vpo sa penya requisitos"
- "residencias temporeros ibiza"
- "convenio hostelería ibiza alojamiento"
- "zermatt staff housing" (para tráfico de referencia internacional si se cubre)
- "whistler housing authority"

Objetivo: top-3 en 3 meses, rich snippet / featured snippet donde se pueda.

### Keywords trilingües (cuando se active)

- Catalán: "habitatge eivissa", "lloguer eivissa", "treballadors temporada eivissa", "sa joveria", "desnonament eivissa"
- Inglés: "ibiza housing crisis", "ibiza seasonal workers housing", "ibiza rent price 2026", "ibiza staff accommodation", "where do ibiza workers live"

El inglés es especialmente valioso: tráfico internacional con intención alta (temporeros planificando la temporada, periodistas internacionales).

### Proceso de keywords research continuo

- Cada edición genera su propio bloque de keywords objetivo en el frontmatter del markdown. Se usa en `<title>`, `<meta description>`, H1 y primeros párrafos.
- Revisión mensual: Google Search Console + Bing Webmaster Tools muestran qué búsquedas reales traen tráfico. Se ajustan long-tail pages según datos.
- Herramienta zero-cost: Google Trends + autocompletado de Google + "People Also Ask" (copiar a mano cada mes).

---

## Elementos técnicos — Fase 0

### Meta tags por página

Plantilla Jekyll en `_layouts/default.html` con lógica:

```html
<title>{{ page.title }}{% if page.title != site.title %} · {{ site.title }}{% endif %}</title>
<meta name="description" content="{{ page.excerpt | default: page.description | default: site.description | strip_html | truncate: 160 }}">
<link rel="canonical" href="{{ page.url | absolute_url }}">
```

Por tipo de página:

- **Home**: `<title>Ibiza Housing Radar · Observatorio semanal de vivienda en Ibiza</title>`
- **Edición**: `<title>{edition_title} · Vivienda y alquiler en Ibiza</title>` con keywords de la semana en meta description.
- **Actor**: `<title>{actor} y la vivienda en Ibiza</title>`
- **Propuesta**: `<title>{proposal_short_title} ({actor}) · Propuesta · IHR</title>`
- **Explica**: `<title>{topic}, qué es y por qué importa en Ibiza</title>` — formato pregunta frecuente.

### Schema.org JSON-LD

Cada edición lleva:

```json
{
  "@context": "https://schema.org",
  "@type": "NewsArticle",
  "headline": "{title}",
  "image": "{og_image_url}",
  "datePublished": "{date}",
  "dateModified": "{date_modified}",
  "author": {
    "@type": "Organization",
    "name": "Ibiza Housing Radar",
    "url": "{site_url}"
  },
  "publisher": {
    "@type": "Organization",
    "name": "Ibiza Housing Radar",
    "url": "{site_url}",
    "logo": {
      "@type": "ImageObject",
      "url": "{logo_url}"
    }
  },
  "description": "{excerpt}",
  "inLanguage": "es",
  "isAccessibleForFree": true,
  "license": "https://creativecommons.org/licenses/by/4.0/"
}
```

Cada página lleva `BreadcrumbList`:

```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {"@type": "ListItem", "position": 1, "name": "Inicio", "item": "{site_url}"},
    {"@type": "ListItem", "position": 2, "name": "{sección}", "item": "{sección_url}"},
    {"@type": "ListItem", "position": 3, "name": "{página}", "item": "{página_url}"}
  ]
}
```

Home lleva `Organization` + `WebSite`:

```json
{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": "Ibiza Housing Radar",
  "url": "{site_url}",
  "inLanguage": "es",
  "potentialAction": {
    "@type": "SearchAction",
    "target": "{site_url}/buscar/?q={search_term_string}",
    "query-input": "required name=search_term_string"
  }
}
```

Propuestas individuales llevan `CreativeWork` con metadata.

### Open Graph y Twitter Cards

En `<head>` de todas las páginas:

```html
<meta property="og:type" content="article"> <!-- o "website" en home -->
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{og_image_url}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="es_ES">
<meta property="og:site_name" content="Ibiza Housing Radar">

<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{description}">
<meta name="twitter:image" content="{og_image_url}">
```

### Open Graph images generadas

Cada edición y cada página "explica" necesita una imagen OG única. Dos rutas:

**Ruta A (recomendada): script Python con Pillow**

- Template SVG/PNG base con marca + zonas de título y fecha.
- Script en `src/og_images.py` recibe `(title, subtitle, date)` y genera `docs/assets/og/{slug}.png` de 1200×630.
- Se ejecuta como parte del pipeline tras `generate.py`.
- Fuente: Instrument Serif bold en título, Inter regular en subtítulo.

**Ruta B (fallback): imagen genérica por tipo de página**

- 1 imagen OG estática para home.
- 1 imagen OG estática para ediciones (con superposición "última edición").
- 1 imagen OG estática para páginas estáticas.

Fase 0 empieza con B y migra a A la segunda semana. B garantiza que el sharing nunca sale sin preview.

### Sitemap

Plugin `jekyll-sitemap` ya instalado. Verificar que incluye:

- Home
- Todas las ediciones
- Todas las páginas estáticas (política, metodología, balance, actores, propuestas, recursos, etc.)
- Todas las fichas de actor
- Todas las fichas de propuesta
- Todas las páginas `/explica/`

Añadir `<lastmod>` en frontmatter de cada página modificable.

### robots.txt

En `docs/robots.txt`:

```
User-agent: *
Allow: /
Disallow: /Gemfile
Disallow: /Gemfile.lock

Sitemap: https://otundra.github.io/ibiza-housing-radar/sitemap.xml
```

`private/` no existe en docs/, no hace falta `Disallow`.

### RSS

Plugin `jekyll-feed` ya instalado. Configurar:

```yaml
feed:
  path: feed.xml
  excerpt_only: false  # contenido completo
  collections:
    editions:
      path: feed.xml
```

Contenido completo (no solo excerpt) para agregadores.

### Canonical URLs

Plantilla ya definida. Verificar que no se duplican URLs con/sin trailing slash. Jekyll sirve con slash; configurar redirect si en algún momento hubiera acceso sin slash.

### Internal linking dirigido

Regla: cada edición enlaza a:

- Edición anterior y siguiente (ya definido en DISENO-WEB).
- Ficha de cada actor citado (`/actores/{slug}/`) — genera enlaces entrantes al directorio.
- Ficha de cada propuesta documentada (`/propuestas/{id}/`) — genera enlaces entrantes al tracker.
- `/explica/` correspondiente cuando se menciona un término técnico (IBAVI, sa Joveria, etc.).
- `/glosario/#termino` cuando es un término menos importante.

Esto se puede automatizar parcialmente en un paso de post-procesado markdown.

### URLs semánticas

Auditar:

- `/ediciones/2026-wNN/` ✅ ya existe.
- `/actores/consell-deivissa/` ← nuevo.
- `/propuestas/2026-w15-consell-ahr-01/` ← nuevo.
- `/explica/sa-joveria/` ← nuevo.

No query strings. Minúsculas y guiones.

### Google Search Console

- GitHub Pages admite verificación por meta tag o HTML file.
- Añadir meta tag `google-site-verification` a `<head>` tras generar el código en Search Console.
- Subir sitemap.xml a Search Console el mismo día del lanzamiento.
- Monitorear: impresiones, clicks, CTR, posición media, páginas indexadas, errores de rastreo.
- Revisión semanal el martes (día después de publicar edición).

### Bing Webmaster Tools

Análogo. Bing importa Search Console así que bajo esfuerzo. Verificación y sitemap iguales.

### Core Web Vitals

Auditoría con:

- PageSpeed Insights (Google, gratis).
- Lighthouse en Chrome DevTools.
- Web Vitals extension.

Objetivo en todas las páginas:

- LCP ≤ 2,5 s
- INP ≤ 200 ms
- CLS ≤ 0,1

Medidas ya comprometidas en DISENO-WEB.md.

### Alt text en imágenes

Regla: toda imagen (OG, logo, iconos, fotos) con alt descriptivo. Iconos decorativos con `alt=""` explícito.

### Keywords por edición incorporadas al prompt

En el frontmatter de cada edición:

```yaml
seo_keywords:
  - "desalojo sa joveria 2026"
  - "asentamiento can misses"
  - "desahucio ibiza temporada"
```

El generador Opus incluye estas keywords de manera natural en el título, H1 del panel, primeros 150 caracteres del excerpt y en la sección "señales" cuando aplique.

Fuentes de keywords automáticas:

1. Títulos de las señales originales (ya son keywords).
2. Nombres de los actores citados (ya son keywords institucionales).
3. Localizaciones mencionadas (microtopónimos como sa Joveria, Can Misses son keywords long-tail).

---

## Contenido estratégico long-tail

Cada página de `/explica/` es una inversión SEO a largo plazo. Se escribe una vez, se mantiene viva, captura tráfico evergreen.

### Estructura canónica de una página `/explica/{tema}/`

1. **H1** con la pregunta típica de búsqueda: "Sa Joveria: qué es y por qué importa".
2. **Resumen en 50 palabras** justo debajo del H1 (para featured snippet).
3. **H2 cronología** con bullets datados (Google ama listas con fechas).
4. **H2 propuestas en circulación** alimentada automáticamente del tracker.
5. **H2 cobertura en ediciones** con enlaces cruzados.
6. **H2 fuentes oficiales** con enlaces externos a actas, informes, noticias primarias.
7. **H2 glosario** breve de términos relacionados.
8. **Fecha de última actualización** visible.
9. **Metadatos schema.org `Article`** con `about`, `mentions`.

Objetivo por página: 600-1200 palabras de contenido denso + lista automática que crece con cada edición relevante.

### Páginas `/explica/` prioritarias Fase 0

- `/explica/sa-joveria/`
- `/explica/can-misses/` (asentamiento)
- `/explica/ibavi/`
- `/explica/consell-deivissa/`
- `/explica/llei-habitatge-baleares/`
- `/explica/alquiler-turistico-ibiza/` (legal vs ilegal, HUT, multas, jurisprudencia TSJIB)
- `/explica/vivienda-temporera/` (qué distingue alquiler de temporada, problemas típicos, actores)
- `/explica/vpo-ibiza/` (qué es, requisitos, convocatorias recientes)

### Ampliación Fase 1-2

- `/explica/residencias-trabajadores-ibiza/`
- `/explica/subarriendo-fraudulento/`
- `/explica/multa-alquiler-turistico-ilegal/`
- `/explica/desahucio-administrativo-vs-judicial/`
- `/explica/convenio-hosteleria-alojamiento/`

Criterio de priorización: búsquedas reales que aparezcan en Search Console a los 2 meses.

---

## Social previews

### Bluesky y Mastodon

Ambos respetan Open Graph. Las imágenes OG generadas (§ "Open Graph images") sirven directamente.

Además, el bot de Bluesky/Mastodon publica un **hilo estructurado** los lunes:

```
Post 1 (lanzamiento): 
"🏠 Nueva edición: Semana N de Mes Año
N señales · N propuestas documentadas · N omisiones
[URL]"

Post 2-N (un post por propuesta principal):
"Propuesta: {title}
Propuesta por: {actor}
Estado: {state}
Fuente: {url}
Detalle: {permalink edition}#propuesta-N"

Post final:
"🗺 Mapa de posiciones esta semana:
- {actor1}: {posición}
- {actor2}: {posición}
[URL]"
```

Cada post con al menos 1 hashtag relevante: `#Ibiza #Vivienda #Habitatge` (CA cuando active trilingüe).

### Newsletter

Buttondown respeta HTML básico. Incluir al principio:

- Título edición
- Imagen OG embebida
- Una línea resumen
- Botón "Leer edición completa" al permalink
- Opcional: los 3 highlights de la semana (1 señal, 1 propuesta, 1 omisión).

Al final de cada newsletter: link a `/cita-esto/` para reenviadores.

---

## Rich results y Google News

### Rich results disponibles

Google soporta estos tipos que podemos ganar:

1. **Article / NewsArticle** — estándar, ya cubierto por schema.org.
2. **Breadcrumbs** — ya cubierto.
3. **FAQ** — aplicable a páginas `/explica/` si incluimos preguntas frecuentes.
4. **HowTo** — no aplica a nuestro contenido editorial.
5. **Sitelinks search box** — con `WebSite.potentialAction` ya cubierto.

### Google News (diferido hasta dominio propio)

Google News exige dominio propio verificado y política editorial clara. Cuando se compre dominio, aplicar en el panel de Google News Publisher Center.

Mientras tanto, Google Search sí indexa contenido tipo noticia con `NewsArticle` aunque no aparezca en Google News.

---

## Métricas y seguimiento

### Stack zero-cost

- **Google Search Console**: búsquedas reales, páginas indexadas, CTR, posición.
- **Bing Webmaster Tools**: segundo motor relevante.
- **GoatCounter**: analítica de tráfico sin cookies ni banner (privacy-friendly).
- **Lighthouse CI** (opcional Fase 1): auditoría automática en cada PR.

### KPIs trimestrales

Trimestre 1 (post lanzamiento):

- 50+ páginas indexadas en Google.
- 500+ impresiones/mes en Search Console.
- Posición media <30.

Trimestre 2:

- 100+ páginas indexadas.
- 2.000+ impresiones/mes.
- Posición media <20.
- Al menos 3 keywords long-tail en top-10.

Trimestre 4:

- 500+ visitas únicas mensuales (GoatCounter).
- 5.000+ impresiones/mes.
- Posición media <15.
- 10+ keywords en top-10, al menos 3 en top-3.
- 5+ backlinks externos.

---

## Backlinks — estrategia pasiva

No se hace outreach agresivo. Los backlinks vienen de:

1. **Citas de medios**: cuando Diario de Ibiza, Periódico de Ibiza o ARA Balears citen el proyecto, pedir enlace (no referencia textual).
2. **Reproducción CC-BY**: facilitar con licencia y kit de prensa. Los reproductores enlazan por obligación de atribución.
3. **Colaboración con entidades**: Cáritas, sindicatos, colectivos mencionan el observatorio en sus webs cuando sea útil para su propio mensaje.
4. **Citación académica**: la página `/cita-esto/` facilita que una tesis o informe incluya el proyecto en referencias bibliográficas con URL.
5. **Directorios**: añadir el proyecto a directorios relevantes de vivienda / periodismo / observatorios.

---

## Red semántica del sitio — cómo Google lo ve

Con todo lo anterior, la web tiene estructura semántica así:

```
Ibiza Housing Radar (Organization)
│
├── publica (hasPart) → ediciones semanales (NewsArticle)
│                         │
│                         ├── menciona (mentions) → actores (Organization/Person)
│                         ├── documenta (about) → propuestas (CreativeWork)
│                         └── referencia (citation) → noticias externas (WebPage)
│
├── explica (hasPart) → páginas /explica (Article)
│                         │
│                         ├── about → conceptos / lugares (Thing)
│                         └── mentions → actores
│
└── mide (hasPart) → balance (Report) con reparto de citas
```

Esta estructura es **exactamente** lo que Google entiende como "observatorio confiable con fuentes estructuradas". Es lo que premia E-E-A-T.

---

## Checklist de lanzamiento SEO Fase 0

Antes de decir "Fase 0 cerrada":

- [ ] Meta tags únicos verificados en las 15+ páginas principales.
- [ ] Schema.org JSON-LD validado con [Schema.org Validator](https://validator.schema.org/) en 5 tipos de página.
- [ ] OG preview probado en [OpenGraph.xyz](https://www.opengraph.xyz/) para home, edición, actor y explica.
- [ ] Twitter Card validada en [Twitter Card Validator](https://cards-dev.twitter.com/validator).
- [ ] Sitemap accesible en `/sitemap.xml`, enviado a Search Console y Bing.
- [ ] robots.txt accesible en `/robots.txt`.
- [ ] RSS accesible en `/feed.xml` con contenido completo.
- [ ] Canonicals correctos (sin duplicados).
- [ ] Google Search Console verificado y recibiendo datos.
- [ ] Bing Webmaster Tools verificado.
- [ ] Lighthouse ≥ 90 en Performance, Accessibility, Best Practices, SEO en home y última edición.
- [ ] Core Web Vitals en verde en móvil y desktop.
- [ ] 8+ páginas `/explica/` publicadas.
- [ ] Internal linking auditado (ninguna página huérfana).
- [ ] GoatCounter instalado y recibiendo datos.
- [ ] 4 ediciones retroactivas publicadas (W14-W17).
- [ ] Balance inicial publicado.
