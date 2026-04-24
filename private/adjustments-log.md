# Registro de ajustes — prompts, umbrales, modelos, reglas

Registro vivo de cada cambio significativo que afecta cómo opera el pipeline. Complementa `postmortems.md`:

- `postmortems.md` registra errores con coste.
- `adjustments-log.md` registra cambios voluntarios (mejoras, recalibraciones).

Cuando más adelante se proponga "subir rigor a 8" o "cambiar modelo de extract a Sonnet", aquí queda la traza de qué se probó antes, qué datos soportaron la decisión y qué efecto se midió.

**Formato de cada entrada:**

- Fecha.
- Qué se cambió (antes → después).
- Motivo (por qué ahora).
- Datos que lo soportan (enlace a archivo o cifra concreta).
- Efecto esperado (hipótesis).
- Efecto medido (cuando haya datos posteriores).
- Reversible sí/no y cómo.

Entradas más recientes arriba.

---

## 2026-04-20 18:35 · Inicialización del log

- **Qué:** se crea este archivo como registro estructurado de cambios.
- **Motivo:** petición del editor: "toda esta información y proceso debe quedar documentado para futuros ajustes". Sin un log estructurado, las decisiones futuras (p.ej. subir umbral de rigor a 8) no tienen contexto histórico.
- **Reversible:** trivialmente (no hay cambio operativo).

---

## 2026-04-20 18:30 · Mejoras iterativas del prompt de `generate.py` tras self-review rigor=6

- **Qué:** se añadieron 4 reglas al SYSTEM prompt de `generate.py`:
  1. **Deduplicación:** dos propuestas con mismo objetivo + actor_type + horizon se fusionan en una sola con otras fuentes listadas.
  2. **Etiqueta de naturaleza de cifras:** `(dato oficial)` / `(estimación periodística)` / `(orientativa)` la primera vez que aparece una cifra.
  3. **Carry-over explícito:** señales anteriores al lunes de la semana cubierta se marcan con `*(carry-over de la semana ISO XX)*`.
  4. **`blocks_cited` limpio:** solo incluye actor_type de actores que PROPONEN (formal o en_movimiento); no los de señales.
- **Motivo:** self-review de la 1ª iteración de 2026-W17 puntuó rigor=6 y detectó 8 warnings, 3 con causa en el prompt del generador.
- **Datos que lo soportan:** [`private/self-review/2026-w17.md`](private/self-review/2026-w17.md) (versión 1, pre-mejora).
- **Efecto esperado:** rigor sube a ≥7. Warnings sobre duplicación, cifras y carry-over desaparecen.
- **Efecto medido:** 2ª iteración puntuó **rigor=7** (subida de 1 punto), balance=8, cobertura=8, claridad=9, reglas=7. 7 warnings residuales menores (detalles de forma, actor sin apellido, etc.) no bloquean. ✅ Éxito.
- **Reversible:** sí, editando `src/generate.py` SYSTEM y revirtiendo al commit `a2d6ccc`.

---

## 2026-04-20 18:30 · Mejora de `extract.py` para clasificación institucional

- **Qué:** se añadió al SYSTEM prompt de `extract.py` una regla explícita de clasificación: "actores vinculados a Consell, Govern, IBAVI, Ayuntamiento, o con cargos ('conseller', 'regidor', 'director general', etc.) son `institucional_publico`, NO `otro`."
- **Motivo:** self-review detectó que "Marí, del Govern" fue clasificado como `actor_type: otro` en vez de `institucional_publico`. Sin la regla explícita, Haiku no deduce el tipo del contexto.
- **Datos:** warning #2 del self-review v1 2026-w17.
- **Efecto esperado:** actores con cargo institucional se clasifican correctamente.
- **Efecto medido:** en la 2ª iteración, Marí aparece con `actor_type: institucional_publico` en la sección Radar. ✅ Éxito.
- **Reversible:** sí.

---

## 2026-04-20 18:25 · `verify.py` — URL handling más tolerante

- **Qué:** `httpx.Client` con User-Agent Chrome + `Accept` + `Accept-Language`. Distinción `(total, blocking, soft)` en `check_urls`: 401/403/405/429 son soft_warning; 404/410 bloquean; 5xx/excepción son soft_warning.
- **Motivo:** post-mortem 2026-04-20 18:24: Cadena SER devolvía 403 a bots, el verify bloqueaba publicación por falso positivo. Coste: 1,10 €.
- **Datos:** [`private/postmortems.md`](postmortems.md) entrada 18:24.
- **Efecto esperado:** 403 no bloquea publicación; 404 reales siguen bloqueando.
- **Efecto medido:** 2ª iteración tras fix: 13 URLs chequeadas, 0 bloqueantes, 0 avisos (Cadena SER pasa con UA Chrome). ✅ Éxito.
- **Reversible:** sí.

---

## 2026-04-20 17:00 · Subir tope blando de 8 € → 12 €

- **Qué:** `MONTHLY_SOFT_CAP_EUR` pasa de 8.00 a 12.00. Nuevas capas: verde <6 / amarilla 6-9 / naranja 9-12 / roja blanda 12-20 / dura >20.
- **Motivo:** pivote documental añade 3 niveles de autoevaluación (self_review semanal ~0,60 €/mes + quarterly_audit ~1,50 €/mes promediado + model_rebench ~1,00 €/mes). Coste proyectado total ~9,86 €/mes. Con tope blando a 8, se dispararía alerta cada mes sin motivo.
- **Datos:** tabla de coste proyectado en [`ARQUITECTURA.md` sección "Reparto de modelos"](../ARQUITECTURA.md#reparto-de-modelos--decisión-2026-04-20).
- **Efecto esperado:** alertas solo cuando haya desviación real respecto al coste proyectado, no por el ruido de la autoevaluación.
- **Efecto medido:** gasto del primer día tras aplicar: 5,02 € (capa 🟢 verde). El modelo de costes se valida en la primera revisión mensual cuando haya datos de 4 ediciones.
- **Reversible:** sí; volver a 8 € si tras 2 meses el coste real estabilizado queda bajo 7 €/mes sin desviaciones.
- **Revisión prevista:** tras ≥4 ediciones publicadas con dato estable. Sin fecha ([D15](../DECISIONES.md)).

---

## Propuestas en evaluación (sin aplicar todavía)

### Umbral de rigor subir de `<7` a `<8`

- **Propuesta del editor 2026-04-20:** considerar subir umbral del self-review que dispara alerta de `score < 7` a `score < 8`.
- **Decisión:** deferida hasta tener ≥4 ediciones bajo modelo documental.
- **Motivo:** sin datos del rango real observado, subirlo puede disparar alertas permanentes por ruido. Primera iteración dio rigor=7; con más datos veremos si ese 7 es consistente o si sube a 8 de forma natural tras pulir más el prompt.
- **Criterio para aplicarlo:** si en 4 ediciones consecutivas el rigor observado es ≥8, se sube el umbral sin riesgo de ruido. Si el rango real es 7-9, se mantiene <7 o se sube a <8 y se acepta que 1 de cada 3-4 ediciones dispare alerta.
- **Dónde se aplicaría:** `src/self_review.py` función `append_log_if_alert`, condición `v < 7`.
