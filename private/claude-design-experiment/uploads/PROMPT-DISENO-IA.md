# Prompt para IA de diseño — Ibiza Housing Radar

---

**Qué es el proyecto**

Ibiza Housing Radar es un observatorio semanal documental sobre la crisis de vivienda en Ibiza. Cada lunes mapea las propuestas que políticos, sindicatos, patronal, ONGs y colectivos ciudadanos formulan públicamente, con fuente verificable (URL). No genera propuestas propias ni toma partido. Es una herramienta periodística/cívica, no una ONG.

---

**Dos públicos con necesidades distintas**

| | Primer visitante no técnico | Profesional recurrente |
|---|---|---|
| Perfil | Ciudadano de Ibiza, temporero, familiar | Periodista, regidor, académico, sindicalista |
| Dispositivo | Móvil (70%) | Desktop (60%) |
| Tiempo | 30-90 segundos | 3-10 minutos, vuelve cada semana |
| Necesita | Entender qué es, ver recursos, confiar | Densidad, verificabilidad, datos citables |
| Huye de | Jerga, muchos clicks, tono activista | Relleno, panfletario, datos sin fuente |

**La home debe servir a ambos en la primera pantalla.**

---

**Paleta extendida para tipar actores** (regla dura: los partidos políticos SIEMPRE en gris neutro, nunca con su color de partido):

| Tipo de actor | Color |
|---|---|
| Institucional público | Azul pizarra |
| Partido político | **Gris neutro — sin excepción** |
| Patronal | Ocre |
| Sindicato | Verde musgo |
| Tercer sector (ONGs) | Terracota |
| Académico | Violeta apagado |
| Judicial | Gris oscuro |
| Colectivo ciudadano | Amarillo mostaza |

---

**Componentes clave a diseñar**

1. **Card de propuesta** — título corto, actor + tipo (chip coloreado), estado (pill), horizonte temporal, viabilidad jurídica/económica (dos mini-pills), enlace a fuente.
2. **Chip de actor** — nombre + tipo como pill coloreado según tabla anterior. Nunca color de partido.
3. **Pill de estado de propuesta** — 6 estados: propuesta / en debate / aprobada / en ejecución / implementada / descartada.
4. **Mini-tabla "Mapa de posiciones"** — compacta, muestra quién propone qué y quién apoya/rechaza.
5. **Footer con indicadores de transparencia** — al estilo Solar Low-Tech: coste API del mes (ej. `0,38 €`), capa de alerta (🟢/🟡/🟠/🔴), última edición publicada, estado del pipeline. Todo en tipografía monospace.
6. **Manifiesto en footer** — texto fijo: *"Ibiza Housing Radar es un observatorio documental. No genera propuestas propias. 5 reglas duras en /politica-editorial/. Balance público en /balance/."*
7. **Nota al margen** (estilo Tufte) — `<aside>` a la derecha en desktop ≥1024px, colapsable en móvil.

---

**Estructura de la home (desktop)**

```
Nav: Logo · Ediciones · Propuestas · Actores · Recursos · Más ▾ · [Suscribir]
───────────────────────────────────────────────────────
Hero:
  H1 "Ibiza Housing Radar"
  Tagline "Observatorio semanal de vivienda en Ibiza.
           Mapeamos lo que se propone, no proponemos nosotros."
  [¿Primera vez? → Cómo usarlo]    [Última edición →]
───────────────────────────────────────────────────────
Bloque resumen semana:
  Semana 4 - Abril 2026 · [N] señales · [N] propuestas · [N] omisiones
───────────────────────────────────────────────────────
Panel editorial (2 columnas):
  Columna A: Señales (4-8 bullets con URL)
  Columna B: Mapa de posiciones (tabla compacta)

  Row completo: Cards de propuestas (4 en desktop, 1 en móvil)

  Row compacto: Rescate · Omisiones · A vigilar
───────────────────────────────────────────────────────
Archivo: últimas 4 ediciones (lista densa)
───────────────────────────────────────────────────────
Sobre el proyecto: 3 líneas + links
───────────────────────────────────────────────────────
Footer con indicadores de transparencia (monospace)
```

---

**Responsive mínimo**

- Cards: 4 col (>1280px) → 3 (1024) → 2 (640) → 1 (móvil).
- Tabla mapa de posiciones → cards apiladas en móvil.
- Menú: hamburguesa sin JS.
- Hero legible a 320px sin scroll horizontal.

---

**Tono visual que busco**

Periódico de referencia, no app de startup. Autoridad sin arrogancia. Neutral sin ser aburrido. Denso sin ser ilegible. El equivalente visual de *El País* o *The Guardian* si hubiera nacido en 2024 con un presupuesto de 0 € en infra y obsesión por la transparencia operacional.

---

**Lo que NO quiero**

- Gradientes ni sombras vistosas.
- Ilustraciones o iconografía de stock genérica.
- Colores de partidos políticos (rojo PSOE, azul PP, verde Vox). Siempre gris.
- Tono activista o panfletario en nada.
- Dependencia de JS para funcionar.
- Cualquier cosa que haga pensar "ONG opositora al gobierno".

---

Propón variantes de: (1) home completa desktop + móvil, (2) card de propuesta con todos los estados, (3) footer de transparencia.
