---
layout: default
title: Ediciones
permalink: /ediciones/
---

<article class="archive">
  <header class="archive-header">
    <p class="archive-kicker">Archivo</p>
    <h1 class="archive-title">Todas las ediciones</h1>
    <p class="archive-lead">Informes semanales publicados desde el arranque del observatorio. El más reciente primero.</p>
  </header>

  {% assign editions = site.editions | sort: "date" | reverse %}
  {% if editions.size == 0 %}
    <p class="archive-empty"><em>Aún no hay ediciones publicadas.</em></p>
  {% else %}
    <ol class="archive-list" reversed>
      {% for e in editions %}
        <li class="archive-item">
          <time class="archive-date" datetime="{{ e.date | date: '%Y-%m-%d' }}">{{ e.date | date: '%Y-%m-%d' }}</time>
          <h2 class="archive-item-title"><a href="{{ e.url | relative_url }}">{{ e.title }}</a></h2>
          {% if e.excerpt %}
            <p class="archive-item-excerpt">{{ e.excerpt }}</p>
          {% endif %}
          <p class="archive-item-meta">
            <a href="{{ e.url | relative_url }}" class="archive-item-link">Leer informe →</a>
          </p>
        </li>
      {% endfor %}
    </ol>
  {% endif %}
</article>
