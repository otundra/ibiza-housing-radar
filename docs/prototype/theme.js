// Toggle de tema manual + Escríbenos flotante.
// Sin frameworks. Ejecuta antes del primer paint la parte de tema para evitar FOUC.

(function () {
  var saved = null;
  try { saved = localStorage.getItem('rvi-theme'); } catch (e) {}
  if (saved === 'light' || saved === 'dark') {
    document.documentElement.setAttribute('data-theme', saved);
  }
})();

document.addEventListener('DOMContentLoaded', function () {
  var root = document.documentElement;

  function syncPressed() {
    var t = root.getAttribute('data-theme');
    var btnLight = document.querySelector('[data-theme-set="light"]');
    var btnDark  = document.querySelector('[data-theme-set="dark"]');
    if (btnLight) btnLight.setAttribute('aria-pressed', String(t === 'light'));
    if (btnDark)  btnDark.setAttribute('aria-pressed',  String(t === 'dark'));
  }

  document.querySelectorAll('[data-theme-set]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var mode = btn.getAttribute('data-theme-set');
      root.setAttribute('data-theme', mode);
      try { localStorage.setItem('rvi-theme', mode); } catch (e) {}
      syncPressed();
    });
  });
  syncPressed();

  // Flotante Escríbenos
  var fab   = document.getElementById('fab-toggle');
  var panel = document.getElementById('fab-panel');
  var close = document.getElementById('fab-close');
  if (fab && panel) {
    fab.addEventListener('click', function () {
      var open = panel.classList.toggle('open');
      fab.setAttribute('aria-expanded', String(open));
      if (open) {
        var first = panel.querySelector('textarea');
        if (first) first.focus();
      }
    });
  }
  if (close && panel) {
    close.addEventListener('click', function () {
      panel.classList.remove('open');
      if (fab) { fab.setAttribute('aria-expanded', 'false'); fab.focus(); }
    });
  }
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && panel && panel.classList.contains('open')) {
      panel.classList.remove('open');
      if (fab) { fab.setAttribute('aria-expanded', 'false'); fab.focus(); }
    }
  });

  // Auto-captura URL origen
  var ref = document.querySelector('input[name="page_url"]');
  if (ref) ref.value = window.location.href;

  // Scroll-spy sidebar (ficha actor)
  var links = document.querySelectorAll('.actor-sidebar a[href^="#"]');
  if (links.length && 'IntersectionObserver' in window) {
    var sections = Array.prototype.map.call(links, function (l) {
      return document.querySelector(l.getAttribute('href'));
    }).filter(Boolean);
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        links.forEach(function (l) { l.classList.remove('active'); });
        var active = document.querySelector('.actor-sidebar a[href="#' + e.target.id + '"]');
        if (active) active.classList.add('active');
      });
    }, { rootMargin: '-30% 0px -60% 0px' });
    sections.forEach(function (s) { io.observe(s); });
  }
});
