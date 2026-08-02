#!/usr/bin/env python3
"""
topic_images.py — per-dataset topic photos to replace simplified map covers.

The user's concern is legitimate: covers are simplified geometry renders and
readers shouldn't trust them for boundary decisions. This pass searches
Openverse per dataset title (CC-licensed, wide aspect), downloads the best
match, and makes it the cover (image_status: "themed_photo"). The city's
own map stays one click away via the page's official-map link, and point
layers keep their interactive marker map.

Datasets where no relevant photo exists keep their geometry cover and the
manifest records the reason. Attribution is stored per dataset.

Usage:
  python3 content/topic_images.py \
      --content-dir hugo-site/content/datasets \
      --static-dir hugo-site/static/img \
      --manifest hugo-site/static/img/manifest.json
"""
import argparse
import json
import os
import re
import sys
import urllib.parse
import urllib.request

UA = {"User-Agent": "CivicDataExplained/0.4 (topic images)"}
STOP = {"the", "a", "an", "and", "of", "in", "on", "for", "data", "dataset",
        "datasets", "map", "maps", "city", "oklahoma", "okc", "memphis",
        "county", "program", "project", "system", "department", "services",
        "service", "info", "information", "update", "updated", "current",
        "trail", "trails", "park", "parks", "station", "stations"}

# Boundary/district datasets keep their geometry cover: a photo cannot
# represent a boundary accurately, and the page's official-map link is the
# authoritative view. Titles/categories containing any of these stay mapped.
BOUNDARY_TERMS = ("zoning", "ward", "district", "parcel", "parcels", "census",
                  "boundary", "boundaries", "tract", "precinct", "zone", "zones",
                  "tif", "jurisdiction", "plat", "lots", "blocks", "grid",
                  "sector", "route areas", "impact fee", "corridor")

CATEGORY_TERMS = {
    "Transportation": "road street highway traffic",
    "Infrastructure": "construction infrastructure utility",
    "Parks & Recreation": "park playground recreation",
    "Public Safety": "police fire emergency",
    "Government": "government building municipal",
    "Finance": "finance money tax",
    "Licensing": "zoning permit license",
    "Default": "city",
}


def http_get(url, timeout=30):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout) as r:
        return r.read()


def openverse_top(query, page_size=5):
    url = ("https://api.openverse.org/v1/images/?q=" + urllib.parse.quote(query)
           + f"&page_size={page_size}&license=cc0,by,by-sa&aspect_ratio=wide")
    try:
        data = json.loads(http_get(url))
    except Exception:
        return None
    for r in data.get("results", []):
        img = r.get("url")
        if not img or not img.startswith("http"):
            continue
        return {
            "url": img,
            "title": r.get("title") or "",
            "creator": (r.get("creator") or ""),
            "license": r.get("license") or "",
            "landing": r.get("foreign_landing_url") or "",
        }
    return None


def query_from_title(title, category):
    words = [w for w in re.split(r"[^a-z0-9]+", title.lower()) if w and w not in STOP]
    q = " ".join(words[:2])
    if q and CATEGORY_TERMS.get(category):
        q = q + " " + CATEGORY_TERMS[category].split()[0]
    return q or CATEGORY_TERMS.get(category, "city")


def is_relevant(hit, query):
    """Accept a hit only when its title shares a significant query keyword —
    rejects 'Backpacking Incan Trail' for a city-trails query (shares no
    keyword once generic trail words are dropped from the query) and
    'GOPR2182_school' for zoning."""
    qwords = [w for w in query.split() if len(w) >= 4]
    t = (hit.get("title") or "").lower()
    return any(w in t for w in qwords)


def is_boundary(title, category):
    text = f"{title} {category}".lower()
    return any(term in text for term in BOUNDARY_TERMS)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--content-dir", required=True)
    ap.add_argument("--static-dir", required=True)
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--only", help="comma slugs (debug)")
    args = ap.parse_args()

    covers_dir = os.path.join(args.static_dir, "covers")
    os.makedirs(covers_dir, exist_ok=True)
    manifest = json.load(open(args.manifest))
    datasets = manifest.get("datasets", [])

    # restore pass: any cover renamed to *--geometry.* during an earlier
    # themed run is restored as the dataset's cover; the loop below then
    # re-decides whether a topic photo is genuinely better
    slugs = {d["slug"] for d in datasets}
    geometry_twins = {}
    for fn in os.listdir(covers_dir):
        if "--geometry." not in fn:
            continue
        for s in slugs:
            if fn.startswith(s + "--"):
                original = fn.replace("--geometry.", ".")
                os.rename(os.path.join(covers_dir, fn), os.path.join(covers_dir, original))
                geometry_twins[s] = original
                break
    for d in datasets:
        if d.get("slug") in geometry_twins:
            d["image_file"] = geometry_twins[d["slug"]]
            d["image_status"] = "map_real_geometry"
            d["image_source"] = "mapbox"
            d["image_note"] = "real geometry cover (official map linked on page)"

    themed, stayed = [], []
    for d in datasets:
        slug = d["slug"]
        if args.only and slug not in args.only.split(","):
            continue
        title = d.get("title") or slug
        if is_boundary(title, d.get("category")):
            stayed.append((slug, title, "boundary dataset — official map link is the accurate view"))
            d["image_note"] = "boundary dataset; geometry cover kept, official map linked on page"
            continue
        q = query_from_title(title, d.get("category"))
        hit = openverse_top(q)
        if not hit or not is_relevant(hit, q):
            stayed.append((slug, title, "no relevant openverse result"))
            d["image_note"] = "topic photo not found; geometry cover kept"
            continue
        # download the photo as the new cover (geometry cover file kept aside)
        try:
            blob = http_get(hit["url"], timeout=45)
        except Exception as e:
            stayed.append((slug, title, f"download failed: {e}"))
            continue
        if len(blob) < 5000:
            stayed.append((slug, title, "download too small (likely placeholder)"))
            continue
        old_file = d.get("image_file")
        if old_file:
            old_path = os.path.join(covers_dir, old_file)
            if os.path.exists(old_path):
                geo_name = old_file.rsplit(".", 1)[0] + "--geometry." + old_file.rsplit(".", 1)[1]
                os.rename(old_path, os.path.join(covers_dir, geo_name))
        ext = hit["url"].split("?")[0].rsplit(".", 1)[-1].lower()
        ext = ext if ext in ("jpg", "jpeg", "png", "webp") else "jpg"
        fname = f"{slug}--{re.sub(r'[^a-z0-9]+', '-', d['category'].lower()).strip('-')}--themed_photo.{ext}"
        with open(os.path.join(covers_dir, fname), "wb") as f:
            f.write(blob)
        d["image_file"] = fname
        d["image_status"] = "themed_photo"
        d["image_source"] = "openverse"
        d["image_note"] = (f"Topic photo: \"{hit['title']}\" by {hit['creator']} "
                           f"({hit['license']}) — {hit['landing']}")
        themed.append((slug, title, hit["title"][:50], hit["license"]))
        # frontmatter cover sync
        md = os.path.join(args.content_dir, slug + ".md")
        if os.path.exists(md):
            raw = open(md).read()
            new, n = re.subn(r'^cover:.*$', f'cover: "covers/{fname}"', raw, count=1, flags=re.M)
            if n:
                open(md, "w").write(new)

    manifest["generated_at"] = __import__("datetime").datetime.now(__import__("datetime").timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    with open(args.manifest, "w") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    print(f"themed: {len(themed)}  stayed-geometry: {len(stayed)}")
    for slug, title, reason in stayed[:15]:
        print(f"  keep: {title[:48]:50s} {reason}")
    for slug, title, hit, lic in themed[:15]:
        print(f"  ✓ {title[:48]:50s} <- {hit[:40]:42s} ({lic})")


if __name__ == "__main__":
    main()
