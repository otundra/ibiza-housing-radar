# Pivote — de generador de propuestas a observatorio documental

**Fecha:** 2026-04-20
**Branch:** `pivote/observatorio-documental`
**Rango:** documento fundacional. Todo lo que siga (ROADMAP, ARQUITECTURA, DISEÑO, SEO, CONTENIDO RETROACTIVO) deriva de las decisiones aquí.
**Estado:** propuesto, pendiente de confirmación del editor antes de arrancar ejecución.

---

## Origen del pivote

El observatorio llevaba un mes con producto tipo "editor jefe": Opus generaba propuestas propias cada lunes. El [estudio crítico del 2026-04-20](private/estudios/2026-04-20-propuestas.md) sobre las 8 propuestas publicadas en W16-W17 detectó tres problemas estructurales que ningún ajuste de prompt resuelve por completo:

1. **Acto generativo = acto político.** Proponer medidas, aunque sea con tono neutro, implica tomar partido. El LLM, además, tiene sesgo estadístico hacia marcos intervencionistas.
2. **Precedentes con riesgo de alucinación.** Al menos 3 casos identificados con nombre y cifra que no resisten verificación básica. Un solo precedente inventado que un periodista verifique destruye la credibilidad del proyecto para siempre.
3. **Concentración de actor-destinatario.** 5 de 8 propuestas cargaban sobre el Consell (gobierno PP+Vox). Sin decirlo, el proyecto se leía como ONG opositora al gobierno insular actual.

El editor reafirmó la voluntad del proyecto: **observatorio de referencia, informativo, imparcial, verificable, movilizador, no partidista**. Generar propuestas propias con un LLM es incompatible con esa voluntad. De ahí el pivote.

---

## Tesis

**El observatorio deja de proponer y empieza a mapear lo que ya se propone en la isla, con trazabilidad total.** El valor editorial se desplaza de "tener buenas ideas" a "ahorrarle al lector 3 h de prensa cruzada y ponerle encima el mapa completo". Ese nicho está vacío en Ibiza.

La debilidad del modelo anterior (sesgo del LLM al generar) se vuelve irrelevante cuando el LLM ya no genera. Solo ordena, verifica y resume lo dicho por actores con nombre, organización y URL.

---

## Las 5 reglas duras

Estas reglas son vinculantes y no negociables. Se publican en `/politica-editorial` y se aplican en cada edición sin excepción.

### 1. Solo se documentan propuestas con autor identificado y URL verificable.

Nada de memoria del LLM. Nada de "se comenta que". Nada de precedentes inventados. Si no hay fuente primaria enlazable, la propuesta no entra en la edición.

### 2. El observatorio no genera propuestas propias.

Mapea, cruza, ordena, resume, rescata lo ya dicho por terceros. La decisión sobre qué hacer queda en manos del lector. El LLM no firma propuestas.

### 3. Ningún actor queda excluido por filiación.

Toda propuesta que cumpla los criterios de admisión se documenta, venga del PP, del PSOE, de Vox, de Més, de Sumar, de CCOO, de CAEB, de Cáritas, de un bufete, de un académico o de un colectivo vecinal. Los criterios son los mismos para todos.

### 4. Balance de actores auditado y publicado cada trimestre.

Página pública `/balance` con el reparto absoluto y relativo de citas por actor y por bloque político en ventanas de 3, 6, 12 meses. Si un bloque supera 50% durante dos trimestres consecutivos, nota metodológica visible en la edición y revisión de criterios.

### 5. Correcciones públicas con traza.

Cualquier error verificado de hecho o atribución se corrige con nota visible, fecha y motivo en `/correcciones`. La edición original se marca "corregida" con enlace a la nota.

---

## Antes / después

| Dimensión | Modelo antiguo (W16-W17) | Modelo nuevo (desde el pivote) |
|---|---|---|
| Output principal | Propuestas redactadas por Opus | Propuestas reales documentadas |
| Autoría de cada propuesta | "Ibiza Housing Radar propone…" | "[Actor con nombre] propone… [fuente]" |
| Verbos permitidos | "condicionar", "afectar", "tope", "moratoria" | "propone", "reclama", "rechaza", "presenta", "solicita" |
| Precedente | Cita de memoria del LLM | URL obligatoria al documento primario |
| Viabilidad jurídica | Asumida | Declarada (alta/media/baja/no evaluada) con motivo |
| Viabilidad económica | Cifra puntual inventada | Rango con método declarado o "sin cifra pública disponible" |
| Actor responsable | Asignado por el LLM | Extraído del texto original |
| Tono editorial | "Lectura" del editor con valoración | "Cronología" objetiva sin valoración |
| Riesgo de alucinación | Alto | Bajo (el LLM reproduce, no inventa) |
| Riesgo de sesgo | Alto y no declarado | Bajo en generación; medido y declarado en selección |
| Nicho diferencial | Ideas del LLM | Inventario + cartografía + rescate + omisiones |

---

## Qué NO cambia

- **Cadencia semanal**: edición cada lunes 05:00 UTC (~07:00 Madrid).
- **Foco geográfico**: Ibiza y Formentera, con énfasis en trabajadores de temporada mayo-octubre.
- **Foco temático**: vivienda, alquileres, desahucios, asentamientos, alquiler turístico ilegal, normativa, políticas locales.
- **Stack técnico**: Python + Anthropic API + Jekyll + GitHub Pages + GitHub Actions. Coste 0 salvo API.
- **Tono literario**: directo, sin adornos, sin lenguaje corporativo.
- **Estructura weekly ISO**: permalinks `/ediciones/YYYY-wWW/`, títulos "Semana N - Mes Año".
- **Compromiso coste cero externo** salvo API y eventualmente un dominio propio.

---

## Qué SÍ cambia (resumen)

1. **Pipeline técnico**: se añaden módulos `extract.py`, `verify.py`, `rescue.py`, `balance.py`. Se reescribe `generate.py` con prompt documental. Schema de clasificación se amplía con campos de propuesta extraída.
2. **Estructura de la edición**: secciones reorganizadas (ver [ARQUITECTURA.md](ARQUITECTURA.md)). Aparece **Mapa de posiciones**, **Rescate**, **Omisiones**.
3. **Web**: +15 páginas nuevas. Home dual (primera vez + recurrente). Detalle en [DISENO-WEB.md](DISENO-WEB.md).
4. **SEO**: pilar fundamental, plan ambicioso en [SEO.md](SEO.md).
5. **Contenido retroactivo**: relato coherente de 4 ediciones (W14-W17) reprocesadas bajo el nuevo modelo, detalle en [CONTENIDO-RETROACTIVO.md](CONTENIDO-RETROACTIVO.md).
6. **Política editorial pública** con las 5 reglas duras.

---

## Indicadores de éxito

Ninguno puede ser un KPI si el proyecto toma partido. Todos son posibles bajo el pivote.

- [ ] Cita pública del proyecto por un regidor del PP **y** un regidor de Més/PSOE en los primeros 6 meses. Si solo cita un bloque, el pivote está fallando.
- [ ] Cero acusaciones públicas de parcialidad por cualquier actor nombrado durante 2 trimestres consecutivos.
- [ ] Al menos un periodista local cita el proyecto como fuente de mapeo (no como editorial).
- [ ] Al menos una propuesta documentada pasa a debate formal (pleno, moción, nota oficial) en los 60 días posteriores. Movilización medible sin exhortación.
- [ ] Balance público trimestral con reparto de citas ±15 puntos respecto al peso institucional real en Baleares.
- [ ] Newsletter con representación de gestión pública, sector privado y tercer sector entre los primeros 30 suscriptores.

---

## Riesgos del pivote — honestidad completa

1. **Menos "punch" semanal.** Dejar de generar propuestas baja la capacidad de titular. Precio real de la imparcialidad. Mitigación: mapa de posiciones, rescate y omisiones dan tres anclas editoriales nuevas.
2. **Semanas flacas.** Si una semana nadie propone nada, la sección queda corta. Mitigación: `rescue.py` + aceptar que un "diagnóstico de silencio" también es información.
3. **Trabajo de fact-checking mayor.** Verificar URL, cargos, estado de propuesta. Mitigable con Haiku y la regla dura "si no hay URL, no publica".
4. **Pérdida parcial del valor actual.** Hay valor en que el LLM sintetice con precedentes cuando no alucina. Tentación de preservar una sección "análisis del editor" marcada aparte. Recomendación: eliminarla los primeros 3-6 meses para que la marca se asiente como neutral. Si luego el producto se percibe corto, se puede reincorporar una sección mínima marcada explícitamente como opinión firmada por el editor. Nunca por el LLM anónimo.
5. **Dependencia de calidad del ecosistema informativo.** Si los actores locales no proponen nada o proponen mal, la edición lo refleja. Eso es información, no fracaso.

---

## Reversibilidad

Todo este bloque de trabajo vive en el branch `pivote/observatorio-documental`. El `main` queda intacto hasta que el editor apruebe el merge. Si tras 4-6 semanas bajo el nuevo modelo el balance muestra que no funciona, se puede revertir con un merge del main anterior al commit del merge.

---

## Referencias

- [Estudio crítico 2026-04-20](private/estudios/2026-04-20-propuestas.md) — diagnóstico del modelo antiguo.
- [ROADMAP.md](ROADMAP.md) — plan de ataque completo.
- [ARQUITECTURA.md](ARQUITECTURA.md) — pipeline técnico nuevo.
- [DISENO-WEB.md](DISENO-WEB.md) — arquitectura de información y UX.
- [SEO.md](SEO.md) — plan SEO ambicioso.
- [CONTENIDO-RETROACTIVO.md](CONTENIDO-RETROACTIVO.md) — plan de las 4 ediciones simuladas.
- [DECISIONES-PENDIENTES.md](DECISIONES-PENDIENTES.md) — preguntas al editor antes de arrancar.
