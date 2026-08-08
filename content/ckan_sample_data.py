#!/usr/bin/env python3
"""ckan_sample_data.py — write real-record sample tables for CKAN cities.

The ArcGIS path (fetch_images.save_sample_records) queries FeatureServer
GeoJSON. CKAN cities have no FeatureServer; their datastore_search API
returns records directly. This mirrors the same output contract:
hugo-site/data/datasets/<slug>.json = {"fields": [...], "rows": [...]}
rendered as the "From the source — real records" table on each page.

Usage:
  python3 content/ckan_sample_data.py --manifest hugo-site/static/lisbon/manifest.json
"""
import argparse
import json
import os
import re
import sys
import time
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UA = {"User-Agent": "CivicDataExplained/0.6 (ckan sample records)"}
EXCLUDE_FIELD = re.compile(
    r"^(_id|objectid|fid|globalid|shape|shape_length|shape_area|length|area|"
    r"created_|edited_|geom|st_|esri_|geometry|coordinates|coordenadas|"
    r"geojsoncoordinates|geojson)$", re.I)


def http_json(url, timeout=30):
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout) as r:
            return json.loads(r.read())
    except Exception as e:
        return {"__error__": str(e)}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--out", default=os.path.join(ROOT, "hugo-site", "data", "datasets"),
                    help="hugo-site/data/datasets (shared across cities)")
    ap.add_argument("--sleep", type=float, default=0.2)
    args = ap.parse_args()

    manifest = json.load(open(args.manifest))
    os.makedirs(args.out, exist_ok=True)
    ok, skipped = [], []
    for d in manifest.get("datasets", []):
        url = d.get("source_url") or ""
        if "datastore_search" not in url:
            skipped.append((d["slug"], "not a datastore URL"))
            continue
        data = http_json(url.rstrip("/") + "&limit=12")
        time.sleep(args.sleep)
        if "__error__" in data or not data.get("success"):
            err = data.get("__error__") if "__error__" in data else (data.get("error") or "query failed")
            skipped.append((d["slug"], str(err) if not isinstance(err, dict) else str(err.get("message", err))))
            continue
        result = data.get("result") or {}
        records = result.get("records") or []
        if not records:
            skipped.append((d["slug"], "no records"))
            continue
        keep = []
        for rec in records[:12]:
            for k in rec:
                if EXCLUDE_FIELD.match(k) or k in keep:
                    continue
                keep.append(k)
        fields = keep[:6]
        rows = []
        for rec in records[:8]:
            rows.append({k: (rec.get(k) if rec.get(k) is not None else "") for k in fields})
        with open(os.path.join(args.out, d["slug"] + ".json"), "w") as f:
            json.dump({"fields": fields, "rows": rows}, f, indent=1, ensure_ascii=False)
        ok.append((d["slug"], len(fields), len(rows)))

    print(f"sample tables: {len(ok)} written, {len(skipped)} skipped")
    for slug, nf, nr in ok:
        print(f"  ✓ {slug[:44]:46s} {nf} fields x {nr} rows")
    for slug, why in skipped[:8]:
        print(f"  ✗ {slug[:44]:46s} {why[:60]}")


if __name__ == "__main__":
    main()
