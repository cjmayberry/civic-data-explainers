#!/usr/bin/env python3
"""Wire Utah into cities.json (Utah AGOL / GIS portal)."""
import json, os

ROOT = "/opt/data/civic-data-explainers"
cities = json.load(open(os.path.join(ROOT, "cities.json")))

if any(c["id"] == "utah" for c in cities):
    print("Utah already in cities.json")
else:
    utah = {
        "id": "utah",
        "name": "Utah",
        "hub_url": "https://gis.utah.gov/",
        "gov_url": "https://utah.gov",
        "state": "UT",
        "active": True,
        "model": None,
        "min_score": 0,
        "content_dir": "hugo-site/content/utah",
        "static_dir": "hugo-site/static/utah",
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
    cities.append(utah)
    json.dump(cities, open(os.path.join(ROOT, "cities.json"), "w"), indent=2)
    print(f"Added Utah to cities.json ({len(cities)} cities total)")
