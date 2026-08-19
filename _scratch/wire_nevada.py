#!/usr/bin/env python3
"""Wire Nebraska-style catalog into cities.json for Nevada (NDOT GeoHub)."""
import json, os, sys

ROOT = "/opt/data/civic-data-explainers"
cities = json.load(open(os.path.join(ROOT, "cities.json")))

nevada = {
    "id": "nevada",
    "name": "Nevada",
    "hub_url": "https://geohub-ndot.hub.arcgis.com/",
    "gov_url": "https://ndot.nv.gov",
    "state": "NV",
    "active": True,
    "model": None,
    "min_score": 0,
    "content_dir": "hugo-site/content/nevada",
    "static_dir": "hugo-site/static/nevada",
    "category_map": {}
}

cities.append(nevada)
json.dump(cities, open(os.path.join(ROOT, "cities.json"), "w"), indent=2)
print(f"Added Nevada to cities.json ({len(cities)} cities total)")
