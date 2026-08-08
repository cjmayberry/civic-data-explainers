#!/usr/bin/env python3
"""ckan_geojson.py — build-time GeoJSON snapshots for CKAN cities.

The MapLibre live-map partial renders any page whose frontmatter has
`geojson_url`. ArcGIS/SODA cities get a live query URL; CKAN datastores
have no native GeoJSON endpoint (datastore_search returns flat records),
so we snapshot the source's own records into static GeoJSON at build time
— the same "pulled from the source when this site was built" contract as
the sample-record tables.

Geometry resolution per dataset:
  - latitude+longitude fields  -> Point features
  - a GeoJSONCoordinates / coordenadas text field -> parse as the feature
    geometry (LineString / Polygon / MultiPolygon)
  - neither                     -> no map (page honestly renders without one)

Usage:
  python3 scripts/ckan_geojson.py --manifest hugo-site/static/lisbon/manifest.json
      --out hugo-site/static/lisbon/geojson [--inject]
--inject also writes `geojson_url` into each page's frontmatter.
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
UA = {"User-Agent": "CivicDataExplained/0.7 (ckan geojson snapshot)"}
LAT_RE = re.compile(r"^lat", re.I)
LON_RE = re.compile(r"^lon", re.I)
GEOM_RE = re.compile(r"^(geojsoncoordinates|coordenadas|geometry)$", re.I)
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---", re.DOTALL)


def http_json(url, timeout=40):
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout) as r:
            return json.loads(r.read())
    except Exception as e:
        return {"__error__": str(e)}


def fetch_all_records(service_url):
    """Page through datastore_search (limit=100) until exhausted."""
    records = []
    base = service_url.rstrip("/") + "&limit=100"
    offset = 0
    while True:
        url = f"{base}&offset={offset}"
        data = http_json(url)
        if "__error__" in data:
            return None, str(data["__error__"])
        if not data.get("success"):
            return None, str(data.get("error") or "datastore_search failed")
        res = data.get("result") or {}
        batch = res.get("records") or []
        records.extend(batch)
        total = res.get("total") or len(records)
        offset += len(batch)
        if not batch or offset >= total:
            break
        time.sleep(0.15)
    return records, None


def build_featurecollection(records, fields):
    """Map flat datastore records to GeoJSON features."""
    lat_f = next((f for f in fields if LAT_RE.match(f)), None)
    lon_f = next((f for f in fields if LON_RE.match(f)), None)
    geom_f = next((f for f in fields if GEOM_RE.match(f)), None)
    features = []
    for rec in records:
        geom = None
        if geom_f and rec.get(geom_f):
            raw = rec[geom_f]
            if isinstance(raw, str):
                try:
                    geom = json.loads(raw)
                except Exception:
                    geom = None
            elif isinstance(raw, dict):
                geom = raw
            if geom and geom.get("type") and geom.get("coordinates"):
                # keep only if it parses as real geometry
                if not (isinstance(geom["coordinates"], list) and geom["coordinates"]):
                    geom = None
        if geom is None and lat_f and lon_f:
            lat, lon = rec.get(lat_f), rec.get(lon_f)
            try:
                lat, lon = float(lat), float(lon)
            except (TypeError, ValueError):
                lat = lon = None
            if lat is not None and lon is not None:
                geom = {"type": "Point", "coordinates": [lon, lat]}
        if geom is None:
            continue
        props = {k: v for k, v in rec.items() if k not in ("_id",)}
        if geom_f:
            props.pop(geom_f, None)
        if lat_f:
            props.pop(lat_f, None)
        if lon_f:
            props.pop(lon_f, None)
        features.append({"type": "Feature", "geometry": geom, "properties": props})
    return {"type": "FeatureCollection", "features": features}


def inject_frontmatter(md_path, slug, url):
    raw = open(md_path).read()
    if "geojson_url:" in raw.split("---")[1]:
        return False
    m = FRONTMATTER_RE.match(raw)
    if not m:
        return False
    fm = m.group(1)
    sm = re.search(r'^source_url:\s*"[^"]*"', fm, re.M)
    if not sm:
        return False
    nl = fm.find("\n", sm.end())
    insert_at = nl + 1
    new_fm = fm[:insert_at] + f'geojson_url: "{url}"\n' + fm[insert_at:]
    new = raw[: m.start(1)] + new_fm + raw[m.end(1):]
    open(md_path, "w").write(new)
    return True


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--out", required=True, help="e.g. hugo-site/static/lisbon/geojson")
    ap.add_argument("--content-dir", default="", help="content dir to inject frontmatter into")
    ap.add_argument("--inject", action="store_true")
    args = ap.parse_args()

    manifest = json.load(open(args.manifest))
    os.makedirs(args.out, exist_ok=True)
    written, skipped = [], []
    for d in manifest.get("datasets", []):
        slug = d["slug"]
        url = d.get("source_url") or ""
        if "datastore_search" not in url:
            skipped.append((slug, "not a datastore URL"))
            continue
        schema = d.get("schema") or {}
        fields = [f.get("name", "") for f in schema.get("fields", [])]
        records, err = fetch_all_records(url)
        if err:
            skipped.append((slug, f"fetch failed: {err[:60]}"))
            continue
        fc = build_featurecollection(records or [], fields)
        if not fc["features"]:
            skipped.append((slug, "no geometry resolvable"))
            continue
        out = os.path.join(args.out, slug + ".geojson")
        with open(out, "w") as f:
            json.dump(fc, f, ensure_ascii=False)
        written.append((slug, len(fc["features"]), fc["features"][0]["geometry"]["type"]))
        if args.inject and args.content_dir:
            md = os.path.join(args.content_dir, slug + ".md")
            if os.path.exists(md):
                inject_frontmatter(md, slug, f"/lisbon/geojson/{slug}.geojson")

    print(f"geojson snapshots: {len(written)} written, {len(skipped)} skipped")
    for slug, n, gtype in written:
        print(f"  ✓ {slug[:42]:44s} {n:4d} features ({gtype})")
    for slug, why in skipped:
        print(f"  ✗ {slug[:42]:44s} {why[:60]}")


if __name__ == "__main__":
    main()
