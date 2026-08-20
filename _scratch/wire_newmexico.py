#!/usr/bin/env python3
"""Wire New Mexico into cities.json (EMNRD GIS portal / NM RGIS hub)."""
import json, os

ROOT = "/opt/data/civic-data-explainers"
cities = json.load(open(os.path.join(ROOT, "cities.json")))

if any(c["id"] == "newmexico" for c in cities):
    print("New Mexico already in cities.json")
else:
    nm = {
        "id": "newmexico",
        "name": "New Mexico",
        "hub_url": "https://geodata.nm.gov/",
        "gov_url": "https://www.newmexico.gov",
        "state": "NM",
        "active": True,
        "model": None,
        "min_score": 0,
        "content_dir": "hugo-site/content/newmexico",
        "static_dir": "hugo-site/static/newmexico",
        "category_map": {
            "boundaries": "Government",
            "transportation": "Transportation",
            "utilitiesCommunication": "Infrastructure",
            "environment": "Environment",
            "planningCadastre": "Government",
            "location": "Government",
            "farming": "Other",
            "inlandWaters": "Environment",
            "structure": "Infrastructure",
            "health": "Health",
            "biota": "Environment",
            "geoscientificInformation": "Environment",
            "society": "Other",
        },
    }
    cities.append(nm)
    json.dump(cities, open(os.path.join(ROOT, "cities.json"), "w"), indent=2)
    print(f"Added New Mexico to cities.json ({len(cities)} cities total)")
