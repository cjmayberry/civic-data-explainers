#!/usr/bin/env python3
"""
placeholder_covers.py — replace geometry map covers with clean branded
placeholders. Per the user's directive: no maps with ambiguous or
simplified information. Verified topical photos (image_status
"themed_photo") are kept; every other cover becomes a placeholder SVG
(title + category + hint that the official city map is linked on the
page). The official map link on each page is the authoritative view.

Usage:
  python3 content/placeholder_covers.py \
      --content-dir hugo-site/content/datasets \
      --static-dir hugo-site/static/img \
      --manifest hugo-site/static/img/manifest.json \
      [--clean-geometry]   # also delete leftover geometry PNG covers
"""
import argparse
import json
import os
import re
import shutil

COLORS = {
    "Transportation": "#0a5da0", "Infrastructure": "#b45309", "Licensing": "#0f766e",
    "Government": "#5b21b6", "Finance": "#065f46", "Parks & Recreation": "#15803d",
    "Public Safety": "#b91c1c", "Default": "#374151",
    "Environment": "#166534", "Health": "#be123c", "Education": "#7c2d12",
    "Housing": "#a16207", "Economy": "#6d28d9",
}


def svg_placeholder(title, category):
    color = COLORS.get(category, COLORS["Default"])
    esc = title.replace("&", "&amp;").replace("<", "&lt;")
    return (
        f"<svg xmlns='http://www.w3.org/2000/svg' width='1200' height='630'>"
        f"<rect width='1200' height='630' fill='#f5f1e8'/>"
        f"<rect width='1200' height='14' fill='{color}'/>"
        f"<text x='60' y='300' font-family='Georgia,serif' font-size='46' fill='#26221c'>{esc[:60]}</text>"
        f"<text x='60' y='352' font-family='sans-serif' font-size='22' fill='#8a8174'>{category}</text>"
        f"<text x='60' y='420' font-family='sans-serif' font-size='18' fill='#6b6356'>Official map is published by the city — linked below.</text>"
        f"<text x='60' y='450' font-family='sans-serif' font-size='18' fill='#6b6356'>Explainer content updated as datasets refresh.</text>"
        f"</svg>"
    )


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--content-dir", required=True)
    ap.add_argument("--static-dir", required=True)
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--clean-geometry", action="store_true")
    args = ap.parse_args()

    covers_dir = os.path.join(args.static_dir, "covers")
    manifest = json.load(open(args.manifest))
    replaced, kept = [], []
    for d in manifest.get("datasets", []):
        slug = d["slug"]
        if d.get("image_status") == "themed_photo":
            kept.append((slug, d.get("title")))
            continue
        cat_slug = re.sub(r"[^a-z0-9]+", "-", d.get("category", "Default").lower()).strip("-")
        fname = f"{slug}--{cat_slug}--placeholder.svg"
        with open(os.path.join(covers_dir, fname), "w") as f:
            f.write(svg_placeholder(d.get("title", slug), d.get("category")))
        d["image_file"] = fname
        d["image_status"] = "placeholder"
        d["image_source"] = "svg_placeholder"
        d["image_note"] = "placeholder cover; official city map linked on the page"
        md = os.path.join(args.content_dir, slug + ".md")
        if os.path.exists(md):
            raw = open(md).read()
            new, n = re.subn(r'^cover:.*$', f'cover: "covers/{fname}"', raw, count=1, flags=re.M)
            if n:
                open(md, "w").write(new)
        replaced.append((slug, d.get("title")))

    if args.clean_geometry:
        removed = 0
        for fn in os.listdir(covers_dir):
            if fn.endswith(("map_real_geometry.png", "cover_only.svg")) and "--placeholder.svg" not in fn:
                os.remove(os.path.join(covers_dir, fn))
                removed += 1
        print(f"geometry/old covers deleted: {removed}")

    manifest["generated_at"] = __import__("datetime").datetime.now(__import__("datetime").timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    with open(args.manifest, "w") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    print(f"replaced with placeholder: {len(replaced)}  kept topical photos: {len(kept)}")
    for s, t in kept:
        print(f"  keep photo: {t}")


if __name__ == "__main__":
    main()
