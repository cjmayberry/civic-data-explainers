# Adaptive City Pipeline — Full Rebuild (Merged)

This prompt merges the best of two prompt variants into a single
authoritative instruction set for Hermes. It replaces the current
OKC-only content engine with one that is schema-driven, city-adaptive,
and grounded in the actual repo structure at `cjmayberry/civic-data-explainers`.

Do not touch the Hugo templates or `build_manifest.py`'s existing
`INQUIRY`, `CATEGORY_OVERRIDES`, or `HAND_AUTHORED` dicts — those are
stable OKC state. The pipeline scripts below are the only targets.

---

## Step 0 — City config file (create or update `cities.json`)

Create `cities.json` at the repo root. This is the single trigger
for every pipeline run. Adding a city here and rerunning is all
that is ever required to add city #3.

```json
[
  {
    "id": "okc",
    "name": "Oklahoma City",
    "hub_url": "https://open-okc.hub.arcgis.com",
    "gov_url": "https://www.okc.gov",
    "state": "OK",
    "active": true,
    "model": null,
    "min_score": 80,
    "content_dir": "hugo-site/content/datasets",
    "static_dir": "hugo-site/static/img",
    "category_map": {}
  },
  {
    "id": "memphis",
    "name": "Memphis",
    "hub_url": "https://data.memphistn.gov",
    "gov_url": "https://www.memphistn.gov",
    "state": "TN",
    "active": true,
    "model": null,
    "min_score": 70,
    "content_dir": "hugo-site/content/memphis",
    "static_dir": "hugo-site/static/img/memphis",
    "category_map": {}
  }
]
```

Field notes:
- `model`: null inherits the run-level `--model` flag; a named model
  string (e.g. `"anthropic/claude-sonnet-4"`) overrides it for this city only.
- `min_score`: per-city completeness threshold for including a dataset.
  Memphis portal quality is lower than OKC's — do not use a global default.
- `content_dir` / `static_dir`: mirrors the existing `--content-dir` /
  `--static-dir` args already in `build_manifest.py` so the manifest builder
  can be called per-city without flags.
- `category_map`: populated by Step 2; empty `{}` on first run.

Never hardcode a city name, URL, slug, or category label anywhere
else in the pipeline.

---

## Step 1 — Schema introspection (runs before any content draft)

For each dataset that passes the `min_score` filter, query the live
ArcGIS feature service to get the real field schema before drafting
anything. Endpoint pattern:

```
GET {dataset.service_url}/query?where=1=1&outFields=*&resultRecordCount=3&f=json
```

The `service_url` is the catalog item's `url` field
(ends in `/FeatureServer/0` or `/MapServer/0`).

From the response, extract and store per dataset:

```json
"schema": {
  "fields": [
    {"name": "PCI", "type": "esriFieldTypeInteger", "alias": "Pavement Condition Index"},
    {"name": "STREET", "type": "esriFieldTypeString", "alias": "Street Name"}
  ],
  "sample": {"PCI": 72, "STREET": "NW 23RD ST"},
  "introspected_at": "2026-08-02T14:00:00Z"
}
```

Key `schema` (not `live_schema`) — `build_manifest.py` and
`regenerate_content.py` reference this key; do not rename it.

Use `resultRecordCount=3` (not 1) to reduce the chance of missing
fields that are null in the first record.

If the service URL is absent, returns 403, or times out:
- Set `"schema": null`
- Set `"content_status": "needs_review"` (not a different key)
- Continue — do not block the whole city run on one bad endpoint
- Log which datasets had no schema so it is visible in the report

Never invent field names. The live schema is authoritative;
catalog description text is supplementary context only.

---

## Step 2 — City taxonomy discovery (replaces hardcoded cat_map)

`build_manifest.py` currently hardcodes `TOPIC_ALIASES` for OKC.
Memphis uses different category path strings. Every new city will too.

Replace with dynamic per-city taxonomy discovery:

1. Read all `categories` values across every dataset in the city's
   catalog after extraction. Build a frequency table.

2. Map each unique category string to a display label using the model
   — one LLM call per city, not per dataset:

   ```
   SYSTEM: You map raw open-data portal category labels to a
   standard display taxonomy. Return JSON only — no explanation.

   USER: City: {city_name}
   Raw category labels and their frequencies:
   {json of {raw_label: count}}

   Map each raw label to the closest label from this taxonomy:
   [Infrastructure, Transportation, Licensing, Government,
   Parks & Recreation, Public Safety, Finance]

   If a label clearly does not fit any category, return "Other".
   Never return "Default".
   Return JSON: {"raw_label": "display_label"}
   ```

3. Cache the result in `cities.json` under the city's `category_map`
   key so re-runs do not re-derive it unless `--refresh-taxonomy`
   is passed.

4. Fallback for datasets with no category signal at all: assign based
   on title keywords using the same taxonomy list via a short LLM call.
   Log any that still cannot be resolved — do not silently drop them
   into "Default" or any raw portal label.

5. For OKC: the existing `TOPIC_ALIASES` and `CATEGORY_OVERRIDES` in
   `build_manifest.py` remain authoritative. Do not overwrite them
   with the LLM map. Apply the LLM map only for cities that do not
   already have a `TOPIC_ALIASES` block in the script.

---

## Step 3 — Adaptive content drafting

The drafting prompt now receives four inputs:

```python
{
  "city": city_config,           # id, name, state, hub_url from cities.json
  "dataset_meta": {
    "title": ...,
    "description": ...,          # raw catalog description — model reads whole
    "update_interval": ...
  },
  "schema": {                    # from Step 1: real fields + sample values
    "fields": [...],
    "sample": {...}
  },
  "display_category": "..."      # from Step 2: resolved display label
}
```

Use this system prompt verbatim — it encodes the Pavement Condition
page quality bar and the existing `HAND_AUTHORED` showcase shape:

---
SYSTEM:
You write plain-language explainers of municipal open-data datasets
for residents and small business owners — not GIS professionals.

You receive a dataset's metadata, its actual field schema from the
live service, and sample values. Use the real field names and real
sample values in your explanation. Never invent a field name or a
value that is not in the schema you were given.

Write exactly four sections with these Markdown headers:

## What this tracks
One sentence. What does this dataset measure or record?

## Why it matters to you
2-4 sentences. Name a specific real-world decision a resident or
business owner would make differently if they knew this data existed.
Use concrete language — not "can be used to view" but "tells you
whether your street will be plowed before you leave for work."
Reference the city by name. Do not write "your city."

## How to read this data
Explain 2-4 of the most meaningful fields using their actual names
from the schema. Format: **FIELD_NAME** — what it means, what its
values look like (use sample values). Skip fields that are purely
technical identifiers with no resident-facing meaning
(ObjectID, Shape, GLOBALID).

## Try it yourself
One specific action the reader can take using this data right now,
tied to their own address, street, ward, or neighborhood where the
dataset supports it. If the dataset does not support address-level
lookup, skip this section entirely — do not write a hollow version.

Under 350 words total. No bullet points in "Why it matters."
---

USER prompt (built per dataset):
```
City: {city_name}, {state}
Dataset: {title}
Category: {display_category}
Update interval: {update_interval}
Description from catalog: {description[:500]}

Schema fields:
{for each field: "FIELD_NAME ({alias}, {type}): sample = {sample[FIELD_NAME]}"}

Write the explainer now.
```

Model selection: use the `--model` CLI flag, overridden by the
city-level `model` in `cities.json` if non-null. No hardcoded
model name anywhere in the pipeline scripts.

```bash
python3 pipeline/run.py cities.json --model anthropic/claude-sonnet-4 --city okc
python3 pipeline/run.py cities.json --model tencent/hy3 --city memphis
```

No `--model` flag = use `model_registry.md` default.

---

## Step 4 — Manifest as build contract

`build_manifest.py` already writes and reads `manifest.json`. The
pipeline must extend — not replace — its output schema. After
introspection and drafting, the manifest entry for each dataset must
contain the following fields (additions to current schema are marked NEW):

```json
{
  "slug": "straight-zoning-388d1b1f",
  "title": "Straight Zoning",
  "city": "Oklahoma City",
  "city_slug": "okc",
  "category": "Licensing",
  "display_category": "Planning, Zoning & Development",
  "content_status": "drafted | stub | needs_review",
  "content_model": "model-name-used-or-null",
  "schema": {"fields": [], "sample": {}},
  "inquiry_enabled": true,
  "inquiry_search_field": "ZONING",
  "inquiry_field": "ZONE_DESC",
  "inquiry_label": "Look up your property's zoning",
  "inquiry_extra": [],
  "image_status": "cover_only",
  "image_source": "svg_cover",
  "image_file": "straight-zoning-388d1b1f--licensing--cover_only.svg",
  "enrichment_status": null,
  "last_updated": "2026-08-02T14:00:00Z"
}
```

Existing fields (`content_status`, `inquiry_*`, `image_*`,
`enrichment_status`) already exist in `build_manifest.py` — do not
duplicate or rename them. NEW fields added by this pipeline:
`city`, `city_slug`, `display_category`, `schema`.

`to_hugo_content.py` (or equivalent) must read all fields from the
manifest at build time. Do not re-derive any field that is already
in the manifest.

---

## Step 5 — Site structure for multi-city

Each city gets its own Hugo section:

```
hugo-site/content/
  datasets/        # existing OKC content — leave in place
  memphis/         # new city section
  _index.md        # homepage — generated from cities.json (Step 6)
```

URL routing: `/{city-id}/{dataset-slug}/`

Existing OKC URLs at `/datasets/{slug}/` must be preserved via
a `_redirects` file at the Cloudflare Pages root:

```
/datasets/:slug/  /okc/:slug/  301
```

Do not break indexed OKC URLs. Add this file before deploying Memphis.

Shared `layouts/` templates read `city` and `display_category`
from frontmatter — no city-specific template files. Footer topic
counts are scoped to the current city section, not the whole site.

---

## Step 6 — Homepage auto-population

`hugo-site/content/_index.md` must be generated from `cities.json`,
not hand-edited. For each active city, render one card showing:
- City name and state
- Dataset count
- Top 3 categories by dataset count
- Link to `/{city-id}/`

When a new city is added to `cities.json` and the pipeline runs,
it appears on the homepage automatically with no manual template edits.

---

## Acceptance criteria

Run both cities end-to-end:

```bash
python3 pipeline/run.py cities.json --model tencent/hy3
```

Then verify:

1. Zero datasets categorized as "Default" or any raw portal label
   in either city — report count of genuinely tag-free datasets
   separately
2. Every dataset page uses field names from its actual live schema —
   spot-check 3 Memphis pages against the live ArcGIS service
3. Memphis and OKC pages do not share phrasing in their
   "Why it matters" sections for datasets with the same name
   but different schemas
4. `/datasets/{slug}/` redirects to `/okc/{slug}/` without 404
5. Adding a third city to `cities.json` and rerunning produces a
   complete city section with no manual intervention

Report back:
- Schema introspection success rate per city (live URL available vs. not)
- Category mapping coverage (how many labels needed new `category_map`
  entries beyond the existing `TOPIC_ALIASES`)
- One before/after content comparison showing a dataset that got
  genuinely different prose because its schema differed
- Live link to one Memphis page where field explanations visibly use
  real field names
