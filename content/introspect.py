#!/usr/bin/env python3
"""
introspect.py — Step 1: live schema introspection.

Queries each dataset's ArcGIS feature service (f=json) for the REAL
field definitions (name, type, alias) plus 3 sample records, and
stores them in the manifest under the `schema` key:

    "schema": {
      "fields": [{"name": "...", "type": "...", "alias": "..."}],
      "sample": {FIELD: value},
      "introspected_at": "ISO"
    }

Failures (no service URL, 403, timeout) are non-fatal: schema stays
null, content_status becomes needs_review, and the dataset is logged.

Usage:
  python3 content/introspect.py --manifest hugo-site/static/img/manifest.json
"""
import argparse
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

UA = {"User-Agent": "CivicDataExplained/0.5 (schema introspection)"}
SKIP_SAMPLE_FIELDS = re.compile(r"^(objectid|globalid|shape|shape__area|shape__length|length|area)$", re.I)


def http_json(url, timeout=30):
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout) as r:
            return json.loads(r.read())
    except Exception as e:
        return {"__error__": str(e)}


def introspect(service_url):
    """Return (schema_dict, error_str_or_None). Tries the URL's own layer,
    then sibling layers 0-5 (Memphis services often keep data on layer 3)."""
    base = service_url.rstrip("/")
    m = re.search(r"/(?:FeatureServer|MapServer)(?:/(\d+))?$", base)
    if not m:
        return None, "not a FeatureServer/MapServer URL"
    root = re.sub(r"/(?:FeatureServer|MapServer)(?:/\d+)?$", "", base)
    primary = int(m.group(1)) if m.group(1) else 0
    layers = [primary] + [i for i in range(6) if i != primary]
    for layer in layers:
        q = f"{root}/FeatureServer/{layer}/query?" + urllib.parse.urlencode({
            "where": "1=1", "outFields": "*", "resultRecordCount": "3", "f": "json",
        })
        data = http_json(q)
        if "__error__" in data:
            continue
        fields = []
        for f in (data.get("fields") or []):
            name = f.get("name")
            if name:
                fields.append({"name": name, "type": f.get("type", ""), "alias": f.get("alias", "")})
        if not fields:
            continue
        sample = {}
        for f in (data.get("features") or []):
            attrs = f.get("attributes") or {}
            for name in [x["name"] for x in fields]:
                if SKIP_SAMPLE_FIELDS.match(name):
                    continue
                if name not in sample and attrs.get(name) is not None:
                    sample[name] = attrs[name]
        return {"fields": fields, "sample": sample, "layer": layer,
                "introspected_at": __import__("datetime").datetime.now(
                    __import__("datetime").timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}, None
    return None, f"no queryable layer (tried {layers})"


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--content-dir", default="")
    ap.add_argument("--only", help="comma slugs (debug)")
    ap.add_argument("--sleep", type=float, default=0.2)
    args = ap.parse_args()

    manifest = json.load(open(args.manifest))
    ok, failed = [], []
    for d in manifest.get("datasets", []):
        slug = d["slug"]
        if args.only and slug not in args.only.split(","):
            continue
        url = d.get("source_url") or ""
        if not url:
            d["schema"] = None
            d["content_status"] = "needs_review"
            failed.append((slug, "no service url"))
            continue
        schema, err = introspect(url)
        time.sleep(args.sleep)
        if err:
            d["schema"] = None
            d["content_status"] = "needs_review"
            failed.append((slug, err))
            continue
        d["schema"] = schema
        # a page whose body is still the scaffold stub and that previously
        # had no schema should return to "stub" so the drafter picks it up
        md = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                          args.content_dir or "", slug + ".md")
        if os.path.exists(md) and "_Stub — drafted by the city-#2 pipeline._" in open(md).read():
            d["content_status"] = "stub"
        ok.append((slug, len(schema["fields"])))

    manifest["generated_at"] = __import__("datetime").datetime.now(
        __import__("datetime").timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    with open(args.manifest, "w") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    print(f"introspected: {len(ok)}  failed: {len(failed)}")
    for slug, n in ok[:8]:
        print(f"  ✓ {slug[:40]:42s} {n} fields")
    for slug, err in failed[:8]:
        print(f"  ✗ {slug[:40]:42s} {err[:60]}")
    print(f"success rate: {len(ok)}/{len(ok) + len(failed)}")


if __name__ == "__main__":
    main()
