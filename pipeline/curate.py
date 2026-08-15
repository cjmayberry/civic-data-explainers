#!/usr/bin/env python3
"""Curate a raw extracted catalog down to a bounded, resident-facing set for a nightly add.

The nightly state+capital job must not scaffold/draft every queryable service
(Kansas = 460). This filters to high-value, resident-facing datasets and caps
the count so a nightly add stays inside the time/token budget.

Drop rules (case-insensitive, matched against title + description):
  - county-scope records (imagery pull risk; full-state is TBs)
  - imagery / basemap / remote-sensing layers (NAIP, aerial, ortho, webmercator,
    satellite, digital-elevation, lidar, point cloud, tile cache, basemap)
  - survey / geodetic / control / benchmark layers (no resident-facing meaning)
  - server / metadata / service-definition records (not data)

Usage:
  python3 pipeline/curate.py --catalog <in.json> --out <filtered.json>
      [--cap N] [--level state|capital] [--keep-slugs a,b,c]
"""
import argparse
import json
import os
import re

IMAGERY_RE = re.compile(
    r"\b(naip|aerial|ortho|orthophot|web ?mercator|imagery|satellite|"
    r"digital elevation|elevation model|\blidar\b|point cloud|basemap|"
    r"tile cache|image service|historical imagery|scanned map|topographic map)\b",
    re.I)
SURVEY_RE = re.compile(
    r"\b(survey control|control point|benchmark|geodetic|datum|"
    r"monument|primary control|secondary control)\b", re.I)
SERVER_RE = re.compile(
    r"\b(server access|data server|web service|service definition|"
    r"metadata|map server|feature server access|access point)\b", re.I)
COUNTY_SCOPE = "county"

def text(rec):
    return " ".join(filter(None, [rec.get("title"), rec.get("description_raw") or rec.get("suitable_use") or ""])).lower()

def keep(rec, force_keep):
    slug = rec.get("slug") or rec.get("name") or rec.get("guid") or ""
    if slug in force_keep:
        return True
    if rec.get("scope") == COUNTY_SCOPE:
        return False
    t = text(rec)
    if IMAGERY_RE.search(t):
        return False
    if SURVEY_RE.search(t):
        return False
    if SERVER_RE.search(t):
        return False
    return True

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--catalog", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--cap", type=int, default=120)
    ap.add_argument("--keep-slugs", default="")
    args = ap.parse_args()

    data = json.load(open(args.catalog))
    recs = data if isinstance(data, list) else data.get("datasets", [])
    force = {s.strip() for s in args.keep_slugs.split(",") if s.strip()}

    kept = [r for r in recs if keep(r, force)]
    dropped = [r for r in recs if not keep(r, force)]

    # cap: if still over, prefer records with a substantive description (more
    # resident-facing) over thin/technical ones — but FIRST preserve the
    # service_url and item_type that the extractor resolved so downstream
    # stages (scaffold_city.py) don't drop every record as "no service".
    if len(kept) > args.cap:
        kept.sort(key=lambda r: (len(r.get("description_raw") or r.get("suitable_use") or "") > 40,
                                 len(r.get("data_dictionary") or []) > 0,
                                 -(r.get("title") and len(r["title"]) or 0)), reverse=True)
        kept = kept[:args.cap]

    # preserve source order
    order = {r.get("guid"): i for i, r in enumerate(recs)}
    kept.sort(key=lambda r: order.get(r.get("guid"), 0))

    json.dump(kept, open(args.out, "w"), indent=1, ensure_ascii=False)
    print(f"curated: {len(recs)} -> {len(kept)} (cap {args.cap})")
    print(f"  dropped: {len(dropped)} (county-scope/imagery/survey/server)")

    # breakdown of kept by first topic
    from collections import Counter
    c = Counter((r.get("topics") or ["(none)"])[0] for r in kept)
    print("  kept by first topic:")
    for t, n in c.most_common(12):
        print(f"    {n:3d}  {t}")

if __name__ == "__main__":
    main()
