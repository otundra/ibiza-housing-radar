// Variant A — Masthead editorial (classic newspaper)
// Heavy masthead, edition number, all-caps small meta, serif headlines,
// dense 4-col proposal grid, tight rules.

const VariantA = () => {
  const d = window.RADAR_DATA;
  return (
    <div className="radar" data-heads="serif" style={{ width: "100%", height: "100%", overflow: "hidden" }}>
      {/* MASTHEAD */}
      <header style={{ padding: "20px 56px 0" }}>
        <div className="row between" style={{ fontSize: 11, letterSpacing: 0.14, textTransform: "uppercase", color: "var(--ink-3)", fontFamily: "var(--ff-mono)" }}>
          <span>Eivissa · Illes Balears · ES</span>
          <span>EDICIÓ Nº {String(d.edition.number).padStart(3, "0")} · LUN 20 ABR 2026</span>
          <span>Any I · Obs. Vivenda</span>
        </div>
        <hr className="rule-thin" style={{ margin: "8px 0 6px" }} />
        <h1 style={{
          fontSize: 78, lineHeight: 0.95, letterSpacing: -0.025,
          fontFamily: "var(--ff-serif)", fontWeight: 500,
          textAlign: "center", padding: "14px 0 8px",
        }}>
          Ibiza Housing Radar
        </h1>
        <div style={{ textAlign: "center", fontStyle: "italic", color: "var(--ink-2)", fontFamily: "var(--ff-serif)", fontSize: 18, marginBottom: 10 }}>
          Observatori setmanal de la crisi de l'habitatge a Eivissa · mapem el que es proposa, no proposem nosaltres
        </div>
        <hr className="rule-double" style={{ margin: "10px 0" }} />
        <div className="row between" style={{ fontSize: 12, color: "var(--ink-2)", fontFamily: "var(--ff-mono)", padding: "4px 0 10px" }}>
          <span>Ediciones · Propuestas · Actores · Recursos · Balance · Política editorial</span>
          <span><a href="#" style={{ color: "var(--ink)" }}>Suscribirse (0 €)</a></span>
        </div>
        <hr className="rule" />
      </header>

      {/* HERO STRAP — week summary */}
      <section style={{ padding: "18px 56px 14px", borderBottom: "1px solid var(--ink)" }}>
        <div className="row between">
          <div>
            <span className="eyebrow">Esta semana</span>
            <div style={{ fontFamily: "var(--ff-serif)", fontSize: 28, fontWeight: 500, lineHeight: 1.1, marginTop: 4, maxWidth: 820 }}>
              El Govern retrasa seis meses el decreto de tope al alquiler.
              <span style={{ color: "var(--ink-3)" }}> La patronal reabre el debate del suelo rústico. Los temporeros, sin casa a tres semanas del inicio.</span>
            </div>
          </div>
          <div className="mono tnum" style={{ textAlign: "right", borderLeft: "1px solid var(--rule)", paddingLeft: 20, minWidth: 160 }}>
            <div style={{ fontSize: 11, color: "var(--ink-3)", letterSpacing: 0.1, textTransform: "uppercase" }}>{d.edition.label}</div>
            <div style={{ fontSize: 14, marginTop: 8, lineHeight: 1.6 }}>
              <div><b>{d.edition.signals}</b> <span className="muted">señales</span></div>
              <div><b>{d.edition.proposals}</b> <span className="muted">propuestas</span></div>
              <div><b>{d.edition.omisiones}</b> <span className="muted">omisiones</span></div>
            </div>
          </div>
        </div>
        <div className="row" style={{ marginTop: 14, gap: 10, fontFamily: "var(--ff-mono)", fontSize: 11.5 }}>
          <a href="#" style={{ border: "1px solid var(--ink)", padding: "5px 12px", color: "var(--ink)", textDecoration: "none" }}>¿PRIMERA VEZ? → CÓMO USARLO</a>
          <a href="#" style={{ border: "1px solid var(--ink)", padding: "5px 12px", color: "var(--paper)", background: "var(--ink)", textDecoration: "none" }}>ÚLTIMA EDICIÓN →</a>
        </div>
      </section>

      {/* PANEL EDITORIAL — 2 cols */}
      <section style={{ padding: "22px 56px", borderBottom: "1px solid var(--ink)" }}>
        <div style={{ display: "grid", gridTemplateColumns: "1.1fr 0.9fr", gap: 40 }}>
          <div>
            <div className="kicker" style={{ marginBottom: 8 }}>A · Señales de la semana</div>
            <SignalList items={d.signals} limit={7} />
          </div>
          <div>
            <div className="kicker" style={{ marginBottom: 8 }}>B · Mapa de posiciones</div>
            <PositionsTable />
            <div className="mono small muted" style={{ marginTop: 10 }}>
              ● apoya · ○ rechaza · ◐ ambiguo · · sin pronunciamiento
            </div>
          </div>
        </div>
      </section>

      {/* PROPOSALS GRID — 4 col */}
      <section style={{ padding: "22px 56px 8px" }}>
        <div className="row between" style={{ marginBottom: 10 }}>
          <div className="kicker">C · Propuestas activas</div>
          <a href="#" className="mono small">Ver todas (11) →</a>
        </div>
        <div className="grid-4">
          {d.proposals.slice(0, 4).map((p, i) => <ProposalCard key={i} p={p} />)}
        </div>
      </section>

      {/* RESCATE · OMISIONES · VIGILAR */}
      <section style={{ padding: "14px 56px 22px", borderTop: "1px solid var(--ink)", marginTop: 18 }}>
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 32 }}>
          <div>
            <div className="kicker" style={{ marginBottom: 8 }}>Rescate del archivo</div>
            <ul className="signals">
              {d.rescate.map((r, i) => (
                <li key={i} style={{ gridTemplateColumns: "auto 1fr" }}>
                  <span className="n mono">{r.year}</span>
                  <span>{r.text}</span>
                </li>
              ))}
            </ul>
          </div>
          <div>
            <div className="kicker" style={{ marginBottom: 8 }}>Omisiones detectadas</div>
            <ul className="signals">
              {d.omisiones.map((o, i) => (
                <li key={i} style={{ gridTemplateColumns: "28px 1fr" }}>
                  <span className="n mono">—</span>
                  <span>{o}</span>
                </li>
              ))}
            </ul>
          </div>
          <div>
            <div className="kicker" style={{ marginBottom: 8 }}>A vigilar</div>
            <ul className="signals">
              {d.vigilar.map((v, i) => (
                <li key={i} style={{ gridTemplateColumns: "auto 1fr" }}>
                  <span className="n mono">{v.when}</span>
                  <span>{v.text}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </section>

      {/* ARCHIVE */}
      <section style={{ padding: "14px 56px 20px", borderTop: "1px solid var(--ink)" }}>
        <div className="kicker" style={{ marginBottom: 8 }}>Archivo · últimas ediciones</div>
        <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 13.5 }}>
          <tbody>
            {d.archive.map((a, i) => (
              <tr key={i} style={{ borderTop: "0.5px solid var(--rule-soft)" }}>
                <td className="mono" style={{ padding: "7px 0", color: "var(--ink-3)", width: 40 }}>Nº {a.n}</td>
                <td className="mono" style={{ padding: "7px 12px", color: "var(--ink-3)", width: 200 }}>{a.label}</td>
                <td style={{ padding: "7px 0", fontFamily: "var(--ff-serif)", fontStyle: "italic" }}>{a.headline}</td>
                <td className="mono small muted" style={{ padding: "7px 0", width: 120, textAlign: "right" }}>{a.signals} s · {a.proposals} p</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>

      <TranspFooter pad="0 56px" />
    </div>
  );
};

window.VariantA = VariantA;
