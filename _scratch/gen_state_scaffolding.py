#!/usr/bin/env python3
"""Generate _index.md + list.html + single.html for states missing scaffolding."""
import json, os

ROOT = "/opt/data/civic-data-explainers"
CONTENT = os.path.join(ROOT, "hugo-site/content")
LAYOUTS = os.path.join(ROOT, "hugo-site/layouts")

cities = json.load(open(os.path.join(ROOT, "cities.json")))

# Skip states that already have scaffolding
skip = {"okc", "memphis", "lisbon", "missouri", "tennessee", "kansas",
        "nebraska", "topeka", "nevada", "newmexico", "idaho", "utah"}

count = 0
for c in cities:
    sid = c["id"]
    if sid in skip:
        continue
    name = c["name"]

    # _index.md
    idx_dir = os.path.join(CONTENT, sid)
    os.makedirs(idx_dir, exist_ok=True)
    idx_path = os.path.join(idx_dir, "_index.md")
    if not os.path.exists(idx_path):
        with open(idx_path, "w") as f:
            f.write(f"""---
title: "{name} explainers"
date: "2026-08-18"
categories: ["Default"]
cover: "covers/_index--default--placeholder.svg"
draft: false
---
""")
        count += 1

    # list.html
    list_dir = os.path.join(LAYOUTS, sid)
    os.makedirs(list_dir, exist_ok=True)
    list_path = os.path.join(list_dir, "list.html")
    if not os.path.exists(list_path):
        with open(list_path, "w") as f:
            f.write(f"""{{ define "main" }}
<h1>{name} explainers</h1>
<section class="page-head">
  <span class="kicker">{name} · open-data explainers</span>
  <p class="meta"><a href="/">← All cities</a></p>
</section>
<section class="card-grid">
  {{ $all := .Pages.ByTitle }}
  {{ if eq (len $all) 0 }}
  <p class="empty-state">No explainers yet for {name}. Check back soon.</p>
  {{ end }}
  {{ range $all }}
  <a class="card" href="{{ .RelPermalink }}">
    {{ with .Params.cover }}<img class="card-cover" src="{{ printf "img/%s" . | relURL }}" alt="" loading="lazy">{{ end }}
    <span class="kicker">{{ .Params.category | default (index .Params.categories 0) }}</span>
    <h3>{{ .Title }}</h3>
    <p>{{ .Params.teaser | default .Description }}</p>
  </a>
  {{ end }}
</section>
{{ end }}
""")
        count += 1

    # single.html
    single_path = os.path.join(list_dir, "single.html")
    if not os.path.exists(single_path):
        with open(single_path, "w") as f:
            f.write("""{{ define "main" }}
{{ partial "dataset-single.html" . }}
{{ end }}
""")
        count += 1

print(f"Generated {count} scaffolding files for {len(cities) - len(skip)} remaining states")
