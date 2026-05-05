# Tablero interno — monitorización del proyecto

*Archivo privado. No se publica en la web. Última actualización: 2026-05-05 19:56 UTC.*

Agrega las señales que otros módulos ya producen: gasto del mes, autoevaluación, verificación, decisiones con revisión pendiente, última edición. No genera datos propios. Ver decisión D14.

## Costes del mes

- **Gasto actual:** 0.60 € (blando 12 € / duro 50 €) — 🟢 Verde (<6 €) — silencio
- **Dashboard detallado:** [`costs.md`](costs.md)

## Decisiones con revisión pendiente

_Ninguna decisión vencida ni próxima. Siguiente revisión: **Ritual de aprendizaje semanal + temperature=0 en self-review** (D17) el 2026-06-08._

### 📆 Futuras (informativo)

- Ritual de aprendizaje semanal + temperature=0 en self-review (D17) — 2026-06-08

## Última edición publicada

- `2026-w19`

## Histórico de propuestas

- **Total acumulado:** 6

## Verificación (última ejecución)

- **Resultado:** ✅ sin fallos bloqueantes
- **URLs comprobadas:** 13, caídas: 0
- **Actores comprobados:** 2, no trazables: 0
- **Avisos blandos:** 0

## Autoevaluación (último corte)

## 2026-W19 · 2026-05-04 07:50 UTC
- Scores bajos: rigor=5, balance=6
- Detalle: [2026-w19.md](private/self-review/2026-w19.md)

## Salud sistémica (termómetro de complejidad)

Termómetro orientativo para detectar pozo de modificación infinita. Disparador de auditoría sistémica (D24) cuando los conteos crezcan más rápido que la utilidad real.

- **Reglas duras adicionales en el prompt del generador:** 17
- **Dimensiones del revisor (self-review):** 6
- **Decisiones vigentes en `DECISIONES.md`:** 21
- **Candidatas a retirar:** ninguna detectada con la heurística actual (ventana 4 ediciones).

---

Fuente de datos: `DECISIONES.md`, `data/costs.csv` (vía `src.costs`), `data/verification_report.json`, `data/proposals_history.json`, `private/self-review-log.md`, `docs/_editions/`. Regenerado por `src.panel`.
