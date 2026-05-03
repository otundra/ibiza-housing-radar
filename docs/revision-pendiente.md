---
layout: page
title: Revisión pendiente
permalink: /revision-pendiente/
---

Propuestas detectadas por el sistema que no superan los controles mínimos para entrar en la edición semanal. Esperamos segunda fuente, corrección aceptada o archivo a los 60 días si nada cambia.

Si conoces el caso de alguna de las propuestas listadas y puedes aportar una segunda fuente o una corrección, [escríbenos](/correcciones/).

---

{% assign activas = site.data.quarantine.activas %}
{% assign resueltas = site.data.quarantine.resueltas %}
{% assign archivadas = site.data.quarantine.archivadas %}

{% if activas and activas.size > 0 %}
## Activas ({{ activas.size }})

{% for p in activas %}
<div class="quarantine-card quarantine-card--activa">
  <div class="quarantine-card__header">
    <span class="tier-badge__dot">🔴</span>
    <strong>{{ p.actor }}</strong> · {{ p.resumen }}
  </div>
  <div class="quarantine-card__meta">
    <span>Detectada: {{ p.detected_at | date: "%-d de %B de %Y" }}</span>
    <span>·</span>
    <span>Motivo: {{ p.motivo }}</span>
    {% if p.url %}<span>·</span><a href="{{ p.url }}" target="_blank" rel="noopener">Fuente original ↗</a>{% endif %}
    <span>·</span>
    <span>Archivo previsto: {{ p.archive_at | date: "%-d de %B de %Y" }}</span>
  </div>
</div>
{% endfor %}

{% else %}
<p class="quarantine-empty">No hay propuestas en revisión activa en este momento.</p>
{% endif %}

---

{% if resueltas and resueltas.size > 0 %}
## Resueltas este mes ({{ resueltas.size }})

{% for p in resueltas %}
<div class="quarantine-card quarantine-card--resuelta">
  <span>✅</span>
  <strong>{{ p.actor }}</strong> · {{ p.resumen }}<br>
  <small>En revisión del {{ p.detected_at | date: "%-d %b" }} al {{ p.resolved_at | date: "%-d %b %Y" }}. Promovida a {{ p.tier_final }} · <a href="{{ p.edition_url }}">Ver edición del {{ p.resolved_at | date: "%-d de %B" }}</a></small>
</div>
{% endfor %}

{% endif %}

{% if archivadas and archivadas.size > 0 %}
## Archivadas a 60 días

{% for p in archivadas %}
<div class="quarantine-card quarantine-card--archivada">
  <span>📁</span>
  <strong>{{ p.actor }}</strong> · {{ p.resumen }}<br>
  <small>Detectada {{ p.detected_at | date: "%-d %b %Y" }}. Sin segunda fuente en 60 días. Archivada {{ p.archive_at | date: "%-d %b %Y" }}. Sigue consultable en <a href="/propuestas/?status=no_verificada">/propuestas/</a>.</small>
</div>
{% endfor %}

{% endif %}

---

## Cómo funciona esta página

El sistema detecta propuestas cada semana y aplica controles automáticos. Las que no los pasan no entran en la edición, pero se publican aquí para que sean visibles y auditables.

Una propuesta puede salir de esta lista de tres formas: aparece en un segundo medio (lo detecta el sistema automáticamente la semana siguiente), alguien nos aporta información vía [/correcciones/](/correcciones/), o la propuesta evoluciona y reaparece como propuesta formal publicada en otro sitio.

Si en 60 días no hay cambios, la propuesta se archiva como no verificada. No se borra — sigue consultable en [/propuestas/](/propuestas/).

Los criterios de admisión completos están en [/que-documentamos/](/que-documentamos/).
