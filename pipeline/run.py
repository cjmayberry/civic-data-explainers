#!/usr/bin/env python3
"""
pipeline/run.py — adaptive city pipeline orchestrator.

Single entry point driven by cities.json. For each active city:
  Step 1  introspection  (content/introspect.py)   — live field schemas
  Step 2  taxonomy       (content/taxonomy.py)     — LLM category map (cached)
  Step 3  drafting       (content/redraft.py)      — schema-grounded explainers
  Step 4  manifest       (build_manifest.py)       — build contract
  Step 5  images         (content/placeholder_covers.py)
  Step 6  site build     (hugo via build.sh)

Usage:
  python3 pipeline/run.py cities.json --model tencent/hy3
  python3 pipeline/run.py cities.json --model anthropic/claude-sonnet-4 --city okc
  python3 pipeline/run.py cities.json --model tencent/hy3 --refresh-taxonomy --redraft-all
"""
import argparse
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)


def sh(cmd, **kw):
    print(f"$ {cmd}", flush=True)
    r = subprocess.run(cmd, shell=True, cwd=ROOT, **kw)
    if r.returncode != 0:
        print(f"! command failed ({r.returncode}): {cmd}", file=sys.stderr)
        sys.exit(r.returncode)
    return r


def city_catalog_path(city, cities):
    cands = [
        os.path.join(ROOT, f"{'okc' if city['id'] == 'okc' else city['id']}_catalog.json"),
        os.path.join(ROOT, "cities", city["id"], "catalog.json"),
        os.path.join(ROOT, "okc_catalog.json") if city["id"] == "okc" else None,
    ]
    for c in cands:
        if c and os.path.exists(c):
            return c
    return cands[0]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("cities_file")
    ap.add_argument("--model", default="deepseek/deepseek-chat-v3-0324")
    ap.add_argument("--city", help="run only this city id")
    ap.add_argument("--refresh-taxonomy", action="store_true")
    ap.add_argument("--redraft-all", action="store_true",
                    help="redraft stub pages (default) — redraft.py only targets stubs")
    ap.add_argument("--skip-draft", action="store_true")
    ap.add_argument("--skip-build", action="store_true")
    args = ap.parse_args()

    cities = json.load(open(args.cities_file))
    active = [c for c in cities if c.get("active", True)]
    if args.city:
        active = [c for c in active if c["id"] == args.city]
    if not active:
        print("no active cities")
        return

    for city in active:
        cid = city["id"]
        print(f"\n===== CITY: {city['name']} ({cid}) =====", flush=True)
        catalog = city_catalog_path(city, cities)
        manifest = os.path.join(ROOT, city["static_dir"], "manifest.json")
        if not os.path.exists(catalog):
            print(f"! catalog missing: {catalog} — run extractor first", file=sys.stderr)
            continue

        # Step 2 — taxonomy (one LLM call, cached in cities.json category_map)
        if not city["category_map"] or args.refresh_taxonomy:
            sh(f"python3 content/taxonomy.py --catalog {catalog} --city {cid} "
               f"--model {args.model}" + (" --refresh-taxonomy" if args.refresh_taxonomy else ""))
            # taxonomy.py rewrites cities.json in its own process — reload so
            # the in-memory config picks up the fresh category_map
            cities = json.load(open(args.cities_file))
            city = next(c for c in cities if c["id"] == cid)

        # category map -> temp json for build_manifest
        cmap_path = os.path.join(ROOT, f".category-map-{cid}.json")
        with open(cmap_path, "w") as f:
            json.dump(city.get("category_map") or {}, f)

        # Step 4 — manifest first (category decision + city fields + injects
        # source_url into entries so introspection can find the services)
        sh(f"python3 build_manifest.py --catalog {catalog} "
           f"--content-dir {city['content_dir']} --static-dir {city['static_dir']} "
           f"--city-id {cid} --city-name \"{city['name']}\" --category-map {cmap_path}")

        # Step 1 — schema introspection (writes schema into the manifest)
        sh(f"python3 content/introspect.py --manifest {manifest} "
           f"--content-dir {city['content_dir']}")

        # Step 3 — drafting (stub pages only unless --redraft-all; schema-grounded)
        if not args.skip_draft:
            drafts = os.path.join(ROOT, f"drafts-{cid}.json")
            model = city.get("model") or args.model
            only = ""
            sh(f"python3 content/redraft.py --content-dir {city['content_dir']} "
               f"--catalog {catalog} --drafts {drafts} --manifest {manifest} "
               f"--city-name \"{city['name']}\" --city-state \"{city['state']}\" "
               f"--model {model}")

        # Step 5 — covers (placeholders; topic photos land later per city)
        sh(f"python3 content/placeholder_covers.py --content-dir {city['content_dir']} "
           f"--static-dir {city['static_dir']} --manifest {manifest}")

        os.remove(cmap_path) if os.path.exists(cmap_path) else None

    # Step 6 — site build
    if not args.skip_build:
        env = dict(os.environ)
        sh("bash build.sh", env=env)
    print("\n===== DONE =====", flush=True)


if __name__ == "__main__":
    main()
