// Shared React components for Ibiza Housing Radar home variants.
// Requires window.RADAR_DATA and system.css to be loaded.

const D = window.RADAR_DATA;

// tiny atoms
const Chip = ({ type, children }) => (
  <span className={`chip ${type}`}>
    <span className="dot" />
    {children}
  </span>
);

const Pill = ({ state, children }) => (
  <span className={`pill s-${state}`}>{children}</span>
);

const Mini = ({ label, v, cls }) => (
  <span className={`mini ${cls}`}>
    <span className="bar"><i style={{ width: v + "%" }} /></span>
    {label} {v}
  </span>
);

const Src = ({ url }) => <span className="src">{url}</span>;

// proposal card
const ProposalCard = ({ p, compact }) => (
  <article className="propcard" style={compact ? { padding: "10px 0 12px" } : {}}>
    <div className="top">
      <Chip type={p.type}>{p.actor}</Chip>
      <Pill state={p.state}>{p.stateLabel}</Pill>
    </div>
    <h3>{p.title}</h3>
    <div className="meta">
      <span className="mono tnum">{p.horizon}</span>
      <span className="muted">·</span>
      <Mini {...p.legal} />
      <Mini {...p.econ} />
    </div>
    <div className="foot">
      <Src url={p.src} />
      <span className="mono small muted">{p.typeLabel}</span>
    </div>
  </article>
);

// positions table
const POS_PARTIES = [
  { k: "PSIB", label: "PSIB", tone: "party" },
  { k: "PP", label: "PP", tone: "party" },
  { k: "Vox", label: "Vox", tone: "party" },
  { k: "Sumar", label: "Sumar", tone: "party" },
  { k: "Reagr", label: "Reagr.", tone: "party" },
  { k: "PIMEEF", label: "PIMEEF", tone: "patronal" },
  { k: "USO", label: "USO", tone: "sindicato" },
  { k: "Caritas", label: "Cáritas", tone: "ong" },
];
const POS_MARK = { yes: "●", no: "○", amb: "◐", nop: "·" };
const POS_CLS = { yes: "yes", no: "no", amb: "amb", nop: "nop" };

const PositionsTable = ({ rows = D.positions, hide }) => (
  <table className="pos-table">
    <thead>
      <tr>
        <th>Propuesta</th>
        {POS_PARTIES.filter((c) => !hide || !hide.includes(c.k)).map((c) => (
          <th key={c.k} style={{ textAlign: "center", width: 42 }}>{c.label}</th>
        ))}
      </tr>
    </thead>
    <tbody>
      {rows.map((r, i) => (
        <tr key={i}>
          <td style={{ maxWidth: 260 }}>{r.prop}</td>
          {POS_PARTIES.filter((c) => !hide || !hide.includes(c.k)).map((c) => (
            <td key={c.k} className={`pos ${POS_CLS[r[c.k] || "nop"]}`} style={{ textAlign: "center" }}>
              {POS_MARK[r[c.k] || "nop"]}
            </td>
          ))}
        </tr>
      ))}
    </tbody>
  </table>
);

// signal list
const SignalList = ({ items = D.signals, limit = 8 }) => (
  <ol className="signals">
    {items.slice(0, limit).map((s, i) => (
      <li key={i}>
        <span className="n">{String(i + 1).padStart(2, "0")}</span>
        <span>
          {s.text}
          <a className="url" href={"https://" + s.url}>{s.url}</a>
        </span>
      </li>
    ))}
  </ol>
);

// Transparency footer (shared)
const TranspFooter = ({ pad = "0 40px" }) => {
  const t = D.transparency;
  return (
    <footer className="transp">
      <div style={{ padding: pad }}>
        <div className="grid">
          <div>
            <span className="k">Coste API del mes</span>
            <span className="v mono tnum">{t.apiCost}</span>
          </div>
          <div>
            <span className="k">Capa de alerta</span>
            <span className={`v alert ${t.alert}`}><span className="dot" /> {t.alertLabel}</span>
          </div>
          <div>
            <span className="k">Última edición publicada</span>
            <span className="v mono tnum">{t.lastEdit}</span>
          </div>
          <div>
            <span className="k">Estado del pipeline</span>
            <span className="v mono">{t.pipeline}</span>
          </div>
        </div>
        <p className="mono small" style={{ marginTop: 18, color: "var(--ink-3)", maxWidth: 720, lineHeight: 1.5 }}>
          Ibiza Housing Radar es un observatorio documental. No genera propuestas propias.
          5 reglas duras en <a href="#">/politica-editorial/</a>.
          Balance público en <a href="#">/balance/</a>.
        </p>
      </div>
    </footer>
  );
};

// Nav
const Nav = ({ tone = "default" }) => (
  <nav className="nav">
    <span className="logo">IBIZA HOUSING RADAR</span>
    <span className="mono small muted">·</span>
    <a href="#">Ediciones</a>
    <a href="#">Propuestas</a>
    <a href="#">Actores</a>
    <a href="#">Recursos</a>
    <a href="#" className="muted">Más ▾</a>
    <span className="spacer" />
    <button className="sub">Suscribir</button>
  </nav>
);

// Sidenote
const Sidenote = ({ n, children }) => (
  <aside className="sidenote">
    {n && <span className="num">NOTA {String(n).padStart(2, "0")}</span>}
    {children}
  </aside>
);

Object.assign(window, {
  Chip, Pill, Mini, Src, ProposalCard,
  PositionsTable, SignalList, TranspFooter, Nav, Sidenote,
  POS_PARTIES, POS_MARK, POS_CLS,
});
