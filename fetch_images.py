#!/usr/bin/env python3
"""
Image pipeline v2 for the Civic Data, Explained Hugo site.

Tiers:
  TIER A — REAL GEOMETRY covers. Reads manifest v2, finds every dataset with
           image_status == "cover_only", and upgrades what it can by querying
           the dataset's own ArcGIS FeatureServer (keyless, public — verified)
           for GeoJSON, then rendering the real geometry:
             - MAPBOX_TOKEN set  -> Mapbox Static Images `geojson()` URL
                                    (first ~40 features; URL length limits)
             - no token          -> local deterministic SVG renderer (600x400,
                                    category color, real shapes) — zero cost,
                                    offline, no rate limit
           Datasets that genuinely can't be rendered (query error, empty
           geometry, non-geometry payload) keep image_status cover_only with a
           reason recorded in image_note. The manifest alone then tells you
           the image state of all 55 datasets.
  TIER B — Openverse hero + category header photos (keyless, CC-licensed).
           Attribution recorded in the manifest.

Cover files follow the self-documenting naming convention:
  {slug}--{category-slug}--{image_status}.{ext}
so a directory listing answers "which datasets still only have cover_only".

Usage:
  python3 fetch_images.py            # Tier B + local-geometry Tier A
  MAPBOX_TOKEN=... python3 fetch_images.py   # Tier A via Mapbox where possible
"""
import json
import os
import re
import sys
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(ROOT, "hugo-site", "static", "img")
COVERS_DIR = os.path.join(IMG_DIR, "covers")
MANIFEST_PATH = os.path.join(IMG_DIR, "manifest.json")
DATASETS_DIR = os.path.join(ROOT, "hugo-site", "content", "datasets")
UA = {"User-Agent": "CivicDataExplained/0.2 (static site image fetch)"}

CATEGORY_QUERIES = {
    "Transportation": "oklahoma city street",
    "Infrastructure": "road construction",
    "Licensing": "urban planning map",
    "Government": "oklahoma city downtown",
    "Finance": "oklahoma city skyline",
    "Parks & Recreation": "scissortail park oklahoma city",
    "Public Safety": "fire engine",
}

CATEGORY_COLORS = {
    "Transportation": ("#0a5da0", "#062f52"),
    "Infrastructure": ("#b45309", "#7c3605"),
    "Licensing": ("#0f766e", "#0b4f4a"),
    "Government": ("#5b21b6", "#3b1178"),
    "Finance": ("#065f46", "#043c2c"),
    "Parks & Recreation": ("#15803d", "#0b4f2a"),
    "Public Safety": ("#b91c1c", "#7f1212"),
    "Default": ("#374151", "#1f2937"),
}

HERO_QUERY = "oklahoma city skyline"
MAX_FEATURES_SVG = 1200          # local render cap
MAPBOX_FEATURES = 5              # representative features for the Mapbox URL
MAPBOX_URL_CEIL = 7500           # keep the static-images URL under ~8KB
MAPBOX_MAX_PTS = 40              # starting per line/ring point cap (shrinks on retry)


def http_get(url, timeout=60):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


# ---------------------------------------------------------------------------
# Tier A: real geometry
# ---------------------------------------------------------------------------
def layer_base(source_url):
    """Return (FeatureServer base URL, primary layer). Handles both
    .../FeatureServer/N and bare .../FeatureServer (layer 0)."""
    url = (source_url or "").rstrip("/")
    m = re.search(r"/FeatureServer/(\d+)$", url)
    if m:
        return re.sub(r"/FeatureServer/\d+$", "/FeatureServer", url), int(m.group(1))
    if url.endswith("/FeatureServer"):
        return url, 0
    return None, None


def fetch_geojson(source_url, max_features=1500):
    """Query the dataset's FeatureServer for GeoJSON. Some datasets are
    multi-layer: the URL points at a tabular sub-layer (plat names, street
    name tables, zoning definitions) while a sibling layer carries the real
    geometry — so fall back across layers 0-3 until a layer returns features
    WITH geometry."""
    base, primary = layer_base(source_url)
    if base is None:
        return None, f"unrecognized source_url: {source_url}"
    layers = [primary] + [i for i in range(4) if i != primary]
    last_err = f"no features with geometry in layers {layers}"
    for layer in layers:
        params = urllib.parse.urlencode({
            "where": "1=1",
            "f": "geojson",
            "outSR": "4326",
            "resultRecordCount": str(max_features),
        })
        q = f"{base}/{layer}/query?" + params
        try:
            raw = http_get(q, timeout=90)
            data = json.loads(raw)
        except Exception as e:
            last_err = f"layer {layer} query failed: {str(e)[:120]}"
            continue
        feats = data.get("features", [])
        if not feats:
            continue
        with_geom = [f for f in feats if f.get("geometry")]
        if with_geom:
            return data, None
        last_err = f"layer {layer} returned {len(feats)} features without geometry"
    return None, last_err


def geometry_kind(data):
    """'point' | 'line' | 'polygon' | None — from the GeoJSON geometry types."""
    kinds = set()
    for f in data.get("features", [])[:200]:
        g = (f or {}).get("geometry") or {}
        t = g.get("type", "")
        if "Point" in t:
            kinds.add("point")
        elif "Line" in t:
            kinds.add("line")
        elif "Polygon" in t:
            kinds.add("polygon")
    if len(kinds) > 1:
        return "mixed"
    return kinds.pop() if kinds else None


def project_coords(geoms, width=600, height=400, margin=28):
    """Fit [lon,lat] coords into the viewBox with aspect preserved."""
    xs, ys = [], []
    def walk(g):
        t = g.get("type", "")
        coords = g.get("coordinates", [])
        if t == "Point":
            xs.append(coords[0]); ys.append(coords[1])
        elif t == "MultiPoint":
            for p in coords:
                xs.append(p[0]); ys.append(p[1])
        elif t in ("LineString", "MultiLineString", "Polygon", "MultiPolygon"):
            def flat(c):
                if c and isinstance(c[0], (int, float)):
                    xs.append(c[0]); ys.append(c[1])
                else:
                    for sub in c:
                        flat(sub)
            flat(coords)
    for g in geoms:
        walk(g)
    if not xs:
        return None
    minx, maxx, miny, maxy = min(xs), max(xs), min(ys), max(ys)
    if maxx - minx < 1e-9 and maxy - miny < 1e-9:
        spanx = spany = 1.0
    else:
        spanx, spany = maxx - minx, maxy - miny
    # fit inside box, preserve aspect
    scale = min((width - 2 * margin) / spanx, (height - 2 * margin) / spany)
    ox = (width - spanx * scale) / 2 - minx * scale
    oy = (height - spany * scale) / 2 + maxy * scale  # y flip for SVG
    def P(lon, lat):
        return (round(lon * scale + ox, 1), round(oy - lat * scale, 1))
    return P


def path_d(geom, P):
    t = geom.get("type", "")
    coords = geom.get("coordinates", [])
    def ring(c):
        return " ".join(f"{P(x, y)[0]},{P(x, y)[1]}" for x, y in c)
    if t == "Point":
        return None, P(*coords)
    if t == "MultiPoint":
        return None, [P(*c) for c in coords]
    if t == "LineString":
        return "M " + ring(coords), None
    if t == "MultiLineString":
        return "M " + " M ".join(ring(c) for c in coords), None
    if t == "Polygon":
        return "M " + " M ".join(ring(c) for c in coords) + " Z", None
    if t == "MultiPolygon":
        parts = []
        for poly in coords:
            parts.append("M " + " M ".join(ring(c) for c in poly))
        return " ".join(parts) + " Z", None
    return None, None


def render_geometry_svg(slug, title, category, data, kind, note):
    """Local deterministic SVG: real geometry on the category gradient."""
    c1, c2 = CATEGORY_COLORS.get(category, CATEGORY_COLORS["Default"])
    feats = data.get("features", [])[:MAX_FEATURES_SVG]
    geoms = [(f or {}).get("geometry") or {} for f in feats]
    geoms = [g for g in geoms if g.get("type")]
    P = project_coords(geoms)
    if P is None:
        return None, f"no plottable coordinates ({kind})"

    def esc(s):
        return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    polys, lines, points = [], [], []
    for g in geoms:
        d, pt = path_d(g, P)
        t = g.get("type", "")
        if pt is not None and "Point" in t:
            if isinstance(pt, tuple):
                points.append(f'<circle cx="{pt[0]}" cy="{pt[1]}" r="2.6"/>')
            else:
                points += [f'<circle cx="{p[0]}" cy="{p[1]}" r="2.2"/>' for p in pt[:400]]
        elif d and "Line" in t:
            lines.append(f'<path d="{d}" fill="none" stroke="rgba(255,255,255,0.92)" stroke-width="1.6" stroke-linecap="round"/>')
        elif d:
            polys.append(f'<path d="{d}" fill="rgba(255,255,255,0.10)" stroke="rgba(255,255,255,0.85)" stroke-width="1.4"/>')

    label = esc(category if category else "Open Data")
    kind_label = {"point": f"{len(feats)} points", "line": f"{len(feats)} line features",
                  "polygon": f"{len(feats)} areas", "mixed": f"{len(feats)} features"}.get(kind, f"{len(feats)} features")
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="600" height="400" viewBox="0 0 600 400">
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{c1}"/>
      <stop offset="1" stop-color="{c2}"/>
    </linearGradient>
  </defs>
  <rect width="600" height="400" fill="url(#g)"/>
  <g opacity="0.5">
    {"".join(polys)}
    {"".join(lines)}
    {"".join(points)}
  </g>
  <text x="44" y="362" font-family="system-ui, sans-serif" font-size="21" letter-spacing="3" fill="rgba(255,255,255,0.95)">{label}</text>
  <text x="44" y="384" font-family="system-ui, sans-serif" font-size="12" letter-spacing="1" fill="rgba(255,255,255,0.65)">REAL GEOMETRY · {kind_label}{note and " · " + esc(note) or ""}</text>
</svg>
"""
    return svg, None


def simplify_geojson(feats, max_pts=MAPBOX_MAX_PTS):
    """Prep geometry for the Mapbox static-images URL, which hard-fails
    (HTTP 414 / 422) on large layers. Strategy:
      - point layers: keep ALL points (they're cheap — cap at 200); the
        cover should show every station/incident, not a sample
      - line/polygon layers: keep only the N most complex features
        (representative shapes), trim rings to a point cap (closed)
      - round coordinates to 4 decimals (~11m precision — plenty for a
        600x400 thumbnail)
      - drop attribute properties (bloat the URL; Mapbox ignores them)
    """
    def vcount(g):
        c = g.get("coordinates", [])
        def walk(coords):
            if coords and isinstance(coords[0], (int, float)):
                return 1
            return sum(walk(x) for x in coords)
        return walk(c)

    is_point_layer = all(
        "Point" in (f.get("geometry") or {}).get("type", "")
        for f in feats if (f.get("geometry") or {}).get("coordinates")
    )
    if is_point_layer:
        # each point costs ~165 URL chars of JSON structure after encoding;
        # 45 points stays under Mapbox's ceiling. The interactive map carries
        # the full feature set — the cover just needs to be legible.
        ranked = feats[:45]
    else:
        ranked = sorted(feats, key=lambda f: -vcount(f.get("geometry") or {}))[:MAPBOX_FEATURES]

    def close(ring):
        return ring + [ring[0]] if len(ring) > 1 and ring[0] != ring[-1] else ring

    def simplify_feature(f):
        g = dict(f.get("geometry") or {})
        t = g.get("type", "")
        c = g.get("coordinates", [])
        def R(v):
            return round(v, 4)
        def pr(p):
            return [R(p[0]), R(p[1])]
        def trim(ring):
            ring = [pr(p) for p in ring]
            if len(ring) > max_pts:
                ring = ring[:: len(ring) // max_pts]
            return ring
        if t == "Point":
            nc = pr(c)
        elif t == "MultiPoint":
            nc = [pr(p) for p in c[:max_pts]]
        elif t == "LineString":
            nc = trim(c)
        elif t == "MultiLineString":
            nc = [trim(s) for s in c[:2]]
        elif t == "Polygon":
            nc = [close(trim(r)) for r in c[:2]]
        elif t == "MultiPolygon":
            nc = [[close(trim(r)) for r in poly[:2]] for poly in c[:2]]
        else:
            nc = c
        g["coordinates"] = nc
        return {"type": "Feature", "properties": {}, "geometry": g}

    return [simplify_feature(f) for f in ranked]


def render_mapbox_png(data, slug):
    """Mapbox Static Images geojson() render (token-gated). Retries with a
    shrinking geometry budget until the URL fits Mapbox's hard limit."""
    token = os.environ.get("MAPBOX_TOKEN", "").strip()
    if not token:
        return None, "no MAPBOX_TOKEN"
    for max_pts in (40, 20, 12, 8, 5):
        feats = simplify_geojson(data.get("features", []), max_pts)
        gj = {"type": "FeatureCollection", "features": feats}
        encoded = urllib.parse.quote(json.dumps(gj, separators=(",", ":")))
        url = ("https://api.mapbox.com/styles/v1/mapbox/streets-v12/static/"
               f"geojson({encoded})/auto/600x400?access_token={token}")
        if len(url) > MAPBOX_URL_CEIL:
            continue
        try:
            png = http_get(url, timeout=60)
        except Exception as e:
            return None, f"mapbox render failed: {e}"
        if not png or len(png) < 500:
            return None, "mapbox returned empty/error image"
        return png, None
    return None, f"geometry too complex for Mapbox URL even at min budget ({len(url)} chars)"


def upgrade_cover(dataset, source_url):
    """Attempt real-geometry upgrade for one dataset. Returns (image_status,
    image_source, file_name, note, kind, data). kind is None when the layer
    couldn't be rendered; data is the fetched GeoJSON for interactive maps."""
    slug = dataset["slug"]
    cat_slug = re.sub(r"[^a-z0-9]+", "-", dataset["category"].lower()).strip("-")
    old_name = dataset.get("image_file") or f"{slug}--{cat_slug}--cover_only.svg"

    data, err = fetch_geojson(source_url)
    if err:
        return "cover_only", "svg_cover", old_name, f"geometry fetch failed: {err[:160]}", None, None
    kind = geometry_kind(data)
    if kind is None:
        return "cover_only", "svg_cover", old_name, "no geometry in layer response", None, data
    if kind == "mixed":
        return "cover_only", "svg_cover", old_name, "mixed geometry types not rendered", None, data

    token = os.environ.get("MAPBOX_TOKEN", "").strip()
    mb_err = ""
    if token:
        png, err = render_mapbox_png(data, slug)
        if not err:
            new_name = f"{slug}--{cat_slug}--map_real_geometry.png"
            with open(os.path.join(COVERS_DIR, new_name), "wb") as f:
                f.write(png)
            return "map_real_geometry", "mapbox", new_name, f"{kind}, {len(data.get('features', []))} features", kind, data
        mb_err = err

    svg, err = render_geometry_svg(slug, dataset["title"], dataset["category"], data, kind, None)
    if err:
        return "cover_only", "svg_cover", old_name, f"svg render failed: {err}", None, data
    new_name = f"{slug}--{cat_slug}--map_real_geometry.svg"
    with open(os.path.join(COVERS_DIR, new_name), "w") as f:
        f.write(svg)
    note = f"{kind}, {len(data.get('features', []))} features"
    if token:
        note += f" | mapbox failed: {mb_err[:80]}"
    return "map_real_geometry", "local_geometry", new_name, note, kind, data


# ---------------------------------------------------------------------------
# Tier B: Openverse photos
# ---------------------------------------------------------------------------
def openverse_search(query, page_size=3):
    url = ("https://api.openverse.org/v1/images/?q="
           + urllib.parse.quote(query)
           + f"&page_size={page_size}")
    data = json.loads(http_get(url))
    out = []
    for r in data.get("results", []):
        out.append({
            "title": r.get("title"), "url": r.get("url"), "creator": r.get("creator"),
            "license": r.get("license"), "license_version": r.get("license_version"),
            "width": r.get("width"), "height": r.get("height"),
            "foreign_landing_url": r.get("foreign_landing_url"),
        })
    return out


def fetch_photo(query, dest_name, min_width=900, max_width=2400, keyword=None):
    results = openverse_search(query, page_size=8)
    candidates = [r for r in results if min_width <= (r.get("width") or 0) <= max_width]
    pick = None
    if keyword and candidates:
        pat = re.compile(r"\b" + re.escape(keyword) + r"\b", re.I)
        pick = next((r for r in candidates if pat.search(r.get("title") or "")), None)
        if not pick:
            print(f"  ! no '{keyword}' match for '{query}' — skipping (avoid irrelevant photo)")
            return None
    if not pick and candidates:
        pick = candidates[0]
    if not pick and results:
        pick = results[0]
    if not pick or not pick["url"]:
        print(f"  ! no Openverse result for '{query}'")
        return None
    ext = os.path.splitext(urllib.parse.urlparse(pick["url"]).path)[1] or ".jpg"
    if ext.lower() not in (".jpg", ".jpeg", ".png", ".webp"):
        ext = ".jpg"
    dest = os.path.join(IMG_DIR, dest_name)
    try:
        data = http_get(pick["url"], timeout=45)
        with open(dest, "wb") as f:
            f.write(data)
    except Exception as e:
        print(f"  ! download failed for '{query}': {e}")
        return None
    print(f"  ✓ {dest_name} ({len(data)//1024}KB) <- {pick['title']} by {pick.get('creator') or 'unknown'} ({pick['license']})")
    return {
        "file": dest_name, "query": query, "url": pick["url"], "title": pick["title"],
        "creator": pick.get("creator"), "license": pick.get("license"),
        "license_version": pick.get("license_version"),
        "source": pick.get("foreign_landing_url") or pick["url"], "bytes": len(data),
    }


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def parse_frontmatter_cover(text):
    m = re.search(r"^cover:\s*\"(.*)\"\s*$", text, re.M)
    return m.group(1) if m else None


def main():
    os.makedirs(COVERS_DIR, exist_ok=True)
    with open(MANIFEST_PATH) as f:
        manifest = json.load(f)
    datasets = manifest.get("datasets", [])
    print(f"# {len(datasets)} datasets in manifest")

    # ----- Tier A: geometry upgrade -----
    print("Tier A: real-geometry covers")
    upgraded = []
    stayed = []
    for d in datasets:
        slug = d["slug"]
        path = os.path.join(DATASETS_DIR, slug + ".md")
        try:
            raw = open(path, encoding="utf-8").read()
        except FileNotFoundError:
            d["image_note"] = "content page missing"
            stayed.append(d)
            continue
        m = re.search(r"^source_url:\s*\"(.*)\"\s*$", raw, re.M)
        source_url = m.group(1) if m else None

        status, source, fname, note, kind, data = upgrade_cover(d, source_url)

        # interactive map data: point layers get a client-side marker map
        # (full feature set, popup-able properties)
        if kind == "point" and data:
            map_dir = os.path.join(IMG_DIR, "data")
            os.makedirs(map_dir, exist_ok=True)
            gj = {"type": "FeatureCollection", "features": data.get("features", [])[:2000]}
            map_fname = slug + ".geojson"
            with open(os.path.join(map_dir, map_fname), "w") as f:
                json.dump(gj, f, ensure_ascii=False)
            d["map_data"] = f"data/{map_fname}"
        else:
            d.pop("map_data", None)

        # clean up stale renamed variants (old status in filename)
        for f in os.listdir(COVERS_DIR):
            if f.startswith(slug + "--") and f != fname:
                try:
                    os.remove(os.path.join(COVERS_DIR, f))
                except OSError:
                    pass

        d["image_status"] = status
        d["image_source"] = source
        d["image_file"] = fname
        d["image_note"] = note
        if status == "map_real_geometry":
            upgraded.append(slug)
            print(f"  ✓ {slug:50s} -> {status} ({source}, {note})")
        else:
            stayed.append(d)
            print(f"  ✗ {slug:50s} stays cover_only — {note}")

        # keep frontmatter cover + map_data in sync with the manifest
        new_cover = f"covers/{fname}"
        fm_raw = raw
        if parse_frontmatter_cover(fm_raw) != new_cover:
            fm_raw = re.sub(r"^cover:.*$", f"cover: {json.dumps(new_cover)}", fm_raw, count=1, flags=re.M)
        map_ref = ("img/" + d["map_data"]) if d.get("map_data") else ""
        if d.get("map_data") and f"map_data: {json.dumps(map_ref)}" not in fm_raw:
            fm_raw = re.sub(r"^(cover:.*)$", r"\1\n" + f"map_data: {json.dumps(map_ref)}", fm_raw, count=1, flags=re.M)
        elif not d.get("map_data"):
            fm_raw = re.sub(r"^map_data:.*$\n?", "", fm_raw, count=1, flags=re.M)
        if fm_raw != raw:
            with open(path, "w", encoding="utf-8") as f:
                f.write(fm_raw)

    print(f"  upgraded {len(upgraded)}/{len(datasets)}; {len(stayed)} stayed cover_only")

    # ----- Tier B: Openverse hero + category photos (only if missing) -----
    print("Tier B: Openverse photos")
    attribution = {"hero": manifest.get("hero"), "categories": manifest.get("categories", {})}
    if not attribution["hero"] or not os.path.exists(os.path.join(IMG_DIR, "hero.jpg")):
        hero = fetch_photo(HERO_QUERY, "hero.jpg")
        if hero:
            attribution["hero"] = hero
    cat_files = {}
    for cat, query in CATEGORY_QUERIES.items():
        slug = re.sub(r"[^a-z0-9]+", "-", cat.lower()).strip("-")
        fname = f"cat-{slug}.jpg"
        key = f"category:{cat}"
        if key not in attribution["categories"] or not os.path.exists(os.path.join(IMG_DIR, fname)):
            kw = "park" if cat == "Parks & Recreation" else None
            info = fetch_photo(query, fname, keyword=kw)
            if info:
                attribution["categories"][key] = info
                cat_files[cat] = info["file"]

    # ----- write manifest -----
    manifest["hero"] = attribution["hero"]
    manifest["categories"] = attribution["categories"]
    manifest["mapbox_enabled"] = bool(os.environ.get("MAPBOX_TOKEN", "").strip())
    with open(MANIFEST_PATH, "w") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    print(f"manifest updated: {MANIFEST_PATH}")


if __name__ == "__main__":
    main()
