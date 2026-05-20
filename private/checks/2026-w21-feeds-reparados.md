# Verificación post-fix: ¿qué entra orgánico en W21 tras reparar los feeds del Diario y Periódico?

**Pendiente para:** lunes 18 may 2026 tras el cron W21 (05:00 UTC).
**Contexto:** [DIARIO 2026-05-12](../../DIARIO.md), [D44](../../DECISIONES.md).

## Por qué este check

Los feeds `Diario de Ibiza · Pitiusas` y `Periódico de Ibiza · Ibiza` llevaban caídos al menos desde el 4 may (probablemente desde W17 o antes — el `feed_health.json` no tiene registro previo y `data/archive/2026-W17/ingested.json` ya no contenía entradas de esos dos medios). Las URLs antiguas se actualizaron el 2026-05-12 a las nuevas (commit `545ab0c`).

Decisión del editor el 2026-05-12: **no forzar nada con `rescue.py`**. Dejar que el cron natural del lunes corra con los feeds reparados y comprobar si los candidatos relevantes entran solos. Si entran, sistema bien calibrado. Si no entran, señal útil para `APRENDIZAJES.md`.

## Candidatos relevantes detectados (cruzando feed actual vs lo ya citado en W17-W20)

### 🔴 Candidatos fuertes (propuesta documentable probable)

- [x] ✅ **"Los ayuntamientos de Ibiza controlarán las caravanas que estén fuera de los campings"**
  Periódico, 11 may.
  `https://www.periodicodeibiza.es/pitiusas/ibiza/2026/05/11/2627317/consell-ibiza-ayuntamientos-refuerzan-control-sobre-au`
  Actor con nombre (Consell + ayuntamientos). Tema central: asentamientos.
  **Resultado:** entró en la edición W21.

- [x] ❌ **"La Comandancia de la Guardia Civil apenas dispone de 500 viviendas en Baleares para alojar"**
  Periódico, 10 may.
  `https://www.periodicodeibiza.es/pitiusas/ibiza/2026/05/10/2626285/comandancia-guardia-civil-apenas-dispone-500-viviendas`
  Datos institucionales sobre vivienda de la GC. Complementa el del 10 may sobre 10 días para encontrar piso que sí entró en W20.
  **Resultado:** no entró. URL ausente de la edición W21 y de cualquier archivo bajo `data/` (ni `proposals_history.json` ni archive). Causa raíz no determinable porque `data/archive/2026-W21/` no existe (ver nota operativa abajo).

- [x] ❌ **"Alquileres en Ibiza: el infierno de algunos propietarios para recuperar sus pisos"**
  Periódico, 11 may.
  `https://www.periodicodeibiza.es/pitiusas/ibiza/2026/05/11/2626743/alquileres-ibiza-infierno-algunos-propietarios-para-re`
  Reportaje de fondo, probable que tenga voces concretas.
  **Resultado:** no entró. URL ausente de la edición y de `data/`. Encaja con el patrón "bloque ausente: propietarios e inmobiliario privado" detectado por el auditor de la W21 — esta URL habría sido la pieza con voz de propietarios.

### 🟡 Candidatos medios (datos sectoriales, sin propuesta clara)

- [x] ❌ **"Casi el 90 % de los hoteles de Ibiza mantendrá su plantilla esta temporada"**
  Periódico, 11 may.
  `https://www.periodicodeibiza.es/pitiusas/ibiza/2026/05/11/2627467/sector-hotelero-ibiza-formentera-preve-temporada-estab`
  **Resultado:** no entró. Esperable como 🟡: sin propuesta concreta, probable que el clasificador lo marcase `has_explicit_proposal=false`. No es fallo del sistema.

- [x] ❌ **"Hoteles de Ibiza prevén una ocupación del 80 % en mayo y cercana al 90 % en verano"**
  Periódico, 12 may.
  `https://www.periodicodeibiza.es/pitiusas/ibiza/2026/05/12/2627505/hoteles-ibiza-preven-ocupacion-del-mayo-cercana-verano`
  **Resultado:** no entró. Mismo análisis: tema sectorial sin propuesta, comportamiento esperado para un 🟡.

- [x] ❌ **"José Luis Benítez (Ocio de Ibiza): La temporada será similar a la de 2025"**
  Diario, 5 may. *(Probablemente fuera de la ventana de 10 días del cron del 18 may.)*
  `https://www.diariodeibiza.es/ibiza/2026/05/05/jose-luis-benitez-gerente-asociacion-temporada-129827686.html`
  **Resultado:** no entró. Confirmado fuera de ventana (5 may queda a 13 días del cron del 18 may, ventana de 10 días). Comportamiento esperado.

### ⚫ Ruido esperado (no debería entrar; si entra es señal de problema en classify)

Tributo bomberos, sanciones almacén Formentera, taxis carga/descarga, residuos Giref, distinciones Family Moments, pasajeros bus, explosión gas Govern/constructora, camping Es Cana cierra, consejos estafa alquiler, perfil víctima estafa.

## Qué hacer el lunes tras el cron W21

1. Leer `docs/_editions/2026-w21.md` cuando se publique.
2. Para cada candidato 🔴 y 🟡, marcar la casilla `[ ]` con resultado:
   - `[x] ✅ entró` si la URL aparece citada en la edición.
   - `[x] ❌ no entró` si no aparece.
   - `[x] ⚠ apareció en cuarentena` (si el sistema lo dejó en `data/quarantine.json` sin publicar).
3. Para cada `❌ no entró`, intentar localizar el porqué en `data/archive/2026-W21/`:
   - ¿Entró a `ingested.json`? Si no, no pasó el filtro de palabras clave o no estaba en ventana.
   - ¿Entró a `classified.json` pero con `has_explicit_proposal=false`? Falso negativo del clasificador → posible ajuste de prompt.
   - ¿Entró a `extracted.json` pero el auditor lo tumbó? Mirar puntuación de auditor.
4. Promover hallazgos relevantes a [`APRENDIZAJES.md`](../../APRENDIZAJES.md) si el patrón aparece en ≥2 ediciones consecutivas (regla del ritual de aprendizaje semanal, [D17](../../DECISIONES.md)).
5. Si todo entró 🔴 + algún 🟡 sin promoverse, sistema bien calibrado tras el fix. Cerrar este check moviéndolo a `private/checks/_resueltos/`.

## No olvidar

- El cron W21 mira ventana de 10 días = ~8-18 may. **Los del 5-6 may ya estarán fuera** — no es fallo del sistema si no entran.
- El feed del Diario solo guarda 10 entradas en su histórico RSS. Material de hace >2 semanas ya no es recuperable vía RSS aunque el feed funcione.
- Si el monitor diario de feeds (D44) dispara aviso entre hoy y el lunes, atender primero.

## Conclusión (rellenada el 2026-05-20)

- **Cobertura real:** 1 de 3 candidatos 🔴 entró (caravanas Consell). Los dos 🔴 ausentes son la pieza de la GC (datos institucionales de vivienda) y el reportaje de propietarios.
- **Diagnóstico parcial:** la URL del reportaje de propietarios encaja exactamente con el patrón **"bloque ausente: voz de propietarios / inmobiliario privado"** que el auditor de la W21 marcó por separado. Que esa URL existiera en el feed reparado y no entrase al pipeline refuerza la señal: no es solo que falte la voz, es que el clasificador o el extractor están dejándola fuera incluso cuando hay material. Si en W22 (cron del 2026-05-25) sigue sin entrar voz de propietarios pese a haber material disponible, asciende a sugerencia con propuesta concreta en [`APRENDIZAJES.md`](../../APRENDIZAJES.md) (segunda aparición consecutiva → criterio D17).
- **Decisión sobre cerrar el check:** **NO se mueve a `_resueltos/`** porque dos 🔴 no entraron y la causa raíz no es plenamente verificable (ver nota operativa abajo). Queda abierto en seguimiento. Se cierra al revisar W22 si el patrón no se repite.

## Nota operativa colateral

- **El archive append-only de W21 no se guardó.** `data/archive/` solo contiene `2026-W17/`. Las W18-W21 no tienen carpeta de archive. Sin archive, este check no puede determinar para cada ❌ si la URL fue filtrada por palabras clave en `ingest.py`, marcada `has_explicit_proposal=false` por `classify.py`, o tumbada por el auditor en `extract.py`. La función `src/archive.py` está en el código pero la integración con `report.py` puede estar rota desde W18 (o nunca llegó a ejecutarse fuera de W17). Apuntar como deuda técnica a investigar en sesión específica — no entra en el alcance de este check.
