# Civic Data, Explained — Content v4 Spec (2026-08-10)

Design foundation for the platform rebuild. This is the working spec the
content/taxonomy work follows. Updated in the `civic-pipeline` thread.

## ACOG
Removed 2026-08-10 (`ff41cb4`). Initial purpose: a candidate scaffold from
the states-exploration (the "pick two states on different platforms" ask).
That purpose was **superseded** — Missouri (Socrata) + Tennessee (ArcGIS
Hub) shipped as the two chosen test states. ACOG (regional org, ArcGIS
Hub) was never requested and its 41 unwired stub pages leaked to the live
site as `/acog/` junk. Deleted; recoverable from git history.

## Taxonomy (12 categories) — Part 1
Replace the 7-category set + kill "Default"/"Other" (164 of 313 datasets
are in Default/Other today). The 12 are deliberately broader because
Missouri/Tennessee carry state-level Health/Environment/Economy data.

| Category | What belongs | Tiebreaker vs neighbors |
|---|---|---|
| Infrastructure | Physical public assets & built systems: streets/centerlines, bridges, sidewalks, water/sewer lines, utilities, building footprints, impervious surfaces, index grids, survey control points, vegetation/tree-canopy-as-asset | vs Environment: "built/managed asset" → Infrastructure; "natural system managed" → Environment |
| Transportation | Movement of people/goods: bike lanes/routes/projects, transit, parking, traffic, roads-as-mobility, snow routes, road work zones | vs Parks: "place to recreate" → Parks; "moving between places" → Transportation |
| Licensing | Regulation/permit/registration: zoning, plats, garage sales, hotel/motel tax licenses, liquor/alcohol, business/contractor licenses, vehicle licensing | vs Government: "permit/registration to operate" → Licensing; "governance/boundaries" → Government |
| Government | Governance & representation: boundaries, wards/districts, elections, council, municipal code, open meetings, city facilities (admin), state labor | vs Licensing: see above |
| Parks & Recreation | Places to recreate: parks, trails, playgrounds, open space, recreation facilities | vs Transportation: see above |
| Public Safety | Police, fire, EMS, emergency responses, 911, crime, disaster, corrections | — |
| Finance | Funds: budgets, taxes, TIF, revenue/expenditure, debt, procurement, payroll | — |
| Environment | Natural systems: water/air quality, streams/rivers/lakes (as ecology), climate, conservation, EPA, impaired waters | vs Infrastructure: see above |
| Health | Public health, health insurance, hospitals/clinics, vital stats, disease, nutrition | — |
| Education | Schools, districts, attendance, funding, libraries (educational) | vs Parks: a library building → Education |
| Housing | Where people live / housing market: housing units, affordability, tenants/rent, occupancy, residential permits, property/parcels (residential) | vs Licensing: a *permit process* for housing → Housing; a *registration program* → Licensing |
| Economy | Jobs/market/business activity: employment, wages, unemployment, economic dev, business, agriculture, industry, tourism | vs Finance: "activity/market" → Economy; "funds/revenue" → Finance |

**Decision order for a dataset:** (1) title + description + tags → best
fit; (2) genuinely ambiguous → dataset's own portal category string;
(3) still tied → the department that maintains it (existing folder-wins
rule). **Every dataset ends in exactly one of the 12. No Default, no Other.**

**Known judgment calls to settle:** waterbodies (Environment vs
Infrastructure — default Environment); trails (Parks vs Transportation —
per route type); zoning (Licensing vs Government — default Licensing as
a regulation/permit system); parcels/lots (Housing vs Licensing — per
residential/platted framing).

## Content template — Part 2 (every page, exactly 5 sections)
1. **What this is** — one sentence naming what the thing *is*.
2. **Why it matters to you** — 2–4 sentences, a real decision, city/state-specific.
3. **The facts behind the data** — 2–4 real fields by live-schema name + what real values mean; never invent.
4. **Verified facts about this topic** — 2–3 sourced facts.
5. **What you can do with this** — LOOKUP / ACT / LEARN MORE.

### Verified facts — SOURCE = municipal open minutes (user directive, 8/10)
Start from the municipality's published open meeting minutes. For each
dataset, find the council/commission meeting minutes that discuss that
dataset's subject and use **direct quotes or explicit correlations to the
specific items the dataset lists**. A fact is included only if it can be
tied to the dataset's items via a quote or correlation, with the source
meeting cited (date, agenda item). Unverifiable → omit. This is the
primary source layer; statutes/definitions/statistics are secondary.

### What you can do with this — Layer 2 scope (user directive, 8/10)
For now, Layer 2 = **the professional-specialists list only** ("A citizen
may need help from…"). Name the profession + what they help with; no
specific firms. Skip any dataset where no specialist genuinely applies
(e.g., survey control points). Department links, related-dataset links,
and external resources are **deferred** until the specialists layer is
done across the platform.

## Staging
- **Phase A — Foundation:** ACOG ✓ · 12-category taxonomy (this doc) + per-city remap (zero Default/Other) · nav fixes (dynamic All-explainers, footer URLs, city intro blocks, state/visitor framing) · manifest v3 fields (`content_status`/`content_version`/`layer2_status`/`outbound_links_verified`/`last_content_update`) + `monitoring.json` builder
- **Phase B — OKC flagship:** full Layer-1 rewrite + minutes-sourced facts + specialists; user reviews 3–5 pages
- **Phase C — Replicate:** Memphis → Lisbon → Missouri → Tennessee
- **Phase D — Monitoring agent** (later; reads monitoring.json)
