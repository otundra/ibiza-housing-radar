// App — Single-variant full-bleed home. Chosen config:
// variant C, comfortable, saturated, serif heads, light (dark toggle in header).

const { useState, useEffect } = React;

const CONFIG = {
  density: "comfortable",
  palette: "saturated",
  heads: "serif",
};

function App() {
  const [dark, setDark] = useState(false);

  // Persist dark pref if the user flips it in-header.
  useEffect(() => {
    try {
      const saved = localStorage.getItem("radar-dark");
      if (saved) setDark(saved === "1");
    } catch (e) {}
  }, []);
  useEffect(() => {
    try { localStorage.setItem("radar-dark", dark ? "1" : "0"); } catch (e) {}
  }, [dark]);

  const tw = { ...CONFIG, dark, variant: "C" };
  const setTw = (k, v) => { if (k === "dark") setDark(v); };

  const { VariantC } = window;

  return (
    <div
      data-theme={dark ? "dark" : "light"}
      data-density={CONFIG.density}
      data-palette={CONFIG.palette}
      data-heads={CONFIG.heads}
      style={{ width: "100%", minHeight: "100vh", overflow: "auto", background: "var(--paper)" }}
    >
      <VariantC tw={tw} setTw={setTw} />
    </div>
  );
}

ReactDOM.createRoot(document.getElementById("app")).render(<App />);
