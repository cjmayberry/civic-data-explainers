#!/usr/bin/env python3
"""Convert hugo-site/data/cities.json to match root cities.json schema.

Old schema: {name, short, hub, gov, center: [lat,lon], blurb}
New schema: mirrors root cities.json fields (id, name, hub_url, gov_url, state, active, model, min_score, content_dir, static_dir, category_map)

For 9 existing entries: preserve blurb + center. For 45 new states: generate blurb.
Fixes kansas/nebraska state codes (US → KS/NE).
"""

import json

ROOT = "/opt/data/civic-data-explainers"

# Read root cities.json (canonical 54-entry registry)
with open(f"{ROOT}/cities.json") as f:
    root = json.load(f)

# Fix kansas/nebraska state codes
for c in root:
    if c["id"] == "kansas":
        c["state"] = "KS"
    elif c["id"] == "nebraska":
        c["state"] = "NE"

# Read old hugo data file
old_path = f"{ROOT}/hugo-site/data/cities.json"
with open(old_path) as f:
    old = json.load(f)

# Index old by id
old_by_id = {cid: entry for cid, entry in old.items()}

# Build new dict
new = {}
for c in root:
    cid = c["id"]
    old_entry = old_by_id.get(cid, {})

    blurb = old_entry.get("blurb", f"{c['name']} open-data explainers from {c['hub_url']}.")
    center = old_entry.get("center", [0, 0])

    new[cid] = {
        "name": c["name"],
        "hub_url": c["hub_url"],
        "gov_url": c["gov_url"],
        "state": c["state"],
        "active": c.get("active", True),
        "model": c.get("model"),
        "min_score": c.get("min_score", 0),
        "content_dir": c["content_dir"],
        "static_dir": c["static_dir"],
        "category_map": c.get("category_map", {}),
        "blurb": blurb,
        "center": center,
    }

# Write
with open(old_path, "w") as f:
    json.dump(new, f, indent=2, ensure_ascii=False)
    f.write("\n")

print(f"Wrote {len(new)} entries to {old_path}")

# Verify
missing = set(c["id"] for c in root) - set(new.keys())
extra = set(new.keys()) - set(c["id"] for c in root)
if missing:
    print(f"MISSING: {missing}")
if extra:
    print(f"EXTRA: {extra}")
if not missing and not extra:
    print("All 54 root entries present in hugo data.")

# Spot-check: show a few entries
for cid in ["okc", "alabama", "texas", "kansas", "nebraska"]:
    e = new.get(cid, {})
    print(f"  {cid}: name={e.get('name')}, state={e.get('state')}, "
          f"hub={e.get('hub_url','')[:50]}, gov={e.get('gov_url','')[:30]}, "
          f"blurb={'✓' if e.get('blurb') else '✗'}")
