#!/usr/bin/env python3
"""Wire Topeka-style catalog into cities.json for Topeka (or update existing)."""
import json, os, sys

ROOT = "/opt/data/civic-data-explainers"
cities = json.load(open(os.path.join(ROOT, "cities.json")))

# Topeka already wired — update hub_url to the DCAT root (already done above)
topeka = next((c for c in cities if c["id"] == "topeka"), None)
if topeka:
    print(f"Topeka already in cities.json: {topeka['name']} → {topeka['content_dir']}")
else:
    topeka = {
        "id": "topeka",
        "name": "Topeka",
        "hub_url": "https://performance.topeka.org/",
        "gov_url": "https://www.topeka.org",
        "state": "KS",
        "active": True,
        "model": None,
        "min_score": 0,
        "content_dir": "hugo-site/content/topeka",
        "static_dir": "hugo-site/static/topeka",
        "category_map": {}
    }
    cities.append(topeka)
    json.dump(cities, open(os.path.join(ROOT, "cities.json"), "w"), indent=2)
    print(f"Added Topeka to cities.json")

# Also wire Nevada if not present
nevada = next((c for c in cities if c["id"] == "nevada"), None)
if not nevada:
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
else:
    print(f"Nevada already in cities.json: {nevada['name']}")
