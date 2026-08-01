#!/usr/bin/env python3
"""
Regenerate all dataset pages for the Civic Data, Explained Hugo site.

Rebuilds hugo-site/content/datasets/*.md from the source of truth:
  - frontmatter: preserves existing values (title, date, description, tags,
    categories, source_url, license, dataset_id, city, site_url) and adds
    `teaser` (card dek) + `dictionary` (real field definitions from the
    catalog, rendered as a table by the single layout).
  - body: 12 showcase datasets get hand-written teachable explainers
    (BODIES below); all others get an honest scripted structure built from
    the catalog's own Suitable Use / update interval / Limitations text.

No invented facts: every field name, description, cadence, and limitation
comes from okc_catalog.json or the existing page frontmatter.

Usage:  python3 regenerate_content.py
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
DATASETS_DIR = os.path.join(ROOT, "hugo-site", "content", "datasets")
CATALOG_PATH = os.path.join(ROOT, "okc_catalog.json")

# ---------------------------------------------------------------------------
# Hand-written showcase explainers (slug -> body markdown)
# ---------------------------------------------------------------------------
BODIES = {
"public-infrastructure-projects-d5e6fb99": """## What this is

This is the city's public to-do list for major construction: every street, bridge, drainage, park and traffic project Oklahoma City has planned or underway, with a budget and a schedule attached.

## Why it matters to you

That orange cone on your commute started as a row in this dataset. If you want to know why a street is torn up, when a project near you is supposed to finish, or whether the city is actually spending what it promised on a neighborhood bond project, this is the ledger to check. For small businesses, a "Planned End Date" can mean the difference between a normal summer and a summer of detoured customers — worth knowing before you lease, hire, or stock inventory.

## How to read this data

- **Project Phase** — where a project sits in its life: planning, design, under construction, or complete. Filter for "under construction" to see what's actively affecting streets today.
- **Planned Start Date / Planned End Date** — the city's estimate. Treat these as a forecast, not a promise.
- **Actual Start Date** — when work really began. The gap between planned and actual is the single most honest number in city infrastructure: compare them and you'll see how realistic the estimates were.
- **Estimated Budget** — the sticker price in USD. Note the word "estimated" — the dataset is honest about it.

## Try it yourself

Open the data service, filter **Project Phase = "under construction"** in your part of town, and check the gap between Planned and Actual Start Date. Pick the project with the biggest gap and ask yourself: what would make a city's schedule slip by that much?
""",

"council-wards-666b9654": """## What this is

Oklahoma City is divided into wards, and each ward elects one council member. This dataset is the official map of those boundaries and who currently represents each one.

## Why it matters to you

Every city service you care about — potholes, parks, zoning, police response — is filtered through your council member's office. When a street light is out for weeks, the person who can actually make it move is the ward representative. This dataset tells you which one is yours, and it's also the answer key for questions like "why is this development in my neighborhood?" — because land-use decisions live on a ward map too.

## How to read this data

- **Ward** — the number of the district (Oklahoma City has 8).
- **Council Member** — the current representative's name. This field changes with every election, so the dataset is only as current as its last update.
- **Area** — the size of the ward in square feet. Wards are drawn to be roughly equal in *population*, not in size — which is why some look huge and empty and others small and dense.

## Try it yourself

Find your address on the ward map and note the Ward number. Then look up when your council member's term ends and whether your ward is up for election this year — most people discover they vote for city council more often than they thought.
""",

"street-centerlines-0e041a93": """## What this is

Every street in Oklahoma City, drawn as a single center line with the street's full name, classification, and the address ranges on each side. It updates **daily**.

## Why it matters to you

When a delivery driver finds your house, when 911 locates a caller, when a map app routes around a closed road — they're all reading address ranges off a dataset like this one. It's also why some streets are "NW 23rd" and others are "Broadway": the dataset separates prefix, name, and suffix so every address in the city can be assembled consistently. If your address doesn't resolve in an app, the problem often traces back to a gap in centerline data.

## How to read this data

- **Full Street Name** — the assembled name, e.g. "N Walker Ave".
- **Street Class** — the city's classification of the road, from neighborhood streets up to major arterials. Higher classes carry more traffic and usually get plowed and repaved first.
- **Left From / Left To Address** — the address range on the left side of the street. Odd/even numbering conventions mean one side of the street carries one range and the other carries another; this is how mapping systems guess which side a house is on.

## Try it yourself

Look up your own street, then compare the **Left To Address** and **Right To Address** ranges. See how the numbering works? Now find a brand-new street — it'll be there, because this dataset refreshes every single day.
""",

"straight-zoning-388d1b1f": """## What this is

The base zoning map of Oklahoma City: every parcel carries a zoning classification (like R-1 or C-3) that sets the rules for what can be built there. This dataset updates **daily**.

## Why it matters to you

Zoning is why you can't open a barbershop in a house on a residential street, and why your neighbor can't pave their front yard for a parking lot. Before you buy a property, lease a space, or even plan a big remodel, the zoning class tells you what's allowed by right. "Straight" zoning is the base layer — separate from the overlay districts and special-use rules that stack on top of it.

## How to read this data

- **Zoning Class** — the abbreviated code (e.g., R-1 for single-family residential, C-3 for heavy commercial). The code is a compact rulebook: the first letter is the broad category (Residential, Commercial, Industrial) and the number refines it.
- **Case Number** — if the area was rezoned, this is the planning case that did it. Look the case up to read the history of why a piece of land changed.

## Try it yourself

Find your own address's zoning class and decode it: what letter does it start with, and what does that allow? Then find a parcel zoned differently one street over — that's the urban fabric changing, one case number at a time.
""",

"tax-increment-financing-districts-08ededb1": """## What this is

A map of the city's Tax Increment Financing (TIF) districts — the areas where Oklahoma City has agreed to use future property-tax growth to pay for development today.

## Why it matters to you

TIF is one of the most powerful — and least understood — tools a city has. When a big development gets a TIF, the tax revenue the development *would* generate is diverted to pay for the infrastructure that makes it possible: roads, sewers, parking garages. For residents, that can mean a new downtown without raising taxes... or it can mean public money quietly subsidizing a private project. Knowing where the TIF districts are is the first step to forming your own opinion on whether they're working.

## How to read this data

- **District** — the name of the TIF area. These are the headline redevelopment zones: core downtown, riverfront, and similar.
- **Year** — when the district was created. Older districts may have already paid off their obligations; newer ones are still spending.
- **Shape / Area** — the physical boundary. The catalog is honest: boundaries are approximate and some areas fall in *multiple* overlapping districts.

## Try it yourself

Pick a TIF district and find its Year. Then ask: what's been built in that area since? That's the whole TIF argument in one question — did the future tax growth the city bet on actually show up?
""",

"parks-fe9dc8e8": """## What this is

The official inventory of Oklahoma City's regional, community, and neighborhood parks — where they are, what type they are, and how big.

## Why it matters to you

Park data is a quiet quality-of-life ledger. Real estate agents use it to price neighborhoods; city planners use it to find "park deserts" — areas with no green space within walking distance; and families use it to answer "which park near me has the most room to run?" The Park Type field tells you what to expect: a neighborhood park is your local green, a community park has more amenities, and a regional park is a destination.

## How to read this data

- **Park Type** — the classification: regional, community, or neighborhood. This is the fastest read on what a park actually is.
- **Park Acres** — the size in acres. Compare this to the surrounding neighborhood's density and you can start spotting which parts of town are park-rich and which aren't.
- **Park Address** — where to find it, useful when the park name isn't a street address.

## Try it yourself

Find the park closest to your home and note its type and acreage. Now find the largest park in the city and the smallest — the gap between them tells you something about how Oklahoma City thinks about green space.
""",

"sidewalks-bc31068e": """## What this is

Every sidewalk maintained by the City of Oklahoma City, mapped with its funding source where known.

## Why it matters to you

Sidewalks are the most used piece of city infrastructure you never think about — until one is missing. This dataset shows which sidewalks exist and, crucially, *who paid for them*. That funding field is the story of how OKC builds walkable neighborhoods: many newer sidewalks were paid for with GO Bond money, which means they were voted on by residents like you. If a sidewalk gap is breaking up your walk to school or the bus stop, this map shows you're not imagining it — the city's own data confirms what's missing.

## How to read this data

- **Sidewalk Funding** — the funding source (GO Bond or other initiatives). The catalog is honest: this is generally only filled in for *newer* sidewalks, so an empty field doesn't mean "no sidewalk" — it means "no funding record."
- **Length** — the length of the sidewalk segment in feet. Chain segments together to measure a whole route.

## Try it yourself

Trace the route from your home to the nearest school or bus stop on the sidewalk map. Count the gaps. If you find one, that's a specific, data-backed request you can take to your council member — city decisions run on documented needs, and this dataset is the documentation.
""",

"building-footprints-2d4cd6c3": """## What this is

The footprint of every building in Oklahoma City — captured from aerial imagery collected in **2020** — with its elevation above sea level.

## Why it matters to you

This is the dataset that makes flood-risk maps, solar-potential calculators, and "how much of my lot is covered by structure?" questions answerable. It's also a time capsule: the data was collected in 2020, so every building built since then is invisible to it. Understanding *when* data was collected is a civic superpower — most arguments about "the data is wrong" turn out to be "the data is old."

## How to read this data

- **Elevation** — height above sea level in feet. Combine with flood zone maps to understand your property's drainage reality.
- **Area** — the building's footprint in square feet. This is the "building coverage" number that matters for lot-coverage rules.
- **Shape** — the actual outline. The data comes from aerial imagery, so outlines may not perfectly match what's on the ground.

## Try it yourself

Find your own home's footprint and check its Area. Now count how many new buildings near you went up after 2020 — anything newer simply won't be in this dataset. That's your reminder to always check a dataset's collection date before trusting it.
""",

"bike-routes-5600dd31": """## What this is

The city's current bike routes — including trail names, types, and status — mapped across Oklahoma City.

## Why it matters to you

If you're choosing where to live, work, or start a business, the bike network is a hidden amenity: routes connect parks, neighborhoods, and downtown, and Trail Type tells you whether you're on a shared street, a dedicated lane, or an off-road trail. For commuters, the Status field separates what's rideable today from what's still being built — the difference between a pleasant 15-minute ride and a surprise dead-end.

## How to read this data

- **Trail Name** — the route's name, if it has one. Named trails are usually the marquee routes with real investment behind them.
- **Trail Type** — what kind of facility it is. This determines who it's comfortable for: a family on cruisers vs. a commuter on a road bike.
- **Status** — current state (planned, under construction, or open). The catalog notes there can be a delay between completion and appearing here.

## Try it yourself

Plot a ride from your home to a destination you visit weekly using only routes marked open. Then look at what's planned near you — that's the network's future, and public comments on those projects actually shape them.
""",

"pavement-condition-e80f59ff": """## What this is

A condition score for every street segment Oklahoma City maintains, based on the Pavement Condition Index (PCI) — the industry-standard rating of road health.

## Why it matters to you

PCI is the number behind the politics of potholes. Streets are scored on a scale (roughly 0–100), and cities use those scores to decide which streets get repaved and which get patched — because fixing a road when its score is 70 costs a fraction of rebuilding it when it's 20. If your street is rough, its PCI score is your evidence; if your street is newly smooth, the score will show the bump. This dataset is also the classic answer to "why did they pave THAT street and not mine?" — because it's a score, not a vibe.

## How to read this data

- **PCI** — the pavement condition index. Higher is better; a low PCI on your segment is the concrete number to quote in a service request.
- **Street Type** — the road's classification. Arterials get repaved on different cycles than neighborhood streets.
- **From / To** — the segment's boundaries, usually cross streets. A whole street isn't one entry — it's many segments, each with its own score.

## Try it yourself

Find your street and check the PCI of the segment right in front of your house. Then check the street one block over. The difference is your neighborhood's pavement story — and it's the exact data the city uses to pick winners and losers in the repaving queue.
""",

"storm-sewer-lines-d97ab7e6": """## What this is

The storm sewer network — the pipes, channels, flumes, and inlets that carry rainwater from streets and neighborhoods out of the city. Every line with its material, size, slope, and elevation.

## Why it matters to you

Storm sewers are why your street doesn't become a river in a downpour. When they fail, you get flooding — and the flood doesn't care about property lines. This dataset is how engineers find where the weak points are: an undersized pipe, a too-gentle slope, a line in the wrong material. For homeowners in flood-prone areas, knowing where the storm infrastructure is (and reading its size and slope) explains a lot about why water behaves the way it does on your street.

## How to read this data

- **Material** — what the pipe is made of. Old materials corrode faster; this field is a first clue to a line's age and health.
- **Nominal Size** — the pipe's diameter. This is the capacity number: bigger pipes move more water.
- **Slope** — the gradient as a percentage. Water flows because of slope — too little and the pipe silts up, too much and it scours.
- **Upstream / Downstream Invert** — the elevation of the pipe at each end. Compare them and you get the drop that drives the flow.

## Try it yourself

Find the storm line nearest your home and note its size and slope. Next heavy rain, watch where the water actually goes — then see if your observations match what the data says the system should do. That's field-checking, and it's how the pros do it.
""",

"fire-stations-7f57d399": """## What this is

The locations of Oklahoma City fire stations — the fixed points the entire emergency response system is built around.

## Why it matters to you

Emergency response is a geometry problem: minutes are saved or lost based on where stations sit relative to where people live and work. This dataset is the anchor for that calculation — planners use station locations to model response times and decide where the next station should go. For you, it answers a practical question: how far is the nearest station from your home or business? (That number shows up in insurance pricing, too.)

## How to read this data

- **Facility Name** — despite the name, the catalog notes this is a *numeric identifier* of the station, not a friendly name. A good reminder to read field descriptions instead of assuming.
- **Facility Address** — where the station is. Cross-reference with ward and zoning maps and you can see how public safety facilities are distributed across the city.

## Try it yourself

Find the nearest station to your home and estimate the drive time. Then check the gaps — which part of town looks farthest from any station? That's where response times are longest, and it's the kind of observation this dataset exists to make.
""",
}

# Showcase card deks (slug -> teaser). Everything else uses description.
TEASERS = {
"public-infrastructure-projects-d5e6fb99": "How OKC plans and pays for the streets, bridges and parks around you — and why \u201cplanned\u201d and \u201cactual\u201d are two different dates.",
"council-wards-666b9654": "The map that decides who speaks for you at city hall — and why ward boundaries quietly change.",
"street-centerlines-0e041a93": "The invisible skeleton under every address in OKC — updated daily, used by 911, delivery apps, and you.",
"straight-zoning-388d1b1f": "The three-letter codes that decide what you can build where — and what \u201cstraight\u201d means next to \u201coverlay.\u201d",
"tax-increment-financing-districts-08ededb1": "The financial engine behind OKC\u2019s big developments — future taxes, borrowed today.",
"parks-fe9dc8e8": "Where OKC\u2019s green space lives — regional, community and neighborhood parks, with real acreage.",
"sidewalks-bc31068e": "The walkability map: every city-maintained sidewalk in OKC — and which ones were paid for with bonds.",
"building-footprints-2d4cd6c3": "Every building in OKC, drawn from the sky in 2020 — and the honest limits of aerial data.",
"bike-routes-5600dd31": "OKC\u2019s bike network, route by route — trail names, types, and what\u2019s still in progress.",
"pavement-condition-e80f59ff": "The bumpiness report card: every OKC street scored on the Pavement Condition Index.",
"storm-sewer-lines-d97ab7e6": "The hidden plumbing under OKC streets — how stormwater gets from your curb to the river.",
"fire-stations-7f57d399": "The response-time backbone: where OKC\u2019s fire stations sit — and what \u201cFacility Name\u201d really is.",
}

FEATURED = "public-infrastructure-projects-d5e6fb99"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def parse_frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m:
        return {}, text
    fm = {}
    for line in m.group(1).splitlines():
        if ":" not in line:
            continue
        key, _, raw = line.partition(":")
        key = key.strip()
        raw = raw.strip()
        if raw.startswith("[") and raw.endswith("]"):
            fm[key] = json.loads(raw)
        elif raw.startswith('"') and raw.endswith('"'):
            fm[key] = json.loads(raw)
        elif raw == "true":
            fm[key] = True
        elif raw == "false":
            fm[key] = False
        else:
            fm[key] = raw
    return fm, m.group(2)


def yaml_str(s):
    return json.dumps(str(s), ensure_ascii=False)


def yaml_list(lst):
    return "[" + ", ".join(yaml_str(x) for x in lst) + "]"


def build_frontmatter(fm, dictionary, teaser):
    out = ["---"]
    for key in ("title", "date", "description"):
        if key in fm:
            out.append(f"{key}: {yaml_str(fm[key])}")
    out.append(f"teaser: {yaml_str(teaser)}")
    for key in ("tags", "categories"):
        if key in fm and fm[key]:
            out.append(f"{key}: {yaml_list(fm[key])}")
    for key in ("source_url", "license", "dataset_id", "city", "site_url"):
        if key in fm:
            out.append(f"{key}: {yaml_str(fm[key])}")
    out.append("draft: false")
    if fm.get("featured"):
        out.append("featured: true")
    if dictionary:
        out.append("dictionary:")
        for item in dictionary:
            out.append(f"  - field: {yaml_str(item.get('field', ''))}")
            out.append(f"    description: {yaml_str(item.get('description', ''))}")
    out.append("---")
    return "\n".join(out)


def slug_of(fname):
    return os.path.splitext(fname)[0]


def truncate(text, limit):
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= limit:
        return text
    cut = text[:limit]
    if " " in cut:
        cut = cut.rsplit(" ", 1)[0]
    return cut.rstrip(" ,;:-") + "\u2026"


def main():
    with open(CATALOG_PATH) as f:
        catalog = json.load(f)
    by_title = {}
    for rec in catalog:
        by_title[re.sub(r"\s+", " ", rec["title"]).strip().lower()] = rec

    files = sorted(f for f in os.listdir(DATASETS_DIR) if f.endswith(".md"))
    stats = {"rewritten": 0, "showcase": 0, "unmatched": []}

    for fname in files:
        slug = slug_of(fname)
        path = os.path.join(DATASETS_DIR, fname)
        with open(path) as f:
            raw = f.read()
        fm, body = parse_frontmatter(raw)

        title = fm.get("title", slug)
        rec = by_title.get(re.sub(r"\s+", " ", title).strip().lower())
        if not rec:
            stats["unmatched"].append(title)
            # still add teaser so cards look right
            teaser = fm.get("description", "")
            with open(path, "w") as f:
                f.write(build_frontmatter(fm, fm.get("dictionary") or [], teaser) + "\n\n" + body)
            continue

        dictionary = [
            {"field": d.get("field", ""), "description": d.get("description", "")}
            for d in (rec.get("data_dictionary") or [])
        ]
        if slug in TEASERS:
            teaser = TEASERS[slug]
            desc = fm.get("description", "")
            # Guard against dictionary-text leaking into `description` on
            # showcase pages too: if it matches one of the catalog's own
            # field descriptions, rebuild from Suitable Use.
            catalog_descs = {d.get("description", "").strip() for rec in catalog for d in (rec.get("data_dictionary") or [])}
            if desc.strip() in catalog_descs:
                desc = (rec.get("suitable_use") or "").strip() or desc
        else:
            # Scripted pages: the ORIGINAL generated frontmatter sometimes had
            # dictionary text leaked into `description` — rebuild it from the
            # catalog's own Suitable Use line instead.
            desc = (rec.get("suitable_use") or "").strip() or fm.get("description", "")
            teaser = truncate(desc, 170)

        if slug in BODIES:
            new_body = BODIES[slug].strip()
            stats["showcase"] += 1
        else:
            suitable = (rec.get("suitable_use") or "").strip()
            interval = (rec.get("update_interval") or "").strip()
            limits = (rec.get("limitations_on_use") or "").strip()
            parts = ["## What this is", suitable or fm.get("description", "")]
            if interval:
                parts += ["", "## When it's updated", interval]
            parts += ["", "## Know before you use it",
                      limits or "The catalog lists no published limitations for this dataset."]
            new_body = "\n".join(parts)
            stats["rewritten"] += 1

        fm2 = dict(fm)
        if slug == FEATURED:
            fm2["featured"] = True
        else:
            fm2.pop("featured", None)
        if slug not in BODIES or desc != fm.get("description", ""):
            fm2["description"] = desc

        with open(path, "w") as f:
            f.write(build_frontmatter(fm2, dictionary, teaser) + "\n\n" + new_body + "\n")

    print(json.dumps(stats, indent=2))


if __name__ == "__main__":
    main()
