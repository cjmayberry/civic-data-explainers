#!/usr/bin/env python3
"""
taxonomy.py — Step 2: per-city display-taxonomy discovery.

One LLM call per city maps the catalog's raw category labels to the
standard display taxonomy. The result is cached in cities.json under
the city's category_map so re-runs don't re-derive it (pass
--refresh-taxonomy to force).

Usage:
  python3 content/taxonomy.py --cities cities.json --catalog okc_catalog.json \
      --city okc [--model deepseek/deepseek-chat-v3-0324] [--refresh-taxonomy]
"""
import argparse
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from content.call_model import call_model  # noqa: E402  (Nous-first, OpenRouter fallback)

TAXONOMY = ["Infrastructure", "Transportation", "Licensing", "Government",
            "Parks & Recreation", "Public Safety", "Finance"]

SYSTEM = (
    "You map raw open-data portal category labels to a standard display "
    "taxonomy. Return JSON only — no explanation. "
    f"Taxonomy: {TAXONOMY}. If a label clearly does not fit any category, "
    'return "Other". Never return "Default". '
    'Return JSON: {"raw_label": "display_label"}'
)


# Portal bucket tags appear on nearly every record (the city's catch-all
# catalog label) — they carry no category signal and must not shadow the
# real topic labels that follow them in a record's topics list.
BUCKET_TAGS = {"memphis open data", "okc open data", "oklahoma city open data",
               "open data", "featured", "dataset", "application"}


def raw_labels(catalog):
    freq = {}
    for rec in catalog:
        for t in (rec.get("topics") or []):
            if t.lower() in BUCKET_TAGS:
                continue
            if t in ("Featured", "Dataset", "Application", "Open Data Type", "Open Data Category"):
                continue
            freq[t] = freq.get(t, 0) + 1
    return freq


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--cities", default=os.path.join(ROOT, "cities.json"))
    ap.add_argument("--catalog", required=True)
    ap.add_argument("--city", required=True)
    ap.add_argument("--model", default="deepseek/deepseek-chat-v3-0324")
    ap.add_argument("--refresh-taxonomy", action="store_true")
    args = ap.parse_args()

    cities = json.load(open(args.cities))
    city = next(c for c in cities if c["id"] == args.city)
    if city["category_map"] and not args.refresh_taxonomy:
        print(f"# {args.city}: category_map already cached ({len(city['category_map'])} labels)")
        return

    catalog = json.load(open(args.catalog))
    freq = raw_labels(catalog)
    if not freq:
        print("# no category labels found in catalog")
        return
    user = (f"City: {city['name']}\nRaw category labels and their frequencies:\n"
            + json.dumps(freq, indent=1))
    resp, err = call_model([{"role": "system", "content": SYSTEM}, {"role": "user", "content": user}],
                           openrouter_model=args.model)
    mapping = {}
    if resp and not err:
        try:
            mapping = json.loads(re.sub(r"^```(json)?|```$", "", resp.strip(), flags=re.M).strip())
        except Exception:
            print("! LLM response not JSON:", resp[:200])
    # keep only known labels + Other; drop anything outside taxonomy
    mapping = {k: (v if v in TAXONOMY + ["Other"] else "Other") for k, v in mapping.items()}
    if not mapping:
        # LLM failure/empty response must NOT wipe a cached category_map
        # (real bug: Missouri's cached map was overwritten to {} mid-flight).
        print("! taxonomy LLM call produced no mapping — keeping cached category_map")
        if city["category_map"]:
            print(f"  cached map retained ({len(city['category_map'])} labels)")
            return
        print("  no cached map exists either; leaving category_map as-is")
        return
    city["category_map"] = mapping
    json.dump(cities, open(args.cities, "w"), indent=2, ensure_ascii=False)
    print(f"# {args.city}: mapped {len(mapping)} labels")
    for k, v in sorted(mapping.items()):
        print(f"  {k!r:44s} -> {v}")
    unresolved = [k for k in freq if k not in mapping]
    if unresolved:
        print(f"  unresolved (left raw): {unresolved}")


if __name__ == "__main__":
    main()
