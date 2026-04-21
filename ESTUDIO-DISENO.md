# Estudio de diseño — Radar Ibiza

**Fecha:** 2026-04-20 · **Cerrado con OK del editor:** 2026-04-21
**Autor:** Claude Opus 4.7 + Raúl Serrano
**Origen:** [PIVOTE.md](PIVOTE.md), [DISENO-WEB.md](DISENO-WEB.md), [ROADMAP.md](ROADMAP.md).
**Alcance:** estudio previo al Bloque B del Roadmap. Consolida identidad de marca, sistema visual, componentes clave, benchmark comparado con 13 referentes, plan de prototipo y decisiones del editor. Al cerrarse este documento, el Bloque B puede ejecutarse sin decisiones de diseño pendientes (salvo D2 logo, diferido hasta revisión del prototipo SVG).

> Este estudio **no reemplaza** a [DISENO-WEB.md](DISENO-WEB.md) (arquitectura de información, mapa del sitio, contenido por página). Lo complementa añadiendo identidad, tokens de sistema, spec de componentes y criterio de prototipado.

> 🏷️ **Rebranding 2026-04-21.** Nombre público nuevo: **Radar Ibiza**. Dominio objetivo `radaribiza.com` (compra pendiente editor). Repo GitHub mantiene slug `ibiza-housing-radar` hasta compra del dominio. Tagline estable: *"Observatorio documental de vivienda"*.

> 🎯 **Dirección visual apuntada:** "mono + seams" — peso tipográfico mono (JetBrains Mono) en más elementos editoriales + separadores tipo costura (dashed, líneas finas). Queda por formalizar al construir el prototipo HTML estático (Paso 1, §10). Iconografía: Unicode puro, no emoji coloreado.

---

## 0. Por qué este documento existe

[DISENO-WEB.md](DISENO-WEB.md) define **qué páginas** existen y **qué contienen**. No define:

- Identidad de marca (logo, wordmark, firma visual reutilizable en OG y RRSS).
- Tokens concretos del sistema (hex exactos de la paleta extendida, escala tipográfica, espaciado).
- Spec de componentes nuevos (card de propuesta, barra de estado de palanca, chrome operacional).
- Orden de construcción del prototipo.
- Benchmark real con referentes comparables.

Sin este estudio, el Bloque B del Roadmap se ejecuta a ciegas. Con él, cada decisión de CSS tiene justificación y referencia.

---

## 1. Punto de partida — qué ya está decidido

Resumen del estado actual (no rehacer):

| Decisión | Referencia | Estado |
|---|---|---|
| Mantener identidad visual actual (terracota + crema editorial) | [DECISIONES-PENDIENTES.md #10](DECISIONES-PENDIENTES.md) | ✅ cerrada 2026-04-20 |
| Evolución incremental, **no rediseño desde cero** | [DECISIONES-PENDIENTES.md #10](DECISIONES-PENDIENTES.md) | ✅ cerrada |
| Inspiración importada: Solar Low-Tech | [DISENO-WEB.md §Solar](DISENO-WEB.md) | ✅ cerrada |
| Tipografías actuales: Instrument Serif + Inter + JetBrains Mono | [main.css](docs/assets/css/main.css) | ✅ implementado |
| Partidos siempre en gris neutro, nunca su color | [DISENO-WEB.md](DISENO-WEB.md) | ✅ regla dura |
| Dos públicos (primer visitante + profesional recurrente) | [DISENO-WEB.md §Públicos](DISENO-WEB.md) | ✅ principio base |
| Sin JS salvo imprescindible, sin frameworks, sin cookies | [DISENO-WEB.md §Rechazo JS](DISENO-WEB.md) | ✅ principio |
| Modo oscuro mantenido | [DECISIONES-PENDIENTES.md](DECISIONES-PENDIENTES.md) | ✅ ya implementado |

Lo que **este estudio decide por primera vez**:

1. Sistema de marca (wordmark + logotype + favicon coherente).
2. Paleta extendida con códigos hex por tipo de actor.
3. Escala tipográfica formal (tamaños, pesos, line-heights).
4. Sistema de espaciado por tokens.
5. Spec de 9 componentes nuevos (más abajo).
6. Plantilla OG image.
7. Plan de prototipo por orden de construcción.
8. Decisiones abiertas para el editor (al final del documento).

---

## 2. Benchmark comparado — 13 referentes

### 2.1 Tabla resumen

| # | Nombre | URL | Paleta (aprox) | Tipografía | Patrón #1 a importar | Qué NO importar |
|---|---|---|---|---|---|---|
| 1 | Solar Low-Tech | [solar.lowtechmagazine.com](https://solar.lowtechmagazine.com/) | #FFF / #111 / gris medio | System fonts | Chrome operacional en footer (tamaño KB, batería) | Dithering 1-bit por estética |
| 2 | Bellingcat | [bellingcat.com](https://bellingcat.com) | #FFF / #1B1F24 / rojo CTA | Sans bold + system | Tags tipográficos `[País]` bajo cada card | Grid pesado con foto |
| 3 | The Pudding | [pudding.cool](https://pudding.cool) | Neutro + color por pieza | Sans + serif accent | Numeración de edición como identidad (#216) | Layout bespoke por artículo |
| 4 | Civio | [civio.es](https://civio.es) | Blanco / negro / rojo crimson | Sans serif único | URLs semánticas jerárquicas + separación periodismo/herramientas | Carruseles |
| 5 | Datadista | [datadista.com](https://datadista.com) | Blanco / negro / gris | Sans moderno | Hubs temáticos permanentes | Heros de imagen |
| 6 | Tortoise | [tortoisemedia.com](https://www.tortoisemedia.com) | Verde bosque #2D4F00 / crema | Sans geo + serif | Un único color primario como firma | Paywall / branding "slow" |
| 7 | El Orden Mundial | [elordenmundial.com](https://elordenmundial.com) | Blanco / negro / azul medio | Sans editorial | Colección paralela "EOM explica" | Carrusel de autores |
| 8 | The Intercept | [theintercept.com](https://theintercept.com) | #FFF / #000 / rojo oscuro | Sans bold potente | Etiqueta de serie coloreada encima del titular | Hero overlay foto |
| 9 | ProPublica | [propublica.org](https://propublica.org) | Blanco / negro / rojo donate | Sans system | Páginas `/corrections/`, `/code-of-ethics/` de primer nivel | CTA donación omnipresente |
| 10 | Rest of World | [restofworld.org](https://restofworld.org) | Navy / cyan / amarillo / rosa | Inter / Helvetica | Toggle modo oscuro accesible desde menú | Paleta amplia sin director de arte |
| 11 | GovTrack | govtrack.us (403) | — | — | Barra de progreso por estado legislativo | — |
| 12 | TheyWorkForYou | [theyworkforyou.com](https://theyworkforyou.com) | Blanco / azul / verde | Sans system | Sidebar persistente en ficha de actor | Emojis en navegación |
| 13 | OpenSecrets | opensecrets.org (403) | — | — | Doble horizonte temporal en ficha (actual / histórico) | Densidad que confunde |

### 2.2 Patrones repetidos (aparecen en 4+ referentes → estándar editorial)

Asumidos sin más debate:

1. **Fondo claro + tinta casi negra** (Bellingcat, Civio, Datadista, Intercept, ProPublica, EOM, Tortoise). Nuestra crema ya cumple.
2. **Un único color de acento usado con disciplina** (rojo en Intercept, verde en Tortoise, rojo CTA en Bellingcat/Civio/ProPublica). Nuestra terracota es equivalente. **No añadir un azul o verde "funcional".**
3. **Navegación doble: tema + tiempo** (Civio, Datadista, EOM, Rest of World). Hub temático vertical + archivo cronológico en paralelo.
4. **Tags visibles bajo el titular** (Bellingcat, Civio, Intercept, Rest of World). Pequeños, monospace o tracked, clickables.
5. **Archivo como colección enumerable** (Pudding #216, TheyWorkForYou por fecha, GovTrack por ciclo). El número es identidad.
6. **Páginas de transparencia/método como URL de primer nivel** (ProPublica, Civio, Bellingcat). `/metodologia/`, `/correcciones/` al mismo nivel que `/ediciones/`.

### 2.3 Tres patrones diferenciadores (oro para nosotros)

Los que **solo 1-2 referentes** hacen y tienen alto encaje con nuestro pivote documental:

1. **Chrome operacional honesto de Solar Low-Tech.** Footer con métricas reales: tamaño del HTML, coste API del mes, build time, fecha de última ejecución. Nadie en nuestra categoría lo hace. Refuerza la tesis documental. Coste: 0 €. → Ver [§6.1](#61-chrome-operacional-footer).
2. **Doble horizonte temporal de OpenSecrets** aplicado a fichas de actor. Toggle "Temporada actual" vs "Histórico". Resuelve dos públicos con un componente. → Ver [§6.9](#69-toggle-histórico).
3. **Barra de estado tipo GovTrack para palancas.** `propuesta → registrada → aprobada → implementada → incumplida`. Nadie en el espacio español periodístico la visualiza así. Elemento más memorable que podemos construir. → Ver [§6.5](#65-pill-de-estado-y-barra-de-progreso).

---

## 3. Principios rectores de diseño

Destilados del benchmark + 5 reglas duras del pivote. Si un componente nuevo no cumple estos principios, se rechaza.

1. **Credibilidad por restricción.** Menos color, menos animación, menos decoración. Densidad tipográfica > imagen.
2. **Un único color de acento** (terracota). Las variaciones por tipo de actor son tonos neutros matizados, no nuevos primarios.
3. **La fuente es la prueba.** Toda afirmación lleva URL visible o enlace a ficha interna. El diseño jerarquiza la fuente tanto como la afirmación.
4. **El primer visitante lee en 30-90 s; el profesional vuelve el lunes.** Cada página sirve a ambos sin sacrificar a ninguno.
5. **Datos en monospace, narrativa en serif, UI en sans.** No mezclar roles tipográficos.
6. **Operación al descubierto.** Costes, estado del pipeline, correcciones, método: siempre a un click. Chrome operacional en footer.
7. **Sin JS salvo imprescindible.** `<details>` nativo para acordeones, `:has()` y radios ocultos para toggles, `position: sticky` para sidebars, `prefers-color-scheme` para modo oscuro.
8. **Trazabilidad editorial.** Numeración de edición (W17) visible en todas partes. Cada propuesta con ID permanente. Cada cambio de estado con fecha.
9. **Accesibilidad no negociable.** AA mínimo, AAA donde se pueda. Navegable por teclado al 100 %. Legible sin JS.
10. **Estable antes que espectacular.** Ningún componente se añade si no es replicable semana tras semana durante 12 meses sin mantenimiento especial.

---

## 4. Identidad de marca

### 4.1 Nombre y wordmark

**Nombre del proyecto:** "Ibiza Housing Radar" (se mantiene hasta decidir dominio propio, ver [ESTUDIOS-PENDIENTES.md](ESTUDIOS-PENDIENTES.md)).

**Wordmark recomendado:** dos líneas, tipografía Instrument Serif, peso regular.

```
Ibiza
Housing Radar
```

- Línea 1 "Ibiza" en Instrument Serif italic, color terracota (`--accent`).
- Línea 2 "Housing Radar" en Instrument Serif regular, color tinta (`--ink`).
- Tracking ligeramente negativo (-0.02em).
- Tamaños:
  - Header (desktop): 22 px / 18 px por línea.
  - Header (móvil): 16 px / 14 px.
  - OG image: 72 px / 56 px.
  - Favicon: no usar wordmark, ver §4.3.

**Alternativa corta** para espacios reducidos (breadcrumbs, OG secundarios, RSS):

```
IHR · W17
```

JetBrains Mono, 13 px, letter-spacing 0.04em, color `--ink-muted`.

### 4.2 Logo / marca gráfica

**Propuesta principal:** punto pulsante + arco de radar.

Concepto: un punto terracota centrado y tres arcos concéntricos como un radar barriendo. Referencia visual al nombre (Radar) y al pulso de información semanal. Ya existe un elemento similar en la home actual (`.dash-pulse` con animación `dash-pulse`), que se puede formalizar como marca.

Especificación SVG (1:1, viewBox 24×24):

```svg
<svg viewBox="0 0 24 24" width="24" height="24" role="img" aria-label="Ibiza Housing Radar">
  <circle cx="12" cy="12" r="2" fill="#c14a2d"/>
  <circle cx="12" cy="12" r="6" fill="none" stroke="#c14a2d" stroke-width="1" opacity="0.45"/>
  <circle cx="12" cy="12" r="10" fill="none" stroke="#c14a2d" stroke-width="1" opacity="0.22"/>
</svg>
```

Sin animación en logo estático. La animación `dash-pulse` se reserva al indicador "en directo" de la home (ya implementada).

**Tamaños oficiales:**

- 16 px — favicon, meta icons.
- 22 px — header actual.
- 48 px — OG secundario.
- 120 px — OG principal (header de la imagen).
- 512 px — PNG descargable en `/cita-esto/`.

**Variantes:**

- **Monocromo tinta** (para fondo claro sin color).
- **Monocromo crema** (para fondo oscuro o terracota pleno, para RRSS).
- **Color completo** (default).

Todas generadas desde el mismo SVG cambiando el `fill` y `stroke`.

### 4.3 Favicon

Actual: `docs/assets/favicon.svg`. Revisar y alinear al logo anterior. Si no encaja, regenerar con el SVG de §4.2.

**Iconos requeridos** (todos derivables del SVG):

- `favicon.svg` (SVG único, Safari usa el path `mask-icon`).
- `favicon-32.png` (32×32).
- `favicon-192.png` (192×192, Android).
- `apple-touch-icon.png` (180×180).
- `og-fallback.png` (1200×630, para casos sin OG específico).

### 4.4 Iconografía

Mantener emojis seccionales actuales: 📡 señales · 🗓 cronología · 🗺 mapa · 📋 propuestas · 🗄 rescate · 🕳 omisiones · 👀 a vigilar. Son reconocibles, cero peso, accesibles.

**No añadir** iconografía SVG custom por sección salvo que un icono concreto falle en cross-platform (por ejemplo, 🕳 "omisiones" podría no renderizar bien en Windows antiguos; si falla, sustituir por ⚬).

**Símbolos de estado** (ya en CLAUDE.md): 🟢 🟡 🟠 🔴 🚨. Uso exclusivo para capas de coste y estado operativo. Nunca decorativo.

---

## 5. Sistema visual

### 5.1 Paleta extendida

**Primarios (ya en `main.css`):**

| Token | Hex (light) | Hex (dark) | Uso |
|---|---|---|---|
| `--bg` | `#f8f4ec` | `#1a1411` | Fondo base |
| `--bg-soft` | `#f2ecdf` | `#221a16` | Fondo secundario (sectiones) |
| `--ink` | `#1e1916` | `#f2ece0` | Texto principal, titulares |
| `--ink-soft` | `#4a3f36` | `#d1c6b5` | Texto cuerpo secundario |
| `--ink-muted` | `#7a6e62` | `#9b8f80` | Metadatos, timestamps |
| `--rule` | `#e2d8c5` | `#362c25` | Líneas divisorias suaves |
| `--rule-strong` | `#bdaf97` | `#4e4138` | Líneas divisorias fuertes |
| `--accent` | `#c14a2d` | `#ef7a5a` | Terracota, acento único |
| `--accent-soft` | `#e86c4a` | `#f8a487` | Terracota hover/sobresaliente |
| `--accent-bg` | `#fbe9de` | `#3a221a` | Fondo de callout con acento |
| `--card` | `#ffffff` | `#241c18` | Superficie de cards |

**Auxiliares semánticos (existentes, usar con moderación):**

| Token | Hex (light) | Hex (dark) | Uso exclusivo |
|---|---|---|---|
| `--success` | `#3f7a4a` | `#6aad7b` | Estado "implementada" en palancas |
| `--warning` | `#a86a00` | `#d49530` | Capa 🟠 naranja en chrome operacional |

**Extensión nueva — tipos de actor** (tonos neutros matizados, no colores nuevos competidores):

| Token | Hex (light) | Hex (dark) | Uso |
|---|---|---|---|
| `--actor-publico` | `#4a5d6e` | `#8fa3b8` | Institucional público (Consell, ayuntamiento, Govern) |
| `--actor-partido` | `#6a645c` | `#aaa299` | Partido (gris neutro, regla dura) |
| `--actor-patronal` | `#8a6b3a` | `#c6a26a` | Asociaciones empresariales (CAEB, PIMEEF, Fecoei) |
| `--actor-sindicato` | `#4a6b48` | `#8cb08a` | CCOO, UGT |
| `--actor-tercer-sector` | `#c14a2d` | `#ef7a5a` | Cáritas, Cruz Roja, GEN-GOB (reutiliza terracota) |
| `--actor-academico` | `#6e4a6b` | `#ad86ab` | UIB, IBESTAT |
| `--actor-judicial` | `#3a352f` | `#8a8179` | TSJIB, juzgados |
| `--actor-colectivo` | `#a88a2e` | `#d4b66a` | PAH Pitiüses, Ens Plantem |

**Verificación de contraste** (AA mínimo, AAA preferido):

- Todos los pares `--ink` / `--bg` verificados ≥ 7:1 (AAA).
- Pares `--ink-soft` / `--bg` ≥ 4.5:1 (AA).
- `--accent` sobre `--bg` ≥ 4.5:1 (AA).
- `--actor-*` sobre `--card` ≥ 4.5:1 → pendiente de verificación en implementación. Si alguno falla, oscurecer 10-15 %.

### 5.2 Tipografía

**Tres familias, roles estancos:**

| Familia | Rol | Pesos cargados | Fallback |
|---|---|---|---|
| Instrument Serif | Titulares, leads en italic, números destacados | 400 (regular), 400i (italic) | Source Serif Pro, Georgia, serif |
| Inter | Cuerpo, UI, navegación | 400, 500, 600 | -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif |
| JetBrains Mono | Datos, URLs, kickers, chrome operacional, IDs | 400, 500 | ui-monospace, SFMono-Regular, Menlo, monospace |

**Carga:**

- `font-display: swap` (ya en uso).
- `preload` solo de Instrument Serif 400 (la más pesada en perceived loading).
- Inter se sirve via Google Fonts (considerar self-host si LCP sufre).
- Subset latin + latin-ext (no necesitamos cirílico, griego, etc.).

**No añadir una cuarta familia.** Si hay tentación de añadir tipografía "decorativa" para kickers o botones, rechazar: la familia existente cumple con variación de peso + letter-spacing.

### 5.3 Escala tipográfica

Base: 17 px (desktop) / 16 px (móvil). Ratio modular 1.2 (minor third) para una escala suave que no grita.

| Token | Desktop | Móvil | Familia | Peso | Uso |
|---|---|---|---|---|---|
| `--fs-display` | clamp(2.4rem, 5vw, 3.8rem) | 2rem | Serif | 400 | Home H1, título de edición |
| `--fs-h1` | clamp(2rem, 4vw, 2.8rem) | 1.8rem | Serif | 400 | Título de página |
| `--fs-h2` | 1.9rem | 1.6rem | Serif | 400 | Secciones en ediciones |
| `--fs-h3` | 1.15rem | 1.05rem | Sans | 600 | Sub-secciones, títulos de card |
| `--fs-h4` | 1rem | 0.95rem | Sans | 600 | Detalles, campos de ficha |
| `--fs-body` | 17px | 16px | Sans | 400 | Cuerpo |
| `--fs-body-lg` | 19px | 17px | Sans | 400 | Hero lead, lede de edición |
| `--fs-small` | 15px | 14px | Sans | 400 | Meta secundaria, captions |
| `--fs-xs` | 13px | 12px | Sans o Mono | 500 | Kickers, tags, breadcrumbs |
| `--fs-mono-sm` | 12.5px | 12px | Mono | 500 | IDs, URLs, timestamps técnicos |

**Line-heights:**

- `--lh-tight` 1.1 — titulares display y H1.
- `--lh-snug` 1.2 — H2, H3.
- `--lh-normal` 1.55 — UI, metadatos.
- `--lh-relaxed` 1.7 — cuerpo de edición (lectura larga).

**Reglas duras:**

- Titulares serif: `letter-spacing: -0.01em` a `-0.015em`, `text-wrap: balance`.
- Kickers y small-caps: `letter-spacing: 0.04em` a `0.12em`, `text-transform: uppercase`, mono o sans.
- Cuerpo: nunca `text-align: justify` (rompe legibilidad en columnas estrechas).
- Medida óptima: 60-75 caracteres por línea (`max-width: 60ch` o 760 px).

### 5.4 Espaciado y grid

**Escala de espaciado** (base 4 px, ratio 1.5 donde aplica):

| Token | Valor | Uso típico |
|---|---|---|
| `--sp-1` | 4px | Espacio mínimo entre elementos inline |
| `--sp-2` | 8px | Gap pequeño, padding de pill |
| `--sp-3` | 12px | Gap medio, padding de input |
| `--sp-4` | 16px | Gap estándar, padding de card compacto |
| `--sp-5` | 24px | Padding de card, margen entre párrafos cortos |
| `--sp-6` | 32px | Margen entre bloques de contenido |
| `--sp-7` | 48px | Margen entre secciones mayores |
| `--sp-8` | 64px | Margen entre zonas de página |
| `--sp-9` | 96px | Separación heroico (hero → primer bloque) |

**Anchuras máximas** (ya en uso):

- `--max` 760 px — texto de lectura.
- `--max-wide` 1040 px — páginas con dos columnas moderadas.
- `--max-dash` 1180 px — dashboard de home, archivo.

**Breakpoints** (ya establecidos, mantener):

- 320 px (iPhone SE mínimo).
- 640 px (móvil grande / phablet).
- 768 px (tablet portrait).
- 1024 px (tablet landscape / laptop pequeño).
- 1280 px (laptop estándar).
- 1920 px (desktop grande).

**Regla de columnas:** cards de propuesta 1 col (<640), 2 (640-1024), 3 (1024-1280), 4 (>1280). Ya implementado en `main.css`.

### 5.5 Modo oscuro

Ya implementado via `@media (prefers-color-scheme: dark)` en `main.css:1137`.

**Pendiente:** toggle manual (rechazado hasta aquí por no querer JS). Solución sin JS: radio oculto + `:checked + body` selector. Coste: +30 líneas de CSS. Recomendación: diferir a Fase 1, `prefers-color-scheme` cubre el 90 % de casos.

**Regla:** el modo oscuro no es una negación del claro. Es una paleta hermana, con personalidad propia. Los hex ya definidos (§5.1) respetan esto: ink crema cálida, no gris lavado; fondo marrón oscuro, no negro puro.

---

## 6. Componentes clave

Nueve componentes nuevos o formalizados. Cada uno tiene: qué resuelve, referencia, especificación, uso.

### 6.1 Chrome operacional (footer)

**Qué resuelve:** transparencia operativa radical. Importa Solar Low-Tech + ProPublica.

**Spec:**

```html
<aside class="chrome-ops" aria-label="Estado operativo del observatorio">
  <ul>
    <li><span class="ops-label">Edición</span> <span class="ops-val">W17 · 2026-04-27</span></li>
    <li><span class="ops-label">Propuestas documentadas</span> <span class="ops-val">23</span></li>
    <li><span class="ops-label">Actores seguidos</span> <span class="ops-val">18</span></li>
    <li><span class="ops-label">Coste API mes</span> <span class="ops-val status-amber">5,84 € / 12 €</span></li>
    <li><span class="ops-label">Última publicación</span> <span class="ops-val">hace 3 días</span></li>
    <li><span class="ops-label">Pipeline</span> <span class="ops-val status-ok">✅ OK</span></li>
  </ul>
</aside>
```

**Estilos:**

- Toda la caja en `font-family: var(--mono)`.
- `font-size: 12.5px`, `line-height: 1.6`, `color: var(--ink-muted)`.
- Grid de 3 columnas en desktop, 2 en tablet, 1 en móvil.
- Labels en `color: var(--ink-muted)`, valores en `color: var(--ink-soft)`.
- Capas de coste con color: `--success` (🟢), `--warning` (🟡/🟠), `--accent` (🔴), tinta (🚨).

**Origen de datos:**

- Jekyll build script lee `data/costs.csv`, `docs/_editions/*.md`, `data/balance.json`.
- Se regenera en cada build. No requiere JS cliente.
- Si falta un dato, mostrar "—" (no romper el layout).

**Colocación:** pie de cada página, encima del footer estándar. No en home hero (compite con el dashboard editorial).

### 6.2 Numeración de edición

**Qué resuelve:** identidad serial visible. Importa Pudding + GovTrack.

**Spec:**

```html
<span class="edition-id">W17 · 2026-04-20</span>
```

**Estilos:**

- `font-family: var(--mono)`, 12.5 px, letter-spacing 0.04em.
- Color `--ink-muted`.
- Usado en:
  - Esquina superior izquierda de cada edición (sobre el titular).
  - Tag en cards del archivo.
  - Identidad en OG images.
  - Breadcrumb.

**Formato:** `W{semana ISO} · {fecha ISO publicación}`. Ejemplo: `W17 · 2026-04-20`.

**Retroactivas (W10-W17):** mismo formato, sin marca especial en el ID. La nota metodológica de edición retroactiva se maneja en el lede, no en el ID.

### 6.3 Tags tipográficos

**Qué resuelve:** navegación temática sin añadir cajas o botones pesados. Importa Bellingcat.

**Spec:**

```html
<ul class="tags">
  <li><a href="/temas/mercado/">[mercado]</a></li>
  <li><a href="/actores/govern-balear/">[actor: govern-balear]</a></li>
  <li><a href="/palancas/limite-hut/">[palanca: limite-hut]</a></li>
</ul>
```

**Estilos:**

- `font-family: var(--mono)`, 12 px.
- Color `--ink-muted`; link hover `--accent`.
- Corchetes literales en el contenido. Sin background, sin border.
- Inline-block con margen derecho 10px.

**Ubicación:** bajo el titular de ediciones y propuestas. No en home hero.

### 6.4 Card de propuesta

**Ya existe en `.dash-propuesta`** de `main.css:781`. Formalizar como componente reutilizable en todas las páginas (home, `/propuestas/`, `/actores/{slug}/`, `/palancas/{slug}/`).

**Spec (ya implementada):**

- Título corto (serif o sans, 1.15rem bold).
- Resumen (sans, 15 px, ink-soft).
- Meta grid: actor · estado · horizonte · viabilidad.
- Link a fuente externa (mono, muted).
- Link a ficha interna (terracota, underline).

**Pendiente de añadir:**

- **Pill de estado** (componente 6.5) visible arriba a la derecha.
- **Chip de tipo de actor** (componente 6.6) antes del nombre del actor.
- **Badge "rescate"** cuando la propuesta viene del módulo rescue. `font-family: var(--mono); text-transform: uppercase; background: var(--accent-bg); color: var(--accent); padding: 2px 6px; border-radius: 3px; font-size: 10.5px; letter-spacing: 0.06em`.

### 6.5 Pill de estado y barra de progreso

**Qué resuelve:** visualiza el ciclo de vida de una palanca/propuesta. Importa GovTrack.

**Estados definidos** (cerrados en [PIVOTE.md](PIVOTE.md) + ampliados):

1. `propuesta` — actor la ha verbalizado públicamente.
2. `registrada` — tiene expediente formal (registro de entrada, BOIB, pleno).
3. `en-debate` — en trámite, comisión, mesa, consulta.
4. `aprobada` — decisión formal tomada.
5. `en-ejecucion` — recursos asignados, implementación en curso.
6. `implementada` — resultado observable y verificable.
7. `descartada` — formalmente rechazada o retirada.
8. `incumplida` — aprobada pero no ejecutada en plazo.

**Pills:**

| Estado | Background | Color | Borde |
|---|---|---|---|
| propuesta | transparent | `--ink-muted` | 1px solid `--rule-strong` |
| registrada | `--bg-soft` | `--ink-soft` | 1px solid `--rule-strong` |
| en-debate | `--accent-bg` | `--accent` | 1px solid `--accent` |
| aprobada | `--accent` | #fff8f0 | transparent |
| en-ejecucion | `--accent-soft` | `--ink` | transparent |
| implementada | `--success` | #fff | transparent |
| descartada | `--rule-strong` | `--ink-soft` | transparent, text-decoration: line-through |
| incumplida | #b83c3c | #fff | transparent |

**Barra de progreso** (ficha de palanca `/palancas/{slug}/`):

```html
<ol class="progress-bar" aria-label="Estado del trámite">
  <li class="done">Propuesta <time>2026-03-02</time></li>
  <li class="done">Registrada <time>2026-03-18</time></li>
  <li class="current">En debate <time>desde 2026-04-07</time></li>
  <li>Aprobada</li>
  <li>En ejecución</li>
  <li>Implementada</li>
</ol>
```

Estilos: lista horizontal, cada paso con circulo + línea; `.done` relleno terracota, `.current` pulsante (reutiliza `@keyframes dash-pulse`), pendientes en `--rule`. En móvil, vertical con línea izquierda.

### 6.6 Chip de actor

**Qué resuelve:** identificar tipo de actor sin competir con el color primario. Importa TheyWorkForYou.

**Spec:**

```html
<span class="actor-chip actor-chip--publico">
  <span class="actor-chip-dot"></span>
  Consell d'Eivissa
</span>
```

**Estilos:**

- Inline-flex, gap 6px, padding 4px 10px.
- `border-radius: 999px`.
- Font Inter 500, 13 px.
- Background `--card`, border 1px solid del token `--actor-{tipo}` aclarado 80 %.
- El dot (6px round) en color `--actor-{tipo}`.
- Color del texto: `--ink`.

**Regla dura:** para `actor-chip--partido`, el dot es `--actor-partido` (gris neutro), NUNCA el color del partido. Mismo para PP, PSOE, Vox, Sumar, Podem, MÉS, Proposta per les Illes. Sin excepción.

### 6.7 Ficha de actor con sidebar sticky

**Qué resuelve:** navegación densa dentro de un actor sin páginas separadas. Importa TheyWorkForYou.

**Layout desktop (≥1024 px):**

```
┌──────────┬────────────────────────────┐
│ Sidebar  │  Contenido principal       │
│ sticky   │                            │
│          │  Cronología de citas       │
│ • Resumen│  Propuestas apoyadas       │
│ • Propue.│  Propuestas rechazadas     │
│ • Declar.│  Datos descargables        │
│ • Votos  │                            │
│ • Ficha  │                            │
│ • Descar.│                            │
└──────────┴────────────────────────────┘
```

**Spec:**

- `grid-template-columns: 220px 1fr`, gap 48px.
- Sidebar: `position: sticky; top: 82px` (headroom del sticky header global).
- Lista vertical, 14 px, sin bullets, cada item con padding-y 8px.
- Item activo: terracota, borde izquierdo 2px terracota, padding-left 10px.

**Móvil (<768 px):** sidebar colapsa a `<details>` desplegable en la cabecera de la ficha.

### 6.8 Margin notes

**Qué resuelve:** aclaraciones técnicas sin romper el flujo del cuerpo. Importa Solar Low-Tech + Edward Tufte.

**Spec:**

```html
<p>
  La Llei 5/2018 introduce la figura del "gran tenedor"<sup>1</sup>.
</p>
<aside class="margin-note" role="note">
  <span class="margin-note-num">1</span>
  Propietario de ≥10 viviendas. Definición en <a href="/glosario/gran-tenedor/">glosario</a>.
</aside>
```

**Estilos desktop (≥1024 px):**

- `position: absolute; right: -280px; width: 240px`.
- Top: alineado con el `<sup>` de referencia via `top: {calc}`.
- Font 13 px, `--ink-muted`, `line-height: 1.45`.
- Border-left 2px `--rule-strong`, padding-left 12px.

**Móvil:**

- `<aside>` se convierte en `<details>`, plegado por defecto, con `<summary>` "Nota: {primer fragmento}".
- Se muestra inline tras el párrafo que la referencia.

**Uso:** solo en ediciones largas, `/explica/`, y `/metodologia/`. No en home ni dashboard.

### 6.9 Toggle histórico (dos horizontes)

**Qué resuelve:** primer visitante ve temporada actual; profesional ve histórico completo. Un solo componente. Importa OpenSecrets.

**Spec HTML (sin JS):**

```html
<div class="horizon-toggle">
  <input type="radio" id="h-temporada" name="horizon" checked>
  <label for="h-temporada">Temporada 2026 (mayo-octubre)</label>

  <input type="radio" id="h-historico" name="horizon">
  <label for="h-historico">Histórico completo (desde W10)</label>

  <div class="horizon-panel horizon-panel--temporada">
    {contenido filtrado a temporada}
  </div>
  <div class="horizon-panel horizon-panel--historico">
    {contenido completo}
  </div>
</div>
```

**Estilos:**

- Radios `display: none`.
- Labels como pills (padding 8px 16px, border-radius 999px, border 1px `--rule-strong`).
- Label del radio `:checked` → background `--accent`, color crema.
- Paneles con `display: none`; el par `input:checked ~ .horizon-panel--temporada` / `:has()` → `display: block`.

Si `:has()` no está disponible en navegador target (Safari 15-), fallback: mostrar ambos paneles apilados con títulos. Progresivo.

**Uso:** fichas de actor (`/actores/{slug}/`), fichas de palanca, `/balance/`.

---

## 7. OG image template

**Por qué importa:** cada edición compartida en prensa, RRSS o Slack se ve como tarjeta OG antes de abrirla. Es la firma visual en entornos que no controlamos.

**Spec de la plantilla:**

- Dimensiones: 1200 × 630 px (estándar OG).
- Fondo: crema `--bg` (#f8f4ec).
- Esquina superior izquierda: logo 48px + wordmark corto "Ibiza Housing Radar" serif.
- Bajo el logo: `W17 · 2026-04-27` en mono, terracota.
- Centro: titular de la edición en Instrument Serif 72 px, 2-3 líneas máximo, `text-wrap: balance`.
- Bajo el titular: subtítulo de 1 línea en Inter 28 px, `--ink-soft`.
- Pie de la imagen: línea mono `23 propuestas · 18 actores · 6 palancas · 3 omisiones` en 22 px, `--ink-muted`.
- Esquina inferior derecha: arco radar del logo grande (opacity 0.25) como filigrana.

**Generación:** script Python con Pillow o con HTML → Puppeteer → PNG. **Recomendación: HTML + Puppeteer** porque permite actualizar el template editando CSS (no binario). Integrado en GitHub Action tras `report.py`.

**Variantes:**

- OG principal por edición (auto-generado).
- OG de página estática (home, `/metodologia/`, `/balance/`) — generado una vez, versionado en repo.
- OG de ficha de actor — auto-generado con nombre del actor + número de propuestas.
- OG de ficha de palanca — auto-generado con nombre de la palanca + barra de progreso simplificada.

**Fallback:** `og-fallback.png` (1200×630) con logo centrado + wordmark + tagline. Sirve cuando falla la generación automática.

---

## 8. Accesibilidad

Objetivo: **AA garantizado, AAA donde sea posible.**

**Checks automáticos** (a correr en CI tras Fase 0):

- Pa11y sobre `/`, `/ediciones/2026-w17/`, `/actores/govern-balear/`, `/propuestas/`.
- Lighthouse accessibility ≥ 95.
- Contraste automatizado via `axe-core`.

**Checks manuales** (una vez, documentados):

- Navegación completa por teclado en todas las páginas modelo.
- Screen reader pass con VoiceOver (macOS) y NVDA (Windows si posible).
- Zoom 200 % sin scroll horizontal ni contenido cortado.
- `prefers-reduced-motion`: desactivar `dash-pulse` y transiciones hover no críticas.

**Reglas duras:**

- Todo SVG decorativo con `aria-hidden="true"`.
- Todo SVG informativo con `role="img"` + `<title>` + `aria-label`.
- Skip link "Saltar al contenido" como primer foco en el DOM.
- `<main>` único por página, correctamente anidado.
- Formularios con `<label>` explícitos (no solo `placeholder`).
- Tablas con `<caption>` y `<th scope>` obligatorios.
- Links descriptivos, nunca "click aquí" o "aquí".
- Focus visible: 2px solid terracota + offset 3px + border-radius 3px (ya en `main.css:1130`).

---

## 9. Performance

**Targets Core Web Vitals** (ya en [DISENO-WEB.md](DISENO-WEB.md)):

- LCP ≤ 2.5 s en 3G lento.
- INP ≤ 200 ms.
- CLS ≤ 0.1.

**Medidas:**

- CSS crítico inline en `<head>` para el fold inicial (evitar FOUC).
- Fuentes con `font-display: swap` + `preload` de Instrument Serif.
- Imágenes en WebP con fallback JPEG, `loading="lazy"` salvo primera imagen visible.
- Sin JS salvo imprescindible (ya principio §3.7).
- Sin librerías externas.
- Lazy-load de OG images en cards (solo se necesitan en hover / al entrar en viewport).

**Budget de peso:**

- HTML por página: ≤ 50 KB.
- CSS total: ≤ 40 KB (actual: ~25 KB). Margen para los 9 componentes nuevos.
- Fuentes: ≤ 120 KB total (3 familias, subset latin).
- Imágenes por edición: ≤ 200 KB (1 OG + opcional 1 inline).
- **Total página típica: ≤ 400 KB.**

Si alguna página supera el budget, investigar antes de publicar.

---

## 10. Plan de prototipo — orden de construcción

Construir en este orden, cada paso valida antes de continuar. **No saltarse pasos.**

### Paso 1 — Prototipo HTML estático (semana 1)

**Objetivo:** validar que las decisiones del estudio funcionan en pantalla real antes de tocar Jekyll.

**Entregables:**

- `prototype/home.html` — home dual con dashboard editorial poblado con datos de W17 reales.
- `prototype/edition.html` — página de edición con 7 secciones, tags, margin notes.
- `prototype/actor.html` — ficha de actor con sidebar sticky.
- `prototype/proposal.html` — ficha de propuesta con pill de estado y barra de progreso.
- `prototype/styles.css` — CSS consolidado con todos los tokens.

**Datos:** usar W17 real (tras generar la edición con el pipeline nuevo). Si no está lista, datos ficticios pero realistas.

**Validación:**

- Abrir los 4 archivos en móvil real (iPhone + Android).
- Navegación por teclado de principio a fin.
- Modo oscuro via `prefers-color-scheme`.
- Lighthouse en los 4 → accessibility ≥ 95, performance ≥ 95.
- Tu juicio editorial: ¿esto soporta 12 meses de publicación sin cansar?

**Si falla:** iterar antes de seguir. No pasar a Paso 2 con dudas.

### Paso 2 — Integración en Jekyll (semana 2)

**Objetivo:** trasladar el prototipo a los layouts Jekyll.

**Entregables:**

- `docs/_layouts/edition.html` actualizado.
- `docs/_layouts/actor.html` nuevo.
- `docs/_layouts/proposal.html` nuevo.
- `docs/_layouts/palanca.html` nuevo.
- `docs/_layouts/default.html` con chrome operacional y footer renovado.
- `docs/_includes/` con partials: `chrome-ops.html`, `tags.html`, `actor-chip.html`, `state-pill.html`, `progress-bar.html`, `margin-note.html`.
- Colecciones Jekyll: `_actores`, `_propuestas`, `_palancas`, `_conceptos` (glosario).
- `docs/assets/css/main.css` consolidado (reemplaza el actual).

**Validación:**

- Build local con `bundle exec jekyll serve`.
- Verificación visual de W14-W17 retroactivas ya publicadas.
- URLs de ficha funcionan: `/actores/govern-balear/`, `/palancas/limite-hut/`.

### Paso 3 — OG images (semana 2)

**Objetivo:** plantilla OG reproducible para cada edición.

**Entregables:**

- `scripts/gen_og.py` o `scripts/gen_og.js` (Puppeteer).
- `docs/assets/og-template.html` (fuente de la imagen).
- Action que corra tras `report.py` y commitee la PNG a `docs/assets/og/{slug}.png`.
- OG fallback estático.

### Paso 4 — Sistema de marca completado (semana 3)

**Objetivo:** logo, favicon, manual mínimo.

**Entregables:**

- `docs/assets/favicon.svg` renovado si hace falta.
- `docs/assets/logo.svg` (color completo) + `logo-mono.svg` (un color).
- `docs/assets/logo-og.png` (alta resolución para citas).
- Sección "Logo" en `/cita-esto/` con las variantes descargables.

### Paso 5 — Auditoría y pulido (semana 3)

- Pa11y + Lighthouse en las 15+ páginas modelo.
- Verificación de contraste en los 8 tokens `--actor-*`.
- Checklist de accesibilidad manual.
- Core Web Vitals medidos en producción con PageSpeed Insights.
- Corrección de los hallazgos.

### Paso 6 — Documentación del sistema (semana 3)

**Entregable:** `docs/_pages/sistema.md` (oculto en `<meta name="robots" content="noindex">`).

Página interna con:

- Paleta extendida con swatches en vivo.
- Escala tipográfica con ejemplos.
- Todos los componentes renderizados en distintos estados.
- Uso permitido / prohibido.

Sirve al editor y a cualquier futuro colaborador. No es público pero es indexable internamente por el propio editor.

---

## 11. Decisiones cerradas por el editor (2026-04-21)

**Las 13 decisiones del estudio resueltas. D2 (logo) diferida hasta que el editor revise [`prototype/logo/preview.html`](prototype/logo/preview.html) con las 3 direcciones SVG.**

| # | Tema | Elección final | Nota |
|---|---|---|---|
| D1 | Wordmark | **D · separable** (monograma + wordmark "Radar Ibiza" como piezas independientes) | |
| D2 | Logo · dirección | **diferido** — 3 direcciones SVG en prototype, editor elige tras ver | Dir 1 punto limpio, Dir 2 "I" italic centro, Dir 3 "I" + arcos lado |
| D3 | Chrome operacional · datos | **A · 6 datos** (edición, propuestas, actores, coste API mes, última publicación, pipeline) | |
| D4 | Chrome operacional · colocación | **A · pie de cada página** (encima del footer estándar) | |
| D5 | Paleta por tipo de actor | **A · 8 categorías con candado** | Taxonomía cerrada, casos fronterizos se asimilan |
| D6 | Ciclo de propuesta | **A · 8 estados + barra de progreso** | Propuesta → registrada → en debate → aprobada → en ejecución → implementada (+descartada e incumplida como ramas) |
| D7 | Ficha de actor | **A · sidebar sticky** en desktop ≥1024 px, `<details>` plegable en móvil | |
| D8 | Notas al margen | **A · Tufte-style** en ediciones, `/explica/` y `/metodologia/` | |
| D9 | Toggle temporal | **A · Temporada YYYY / Pre-temporada YYYY + Histórico** | Etiquetas públicas sin "invierno" (ambiguo); fechas reales internas por opening/closing de clubs |
| D10 | OG images | **A · Puppeteer (HTML → PNG)** | Plantilla editable en CSS, runner CI |
| D11 | Modo oscuro manual | **Híbrido · automático default + dos botones ○/● con localStorage** | Sin opción "auto" explícita; una vez elegido, queda fijado |
| D12 | Documentación del sistema visual | **A · `/sistema/` interna con noindex,nofollow** | Accesible por URL directa |
| D13 | Formulario universal | **A · "Escríbenos" flotante** (Formspree, campos opcionales salvo mensaje) | Botón fijo esquina inferior derecha en todas las páginas |

### Matices registrados

- **Numeración de edición:** "W17" fuera de toda comunicación pública. URLs usan fecha ISO del lunes: `/ediciones/2026-04-20/`. Cabecera, OG, chrome operacional: rango de fechas (`Edición del 20-26 abril 2026`). "W17" solo como slug interno (archivos, logs, commits).
- **Temporadas:** etiquetas públicas `Temporada YYYY` y `Pre-temporada YYYY`. Fechas reales internas: opening/closing de Pacha/Hï/Ushuaïa/Amnesia (2026: 24 abril → ~12 octubre). Automatización anual `src/update_temporadas.py` (A17 en ROADMAP) consulta news y alerta Telegram con fechas candidatas para el año siguiente; el editor actualiza `data/temporadas.yml` manualmente.
- **Modo oscuro:** símbolos Unicode puros `○` (claro) y `●` (oscuro), no emoji. Persistencia en `localStorage` (no cookie, GDPR-OK, compatible con política "sin cookies").
- **Formulario "Escríbenos":** abierto a correcciones, datos nuevos, pistas, testimonios, dudas, críticas, colaboraciones. Nombre y email **opcionales**. Solo mensaje obligatorio. Nota explícita: *"Si aportas un dato, adjunta URL a fuente primaria. Sin fuente verificable no lo incorporamos, pero lo leemos igual."*

### Nota histórica sobre las opciones desechadas

Las opciones A/B/C originalmente presentadas aquí se conservan abajo a título documental — muestran el rango de alternativas consideradas en cada decisión. El editor eligió la recomendación (A) en 11 de 13 y una variante híbrida en D11.

---

## 11bis. Opciones desechadas — referencia histórica

**Cada decisión tenía recomendación y alternativas. Se conservan abajo para trazabilidad.**

### D1. Wordmark de dos líneas

Propuesta: `Ibiza` (serif italic, terracota) / `Housing Radar` (serif regular, tinta).

- **A. Aceptar propuesta.**
- B. Una sola línea: `Ibiza Housing Radar` en serif regular tinta (más sobrio).
- C. Otro wordmark — describe cuál.

**Recomendación: A.** La doble línea con italic en "Ibiza" evoca cabecera de diario y aporta carácter. Compatible con dominios futuros (si cambia nombre, el wordmark se adapta sin rediseño).

### D2. Logo: radar pulsante con tres arcos

Propuesta descrita en §4.2.

- **A. Aceptar.**
- B. Sin logo gráfico, solo wordmark (más minimalista).
- C. Otro concepto — describe.

**Recomendación: A.** Encaja con el nombre y con la animación ya existente (`dash-pulse`). Coste de ejecutar: 10 minutos (SVG trivial). Reversible.

### D3. Chrome operacional: datos a mostrar

Propuesta (§6.1): 6 datos — Edición, Propuestas documentadas, Actores seguidos, Coste API mes, Última publicación, Pipeline.

- **A. Aceptar los 6.**
- B. Solo 3 (Edición, Coste API mes, Pipeline). Más sobrio.
- C. Ampliar: añadir "Correcciones registradas", "HTML page weight", "Build time".

**Recomendación: A.** Seis es el equilibrio. Tres es insuficiente para la tesis "transparencia radical". Nueve empieza a ser ruido.

### D4. Colocación del chrome operacional

- **A. Pie de cada página** (encima del footer estándar).
- B. Solo en home y en `/estado/`.
- C. Barra fija inferior (sticky) en todas las páginas, 32 px de altura.

**Recomendación: A.** Solar Low-Tech usa barra fija pero ocupa espacio permanente y compite con el contenido. Footer es suficiente: quien busca, baja.

### D5. Paleta por tipo de actor (8 tokens `--actor-*`)

Propuesta §5.1.

- **A. Aceptar los 8.**
- B. Reducir a 4 tipos (público, privado, ciudadano, otro).
- C. No diferenciar por color; solo por etiqueta de texto.

**Recomendación: A.** La diferenciación cromática sutil (todos tonos apagados) acelera reconocimiento visual. No compite con terracota. Reducir a 4 mezcla categorías que el lector distingue (sindicato ≠ patronal ≠ colectivo ciudadano).

### D6. Pill de estado + barra de progreso para palancas

Propuesta §6.5 con 8 estados y colores definidos.

- **A. Aceptar los 8 estados.**
- B. Reducir a 5 (propuesta / en debate / aprobada / implementada / descartada).
- C. Solo pills sin barra de progreso.

**Recomendación: A.** Los 8 estados reflejan la realidad institucional. Reducir pierde información (una propuesta "registrada" es ≠ "propuesta"; "incumplida" es distinto de "descartada"). La barra de progreso es el elemento más diferenciador del proyecto.

### D7. Ficha de actor con sidebar sticky

Propuesta §6.7.

- **A. Aceptar.**
- B. Sin sidebar, solo anchors en la parte superior.
- C. Con sidebar pero no sticky (scroll normal).

**Recomendación: A.** El sidebar sticky es el único patrón que convierte la ficha en herramienta (el profesional puede navegar facetas sin perder posición). Coste CSS: ~40 líneas.

### D8. Margin notes (Tufte-style)

Propuesta §6.8.

- **A. Aceptar, usar en ediciones + `/explica/` + `/metodologia/`.**
- B. Diferir a Fase 1. Usar notas al pie tradicionales en Fase 0.
- C. Nunca; las notas van inline entre paréntesis.

**Recomendación: A.** Es el elemento que convierte una edición densa en lectura fluida. Si las ediciones W14-W17 no las usan, se añaden en Fase 1 sin dolor. Pero tener el componente listo cuesta lo mismo ahora.

### D9. Toggle histórico (dos horizontes)

Propuesta §6.9.

- **A. Aceptar, aplicar en fichas de actor, palancas y `/balance/`.**
- B. Diferir: en Fase 0 solo "temporada actual", añadir histórico en Fase 1.
- C. No separar; mostrar siempre todo cronológico.

**Recomendación: A.** Sin toggle, el primer visitante se pierde en histórico o el profesional se frustra viendo solo reciente. Dos paneles HTML + radios cuestan 20 líneas.

### D10. OG image: generación automática

Propuesta §7: HTML → Puppeteer → PNG, integrado en Action.

- **A. Sí, con Puppeteer.**
- B. Sí, con Pillow (Python puro, más ligero, menos flexibilidad).
- C. OG manual una vez por edición (editor hace screenshot).

**Recomendación: A.** Puppeteer permite editar CSS del template y ver cambios al instante. Pillow obliga a manipular píxeles. Coste adicional del runner Action: ~10 s / edición. Aceptable.

### D11. Toggle modo oscuro manual

- A. Sí, implementar en Fase 0 (CSS puro, ~30 líneas).
- **B. No, solo `prefers-color-scheme`. Diferir toggle a Fase 1.**
- C. Sí, y con 3 estados (claro / oscuro / auto).

**Recomendación: B.** `prefers-color-scheme` cubre el 90 % de lectores. El toggle es lujo que añade superficie sin aportar a la credibilidad. Fase 1.

### D12. Documentación del sistema interna (`/sistema/`)

Propuesta §10 paso 6.

- **A. Sí, indexar solo para editor (noindex en robots).**
- B. Sí, y público (añade transparencia).
- C. No; toda la spec vive en este doc markdown.

**Recomendación: A.** Público es exceso (nadie va a reutilizar nuestro sistema). No tenerla es riesgo: futuros colaboradores o yo mismo en 6 meses no vamos a recordar los tokens sin referencia visual. Solución privada es lo más eficiente.

---

## 12. Fuera de alcance — Fase 2+

Explicitado para **no** hacer en Fase 0:

- **Dithering OG images** (Solar Low-Tech). Añade peso visual pero no aporta credibilidad en nuestra tesis social. Decisión final tras ver prototipo en Fase 2.
- **Ilustraciones custom por tema** (Rest of World, The Pudding). Requiere director de arte. Fase 3+.
- **Podcast / audio player** (Tortoise). Fuera del alcance del proyecto hasta que haya contenido de audio.
- **Perfiles de autor con biografía extendida** (EOM, ProPublica). Solo hay un editor (Raúl), `/acerca/` lo cubre.
- **Donación pública / membership / Pro tier** (Tortoise, ProPublica, Bellingcat). Modelo híbrido Pro solo en Fase 2 (ver [DECISIONES-PENDIENTES.md](DECISIONES-PENDIENTES.md) #7).
- **Integraciones externas** tipo WriteToThem (TheyWorkForYou). Posible en Fase 3 si hay demanda.
- **Multiidioma** (Rest of World). Fase 4 diferido, ver [PLAN.md](PLAN.md).

---

## 13. Checklist — Fase 0 diseño

Al completar el Bloque B del Roadmap, estas casillas deben estar marcadas:

- [ ] D1–D12 decididas por el editor.
- [ ] `prototype/` HTML estático validado.
- [ ] Logo SVG final + favicon renovado.
- [ ] Paleta extendida implementada en `main.css`.
- [ ] Escala tipográfica implementada con tokens `--fs-*`, `--lh-*`.
- [ ] Sistema de espaciado implementado con tokens `--sp-*`.
- [ ] 9 componentes con layouts y partials en Jekyll.
- [ ] Chrome operacional poblado con datos reales del repo.
- [ ] OG template auto-generado funcional.
- [ ] Modo oscuro auditado tras cambios.
- [ ] Pa11y + Lighthouse ≥ 95 en 5 páginas modelo.
- [ ] Contraste AA verificado en todos los tokens de actor.
- [ ] Core Web Vitals ≤ targets en producción.
- [ ] `/sistema/` interno documentado.
- [ ] Budget de peso cumplido en todas las páginas modelo.

---

## 14. Referencias

### Primarios

- [PIVOTE.md](PIVOTE.md) — 5 reglas duras.
- [DISENO-WEB.md](DISENO-WEB.md) — arquitectura de información, mapa del sitio.
- [ROADMAP.md](ROADMAP.md) — Bloque B tareas.
- [DECISIONES-PENDIENTES.md](DECISIONES-PENDIENTES.md) — decisiones cerradas 2026-04-20.
- [SEO.md](SEO.md) — impacto de diseño en SEO.

### Benchmark editorial

- [Solar Low-Tech Magazine](https://solar.lowtechmagazine.com/)
- [Bellingcat](https://bellingcat.com)
- [The Pudding](https://pudding.cool)
- [Civio](https://civio.es)
- [Datadista](https://datadista.com)
- [Tortoise Media](https://www.tortoisemedia.com)
- [El Orden Mundial](https://elordenmundial.com)
- [The Intercept](https://theintercept.com)
- [ProPublica](https://propublica.org)
- [Rest of World](https://restofworld.org)
- [TheyWorkForYou](https://theyworkforyou.com)
- [GovTrack.us — Wikipedia](https://en.wikipedia.org/wiki/GovTrack.us)
- [OpenSecrets](https://www.opensecrets.org/)

### Técnicos

- [Core Web Vitals](https://web.dev/vitals/)
- [WCAG 2.2 AA](https://www.w3.org/WAI/WCAG22/quickref/)
- [Pa11y](https://pa11y.org/)
- [Instrument Serif on Google Fonts](https://fonts.google.com/specimen/Instrument+Serif)

---

**Fin del estudio.** Con D1–D12 decididas, el Bloque B es ejecutable sin paradas.
