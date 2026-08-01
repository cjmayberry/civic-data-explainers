#!/usr/bin/env python3
"""
enrich.py — System B: named-place enrichment (photos + verified name origins).

For each named-place dataset in the manifest (City Trails, Parks, Park
Facilities, City Facilities, Police Stations):
  1. Fetch records from the dataset's ArcGIS service.
  2. Filter to records with REAL proper names (generic labels skipped).
  3. Per record: Wikipedia search "<name> Oklahoma City" -> article summary
     (lead image) -> wikibase item -> Wikidata claim P138 (named after).
  4. Write hugo-site/data/enrichment/<slug>.json with per-record status
     (pending | found | not_available) and update the manifest aggregate.

HARD RULE (name origins): the "named after" note comes ONLY from structured
Wikidata P138 claims, with a link to the source entity. No inference, no
local lore, no plausible-sounding guesses. If it can't be verified, the
field is omitted from the page entirely — the image stands alone.

Accepted-match rule (avoids wrong-place matches like Missouri's Katy Trail):
the top Wikipedia hit must (a) match the record's name loosely, and
(b) its summary/description must mention Oklahoma (or OKC). Everything is
deterministic and auditable via the stored titles/links.

Usage:  python3 content/enrich.py [--limit 40] [--only slug,...]
"""
import argparse
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENRICH_DIR = os.path.join(ROOT, "hugo-site", "data", "enrichment")
MANIFEST_PATH = os.path.join(ROOT, "hugo-site", "static", "img", "manifest.json")
UA = {"User-Agent": "CivicDataExplained/0.3 (civic explainer enrichment; no bulk scraping)"}
SLEEP = 0.25

# dataset -> name field that holds the proper place name
DATASET_NAME_FIELD = {
    "city-trails-1e65b61d": "TrailName",
    "parks-fe9dc8e8": "Name",
    "park-facilities-ceaabc8e": "PK_LOCATION",
    "city-facilities-d5c5b7b2": "FacilityName",
    "police-stations-fdb1ea86": "Facility",
    # fire-stations excluded: records carry numeric identifiers, not names
}

GENERIC_NAMES = {
    "", "park", "trail", "trails", "unknown", "none", "n/a", "na", "tbd",
    "other", "various", "misc", "facility", "station", "green space",
}


def http_json(url, retries=2):
    for i in range(retries + 1):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=45) as r:
                return json.loads(r.read())
        except Exception as e:
            if i == retries:
                return {"__error__": str(e)}
            time.sleep(1.0)
    return {"__error__": "unreachable"}


def query_features(source_url, name_field, cap=1500):
    url = source_url.rstrip("/")
    base = re.sub(r"/FeatureServer/\d+$", "/FeatureServer", url)
    m = re.search(r"/FeatureServer/(\d+)$", url)
    primary = int(m.group(1)) if m else 0
    q = f"{base}/{primary}/query?" + urllib.parse.urlencode({
        "where": "1=1", "f": "geojson", "outFields": "*",
        "resultRecordCount": str(cap),
    })
    data = http_json(q)
    if "__error__" in data:
        return [], f"query failed: {data['__error__']}"
    feats = data.get("features", [])
    # try sibling layers if the primary one returns no named records
    if not feats:
        for layer in range(4):
            if layer == primary:
                continue
            q2 = f"{base}/{layer}/query?" + urllib.parse.urlencode({
                "where": "1=1", "f": "geojson", "outFields": "*", "resultRecordCount": str(cap)})
            data2 = http_json(q2)
            if "features" in data2 and data2["features"]:
                feats = data2["features"]
                break
    names, seen = [], set()
    for f in feats:
        p = f.get("properties") or {}
        name = (p.get(name_field) or "").strip()
        if not name or name.lower() in GENERIC_NAMES:
            continue
        if re.fullmatch(r"[\d\s\-]+", name):
            continue
        if len(name) < 4:
            continue
        key = name.lower()
        if key in seen:
            continue
        seen.add(key)
        names.append(name)
    return names, None


def strong_match(name, title, summary):
    """A record is only enriched when the article is ABOUT that exact place,
    in Oklahoma City. Two requirements, both mandatory:
      (1) name containment both ways — the normalized article title must
          contain the full record name, or the record name must contain the
          title ("South River Trail" -> "South River Trail (Oklahoma City)";
          never "Cimarron River" because it shares the token 'river').
      (2) the article must explicitly say "Oklahoma City" (or OKC) — not just
          "Oklahoma" (a park in Tulsa would pass 'oklahoma')."""
    n = re.sub(r"\s*\(.*?\)\s*", " ", name).lower().strip()
    t = title.lower().strip()
    n = re.sub(r"\s+", " ", n)
    t = re.sub(r"\s+", " ", t)
    if not (t in n or n in t):
        return False
    text = ((summary.get("extract") or "") + " " + (summary.get("description") or "")).lower()
    return "oklahoma city" in text or "okc" in text


def wikipedia_lookup(name):
    """Return (article_title, summary_dict) or (None, None)."""
    search = http_json("https://en.wikipedia.org/w/api.php?" + urllib.parse.urlencode({
        "action": "query", "list": "search", "format": "json",
        "srsearch": f"{name} Oklahoma City", "srlimit": "8", "srprop": "snippet",
    }))
    hits = (search.get("query") or {}).get("search") or []
    if not hits:
        return None, None
    best = None
    for h in hits:
        title = h.get("title", "")
        if not title:
            continue
        summary = http_json("https://en.wikipedia.org/api/rest_v1/page/summary/"
                            + urllib.parse.quote(title.replace(" ", "_")))
        if "__error__" in summary or summary.get("type") == "disambiguation":
            continue
        if not strong_match(name, title, summary):
            continue
        best = (title, summary)
        break
    if best is None:
        return None, None
    return best


def wikidata_origin(wiki_title):
    """Return (named_after_label, named_after_link) via Wikidata P138, or (None, None)."""
    pp = http_json("https://en.wikipedia.org/w/api.php?" + urllib.parse.urlencode({
        "action": "query", "prop": "pageprops", "ppprop": "wikibase_item",
        "titles": wiki_title, "format": "json"}))
    pages = (pp.get("query") or {}).get("pages") or {}
    qid = None
    for pg in pages.values():
        qid = (pg.get("pageprops") or {}).get("wikibase_item")
        if qid:
            break
    if not qid:
        return None, None
    ent = http_json("https://www.wikidata.org/w/api.php?" + urllib.parse.urlencode({
        "action": "wbgetentities", "ids": qid, "props": "claims", "format": "json"}))
    claims = ((ent.get("entities") or {}).get(qid) or {}).get("claims") or {}
    for claim in claims.get("P138", []):
        dv = ((claim.get("mainsnak") or {}).get("datavalue") or {}).get("value") or {}
        target = dv.get("id")
        if not target:
            continue
        lbl = http_json("https://www.wikidata.org/w/api.php?" + urllib.parse.urlencode({
            "action": "wbgetentities", "ids": target, "props": "labels", "languages": "en",
            "format": "json"}))
        label = (((lbl.get("entities") or {}).get(target) or {}).get("labels") or {}).get("en", {}).get("value")
        if label:
            return label, f"https://www.wikidata.org/wiki/{target}"
    return None, None


def enrich_dataset(slug, source_url, name_field, limit):
    out_path = os.path.join(ENRICH_DIR, slug + ".json")
    prev = {}
    if os.path.exists(out_path):
        try:
            prev = {r["name"]: r for r in json.load(open(out_path))["records"]}
        except Exception:
            prev = {}

    names, err = query_features(source_url, name_field)
    if err:
        print(f"  ! {slug}: {err}", file=sys.stderr)
        return None
    print(f"  {slug}: {len(names)} named records (field {name_field})", file=sys.stderr)

    records = []
    pending = [n for n in names if n not in prev or prev[n].get("status") == "pending"]
    todo = pending[:limit]
    for name in names:
        if name in prev and prev[name].get("status") != "pending":
            records.append(prev[name])
            continue
        if name not in todo:
            records.append({"name": name, "status": "pending"})
            continue
        hit, summary = wikipedia_lookup(name)
        time.sleep(SLEEP)
        if not hit:
            records.append({"name": name, "status": "not_available", "reason": "no verified Oklahoma match"})
            continue
        rec = {
            "name": name,
            "status": "found",
            "wikipedia_title": hit,
            "wikipedia_link": summary.get("content_urls", {}).get("desktop", {}).get("page")
                              or f"https://en.wikipedia.org/wiki/{hit.replace(' ', '_')}",
        }
        img = (summary.get("originalimage") or {}).get("source")
        if img:
            rec["image"] = img
        na, na_link = wikidata_origin(hit)
        time.sleep(SLEEP)
        if na:
            rec["named_after"] = na
            rec["named_after_link"] = na_link
        records.append(rec)
        print(f"    {'✓' if rec['status']=='found' else '·'} {name[:44]:46s} "
              f"{('img' if 'image' in rec else '')} {'origin:' + rec['named_after'][:24] if 'named_after' in rec else ''}", file=sys.stderr)

    os.makedirs(ENRICH_DIR, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump({"slug": slug, "name_field": name_field, "records": records}, f, indent=1, ensure_ascii=False)

    found = sum(1 for r in records if r["status"] == "found")
    avail = sum(1 for r in records if r["status"] == "not_available")
    pend = sum(1 for r in records if r["status"] == "pending")
    return {"total": len(records), "found": found, "not_available": avail, "pending": pend}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit", type=int, default=40, help="max NEW records researched per dataset per run")
    parser.add_argument("--only", help="comma-separated slugs to process")
    args = parser.parse_args()

    with open(MANIFEST_PATH) as f:
        manifest = json.load(f)
    by_slug = {d["slug"]: d for d in manifest["datasets"]}

    report = {}
    for slug, name_field in DATASET_NAME_FIELD.items():
        if args.only and slug not in args.only.split(","):
            continue
        d = by_slug.get(slug)
        if not d:
            continue
        raw = open(os.path.join(ROOT, "hugo-site", "content", "datasets", slug + ".md")).read()
        m = re.search(r'^source_url:\s*"(.*)"\s*$', raw, re.M)
        source_url = m.group(1) if m else None
        if not source_url:
            continue
        stats = enrich_dataset(slug, source_url, name_field, args.limit)
        if stats:
            d["enrichment_status"] = "found" if stats["found"] else ("not_available" if stats["not_available"] else "pending")
            report[slug] = stats

    with open(MANIFEST_PATH, "w") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
