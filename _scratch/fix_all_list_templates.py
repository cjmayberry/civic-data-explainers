#!/usr/bin/env python3
"""
Rewrite all state list.html files using the correct Tennessee template pattern.
The gen_state_scaffolding.py generated files with single-brace syntax ({ define,
{ $var, etc.) which is invalid Hugo. This script fixes all 54 list.html files.
"""

import os
import json

ROOT = "/opt/data/civic-data-explainers"
LAYOUTS = f"{ROOT}/hugo-site/layouts"

# Read cities.json for all ids + state names for display
with open(f"{ROOT}/cities.json") as f:
    cities = json.load(f)

city_by_id = {c["id"]: c for c in cities}

# The correct template from tennessee/list.html
TEMPLATE = """{{ define "main" }}
{{ $city := index $.Site.Data.cities (.Params.city | default .Section) }}
{{ $all := .Pages.ByTitle }}
{{/* collect unique categories present in this section */}}
{{ $cats := slice }}
{{ range $all }}{{ $c := .Params.category | default (index .Params.categories 0) }}{{ if $c }}{{ $cats = $cats | append $c }}{{ end }}{{ end }}
{{ $uniq := $cats | uniq | sort }}
<section class="page-head">
  <span class="kicker">{{ $city.name }} · open-data explainers</span>
  <h1>{{ $city.name }} explainers</h1>
  <p class="dek">{{ $city.blurb }}</p>
  <p class="meta"><a href="{{ "/" | relURL }}">← All cities</a></p>
</section>
{{ if gt (len $uniq) 1 }}
<section class="section-filter" aria-label="Filter by topic">
  <button class="filter-btn active" data-filter="all">All ({{ len $all }})</button>
  {{ range $uniq }}<button class="filter-btn" data-filter="{{ . }}">{{ . }}</button>{{ end }}
</section>
{{ end }}
<section class="card-grid">
  {{ range $all }}
  <a class="card" href="{{ .RelPermalink }}" data-category="{{ .Params.category | default (index .Params.categories 0) }}">
    {{ with .Params.cover }}<img class="card-cover" src="{{ printf "img/%s" . | relURL }}" alt="" loading="lazy">{{ end }}
    <span class="kicker">{{ .Params.category | default (index .Params.categories 0) }}</span>
    <h3>{{ .Title }}</h3>
    <p>{{ .Params.teaser | default .Description }}</p>
  </a>
  {{ end }}
</section>
<script src="{{ "js/section-filter.js" | relURL }}" defer></script>
{{ end }}
"""

written = 0
for cid, city in city_by_id.items():
    list_path = f"{LAYOUTS}/{cid}/list.html"
    os.makedirs(os.path.dirname(list_path), exist_ok=True)
    with open(list_path, "w") as f:
        f.write(TEMPLATE)
    written += 1

print(f"Wrote {written} list.html files from correct template")

# Verify syntax: check no single-brace patterns remain
import re
remaining = 0
for cid in city_by_id:
    list_path = f"{LAYOUTS}/{cid}/list.html"
    with open(list_path) as f:
        content = f.read()
    if re.search(r'\{[^{]', content):  # single { not followed by another {
        print(f"  STILL BROKEN: {cid}/list.html")
        remaining += 1

if remaining == 0:
    print("All files have correct double-brace syntax ✓")
else:
    print(f"{remaining} files still have issues")
