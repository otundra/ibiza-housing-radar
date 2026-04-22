// Variant B — Sumario / TOC-style hero
// Hero is an INDEX of this week's edition: numbered items you can scan
// and jump to. Sans titles, more dashboardy but still editorial.

const VariantB = () => {
  const d = window.RADAR_DATA;
  return (
    <div className="radar" data-heads="sans" style={{ width: "100%", height: "100%", overflow: "hidden" }}>
      {/* NAV */}
      <div style={{ padding: "0 48px", borderBottom: "1px solid var(--ink)" }}>
        <Nav />
      </div>

      {/* HERO — TOC */}
      <section style={{ padding: "28px 48px 26px", borderBottom: "1px solid var(--ink)", background: "var(--paper-2)" }}>
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1.2fr", gap: 48, alignItems: "end" }}>
          <div>
            <div className="eyebrow" style={{ marginBottom: 10 }}>Edición nº {d.edition.number} · {d.edition.label}</div>
            <h1 style={{ fontSize: 56, lineHeight: 1.02, letterSpacing: -0.02, fontWeight: 650 }}>
              Ibiza Housing<br/>Radar<span style={{ color: "var(--ink-3)" }}>.</span>
            </h1>
            <p style={{ marginTop: 16, fontSize: 17, color: "var(--ink-2)", maxWidth: 420, lineHeight: 1.5 }}>
              Observatorio semanal de vivienda en Ibiza.
              Mapeamos lo que se propone, no proponemos nosotros.
            </p>
            <div className="row" style={{ marginTop: 18, gap: 10 }}>
              <a href="#" style={{ border: "1px solid var(--ink)", padding: "8px 14px", fontSize: 13, textDecoration: "none", color: "var(--ink)", background: "var(--paper)" }}>¿Primera vez? → Cómo usarlo</a>
              <a href="#" style={{ border: "1px solid var(--ink)", padding: "8px 14px", fontSize: 13, textDecoration: "none", color: "var(--paper)", background: "var(--ink)" }}>Última edición →</a>
            </div>
          </div>
          <div>
            <div className="kicker" style={{ marginBottom: 12 }}>Sumario de la edición</div>
            <ol style={{ listStyle: "none", padding: 0, margin: 0, borderTop: "1px solid var(--ink)" }}>
              {[
                { n: "01", t: "Señales de la semana", meta: "08 ítems" },
                { n: "02", t: "Mapa de posiciones", meta: "5 × 8 actores" },
                { n: "03", t: "Propuestas activas", meta: `${d.edition.proposals} cards` },
                { n: "04", t: "Rescate · Omisiones · A vigilar", meta: "2 · 4 · 4" },
                { n: "05", t: "Archivo", meta: "últimas 4 ediciones" },
              ].map((r) => (
                <li key={r.n} style={{ display: "grid", gridTemplateColumns: "auto 1fr auto auto", gap: 16, padding: "10px 0", borderBottom: "0.5px solid var(--rule-soft)", fontSize: 14.5, alignItems: "baseline" }}>
                  <span className="mono" style={{ color: "var(--ink-3)" }}>§ {r.n}</span>
                  <span style={{ fontWeight: 500 }}>{r.t}</span>
                  <span className="mono small muted">{r.meta}</span>
                  <span className="mono small muted">↓</span>
                </li>
              ))}
            </ol>
          </div>
        </div>
      </section>

      {/* KPIS STRIP */}
      <section style={{ padding: "0", borderBottom: "1px solid var(--ink)" }}>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)" }}>
          {[
            { k: "Señales", v: d.edition.signals, sub: "+4 vs. S-15" },
            { k: "Propuestas activas", v: d.edition.proposals, sub: "1 nueva · 0 descartada" },
            { k: "Omisiones", v: d.edition.omisiones, sub: "de relevancia editorial" },
            { k: "Actores mapeados", v: 27, sub: "en 8 categorías" },
          ].map((it, i) => (
            <div key={i} style={{ padding: "18px 24px", borderRight: i < 3 ? "1px solid var(--rule)" : "none" }}>
              <div className="eyebrow">{it.k}</div>
              <div style={{ fontSize: 40, fontWeight: 650, lineHeight: 1, marginTop: 8, letterSpacing: -0.02 }} className="tnum">{it.v}</div>
              <div className="mono small muted" style={{ marginTop: 6 }}>{it.sub}</div>
            </div>
          ))}
        </div>
      </section>

      {/* 2 cols: signals + positions */}
      <section style={{ padding: "24px 48px", borderBottom: "1px solid var(--ink)" }}>
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 40 }}>
          <div>
            <div className="row between" style={{ marginBottom: 10 }}>
              <div className="kicker">§ 01 · Señales</div>
              <span className="mono small muted">8 de 23 · ver todas →</span>
            </div>
            <SignalList items={d.signals} limit={7} />
          </div>
          <div>
            <div className="row between" style={{ marginBottom: 10 }}>
              <div className="kicker">§ 02 · Mapa de posiciones</div>
              <span className="mono small muted">ampliar →</span>
            </div>
            <PositionsTable />
            <div className="mono small muted" style={{ marginTop: 10 }}>
              ● apoya · ○ rechaza · ◐ ambiguo · · sin pronunciamiento. Partidos siempre en gris.
            </div>
          </div>
        </div>
      </section>

      {/* Proposals */}
      <section style={{ padding: "24px 48px", borderBottom: "1px solid var(--ink)" }}>
        <div className="row between" style={{ marginBottom: 14 }}>
          <div className="kicker">§ 03 · Propuestas activas</div>
          <span className="mono small muted">mostrando 4 de {d.edition.proposals}</span>
        </div>
        <div className="grid-4">
          {d.proposals.slice(0, 4).map((p, i) => <ProposalCard key={i} p={p} />)}
        </div>
      </section>

      {/* Rescate · Omisiones · Vigilar */}
      <section style={{ padding: "22px 48px", borderBottom: "1px solid var(--ink)" }}>
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 32 }}>
          <div>
            <div className="kicker" style={{ marginBottom: 8 }}>§ 04a · Rescate</div>
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
            <div className="kicker" style={{ marginBottom: 8 }}>§ 04b · Omisiones</div>
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
            <div className="kicker" style={{ marginBottom: 8 }}>§ 04c · A vigilar</div>
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

      {/* Archive */}
      <section style={{ padding: "18px 48px 24px" }}>
        <div className="kicker" style={{ marginBottom: 10 }}>§ 05 · Archivo</div>
        <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 14 }}>
          <tbody>
            {d.archive.map((a, i) => (
              <tr key={i} style={{ borderTop: "0.5px solid var(--rule-soft)" }}>
                <td className="mono" style={{ padding: "8px 0", color: "var(--ink-3)", width: 40 }}>Nº {a.n}</td>
                <td className="mono" style={{ padding: "8px 14px", color: "var(--ink-3)", width: 210 }}>{a.label}</td>
                <td style={{ padding: "8px 0" }}>{a.headline}</td>
                <td className="mono small muted" style={{ padding: "8px 0", width: 130, textAlign: "right" }}>{a.signals} s · {a.proposals} p</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>

      <TranspFooter pad="0 48px" />
    </div>
  );
};

window.VariantB = VariantB;
