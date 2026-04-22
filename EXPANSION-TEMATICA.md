# Expansión temática — estudio de temas "hermanos" de vivienda

**Fecha:** 2026-04-22 (tarde) · **Estado:** hipótesis post-tracción (no ejecutable ahora).

**Condición única de activación:** framework de señales de tracción a 90 días (RT23) da verde en Ibiza. Sin tracción demostrada en vivienda, ninguna expansión temática tiene sentido.

Documento paralelo a la sección *Hipótesis post-tracción — Escalabilidad provincial* de [`ROADMAP.md`](ROADMAP.md). Mientras aquella contempla replicar el modelo a otras geografías, esta contempla ampliar el modelo a otros temas dentro de Ibiza.

---

## 1. Definición de "tema hermano"

Un tema es hermano de vivienda cuando cumple las tres condiciones:

1. **Estructural con presencia semanal** en prensa local (Diario de Ibiza, Periódico de Ibiza, Google News + RSS disponibles).
2. **Actores identificables formulando propuestas públicas verificables** — condición dura del modelo documental. Sin propuestas con URL trazable no hay materia prima.
3. **Pipeline actual lo puede tratar sin rediseño** (ingest → classify → extract → verify → balance).

Los temas que solo generan debate sin propuestas, tienen fuentes opacas, o tienen densidad informativa baja (< 3 noticias/semana de media anual) quedan fuera.

---

## 2. Candidatos evaluados

### Tier 1 — encaje casi directo

| Tema | Por qué encaja | Riesgo principal | Viabilidad |
|---|---|---|---|
| **Saturación turística / regulación de capacidad** | Actores casi idénticos a vivienda (Consell, patronales PIMEEF, sindicatos, GEN-GOB, colectivos ciudadanos). Propuestas públicas semanales: ecotasa, límites de cruceros, moratoria de licencias, regulación de alquiler turístico. | Solapamiento fuerte con vivienda — los mismos titulares cuentan para ambos ejes. | 🟢 Alta |
| **Agua y recursos hídricos** | Crisis estructural permanente en Baleares (acuíferos sobreexplotados, desalación, consumo turístico vs. residente). Actores claros: GOIB, Consell, ABAQUA, agricultores, hoteleros. Propuestas regulares en BOIB. | Estacionalidad acentuada (pico verano), densidad irregular en invierno. | 🟢 Alta |
| **Movilidad y transporte** | Noticias semanales (atascos, carril bus, bici, rent-a-car, aparcamiento, puerto, aeropuerto). Actores múltiples (Consell, ayuntamientos, TIB, Port, AENA, colectivos). Propuestas muy concretas. | Muy disperso — "movilidad" abarca desde bicis hasta puerto. Requiere sub-palancas internas. | 🟢 Alta |

### Tier 2 — encaja con adaptación

| Tema | Por qué encaja | Problema | Viabilidad |
|---|---|---|---|
| **Trabajo de temporada y condiciones laborales** | Fuentes sindicales sólidas (CCOO, UGT), Inspección de Trabajo publica actas, convenios se negocian en prensa. Umbilicalmente ligado a vivienda. | Solapamiento extremo con vivienda — el temporero es el mismo sujeto. Riesgo de canibalizar el foco actual. | 🟡 Media |
| **Medio ambiente y territorio** (posidonia, costa, urbanismo protegido) | Actores bien definidos (GEN-GOB, Amics de la Terra, Consell, Demarcación de Costas). Temas recurrentes. | Las propuestas son menos frecuentes que las denuncias — el modelo documental puede quedarse vacío ciertas semanas. | 🟡 Media |
| **Residuos, limpieza y saneamiento** | Estacional pero muy visible en verano. Actores claros (ayuntamientos, concesionarias, Consell). | Solo 4-5 meses de densidad informativa real. Invierno seco. | 🟡 Media |

### Tier 3 — descartables o diferibles

- **Sanidad (Can Misses, personal que no se aloja)** — el bucle con vivienda es potente, pero las propuestas públicas son pocas y muy técnicas. Mejor tratarlo como *palanca* dentro de vivienda ("sanitarios que abandonan Ibiza por alquiler"), no como eje propio.
- **Educación** — mismo patrón. Palanca, no vertical.
- **Energía** — estructural y lento. El cable submarino con Mallorca no genera noticia semanal. Densidad baja.
- **Patrimonio / cultura / lengua** — demasiado difuso, actores fragmentados. No encaja con el modelo documental.
- **Seguridad y convivencia** — fuentes opacas, mucho ruido, pocas propuestas verificables.
- **Gobernanza y transparencia** — meta-tema que atraviesa todos los demás. No funciona como eje propio; sí como lente transversal ya implícita en el modelo actual.

---

## 3. Tres modelos posibles de expansión

La decisión no es *qué* temas añadir, es **cómo**.

### Modelo A — Verticales independientes

`radar))ibiza_turismo`, `radar))ibiza_agua`, `radar))ibiza_movilidad`... Cada tema es un sitio, un repo, un dominio.

- ✅ Marca clara por tema, SEO limpio y específico.
- ❌ Multiplica coste operativo: pipeline, CI, dominio, revisión semanal y ~2-3 €/mes de API por vertical.
- ❌ Solapamiento forzado: una noticia de alquiler turístico pertenece a vivienda y a turismo → o se duplica o se decide arbitrariamente.
- ❌ Divide la audiencia ganada en vivienda entre N sitios.

### Modelo B — Un solo observatorio con secciones temáticas

`radar))ibiza` con secciones de vivienda, turismo, agua, movilidad.

- ✅ Una sola revisión editorial, un solo dominio, SEO concentrado.
- ✅ Los solapamientos dejan de serlo: una noticia puede llevar 2-3 etiquetas temáticas.
- ✅ La audiencia ganada en vivienda alimenta los otros ejes.
- ❌ Dilución del foco: "radar de la isla" es menos memorable que "radar de vivienda".
- ❌ El nombre actual `radar))ibiza_vivienda` habría que repensarlo a `radar))ibiza` con secciones → rediseño de marca.

### Modelo C — Híbrido: observatorio vertical + palancas transversales

El radar principal sigue siendo vivienda, pero el pipeline añade **palancas temáticas** (turismo, agua, movilidad, trabajo) como tags cruzados en la clasificación. Cada edición semanal menciona cómo las otras palancas afectan a vivienda esa semana.

- ✅ No diluye marca, no duplica infraestructura, enriquece el producto actual.
- ✅ Extensión incremental del pipeline (añadir campos de clasificación, no cambiar la edición).
- ✅ Prueba barata de qué tema da para vertical propio: si una palanca genera mucho tráfico y engagement sostenido, graduarla a vertical (Modelo A) en año 2-3.
- ❌ No es un observatorio "de turismo" con identidad propia; es vivienda con contexto ampliado.

**Lectura:** el Modelo C es con diferencia el más inteligente para el estado actual del proyecto. Los Modelos A y B son rediseños profundos; el C es una extensión incremental del pipeline existente.

---

## 4. Recomendación de orden

**Fase inmediata (ahora mismo):** no tocar nada. Terminar el relanzamiento de vivienda, validar tracción a 90 días con RT23.

**Si Ibiza vivienda da verde en RT23:**

1. **Primer paso — Modelo C aplicado a turismo.** Añadir al pipeline de clasificación palancas transversales nuevas: `afecta_a_turismo` (prioritaria), `afecta_a_agua`, `afecta_a_movilidad`. Coste marginal: ~0,5 €/mes. Cada edición semanal gana contexto. Medir en analítica (GoatCounter + Search Console) si los lectores enganchan con esas palancas.

2. **Segundo paso — graduar turismo a vertical propio.** Solo si la palanca de turismo demuestra demanda real (búsquedas específicas en Search Console, clics sostenidos en la sección, emails del formulario preguntando por turismo). Lanzar `radar))ibiza_turismo` como primera réplica del Modelo A. Sirve además de prueba del concepto de "motor reutilizable" que contempla la sección de escalabilidad provincial — los mismos problemas arquitectónicos (monorepo motor + config por instancia) aparecen.

3. **Tercer paso — agua y movilidad como verticales.** En cola detrás de turismo. Lanzarlas solo si turismo demuestra que el modelo-réplica funciona operativamente.

4. **Trabajo de temporada, medio ambiente, residuos** se quedan como palancas dentro de los verticales existentes. No merecen sitio propio salvo que un actor aliado lo empuje (p. ej. un sindicato que quiera co-editar un radar de trabajo con su nombre).

---

## 5. Tres cosas honestas

1. **No hay prisa.** Ampliar temas sin haber consolidado vivienda es la forma más rápida de matar el proyecto. Un observatorio mediocre de tres temas vale menos que uno bueno de uno.
2. **El cuello de botella real es editorial, no técnico.** El pipeline puede generar 5 ediciones semanales sin despeinarse. El editor (Raúl) no puede revisar 5 lunes. La expansión temática está limitada por tiempo humano, no por API.
3. **Turismo es el único hermano obvio de vivienda.** Los demás son primos. Si solo se abre un eje nuevo, que sea turismo — y probablemente lo correcto es empezar como palanca transversal dentro del radar actual, no como vertical separado.

---

## 6. Interacción con la escalabilidad provincial

Ambas hipótesis (expansión temática + escalabilidad provincial) comparten **la misma condición de activación** (RT23 verde) y **la misma arquitectura técnica** (motor compartido + configuración por instancia). La única diferencia es el eje por el que varía la configuración:

- **Escalabilidad provincial:** `config/valencia.yaml`, `config/mallorca.yaml`... (mismo tema, distinta geografía).
- **Expansión temática:** `config/ibiza_turismo.yaml`, `config/ibiza_agua.yaml`... (misma geografía, distinto tema).

**Orden recomendado:** primera réplica = turismo en Ibiza (expansión temática). Esto valida el motor reutilizable con un tema cuyos actores y fuentes ya conocemos. La escalabilidad provincial llega después, cuando se ha resuelto la ingeniería del motor multi-instancia.

---

## 7. Decisión

**Nada que decidir ahora.** Documento vivo. Revisar cuando RT23 dé verde en la evaluación de 90 días post-relanzamiento.
