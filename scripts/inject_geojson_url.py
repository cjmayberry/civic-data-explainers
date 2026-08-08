#!/usr/bin/env python3
"""Inject geojson_url into content frontmatter for existing cities.

The MapLibre live-map path needs `geojson_url` in every dataset page's
frontmatter (the maplibre-map partial only renders when it's set).
scaffold_city.py writes it for NEW scaffolds; this backfills cities that
were scaffolded before derive_geojson_url existed (OKC, Memphis, ...).

Surgical line insertion after the `source_url:` line — never re-dumps the
frontmatter, so nested blocks (dictionary:, inquiry_extra:) and quoting
are untouched.

Usage:
  python3 scripts/inject_geojson_url.py [--dry-run] [content-dir ...]
Defaults to hugo-site/content/okc hugo-site/content/memphis.
"""
import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "content"))
from scaffold_city import derive_geojson_url  # noqa: E402

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---", re.DOTALL)


def inject(path: str) -> bool:
    with open(path) as f:
        raw = f.read()
    m = FRONTMATTER_RE.match(raw)
    if not m:
        return False
    fm = m.group(1)
    if "geojson_url:" in fm:
        return False
    sm = re.search(r'^source_url:\s*"([^"]*)"', fm, re.M)
    if not sm:
        sm = re.search(r"^source_url:\s*'([^']*)'", fm, re.M)
    if not sm:
        return False
    source_url = sm.group(1)
    geo = derive_geojson_url(source_url)
    if not geo:
        return False
    # insert right after the source_url line, inside the frontmatter
    nl = fm.find("\n", sm.end())
    insert_at = nl + 1
    new_fm = fm[:insert_at] + f'geojson_url: "{geo}"\n' + fm[insert_at:]
    new = raw[: m.start(1)] + new_fm + raw[m.end(1):]
    with open(path, "w") as f:
        f.write(new)
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument(
        "dirs",
        nargs="*",
        default=[
            "hugo-site/content/okc",
            "hugo-site/content/memphis",
        ],
    )
    args = ap.parse_args()
    total = 0
    for d in args.dirs:
        n = 0
        for fn in sorted(os.listdir(d)):
            if not fn.endswith(".md"):
                continue
            p = os.path.join(d, fn)
            if args.dry_run:
                with open(p) as f:
                    raw = f.read()
                m = FRONTMATTER_RE.match(raw)
                if not m:
                    continue
                fm = m.group(1)
                if "geojson_url:" in fm:
                    continue
                sm = re.search(r'^source_url:\s*"([^"]*)"', fm, re.M) or re.search(
                    r"^source_url:\s*'([^']*)'", fm, re.M
                )
                if sm and derive_geojson_url(sm.group(1)):
                    n += 1
            else:
                if inject(p):
                    n += 1
        total += n
        print(f"{d}: {'would add' if args.dry_run else 'added'} geojson_url to {n} pages")
    print(f"TOTAL {total}")


if __name__ == "__main__":
    main()
