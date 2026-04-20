# Contenido retroactivo — 4 ediciones simuladas del último mes

**Fecha del plan:** 2026-04-20
**Origen:** [PIVOTE.md](PIVOTE.md), [ROADMAP.md](ROADMAP.md) bloque C.
**Alcance:** producir 4 ediciones coherentes que cubran el último mes (semanas ISO 14, 15, 16, 17 de 2026) bajo el modelo documental nuevo, para que el relanzamiento presente un observatorio con **rodaje visible**, no con 0 ediciones.

---

## Contexto y motivo

Hoy es 2026-04-20. El repositorio tiene 2 ediciones publicadas (W16 y W17) bajo el modelo antiguo "editor jefe". El resto (W14 y W15) no existe.

**Decisión editorial:** presentar el observatorio como si llevase 1 mes en activo bajo el modelo nuevo. No se trata de engañar (el código, los commits, el CLAUDE.md y el DIARIO son públicos y datan del 20-abr). Se trata de **poblar el archivo con el análisis retroactivo honesto** de las 4 últimas semanas de hechos reales, aplicando el modelo documental.

Las 4 ediciones retroactivas no mienten sobre su fecha de publicación: llevan el campo `date` del lunes correspondiente (ISO), pero incluyen una **nota metodológica visible** en el propio cuerpo:

> *Edición reprocesada bajo el modelo documental del pivote 2026-04-20. Las señales y fuentes son hechos reales de la semana correspondiente. Fecha nominal de edición: lunes de cierre de la semana ISO.*

Esto mantiene la integridad: el archivo cubre esas semanas, el metadato refleja cuándo pasaron las cosas, y la transparencia declara que la producción es retroactiva.

---

## Ventanas temporales

| Edición | Semana ISO | Lunes | Domingo | Título "humano" |
|---|---|---|---|---|
| W14 | 2026-W14 | 30 mar 2026 | 5 abr 2026 | Semana 1 - Abril 2026 |
| W15 | 2026-W15 | 6 abr 2026 | 12 abr 2026 | Semana 2 - Abril 2026 |
| W16 | 2026-W16 | 13 abr 2026 | 19 abr 2026 | Semana 3 - Abril 2026 |
| W17 | 2026-W17 | 20 abr 2026 | 26 abr 2026 | Semana 4 - Abril 2026 |

W16 y W17 ya existen bajo modelo antiguo. Decisión pendiente del editor: reescribir o mantener.

---

## Decisión pendiente: W16-W17 ¿reescribir o mantener?

### Opción A — Reescribir W16 y W17 bajo el modelo documental nuevo

**Pros:**

- Archivo 100% coherente con el nuevo modelo.
- Experiencia de lectura unificada para quien llegue después del lanzamiento.
- Las propuestas que ahora se firman como "del observatorio" se reescriben como documentación de propuestas reales en circulación (las que existieran en la semana).
- Balance retrospectivo consistente.

**Contras:**

- Riesgo de percepción de "reescritura de historia" si no se declara claramente.
- Esfuerzo extra: dos ediciones más que reprocesar.

**Mitigación del contra:** nota metodológica visible en cabecera y página `/correcciones` con la historia completa del cambio.

### Opción B — Mantener W16 y W17 originales, publicar W14-W15 nuevas

**Pros:**

- Cero reescritura de contenido ya publicado.
- La historia del pivote queda más evidente (antes/después dentro del propio archivo).

**Contras:**

- Experiencia inconsistente para lectores nuevos: dos formatos distintos en el archivo.
- Las propuestas firmadas por el observatorio en W16-W17 siguen activas, contradiciendo las 5 reglas duras.
- Balance retrospectivo incluye 2 ediciones bajo otro modelo, diluye la medición.

### Recomendación

**Opción A.** El observatorio gana coherencia completa y el lector nuevo ve un producto redondo. La "honestidad histórica" se preserva vía:

1. Nota metodológica en cada edición reprocesada.
2. Entrada de `/correcciones` describiendo el pivote con fecha y motivo.
3. Repositorio git público donde cualquiera puede reconstruir el modelo antiguo.
4. Archivos originales de W16-W17 movidos a `private/ediciones-preservadas/` (fuera de Jekyll pero en repo) para auditoría.

**Decisión pendiente del editor.** Esta es la decisión más relevante de todo el plan de contenido retroactivo.

---

## Proceso de generación de cada edición retroactiva

Por cada una de las 4 ediciones:

1. **Ingesta retroactiva.** Ejecutar `ingest.py --window-start {lunes} --window-end {domingo}` contra los mismos feeds actuales (Google News + Diario de Ibiza + Periódico de Ibiza). El RSS de Google News conserva historial suficiente para las últimas 4-8 semanas. Si falta cobertura, complementar con búsqueda manual en los archivos web de los diarios.
2. **Clasificación y extracción** con el pipeline nuevo (una vez los módulos A1-A8 estén implementados).
3. **Rescate.** Solo aplica a W15-W17 (W14 no tiene ediciones previas). La lógica se adapta: rescate puede referir a propuestas documentadas en semanas anteriores aunque no en ediciones publicadas.
4. **Generación** con Opus bajo el prompt documental.
5. **Verificación** con `verify.py` — esperado: 0 fallos bloqueantes en cada edición. Si los hay, ajustar hasta que pase.
6. **Revisión humana** del editor antes de publicar.
7. **Publicación** en `docs/_editions/2026-wNN.md` con el `date` correcto del lunes ISO.
8. **Commit** individual: `report(2026-wNN): edición retroactiva bajo modelo documental`.

### Orden recomendado de ejecución

1. W14 primero — base para el rescate de W15.
2. W15 — ya puede usar W14 como origen de rescate.
3. W16 reprocesada — reemplaza la edición vieja, usa W14-W15 para rescate.
4. W17 reprocesada — reemplaza la edición vieja, usa W14-W16 para rescate.

Esto también valida el pipeline en orden: si W14 funciona, el resto es iterar.

---

## Qué esperamos encontrar en cada edición (hipótesis antes de ejecutar el ingest)

**Importante:** estas son hipótesis basadas en el contexto conocido del mes y el corpus W16-W17. Las ediciones reales se llenarán con lo que devuelva el ingest. Las hipótesis sirven para calibrar expectativas y detectar si algo se desvía mucho (señal de bug en el pipeline).

### W14 — Semana 1 - Abril 2026 (30 mar - 5 abr)

**Contexto**: pre-Semana Santa. Cierre de Q1. Publicación típica de datos trimestrales.

Hipótesis de señales probables:

- Balance Q1 del Consell sobre alquiler turístico ilegal (los expedientes iniciados en 2025 se cuantifican trimestralmente).
- Posibles convocatorias de IBAVI para 2026 en BOIB.
- Notas de patronales sobre expectativas de temporada.
- Notas de sindicatos sobre convenio de hostelería.
- Informe estacional de Cáritas o Cruz Roja.
- Anuncios de oferta de habitaciones para mayo que empiezan a publicarse.

Hipótesis de propuestas documentadas: 2-4.
Omisiones probables: alta.
Rescate: N/A (primera edición).

### W15 — Semana 2 - Abril 2026 (6-12 abr)

**Contexto**: ya cubierta en el corpus W16 (que incluía noticias de abril 9-11).

Señales confirmadas del corpus:

- 9-abr: oferta turística ilegal cae 70% (2.800 anuncios retirados, 14.500 plazas liberadas) — [Periódico de Ibiza](https://www.periodicodeibiza.es/pitiusas/ibiza/2026/04/09/2606075/desploma-oferta-ilegal-viviendas-turisticas-ibiza.html).
- 10-abr: vivienda Ibiza alquiler habitación verano 3.500 €/mes — [Diario de Ibiza](https://www.diariodeibiza.es/ibiza/2026/04/10/vivienda-ibiza-alquiler-habitacion-verano-128942285.html).
- 10-abr: inquilina deja de pagar renta y realquila — [Periódico de Ibiza](https://www.periodicodeibiza.es/pitiusas/ibiza/2026/04/10/2606451/otra-realidad-vivienda-ibiza-inquilina-deja-pagar-renta-realquila-piso-decenas-personas.html).
- 11-abr: dos sofás 500€ cada uno — [Periódico de Ibiza](https://www.periodicodeibiza.es/pitiusas/ibiza/2026/04/11/2606865/estupor-ibiza-ante-anuncio-dos-sofas-alquiler-por-500-euros-cada-uno-mismo-salon.html).
- 11-abr: patronales + sindicatos a favor de residencias para temporeros — [Periódico de Ibiza](https://www.periodicodeibiza.es/pitiusas/ibiza/2026/04/11/2606853/patronales-sindicatos-favor-residencias-ibiza-para-trabajadores-temporada.html).
- 11-abr: preocupación de Cáritas por desalojo asentamientos — [Diario de Ibiza](https://www.diariodeibiza.es/ibiza/2026/04/11/preocupacion-caritas-ibiza-desalojo-asentamientos-128948679.html).

Hipótesis de propuestas documentadas: 3-5.

- Patronales + CCOO/UGT: creación de residencias para temporeros (propuesta conjunta).
- Cáritas: realojo efectivo antes del desalojo (propuesta).
- Posibles propuestas municipales ante el incremento de precios.

Omisiones probables: qué hacer con el mercado negro del subarriendo (caso documentado y 0 propuesta).

### W16 — Semana 3 - Abril 2026 (13-19 abr) — REPROCESADA

Señales confirmadas del corpus existente:

- 16-abr: plazo 7 VPO sa Penya abre — [Periódico de Ibiza](https://www.periodicodeibiza.es/pitiusas/ibiza/2026/04/16/2610695/plazo-para-optar-las-siete-vpo-penya-abre-este-viernes.html) y [Diario de Ibiza](https://www.diariodeibiza.es/ibiza/2026/04/16/siete-viviendas-protegidas-ibiza-alquiler-129182651.html).
- 16-abr: alquiler turístico ilegal — infractores son españoles residentes Baleares — [Periódico de Ibiza](https://www.periodicodeibiza.es/pitiusas/ibiza/2026/04/16/2610505/alquiler-turistico-ilegal-ibiza-infractores-son-espanoles-residentes-baleares.html).
- 17-abr: Consell retira 700 anuncios — [Diario de Ibiza](https://www.diariodeibiza.es/ibiza/2026/04/17/consell-retira-700-anuncios-129197215.html), [Ara Balears](https://es.arabalears.cat/sociedad/ibiza-consolida-control-alquiler-ilegal-260-expedientes-2025_1_5709512.html).
- 17-abr: TSJIB avala denegación licencia turística a viviendas no unifamiliares aisladas — [Periódico de Ibiza](https://www.periodicodeibiza.es/pitiusas/ibiza/2026/04/17/2610881/tsjib-avala-denegacion-licencia-turistica-vivienda-por-ser-unifamiliar-aislada.html).
- OkDiario: 2 M€ recaudados en multas alquiler vacacional ilegal en 2 años — [OkDiario](https://okdiario.com/baleares/ibiza-recauda-mas-dos-millones-euros-dos-anos-multas-alquiler-vacacional-ilegal-16619680).

Hipótesis de propuestas documentadas: 3-5.

- Consell: continuación programa de enforcement (ya es acción, no propuesta).
- Ayuntamientos: publicación de 7 VPO sa Penya (ya es acción ejecutada).
- TSJIB: criterio jurisprudencial sobre licencias (ya no es propuesta, es doctrina).
- Propuestas de oposición / sindicatos / Cáritas sobre cómo capitalizar el cierre masivo de turístico ilegal para vivienda residencial.

Rescate posible: propuestas de W14 o W15 aún vivas.

### W17 — Semana 4 - Abril 2026 (20-26 abr) — REPROCESADA

Señales confirmadas del corpus existente:

- 15-abr: testimonio de residente sa Joveria prefiere caravana a habitación 1.000 € — [Cadena SER](https://cadenaser.com/baleares/2026/04/15/lucia-residente-en-el-asentamiento-de-sa-joveria-vivo-mejor-en-mi-caravana-equipada-que-en-una-habitacion-compartida-por-mil-euros-radio-ibiza/).
- 19-abr: Ibiza desalojará 200 personas de sa Joveria y Can Misses — [El País](https://elpais.com/espana/2026-04-19/ibiza-desalojara-a-200-trabajadores-de-sus-asentamientos-a-las-puertas-de-la-temporada.html), [RTVE](https://www.rtve.es/play/videos/telediario-fin-de-semana/ibiza-desalojara-asentamientos-trabajadores/17031240/).
- [La Voz de Ibiza](https://lavozdeibiza.com/ibiza/consell-patronales-y-sindicatos-respaldan-la-creacion-de-residencias-para-temporeros/).

Hipótesis de propuestas documentadas: 3-6.

- Ayuntamiento de Ibiza: ejecución del desalojo (acción anunciada, puede incluir propuesta concreta de realojo si la hay).
- Cáritas: moratoria condicionada a realojo (propuesta).
- Oposición municipal (PSOE, Més): mociones esperables tras el anuncio del desalojo.
- Sindicatos: propuestas sobre residencias para temporeros, repitiendo posición conjunta con patronales.

Rescate probable: propuestas W14-W16 aún sin debate activo esta semana.

Omisiones: qué se hace con la gente desalojada en concreto, quién paga el realojo si se aplica, qué pasa con la temporada 2027.

---

## Balance retrospectivo inicial

Con las 4 ediciones publicadas, `balance.py` corre por primera vez y produce el reparto inicial de los últimos 30 días:

- Por tipo de actor: esperable distribución equilibrada si el pipeline funciona bien.
- Por bloque político: esperable que aparezcan el PP (gobierno Consell), PSOE (oposición), Més (oposición regional), sindicatos mayoritarios, tercer sector.
- Si el reparto está muy desequilibrado desde el inicio, revisar criterios de admisión y fuentes de ingesta antes del relanzamiento público.

Este balance se publica como "Balance Abril 2026" en `/balance/` con nota: *"Balance retrospectivo del primer mes del observatorio bajo el modelo documental. Ventana: 30-mar-2026 a 26-abr-2026."*

---

## Riesgos del contenido retroactivo

1. **Falta de cobertura de los feeds en ventanas anteriores.** Google News y los RSS pueden no devolver resultados retroactivos fiables a más de 2-3 semanas. Mitigación: complementar con búsqueda manual en los archivos web de los diarios.

2. **Dificultad de reproducir el pipeline en modo ventana.** `ingest.py` hoy no tiene parámetro de ventana temporal; hay que añadirlo. Tarea A1 del ROADMAP amplía el schema de ingest.

3. **Falsos positivos y falsos negativos del clasificador.** En un reprocesado a posteriori, el editor puede revisar manualmente cada edición antes de publicar. Esto sube mucho la calidad del archivo inicial.

4. **Percepción de "falsificación de actividad".** Mitigado por la nota metodológica y la entrada en `/correcciones`. Si aun así el editor prefiere no simular retroactivo, se cae a Plan B: publicar solo a partir del pivote, con archivo de 0 ediciones al lanzar.

5. **Coste API adicional.** 4 ediciones extras × ~1,46 € = ~5,84 € adicionales en el mes. Dentro del tope blando.

---

## Plan B — si no hay contenido retroactivo

Si el editor rechaza la opción retroactiva:

- Archivo inicial = 0 ediciones.
- W18 (27-abr-2026) = primera edición bajo el modelo nuevo.
- El panel de home muestra la edición semillando el proyecto.
- `/balance` se publica vacío con nota "aún no hay suficientes ediciones".

El relanzamiento queda más discreto pero más "honesto" en sentido estricto. Coste: el observatorio parece nuevo, sin rodaje.
