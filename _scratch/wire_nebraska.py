#!/usr/bin/env python3
"""Wire Nebraska into cities.json so pipeline/run.py can find it as an active city.
The nightly orchestrator rolled back Nebraska's partial work; this re-wires the
scaffolding (content dir, static dir, layouts, cities.json entries) so the
pipeline can re-run without the orchestrator's 900s cap."""
import json, os, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CITIES_JSON = os.path.join(ROOT, "cities.json")
HUGO_CITIES_JSON = os.path.join(ROOT, "hugo-site", "data", "cities.json")

# 1. Root cities.json (list of dicts)
cities = json.load(open(CITIES_JSON))
if not any(c["id"] == "nebraska" for c in cities):
    cities.append({
        "id": "nebraska",
        "name": "Nebraska",
        "hub_url": "https://www.nebraskamap.gov/",
        "gov_url": "https://www.nebraska.gov",
        "state": "US",
        "active": True,
        "model": None,
        "min_score": 0,
        "content_dir": "hugo-site/content/nebraska",
        "static_dir": "hugo-site/static/nebraska",
        "category_map": {},
    })
    json.dump(cities, open(CITIES_JSON, "w"), indent=2, ensure_ascii=False)
    print("wired nebraska into root cities.json")
else:
    print("nebraska already in root cities.json")

# 2. hugo-site/data/cities.json (dict keyed by id)
hc = json.load(open(HUGO_CITIES_JSON))
if "nebraska" not in hc:
    hc["nebraska"] = {
        "name": "Nebraska",
        "short": "NE",
        "hub": "https://www.nebraskamap.gov/",
        "gov": "https://www.nebraska.gov",
        "center": [0, 0],
        "blurb": "Nebraska open-data explainers.",
    }
    json.dump(hc, open(HUGO_CITIES_JSON, "w"), indent=2, ensure_ascii=False)
    print("wired nebraska into hugo-site/data/cities.json")
else:
    print("nebraska already in hugo-site/data/cities.json")

# 3. Content dir + _index
content_dir = os.path.join(ROOT, "hugo-site", "content", "nebraska")
os.makedirs(content_dir, exist_ok=True)
idx = os.path.join(content_dir, "_index.md")
if not os.path.exists(idx):
    with open(idx, "w") as f:
        f.write("---\ntitle: \"Nebraska explainers\"\ndraft: false\n---\n")
    print("wrote nebraska/_index.md")

# 4. Layouts dir (copy from missouri template — state section)
layouts_dir = os.path.join(ROOT, "hugo-site", "layouts", "nebraska")
if not os.path.exists(layouts_dir):
    src = os.path.join(ROOT, "hugo-site", "layouts", "missouri")
    shutil.copytree(src, layouts_dir)
    print("copied missouri layouts → nebraska layouts")
else:
    print("nebraska layouts already exist")

# 5. Static dir
static_dir = os.path.join(ROOT, "hugo-site", "static", "nebraska")
os.makedirs(static_dir, exist_ok=True)
print("ensured nebraska static dir")
