#!/usr/bin/env python3
"""
scaffold_city.py — turn a fresh city catalog into draft-ready content stubs.

The missing link for city #2: the extractor produces a normalized catalog,
but nothing turns it into content/*.md files with correct frontmatter. This
script does that, and also enriches RSS catalogs with real service URLs:

  1. Load an extractor catalog (rss/dcat/ckan output — same normalized schema).
  2. Resolve each record's ArcGIS item id via the item API
     (https://www.arcgis.com/sharing/rest/content/items/<id>?f=json).
  3. Filter to records whose item type is a queryable data service
     (Feature Service / Map Service / Image Service / Table) — web apps,
     dashboards, story maps, CSV uploads are dropped with a count.
  4. Write <city>_catalog.json (enriched: service_url, item_type, item_id)
     and content stubs into <out-dir>/<slug>.md with full frontmatter.

The pipeline's own scripts then consume these exactly as they consume OKC's.

Usage:
  python3 content/scaffold_city.py --catalog /tmp/memphis_catalog.json \
      --city memphis --site-url https://civic-data-explainers.pages.dev \
      --out hugo-site/content/memphis --static-out hugo-site/static/memphis
"""
import argparse
import html
import json
import os
import re
import sys
import time
import urllib.request

UA = {"User-Agent": "civic-data-pipeline/1.0 (city scaffold)"}
ITEM_API = "https://www.arcgis.com/sharing/rest/content/items/{id}?f=json"
DATA_TYPES = {"Feature Service", "Map Service", "Image Service", "Table"}
DROPPED_TYPES = {"Web Mapping Application", "Dashboard", "StoryMap", "Web Map",
                 "CSV", "PDF", "Geodata Service", "Image", "KML", "GeoJSON"}


def http_json(url, timeout=15):
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout) as r:
            return json.loads(r.read())
    except Exception as e:
        return {"__error__": str(e)}


def item_id_from_guid(guid):
    m = re.search(r"[?&]id=([0-9a-f]{32})", guid or "")
    return m.group(1) if m else None


def slugify(title, item_id):
    s = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return f"{s[:48]}-{item_id[:8]}" if item_id else s[:48]


def strip_html(raw):
    s = re.sub(r"<[^>]+>", " ", raw or "")
    return html.unescape(re.sub(r"\s+", " ", s)).strip()


def derive_geojson_url(service_url: str) -> str:
    """Build a keyless GeoJSON query URL from a dataset's service_url.
    ArcGIS FeatureServer/MapServer: append /query?f=geojson (layer 0 when
    bare). Socrata SODA: /resource/<id>.json -> .geojson. Else None."""
    su = (service_url or "").strip()
    if not su:
        return ""
    if "/FeatureServer" in su or "/MapServer" in su or "/ImageServer" in su:
        base = su.rstrip("/")
        if base.endswith("/FeatureServer") or base.endswith("/MapServer"):
            base += "/0"
        return f"{base}/query?where=1%3D1&f=geojson&outSR=4326&resultRecordCount=1500"
    if "/resource/" in su and su.endswith(".json"):
        return su[:-5] + ".geojson"
    return ""


def make_stub(title, city, site_url, source_url, dataset_id, description, teaser, topics, map_link="", geojson_url=""):
    desc = description or "An open-data dataset from this city's catalog."
    return (
        f"---\n"
        f"title: {json.dumps(title)}\n"
        f"date: \"2026-08-02\"\n"
        f"description: {json.dumps(desc)}\n"
        f"teaser: {json.dumps(teaser or desc)}\n"
        f"tags: {json.dumps(topics)}\n"
        f"categories: []\n"
        f"source_url: {json.dumps(source_url)}\n"
        f"license: \"\"\n"
        f"dataset_id: {json.dumps(dataset_id)}\n"
        f"city: {json.dumps(city)}\n"
        f"site_url: {json.dumps(site_url)}\n"
        f"{f'map_link: {json.dumps(map_link)}\n' if map_link else ''}"
        f"{f'geojson_url: {json.dumps(geojson_url)}\n' if geojson_url else ''}"
        f"draft: false\n"
        f"---\n\n"
        f"## What this is\n\n_Stub — awaiting a schema-grounded draft._\n\n"
        f"## Why it matters to you\n\n## How to read this data\n\n"
        f"## Where this leaves you\n\n## Look it up yourself\n"
    )


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--catalog", required=True)
    ap.add_argument("--city", required=True)
    ap.add_argument("--site-url", required=True)
    ap.add_argument("--out", required=True, help="content dir, e.g. hugo-site/content/memphis")
    ap.add_argument("--static-out", required=True, help="static img dir, e.g. hugo-site/static/memphis")
    ap.add_argument("--resolve/--no-resolve", dest="resolve", default=True, action=argparse.BooleanOptionalAction)
    ap.add_argument("--source", default="arcgis", choices=["arcgis", "ckan"],
                    help="Catalog family: arcgis (default, item-API resolution) "
                         "or ckan (skip item resolution; datastore-backed records kept as-is)")
    args = ap.parse_args()

    catalog = json.load(open(args.catalog))
    kept, dropped = [], []
    for rec in catalog:
        title = rec.get("title") or ""
        guid = rec.get("guid") or rec.get("link") or ""
        iid = item_id_from_guid(guid)
        item_type, url = None, None
        if args.source == "ckan":
            # CKAN records are already normalized data services; nothing to
            # resolve against ArcGIS. Keep any record with a service URL or
            # datastore resource id (drops nothing for well-formed portals).
            if rec.get("service_url") or rec.get("datastore_resource_id"):
                item_type = "CKAN Datastore"
                url = rec.get("service_url")
            else:
                dropped.append({"title": title, "item_type": "ckan",
                                "reason": "no service_url / datastore resource"})
                continue
        elif iid and args.resolve:
            info = http_json(ITEM_API.format(id=iid))
            if "__error__" not in info:
                item_type = info.get("type")
                url = info.get("url")
            time.sleep(0.12)
        if item_type in DATA_TYPES or item_type == "CKAN Datastore":
            rec["item_id"] = iid
            rec["item_type"] = item_type
            rec["service_url"] = url or rec.get("service_url")
            kept.append(rec)
        else:
            dropped.append({"title": title, "item_type": item_type or "unresolved",
                            "reason": "not a queryable data service" if item_type not in DROPPED_TYPES else f"{item_type} (non-service)"})

    os.makedirs(args.out, exist_ok=True)
    os.makedirs(args.static_out, exist_ok=True)
    written = 0
    for rec in kept:
        title = rec.get("title") or "Untitled"
        iid = rec.get("item_id") or ""
        # CKAN portals publish their own slug (`name`); prefer it so URLs
        # match the source portal (cyclinglanes -> /lisbon/cyclinglanes/).
        if args.source == "ckan" and rec.get("name"):
            slug = re.sub(r"[^a-z0-9]+", "-", rec["name"].lower()).strip("-")
        else:
            slug = slugify(title, iid)
        source_url = rec.get("service_url") or rec.get("link") or ""
        desc = (rec.get("suitable_use") or "").strip() or strip_html(rec.get("description_raw"))[:220]
        teaser = strip_html(rec.get("description_raw"))[:140] or desc[:140]
        topics = rec.get("topics") or []
        with open(os.path.join(args.out, f"{slug}.md"), "w") as f:
            f.write(make_stub(title, args.city, args.site_url, source_url,
                              rec.get("guid") or "", desc, teaser, topics,
                              map_link=rec.get("link") or "",
                              geojson_url=derive_geojson_url(rec.get("service_url") or "")))
        rec["slug"] = slug
        written += 1

    with open(f"{args.city}_catalog.json", "w") as f:
        json.dump(kept, f, indent=2, ensure_ascii=False)

    print(f"CITY={args.city} total={len(catalog)} kept={written} dropped={len(dropped)}")
    for d in dropped[:12]:
        print(f"  drop: {d['title'][:50]:52s} ({d['item_type']})")
    print(f"catalog: {args.city}_catalog.json | stubs: {args.out}/ ({written} files)")


if __name__ == "__main__":
    main()
