# Civic Data Pipeline

Generic pipeline: any ArcGIS Hub site → structured catalog JSON → drafted
plain-language explainers → Hugo site (deploy to Cloudflare Pages).

Current instance: Oklahoma City Open Data Hub → **Civic Data, Explained**
(baseURL: `https://civic-data-explainers.pages.dev/`).

## Pipeline stages (run in order)

```
extract_catalog.py  → okc_catalog.json      raw ArcGIS Hub RSS → JSON
                      odot_catalog.json     ODOT Hub DCAT data.json (100)
                      occ_catalog.json      OCC Hub DCAT data.json (40)
                      okgov_catalog.json    data.ok.gov CKAN (390)
build_manifest.py   → manifest.json (v2)    THE category source of truth
content/redraft.py  → drafts-v2.json        content re-draft (4-part template)
fetch_images.py     → covers/*.svg|png      real-geometry image upgrade
hugo build          → public/               static site
```

Each stage owns a disjoint set of manifest fields and preserves the others'
state, so re-running any stage is safe:

| Stage | Owns |
|---|---|
| `build_manifest.py` | `category`, frontmatter rewrite, first-time cover naming |
| `content/redraft.py` | `content_status`, `content_model` |
| `fetch_images.py` | `image_status`, `image_source`, `image_file`, `image_note` |

## manifest.json v2 schema

The manifest is the single source of truth an agent reads to know the state
of every page without opening a single content file:

```json
{
  "slug": "pavement-condition-e80f59ff",
  "title": "Pavement Condition",
  "category": "Transportation",          // drives card + page + cover name
  "content_status": "drafted" | "stub" | "needs_review",
  "content_model": "openrouter/deepseek/deepseek-chat-v3-0324/v2-pavement-shape",
  "image_status": "cover_only" | "map_real_geometry",
  "image_source": "svg_cover" | "local_geometry" | "mapbox" | null,
  "image_file": "pavement-condition-e80f59ff--transportation--map_real_geometry.svg",
  "image_note": "polygon, 640 features", // or the reason it stayed cover_only
  "last_updated": "2026-07-31T..."
}
```

### Category: one decision, one place

`build_manifest.py` decides every dataset's category with a documented,
re-runnable rule:

1. `CATEGORY_OVERRIDES[slug]` — curated exceptions, each with a written
   reason (e.g. Snow Routes → Transportation: the city's own ArcGIS folder
   is `OpenData/Transportation`; Hub tags it Public Safety first).
2. else: first catalog `topics` entry mapped through `TOPIC_ALIASES`
   (Recreation → Parks & Recreation, Utilities → Infrastructure).
3. else: "Default".

Tie-break philosophy: where Hub's tag order disagrees with the city's own
service folder, the folder wins — it reflects the department that maintains
the data. Frontmatter `categories: ["<canonical>"]` is a materialized copy
(single element keeps the Hugo taxonomy working); the manifest is canonical.

## Content template (prompt v2 — "pavement shape")

`content/prompts.py` holds the canonical prompt (`v2-pavement-shape`), the
structure that made Pavement Condition work, generalized:

1. **What this is** — one sentence.
2. **Why it matters** — a concrete real-world decision the reader faces.
3. **How to read this data** — 2-4 real dictionary fields, plain language.
4. **Try it yourself** — anchored to the reader's own address/street/ward,
   ONLY when the dataset supports it (field-anchor check in `redraft.py`).

Datasets with no location anchor (survey control points, elevation
contours, zoning classes, waterbodies) get `content_status: needs_review`
and a "Where this leaves you" section instead of a hollow step 4 — an
honest omission beats a fake one. `redraft.py` also validates every draft:
required sections present, no bolded field that isn't in the real
dictionary, length cap.

Model path: `content/call_model.py` tries the Nous inference API first
(`NVIDIA_API_KEY`), falls back to OpenRouter (`OPENROUTER_API_KEY`).
`content_model` records which provider/model/prompt actually wrote each
body.

## Image pipeline

Cover files are self-documenting by name:

```
{slug}--{category-slug}--{image_status}.{ext}
pavement-condition-e80f59ff--transportation--map_real_geometry.svg
```

A directory listing answers "which datasets still only have cover_only?"
without parsing JSON. `fetch_images.py` Tier A queries each dataset's own
ArcGIS FeatureServer (keyless, public — verified working) for GeoJSON and
renders real geometry: via Mapbox Static Images when `MAPBOX_TOKEN` is set,
else a local deterministic SVG renderer (category gradient + real shapes,
zero cost, offline). Datasets that can't render keep `cover_only` with the
reason in `image_note`.

## Interactive map basemap (decision)

When the on-page map feature is built (GeoJSON overlay on a basemap), use
**MapLibre GL JS + OpenFreeMap public instance** — no account, no API key,
no view limits, commercial use OK, attribution auto-added. The GeoJSON from
`fetch_images.py` Tier A embeds per-page and renders client-side. Reserve
Mapbox only for geocoding (address search) or static-image social cards.
Full research + rationale: `Ocean/knowledge/research/2026-07-31--mapbox-tiers-static-site.md`.

## Ads

Leaderboard and rectangle ad slots were removed from all templates and CSS
(2026-07-31). Decision: disclosed civic-explainer content next to
unverified LLM-drafted text about municipal data is not a monetization
model to back into via a scaffold default. If ads return, it is a
deliberate choice.

## Cloudflare Pages build settings

The Pages built-in Hugo buildpack may pick an old default Hugo (0.54-era)
that cannot parse `hugo.toml` / the modern templates. Use the pinned build:

- Build command: `bash build.sh`
- Build output directory: `public`
- (Optional) `HUGO_VERSION` env var: `0.147.2`

`build.sh` downloads the exact pinned Hugo binary and builds with it, so
the deploy is deterministic regardless of the buildpack defaults.

## Interactive maps (point datasets)

Point layers (fire stations, police stations, work zones, survey points,
garage sales, …) get a client-side Mapbox GL marker map on their page —
every published location as a marker, with address popups. Set in Pages:
**Settings → Environment variables → Production + Preview**:

```
MAPBOX_TOKEN=pk.…your public Mapbox token
```

Without it the page falls back to the static cover (the map section is
hidden). The token is injected into the page at build time via Hugo's
`getenv` (allowlisted in `hugo.toml`) — it is never committed to the repo.
A `pk.` token is Mapbox's public token type, designed for client-side
embedding; optionally restrict it in the Mapbox dashboard to
`civic-data-explainers.pages.dev` to cap usage to this site.

## System A — live inquiry (address/street lookup)

14 datasets carry a live lookup box ("Look it up yourself — live"):
reader types a street/address/facility name, the page queries the
dataset's own ArcGIS service and shows the matching record's value
(e.g. Pavement Condition → the PCI of your street's segment). One
reusable component: `layouts/partials/inquiry.html` + `static/js/inquiry.js`,
driven entirely by per-page data attributes from the manifest
(`inquiry_enabled`, `inquiry_search_field`, `inquiry_field`,
`inquiry_label`, `inquiry_extra`).

Excluded (with reasons in `build_manifest.py`'s INQUIRY block): zoning
and ward layers (no text field — a spatial/parcel lookup would be needed),
lot/block tables, survey points, vegetation, boundaries, and name-only
layers (trails, waterbodies — those are System B territory). Note the
live service schemas differ from the catalog dictionary (e.g. real
pavement fields are `XSTREET_NA`/`PCICurrent`, not `Street`/`PCI`) —
the INQUIRY config uses the verified live field names, and the JS queries
with `f=geojson` (the services return ESRI `attributes` under `f=json`).

## System B — named-place enrichment (photos + verified name origins)

`content/enrich.py` researches named records (City Trails, Parks, Park
Facilities, City Facilities, Police Stations; fire stations excluded —
their records carry numeric identifiers, not names) against Wikipedia +
Wikidata: lead image from the article, and a "named after" note ONLY from
structured Wikidata claim P138, always with a source link. Per-record
`enrichment_status: pending | found | not_available` is stored in
`hugo-site/data/enrichment/<slug>.json` (re-runs skip already-checked
records) and aggregated in the manifest. Hard rule: an unverifiable name
origin is treated the same as a missing one — the image stands alone, the
note is omitted, no guesses.

## State sources (Oklahoma)

| Source | Extractor mode | Feed | Records |
|---|---|---|---|
| ODOT Hub (`gis-okdot.opendata.arcgis.com`) | `dcat` | `data.json` | 100 (roads, bridges, rail, boundaries) |
| OCC Hub (`gisdata-occokc.opendata.arcgis.com`) | `dcat` | `data.json` | 40 (oil/gas wells, seismicity) |
| data.ok.gov | `ckan` | `/api/3/action/package_search` | 390 (payroll, vendor payments, PCard) |

`extract_catalog.py` auto-detects the format from the URL (`data.json` →
dcat, `/api/3/action` → ckan, else rss); `--format rss|dcat|ckan` overrides.
All three modes emit the **same normalized record schema** (`title, link,
guid, type, featured, topics, pub_date_iso, maintained_by, suitable_use,
limitations_on_use, update_interval, data_dictionary, description_raw,
structure_detected, source, formats, service_url, scope`), so downstream
stages don't care which source produced a record.

`service_url` carries the dataset's ArcGIS FeatureServer REST URL (dcat) or
datastore/API URL (ckan) when the source exposes one — that's what
`fetch_images.py`-style geometry pulls would hit. `formats` lists the
distribution formats (GeoJSON, CSV, GDB, ...).

Refresh all catalogs in one command:

```bash
bash extractor/extract_state_catalogs.sh   # writes okc/odot/occ/okgov catalogs
```

County-scope rule: LiDAR / NAIP / orthoimagery / DEM-style records are
flagged `scope: "county"` by the extractor — full-state pulls are TBs and
must never be attempted. If a catalog stage is asked for imagery, restrict
to the county-scoped records. No full-state imagery pull exists in this
pipeline by design.

Note on data.ok.gov: it is CKAN 2.9 (OpenGov), NOT Socrata — all legacy
Socrata endpoints return 404. Also, the portal's WAF 502s on User-Agent
strings containing "extractor"; the extractor uses `civic-data-pipeline/1.0`.

## Running for a second city

```bash
python3 extractor/extract_catalog.py https://<city>.hub.arcgis.com --pretty > catalog.json
# swap CATALOG_PATH / city / site_url in build_manifest.py, redraft.py, fetch_images.py
python3 build_manifest.py                 # categories + manifest v2
set -a && source /opt/data/.env && set +a
python3 content/redraft.py --model deepseek/deepseek-chat-v3-0324
python3 fetch_images.py                   # or MAPBOX_TOKEN=... python3 fetch_images.py
cd hugo-site && hugo                       # build
```

The category overrides and anchor heuristic are OKC-tuned guesses with one
data point — expect to adjust for a second city's tagging conventions
(`TOPIC_ALIASES`, `CATEGORY_OVERRIDES`, `ANCHOR_RE` in redraft.py).

## Known gaps, honestly

- `NVIDIA_API_KEY` (Nous inference) currently returns 401/403 — the
  `content_model` for the 2026-07-31 batch is OpenRouter
  (deepseek-chat-v3-0324). Re-verify before a fresh run.
- No `MAPBOX_TOKEN` in the environment: geometry renders are local SVG
  (`image_source: local_geometry`). The Mapbox path is implemented and
  token-gated.
- ArcGIS FeatureServer layer indexing: pages whose source_url ends in
  `/FeatureServer/N` query layer N; bare `/FeatureServer` URLs assume layer
  0. A handful of datasets may live on other layers — `image_note` records
  the failure reason when a query misses.
- Taxonomy URLs for "Parks & Recreation" slugify to `parks--recreation`
  (double dash from `&`). Cosmetic.
