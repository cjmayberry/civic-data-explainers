#!/usr/bin/env python3
"""
build_manifest.py — manifest v2 builder + category single-source-of-truth.

The category for every dataset is decided HERE, in exactly one place, and
everything else (Hugo card badge, page header tag, cover filename, homepage
topic blocks, taxonomy) reads the result. This kills the old bug where the
card showed `categories[0]` from the catalog's raw tag order while the
manifest showed a different hand-derived category.

Decision rule (documented, deterministic, re-runnable):
  1. CATEGORY_OVERRIDES[slug] — explicit curated exceptions, each with a
     reason. Only used where the catalog's own tag order is misleading.
  2. else: first catalog `topics` entry mapped through TOPIC_ALIASES
     (Recreation -> Parks & Recreation, Utilities -> Infrastructure).
  3. else: "Default".

Tie-break philosophy: where the ArcGIS Hub tag order disagrees with the
city's own service folder (e.g. OpenData/Transportation), the city's folder
wins — it reflects the department that actually maintains the data.

Outputs:
  - hugo-site/static/img/manifest.json  (v2 per-dataset schema; image fields
    are filled in by fetch_images.py, content fields by the redraft script)
  - rewrites content/datasets/*.md frontmatter: `categories: ["<canonical>"]`
    (single element, keeps the Hugo taxonomy working) + `cover:` filename
  - renames cover art to {slug}--{category-slug}--{image_status}.{ext}

Usage:  python3 build_manifest.py [--catalog PATH]
"""
import json
import os
import re
import sys
import argparse
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.abspath(__file__))
DATASETS_DIR = os.path.join(ROOT, "hugo-site", "content", "datasets")
IMG_DIR = os.path.join(ROOT, "hugo-site", "static", "img")
COVERS_DIR = os.path.join(IMG_DIR, "covers")
CATALOG_PATH = os.path.join(ROOT, "okc_catalog.json")
MANIFEST_PATH = os.path.join(IMG_DIR, "manifest.json")
KNOWN_CATEGORIES = [
    "Transportation", "Infrastructure", "Licensing", "Government",
    "Finance", "Parks & Recreation", "Public Safety", "Default",
    "Environment", "Health", "Education", "Housing", "Economy",
]

# Catalog tag -> canonical category. Utilities data (trash/recycle zones,
# bulky waste) is city infrastructure; the old generator left it unmapped
# (those pages rendered with empty categories -> "Default").
TOPIC_ALIASES = {
    "Recreation": "Parks & Recreation",
    "Utilities": "Infrastructure",
    "Transportation": "Transportation",
    "Infrastructure": "Infrastructure",
    "Licensing": "Licensing",
    "Government": "Government",
    "Finance": "Finance",
    "Public Safety": "Public Safety",
}

# Curated exceptions. Each entry: slug -> (category, reason).
# The city's own ArcGIS service folder (in source_url) is the tie-breaker
# where Hub's tag order is misleading.
CATEGORY_OVERRIDES = {
    "snow-routes-a58d4715": (
        "Transportation",
        "City's own folder is OpenData/Transportation; snow routes are street-maintenance "
        "routes, not emergency response (Hub tags Public Safety first)."),
    "work-zones-ead80c5e": (
        "Transportation",
        "Road construction work zones; city folder OpenData/Transportation (Hub tags Public Safety first)."),
    "sidewalks-bc31068e": (
        "Transportation",
        "Pedestrian street infrastructure; city folder OpenData/Transportation."),
    "pavement-condition-e80f59ff": (
        "Transportation",
        "Street-condition (PCI) data; city folder OpenData/Transportation."),
    "street-centerlines-0e041a93": (
        "Transportation",
        "Address/street skeleton; city folder OpenData/Transportation_Streets."),
    "street-names-adea21af": (
        "Transportation",
        "Street naming data; city folder OpenData/Transportation_Streets."),
    "trail-projects-68777530": (
        "Infrastructure",
        "Capital construction projects; city folder OpenData/Infrastructure_Projects."),
    "pedestrian-projects-34783ad4": (
        "Infrastructure",
        "Capital construction projects; city folder OpenData/Infrastructure_Projects."),
    "bike-projects-b67f6cb2": (
        "Infrastructure",
        "Capital construction projects; city folder OpenData/Infrastructure_Projects."),
    "city-facilities-d5c5b7b2": (
        "Government",
        "City-owned public buildings/places; city folder OpenData/Government_Places "
        "(Hub tags Recreation first, which reads as parks)."),
    "city-trails-1e65b61d": (
        "Parks & Recreation",
        "Trail network maintained under the parks/recreation division; city folder OpenData/Recreation_Parks."),
    "hotel-motel-tax-b6e78aa9": (
        "Finance",
        "Tax dataset; city folder OpenData/Finance (Hub tags Licensing first)."),
    "tax-increment-financing-districts-08ededb1": (
        "Finance",
        "TIF = tax-financing zones; city folder OpenData/Finance."),
    "fire-stations-7f57d399": (
        "Public Safety",
        "Hub tag order AND city folder agree (Public_Safety); old manifest said Government."),
    "police-stations-fdb1ea86": (
        "Public Safety",
        "Hub tag order AND city folder agree (Public_Safety); old manifest said Government."),
    "storm-siren-sectors-58b572ce": (
        "Public Safety",
        "Hub tag order AND city folder agree (Public_Safety); old manifest said Government."),
    # --- v4 12-category taxonomy (2026-08-10, docs/content-v4-spec.md) ---
    "waterbodies-a6b9c703": ("Environment",
        "Natural water bodies (lakes/ponds) — natural system, per v4; was Infrastructure."),
    "waterways-7107d3b8": ("Environment",
        "Rivers/streams — natural system, per v4; was Infrastructure."),
    "vegetation-points-1fcba99b": ("Environment",
        "Trees/shrubs land-cover — natural system, per v4; was Infrastructure."),
    "vegetation-polygons-a4b7be23": ("Environment",
        "Tree-canopy land-cover — natural system, per v4; was Infrastructure."),
    "impervious-surfaces-ad208d72": ("Environment",
        "Paved/water-resistant land cover — environmental land-cover assessment, per v4; was Infrastructure."),
    "parks-impact-fees-benefit-areas-08f4c8d6": ("Finance",
        "Development impact fees — a financing mechanism, not a permit (Hub tags Licensing); per v4 → Finance."),
    "parks-impact-fees-existing-local-service-b8d5a300": ("Finance",
        "Development impact-fee exemption areas — financing mechanism, per v4 → Finance."),
    "streets-development-program-benefit-areas-5377697e": ("Finance",
        "Streets development program benefit areas — financing/benefit districts, per v4 → Finance."),
    "land-documents-fd9dbc81": ("Government",
        "Legal land records (deeds/easements/ordinances) — public legal records, per v4 → Government."),
    # --- Memphis v4 12-category taxonomy (2026-08-11) ---
    "bike-facilities-existing-and-programmed-eec74e9a": ("Transportation", "Bike facilities — mobility, per v4."),
    "city-council-districts-cfc3ba75": ("Government", "Council districts — governance/representation."),
    "city-council-super-districts-a06f2c70": ("Government", "Council super-districts — governance/representation."),
    "city-of-memphis-parks-92001696": ("Parks & Recreation", "Parks."),
    "downtown-memphis-commission-boundaries-a5088e8d": ("Government", "DMC district boundary — governance."),
    "downtown-memphis-commission-projects-b244cada": ("Economy", "DMC development projects — economic development."),
    "dpd-building-permits-3018811a": ("Licensing", "Building permits — permit/registration."),
    "economic-development-growth-engine-edge-bonds-31650a2c": ("Economy", "EDGE economic-development bonds."),
    "economic-development-growth-engine-edge-loans-71211088": ("Economy", "EDGE economic-development loans."),
    "economic-development-growth-engine-edge-other-pr-471e8b88": ("Economy", "EDGE other economic-development programs."),
    "economic-development-growth-engine-edge-pilots-7f19e39d": ("Economy", "EDGE PILOTs — economic-development tax agreements."),
    "economic-development-growth-engine-edge-tifs-0a78f310": ("Economy", "EDGE TIFs — economic-development financing."),
    "hcd-property-investments-41f0fa52": ("Housing", "Housing & Community Development property investments."),
    "mata-stops-6892a5f9": ("Transportation", "Transit stops."),
    "memphis-3-0-planning-districts-7855c7be": ("Government", "Planning districts — land-use governance."),
    "memphis-community-centers-31fee209": ("Parks & Recreation", "Community/recreation centers."),
    "memphis-employment-data-f530c6a3": ("Economy", "Employment — jobs/economy."),
    "memphis-jurisdiction-boundary-a4b1d1fc": ("Government", "City jurisdiction boundary."),
    "memphis-medical-district-collaborative-boundarie-d9d67533": ("Government", "Medical district boundary — governance."),
    "memphis-msa-counties-b349826e": ("Government", "MSA county boundaries — geography."),
    "memphis-public-libraries-77458ce9": ("Education", "Public libraries."),
    "memphis-zip-codes-49d6b5e5": ("Government", "ZIP-code geography."),
    "mfd-fire-stations-84f2c8ed": ("Public Safety", "Fire stations."),
    "mpd-district-areas-cf62a73a": ("Public Safety", "Police district areas."),
    "mpd-precinct-areas-0334e3fb": ("Public Safety", "Police precinct areas."),
    "mpd-station-location-13adc19e": ("Public Safety", "Police station locations."),
    "mpd-wards-cfbaeae2": ("Public Safety", "Police wards."),
    "shelby-co-tract-acs-demo-5y-2024-9606abac": ("Government", "ACS demographic data by tract — census/socioeconomic reference, per v4."),
    "shelby-county-census-tracts-72568279": ("Government", "Census tracts — geography."),
    "shelby-county-zip-codes-d21250ed": ("Government", "ZIP-code geography."),
    "solid-waste-areas-2c82a883": ("Infrastructure", "Waste-collection service areas — public services infra."),
}

# Showcase pages carry hand-written bodies (regenerate_content.py BODIES)
HAND_AUTHORED = {
    "public-infrastructure-projects-d5e6fb99", "council-wards-666b9654",
    "street-centerlines-0e041a93", "straight-zoning-388d1b1f",
    "tax-increment-financing-districts-08ededb1", "parks-fe9dc8e8",
    "sidewalks-bc31068e", "building-footprints-2d4cd6c3",
    "bike-routes-5600dd31", "pavement-condition-e80f59ff",
    "storm-sewer-lines-d97ab7e6", "fire-stations-7f57d399",
}
HAND_AUTHORED_MODEL = "manual:regenerate_content.py-BODIES (hand-authored 2026-06-10)"

# ---------------------------------------------------------------------------
# System A — inquiry (address/street lookup)
# A dataset is inquiry-capable when its service carries a real text field the
# reader would plausibly type (street name, address, facility name). Each
# entry: search = the field matched against input, field = the value returned
# (the "so what" of the lookup), label = box prompt, extra = extra display
# fields. Excluded on purpose: zoning/ward layers (no address field — need a
# spatial/parcel lookup, v2 candidate), lot/block tables, survey points,
# vegetation, boundaries, and name-only layers (trails, waterbodies — those
# are System B's named-place enrichment territory).
INQUIRY = {
    "pavement-condition-e80f59ff": {"search": "XSTREET_NA", "field": "PCICurrent",
        "label": "Find your street's pavement score", "extra": ["BEGDESC", "ENDDESC"]},
    "street-centerlines-0e041a93": {"search": "FNAME", "field": "STREETCLASS",
        "label": "Look up a street's classification", "extra": ["FDPRE", "FTYPE", "LEFTADD1"]},
    "street-names-adea21af": {"search": "StreetName", "field": "StreetName",
        "label": "Look up a street's official name", "extra": ["StreetPrefix", "StreetSuffix"]},
    "snow-routes-a58d4715": {"search": "location1", "field": "Quadarant",
        "label": "Is your street a snow route?", "extra": ["location2"]},
    "work-zones-ead80c5e": {"search": "Worklocation", "field": "Worktype",
        "label": "Check for active work near a street", "extra": ["Startdate", "Enddate"]},
    "adopted-streets-0ad77166": {"search": "Adopted_Street", "field": "Adopting_Organization",
        "label": "Is your street adopted — and by whom?", "extra": []},
    "garage-sales-a2b13b6d": {"search": "Address", "field": "Permit_Date",
        "label": "Check a garage sale permit", "extra": []},
    "emergency-responses-01c97e29": {"search": "Address", "field": "Call_Type",
        "label": "See recent calls near an address", "extra": ["Reported_Time"]},
    "city-facilities-d5c5b7b2": {"search": "FacilityName", "field": "FacilityType",
        "label": "Look up a city facility", "extra": ["Address"]},
    "park-facilities-ceaabc8e": {"search": "Facility_Name", "field": "Facility_Type",
        "label": "Look up a park facility", "extra": ["PK_LOCATION", "Address"]},
    "fire-stations-7f57d399": {"search": "STATION_ADDR", "field": "STATION_ADDR",
        "label": "Find a fire station by address", "extra": ["STATION_NO"]},
    "police-stations-fdb1ea86": {"search": "Facility", "field": "Address",
        "label": "Look up a police station", "extra": []},
    "land-documents-fd9dbc81": {"search": "Address", "field": "IndexType",
        "label": "Check documents recorded at an address", "extra": ["Number", "Grantor"]},
    "hotel-motel-tax-b6e78aa9": {"search": "LegalName", "field": "Sector",
        "label": "Check a hotel/motel registration", "extra": ["Address", "Certificate"]},
}

# ---------------------------------------------------------------------------
# System B — named-place enrichment (images + verified name origins)
ENRICHMENT_DATASETS = {
    "city-trails-1e65b61d", "park-facilities-ceaabc8e", "city-facilities-d5c5b7b2",
    "fire-stations-7f57d399", "police-stations-fdb1ea86", "parks-fe9dc8e8",
}


def category_slug(category):
    return re.sub(r"[^a-z0-9]+", "-", category.lower()).strip("-")


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


def build_frontmatter(fm, category, cover, inquiry=None):
    """Emit frontmatter with categories reduced to the canonical single element.
    inquiry = the INQUIRY dict entry (or None) for the System A lookup box."""
    out = ["---"]
    for key in ("title", "date", "description"):
        if key in fm:
            out.append(f"{key}: {yaml_str(fm[key])}")
    if "teaser" in fm:
        out.append(f"teaser: {yaml_str(fm['teaser'])}")
    if "tags" in fm and fm["tags"]:
        out.append(f"tags: {yaml_list(fm['tags'])}")
    out.append(f"categories: {yaml_list([category])}")
    out.append(f"cover: {yaml_str(cover)}")
    if inquiry:
        out.append(f"inquiry_enabled: true")
        out.append(f"inquiry_search: {yaml_str(inquiry['search'])}")
        out.append(f"inquiry_field: {yaml_str(inquiry['field'])}")
        out.append(f"inquiry_label: {yaml_str(inquiry['label'])}")
        if inquiry.get("extra"):
            out.append(f"inquiry_extra: {yaml_list(inquiry['extra'])}")
    for key in ("source_url", "license", "dataset_id", "city", "site_url",
                "map_link", "geojson_url", "maintained_by"):
        if key in fm:
            out.append(f"{key}: {yaml_str(fm[key])}")
    out.append("draft: false")
    if fm.get("featured"):
        out.append("featured: true")
    dictionary = fm.get("dictionary") or []
    if dictionary:
        out.append("dictionary:")
        for item in dictionary:
            out.append(f"  - field: {yaml_str(item.get('field', ''))}")
            out.append(f"    description: {yaml_str(item.get('description', ''))}")
    out.append("---")
    return "\n".join(out)


def classify_content(body, slug):
    """content_status from the current body: does it follow the 4-part shape?"""
    if slug in HAND_AUTHORED:
        return "drafted", HAND_AUTHORED_MODEL
    if re.search(r"try it yourself", body, re.I):
        return "drafted", "unknown:follows-shape-v1"
    return "stub", None


def parse_dictionary(raw):
    """Parse the `dictionary:` YAML block from a content file's frontmatter.
    The generic line parser can't handle the nested list, so this does it
    properly:  `- field: "X"` / `description: "Y"` pairs."""
    out = []
    m = re.search(r"^---\n(.*?)\n---", raw, re.S)
    if not m:
        return out
    lines = m.group(1).splitlines()
    in_dict = False
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.strip() == "dictionary:":
            in_dict = True
            i += 1
            continue
        if in_dict:
            if line.startswith("  - field:"):
                field = line.split(":", 1)[1].strip().strip('"')
                desc = ""
                if i + 1 < len(lines) and lines[i + 1].strip().startswith("description:"):
                    desc = lines[i + 1].split(":", 1)[1].strip().strip('"')
                    i += 1
                out.append({"field": field, "description": desc})
            elif line.strip() and not line.startswith("    "):
                in_dict = False
        i += 1
    return out


def main():
    global DATASETS_DIR, IMG_DIR, COVERS_DIR, MANIFEST_PATH
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", default=CATALOG_PATH,
                        help="Catalog JSON to read topics from (default: okc_catalog.json). "
                             "Point at a city catalog (e.g. memphis_catalog.json) for city #2.")
    parser.add_argument("--content-dir", default=DATASETS_DIR,
                        help="Content dir for the target city (default: hugo-site/content/datasets).")
    parser.add_argument("--static-dir", default=IMG_DIR,
                        help="Static img dir for the target city (default: hugo-site/static/img).")
    parser.add_argument("--city-id", default="okc",
                        help="City slug key (frontmatter city:), e.g. okc, memphis")
    parser.add_argument("--city-name", default="Oklahoma City",
                        help="Display city name written into the manifest")
    parser.add_argument("--category-map", default="",
                        help="JSON file of {raw_label: display_label} for cities without "
                             "TOPIC_ALIASES/CATEGORY_OVERRIDES (from content/taxonomy.py)")
    args = parser.parse_args()
    DATASETS_DIR = args.content_dir
    IMG_DIR = args.static_dir
    COVERS_DIR = os.path.join(IMG_DIR, "covers")
    MANIFEST_PATH = os.path.join(IMG_DIR, "manifest.json")
    CITY_ID = args.city_id
    CITY_NAME = args.city_name
    CATEGORY_MAP = {}
    if args.category_map:
        CATEGORY_MAP = json.load(open(args.category_map))

    with open(args.catalog) as f:
        catalog = json.load(f)
    by_title = {}
    for rec in catalog:
        by_title[re.sub(r"\s+", " ", rec["title"]).strip().lower()] = rec

    os.makedirs(COVERS_DIR, exist_ok=True)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    # carry forward state owned by other steps (content redraft, image fetch)
    old_by_slug = {}
    if os.path.exists(MANIFEST_PATH):
        try:
            with open(MANIFEST_PATH) as f:
                for d in json.load(f).get("datasets", []):
                    old_by_slug[d["slug"]] = d
        except Exception:
            old_by_slug = {}

    datasets = []
    mapping_rows = []
    renamed = []
    errors = []

    files = sorted(f for f in os.listdir(DATASETS_DIR) if f.endswith(".md"))
    for fname in files:
        slug = os.path.splitext(fname)[0]
        path = os.path.join(DATASETS_DIR, fname)
        with open(path, encoding="utf-8") as f:
            raw = f.read()
        fm, body = parse_frontmatter(raw)

        rec = by_title.get(re.sub(r"\s+", " ", fm.get("title", slug)).strip().lower())
        topics = (rec or {}).get("topics", []) or []

        # ---- THE one category decision ----
        # For cities with their own TOPIC_ALIASES (OKC), the alias map +
        # CATEGORY_OVERRIDES stay authoritative. Other cities pass an
        # LLM-derived category_map (content/taxonomy.py) via --category-map.
        if slug in CATEGORY_OVERRIDES:
            category, reason = CATEGORY_OVERRIDES[slug]
        else:
            reason = None
            category = "Default"
            if CATEGORY_MAP:
                for t in topics:
                    c = CATEGORY_MAP.get(t)
                    if c:
                        category = c
                        break
            else:
                for t in topics:
                    c = TOPIC_ALIASES.get(t)
                    if c:
                        category = c
                        break

        old = old_by_slug.get(slug, {})
        if old.get("content_status"):
            content_status, content_model = old["content_status"], old.get("content_model")
        else:
            content_status, content_model = classify_content(body, slug)
        image_status = old.get("image_status", "cover_only")
        image_source = old.get("image_source", "svg_cover")
        image_note = old.get("image_note")
        image_file = old.get("image_file") or f"{slug}--{category_slug(category)}--cover_only.svg"

        # file rename: ONLY for first-time naming (no carried state) — the
        # image pipeline owns files once it has run
        if not old.get("image_file"):
            new_name = f"{slug}--{category_slug(category)}--cover_only.svg"
            for old_cov in os.listdir(COVERS_DIR):
                if old_cov.startswith(slug + "--") or old_cov == slug + ".svg":
                    if old_cov != new_name:
                        os.rename(os.path.join(COVERS_DIR, old_cov), os.path.join(COVERS_DIR, new_name))
                        renamed.append((slug, old_cov, new_name))
            image_file = new_name

        # frontmatter rewrite: single canonical category + cover field
        # rebuild the dictionary list properly (the generic parser can't
        # handle the nested YAML block) and backfill pages that lack it —
        # the 12 hand-authored showcase pages were written without one
        if not isinstance(fm.get("dictionary"), list):
            fm["dictionary"] = parse_dictionary(raw)
        if not fm.get("dictionary") and rec and (rec.get("data_dictionary") or []):
            fm["dictionary"] = [
                {"field": x.get("field", ""), "description": x.get("description", "")}
                for x in rec["data_dictionary"]
            ]
        # repair the old dictionary-text leak in `description` (some pages'
        # description was overwritten with a field definition's text)
        if rec:
            catalog_descs = {
                d.get("description", "").strip()
                for r2 in catalog
                for d in (r2.get("data_dictionary") or [])
            }
            if (fm.get("description") or "").strip() in catalog_descs:
                fm["description"] = (rec.get("suitable_use") or "").strip() or fm.get("description")
        cover_path = os.path.join(COVERS_DIR, image_file)
        cover_ref = f"covers/{image_file}" if os.path.exists(cover_path) else ""
        fm2 = build_frontmatter(fm, category, cover_ref, INQUIRY.get(slug))
        with open(path, "w", encoding="utf-8") as f:
            f.write(fm2 + "\n\n" + body)

        datasets.append({
            "slug": slug,
            "title": fm.get("title", slug),
            "city": CITY_NAME,
            "city_slug": CITY_ID,
            "display_category": category,
            "category": category,
            "content_status": content_status,
            "content_model": content_model,
            "image_status": image_status,
            "image_source": image_source,
            "image_file": image_file,
            "image_note": image_note,
            "schema": old.get("schema"),
            "source_url": fm.get("source_url"),
            "inquiry_enabled": slug in INQUIRY,
            "inquiry_search_field": INQUIRY[slug]["search"] if slug in INQUIRY else None,
            "inquiry_field": INQUIRY[slug]["field"] if slug in INQUIRY else None,
            "inquiry_label": INQUIRY[slug]["label"] if slug in INQUIRY else None,
            "inquiry_extra": INQUIRY[slug]["extra"] if slug in INQUIRY else [],
            "enrichment_status": old.get("enrichment_status", "pending" if slug in ENRICHMENT_DATASETS else None),
            "last_updated": now,
        })
        mapping_rows.append((slug, fm.get("title", slug), topics, category, reason))

    # ---- write manifest v2 ----
    old = {}
    if os.path.exists(MANIFEST_PATH):
        try:
            with open(MANIFEST_PATH) as f:
                old = json.load(f)
        except Exception:
            old = {}

    manifest = {
        "hero": old.get("hero"),
        "categories": old.get("categories", {}),
        "mapbox_enabled": bool(os.environ.get("MAPBOX_TOKEN", "").strip()),
        "generated_at": now,
        "dataset_schema": 2,
        "datasets": datasets,
    }
    with open(MANIFEST_PATH, "w") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    # ---- report ----
    print(f"# manifest v2 written: {len(datasets)} datasets -> {MANIFEST_PATH}")
    print(f"# covers renamed: {len(renamed)}")
    if errors:
        print("# ERRORS:")
        for e in errors:
            print("  ", e)
    print("\n# Category mapping (slug | title | hub-topics | canonical | reason-if-override)")
    for slug, title, topics, category, reason in sorted(mapping_rows):
        flag = f"  <-- {reason}" if reason else ""
        print(f"{slug:55s} | {title[:32]:32s} | {str(topics):42s} | {category}{flag}")
    from collections import Counter
    print("\n# Category counts:", dict(Counter(c for _, _, _, c, _ in mapping_rows)))


if __name__ == "__main__":
    main()
