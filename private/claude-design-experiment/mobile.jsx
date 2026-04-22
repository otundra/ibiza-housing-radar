// Mobile artboards (390×900). Each variant gets a mobile condensation.
// Shared mobile nav + hamburger (CSS-only via <details>).

const MobileNav = () => (
  <div style={{ padding: "10px 16px", borderBottom: "1px solid var(--ink)", display: "flex", justifyContent: "space-between", alignItems: "center", background: "var(--paper)" }}>
    <span style={{ fontWeight: 700, letterSpacing: -0.01, fontSize: 14 }}>IBIZA HOUSING RADAR</span>
    <details style={{ position: "relative" }}>
      <summary style={{ listStyle: "none", cursor: "pointer", fontFamily: "var(--ff-mono)", fontSize: 11, padding: "4px 8px", border: "1px solid var(--ink)" }}>MENÚ</summary>
    </details>
  </div>
);

const MobileA = () => {
  const d = window.RADAR_DATA;
  return (
    <div className="radar" data-heads="serif" style={{ width: "100%", height: "100%", overflow: "auto" }}>
      <MobileNav />
      <header style={{ padding: "18px 16px 14px", borderBottom: "1px solid var(--ink)", textAlign: "center" }}>
        <div className="mono small muted" style={{ fontSize: 10, letterSpacing: 0.12, textTransform: "uppercase" }}>Ed. Nº {String(d.edition.number).padStart(3, "0")} · lun 20 abr 2026</div>
        <h1 style={{ fontFamily: "var(--ff-serif)", fontSize: 38, fontWeight: 500, lineHeight: 0.98, marginTop: 8, letterSpacing: -0.02 }}>
          Ibiza Housing<br/>Radar
        </h1>
        <div style={{ fontFamily: "var(--ff-serif)", fontStyle: "italic", fontSize: 14, color: "var(--ink-2)", marginTop: 8 }}>
          Observatorio semanal · Mapeamos lo que se propone.
        </div>
        <div style={{ display: "flex", gap: 6, marginTop: 14, justifyContent: "center", fontFamily: "var(--ff-mono)", fontSize: 10.5 }}>
          <a href="#" style={{ border: "1px solid var(--ink)", padding: "5px 9px", textDecoration: "none", color: "var(--ink)" }}>¿PRIMERA VEZ?</a>
          <a href="#" style={{ border: "1px solid var(--ink)", padding: "5px 9px", textDecoration: "none", color: "var(--paper)", background: "var(--ink)" }}>ÚLTIMA ED. →</a>
        </div>
      </header>
      <section style={{ padding: "14px 16px", borderBottom: "1px solid var(--ink)", background: "var(--paper-2)" }}>
        <div className="mono small muted" style={{ fontSize: 10.5, letterSpacing: 0.1, textTransform: "uppercase" }}>{d.edition.label}</div>
        <div className="row" style={{ marginTop: 6, gap: 18 }}>
          <span><b style={{ fontSize: 18 }}>{d.edition.signals}</b> <span className="small muted">señales</span></span>
          <span><b style={{ fontSize: 18 }}>{d.edition.proposals}</b> <span className="small muted">prop.</span></span>
          <span><b style={{ fontSize: 18 }}>{d.edition.omisiones}</b> <span className="small muted">omis.</span></span>
        </div>
      </section>
      <section style={{ padding: "14px 16px", borderBottom: "1px solid var(--ink)" }}>
        <div className="kicker" style={{ marginBottom: 8 }}>Señales</div>
        <SignalList items={d.signals} limit={4} />
      </section>
      <section style={{ padding: "14px 16px", borderBottom: "1px solid var(--ink)" }}>
        <div className="kicker" style={{ marginBottom: 8 }}>Propuestas</div>
        {d.proposals.slice(0, 3).map((p, i) => <ProposalCard key={i} p={p} />)}
      </section>
      <section style={{ padding: "14px 16px", borderBottom: "1px solid var(--ink)" }}>
        <div className="kicker" style={{ marginBottom: 8 }}>Mapa de posiciones</div>
        <div style={{ overflow: "auto" }}>
          <PositionsTable hide={["Sumar", "Reagr", "Caritas"]} />
        </div>
      </section>
      <section style={{ padding: "14px 16px", borderBottom: "1px solid var(--ink)" }}>
        <div className="kicker" style={{ marginBottom: 8 }}>A vigilar</div>
        <ul className="signals">
          {d.vigilar.slice(0, 3).map((v, i) => (
            <li key={i} style={{ gridTemplateColumns: "auto 1fr" }}>
              <span className="n mono">{v.when}</span>
              <span>{v.text}</span>
            </li>
          ))}
        </ul>
      </section>
      <footer className="transp" style={{ padding: "14px 16px" }}>
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 10, fontFamily: "var(--ff-mono)", fontSize: 11 }}>
          <div><span className="muted small">API/mes</span><div>{d.transparency.apiCost}</div></div>
          <div><span className="muted small">Alerta</span><div>🟡 {d.transparency.alertLabel}</div></div>
          <div><span className="muted small">Última</span><div>{d.transparency.lastEdit}</div></div>
          <div><span className="muted small">Pipeline</span><div>{d.transparency.pipeline}</div></div>
        </div>
        <p className="mono small" style={{ marginTop: 12, color: "var(--ink-3)", fontSize: 10.5 }}>
          Observatorio documental. No propuestas propias.<br/>
          <a href="#">/politica-editorial/</a> · <a href="#">/balance/</a>
        </p>
      </footer>
    </div>
  );
};

const MobileB = () => {
  const d = window.RADAR_DATA;
  return (
    <div className="radar" data-heads="sans" style={{ width: "100%", height: "100%", overflow: "auto" }}>
      <MobileNav />
      <header style={{ padding: "22px 16px 18px", borderBottom: "1px solid var(--ink)", background: "var(--paper-2)" }}>
        <div className="eyebrow">Ed. {d.edition.number} · {d.edition.label}</div>
        <h1 style={{ fontSize: 36, lineHeight: 1, letterSpacing: -0.02, fontWeight: 650, marginTop: 10 }}>Ibiza Housing<br/>Radar<span style={{ color: "var(--ink-3)" }}>.</span></h1>
        <p style={{ marginTop: 10, fontSize: 14, color: "var(--ink-2)", lineHeight: 1.45 }}>Observatorio semanal de vivienda en Ibiza. Mapeamos lo que se propone, no proponemos nosotros.</p>
        <div className="row" style={{ marginTop: 12, gap: 6, flexWrap: "wrap" }}>
          <a href="#" style={{ border: "1px solid var(--ink)", padding: "6px 10px", fontSize: 11.5, textDecoration: "none", color: "var(--ink)", background: "var(--paper)" }}>Cómo usarlo</a>
          <a href="#" style={{ border: "1px solid var(--ink)", padding: "6px 10px", fontSize: 11.5, textDecoration: "none", color: "var(--paper)", background: "var(--ink)" }}>Última edición →</a>
        </div>
      </header>
      <section style={{ display: "grid", gridTemplateColumns: "1fr 1fr", borderBottom: "1px solid var(--ink)" }}>
        {[
          { k: "Señales", v: d.edition.signals },
          { k: "Propuestas", v: d.edition.proposals },
          { k: "Omisiones", v: d.edition.omisiones },
          { k: "Actores", v: 27 },
        ].map((it, i) => (
          <div key={i} style={{ padding: "12px 14px", borderRight: i % 2 === 0 ? "1px solid var(--rule)" : "none", borderTop: i > 1 ? "0.5px solid var(--rule)" : "none" }}>
            <div className="eyebrow">{it.k}</div>
            <div style={{ fontSize: 28, fontWeight: 650, marginTop: 4 }} className="tnum">{it.v}</div>
          </div>
        ))}
      </section>
      <section style={{ padding: "14px 16px", borderBottom: "1px solid var(--ink)" }}>
        <div className="kicker" style={{ marginBottom: 8 }}>§ 01 · Señales</div>
        <SignalList items={d.signals} limit={4} />
      </section>
      <section style={{ padding: "14px 16px", borderBottom: "1px solid var(--ink)" }}>
        <div className="kicker" style={{ marginBottom: 8 }}>§ 03 · Propuestas</div>
        {d.proposals.slice(0, 3).map((p, i) => <ProposalCard key={i} p={p} />)}
      </section>
      <footer className="transp" style={{ padding: "14px 16px" }}>
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 10, fontFamily: "var(--ff-mono)", fontSize: 11 }}>
          <div><span className="muted small">API/mes</span><div>{d.transparency.apiCost}</div></div>
          <div><span className="muted small">Alerta</span><div>🟡 {d.transparency.alertLabel}</div></div>
          <div><span className="muted small">Última</span><div>{d.transparency.lastEdit}</div></div>
          <div><span className="muted small">Pipeline</span><div>{d.transparency.pipeline}</div></div>
        </div>
      </footer>
    </div>
  );
};

const MobileC = () => {
  const d = window.RADAR_DATA;
  return (
    <div className="radar" data-heads="sans" style={{ width: "100%", height: "100%", overflow: "auto", fontFamily: "var(--ff-mono)" }}>
      <div style={{ background: "var(--ink)", color: "var(--paper)", padding: "6px 14px", fontSize: 10.5, letterSpacing: 0.05 }}>
        <span>● PIPELINE.OK</span> · API <b>{d.transparency.apiCost}</b> · ALRT 2/4
      </div>
      <header style={{ padding: "16px 16px 12px", borderBottom: "2px solid var(--ink)" }}>
        <div className="small muted" style={{ fontSize: 10.5 }}>/home/ibiza-housing-radar/ · ed_{String(d.edition.number).padStart(3, "0")}.md</div>
        <h1 style={{ fontSize: 26, fontWeight: 600, marginTop: 10, fontFamily: "var(--ff-mono)" }}>
          ibiza_housing_radar <span className="muted">v.17</span>
        </h1>
        <p style={{ fontSize: 13, color: "var(--ink-2)", marginTop: 10, lineHeight: 1.5 }}>
          // Observatorio semanal de vivienda.<br/>
          // No proponemos. Mapeamos.
        </p>
      </header>
      <section style={{ padding: "12px 16px", borderBottom: "1px solid var(--ink)", background: "var(--paper-2)" }}>
        <div style={{ display: "flex", gap: 16, fontSize: 12 }}>
          <span>S-{d.edition.week}</span>
          <span><b>{d.edition.signals}</b> sig.</span>
          <span><b>{d.edition.proposals}</b> prop.</span>
          <span><b>{d.edition.omisiones}</b> omis.</span>
        </div>
      </section>
      <section style={{ padding: "12px 16px", borderBottom: "1px solid var(--ink)" }}>
        <div className="small muted" style={{ marginBottom: 8 }}>## signals.md</div>
        {d.signals.slice(0, 5).map((s, i) => (
          <div key={i} style={{ padding: "6px 0", borderTop: i > 0 ? "0.5px dashed var(--rule)" : "0", fontSize: 12, lineHeight: 1.5 }}>
            <span className="muted">{String(i + 1).padStart(3, "0")} · {s.actor}</span><br/>
            {s.text}<br/>
            <a href="#" className="muted" style={{ fontSize: 10.5 }}>↗ {s.url}</a>
          </div>
        ))}
      </section>
      <section style={{ padding: "12px 16px", borderBottom: "1px solid var(--ink)" }}>
        <div className="small muted" style={{ marginBottom: 8 }}>## proposals.json</div>
        {d.proposals.slice(0, 3).map((p, i) => <ProposalCard key={i} p={p} compact />)}
      </section>
      <footer style={{ padding: "12px 16px", background: "var(--paper-2)", borderTop: "1px solid var(--ink)", fontSize: 11 }}>
        <div>API_MTD = {d.transparency.apiCost} · ALERT = yellow</div>
        <div>LAST = {d.transparency.lastEdit}</div>
        <div>PIPE = {d.transparency.pipeline}</div>
      </footer>
    </div>
  );
};

const MobileD = () => {
  const d = window.RADAR_DATA;
  return (
    <div className="radar" data-heads="serif" style={{ width: "100%", height: "100%", overflow: "auto", fontFamily: "var(--ff-serif)" }}>
      <MobileNav />
      <header style={{ padding: "28px 20px 22px" }}>
        <div className="eyebrow">{d.edition.label}</div>
        <h1 style={{ fontSize: 42, fontWeight: 400, lineHeight: 1, letterSpacing: -0.02, marginTop: 14, fontFamily: "var(--ff-serif)" }}>
          <span style={{ fontStyle: "italic" }}>Ibiza</span><br/>Housing Radar
        </h1>
        <p style={{ fontSize: 16, marginTop: 16, lineHeight: 1.4, color: "var(--ink-2)", fontFamily: "var(--ff-serif)" }}>
          Observatorio semanal de vivienda en Ibiza. Mapeamos lo que se propone,
          <em style={{ color: "var(--ink)" }}> no proponemos nosotros</em>.
        </p>
      </header>
      <hr className="rule" style={{ margin: "0 20px" }} />
      <section style={{ padding: "20px" }}>
        <div className="row" style={{ gap: 24 }}>
          {[
            { k: "señales", v: d.edition.signals },
            { k: "propuestas", v: d.edition.proposals },
            { k: "omisiones", v: d.edition.omisiones },
          ].map((it) => (
            <div key={it.k}>
              <div style={{ fontSize: 28, fontFamily: "var(--ff-serif)", lineHeight: 1 }} className="tnum">{it.v}</div>
              <div className="small muted" style={{ marginTop: 4, fontSize: 11 }}>{it.k}</div>
            </div>
          ))}
        </div>
      </section>
      <hr className="rule" style={{ margin: "0 20px" }} />
      <section style={{ padding: "20px" }}>
        <div className="kicker" style={{ marginBottom: 10, fontFamily: "var(--ff-sans)" }}>I · Señales</div>
        <SignalList items={d.signals} limit={4} />
      </section>
      <hr className="rule" style={{ margin: "0 20px" }} />
      <section style={{ padding: "20px" }}>
        <div className="kicker" style={{ marginBottom: 10, fontFamily: "var(--ff-sans)" }}>III · Propuestas</div>
        {d.proposals.slice(0, 2).map((p, i) => <ProposalCard key={i} p={p} />)}
      </section>
      <footer className="transp" style={{ padding: "16px 20px" }}>
        <div style={{ fontFamily: "var(--ff-mono)", fontSize: 11, color: "var(--ink-2)" }}>
          <div>Coste API/mes · <b>{d.transparency.apiCost}</b></div>
          <div>🟡 {d.transparency.alertLabel} · última {d.transparency.lastEdit}</div>
          <div>Pipeline · {d.transparency.pipeline}</div>
        </div>
      </footer>
    </div>
  );
};

window.MobileA = MobileA;
window.MobileB = MobileB;
window.MobileC = MobileC;
window.MobileD = MobileD;
