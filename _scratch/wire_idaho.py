#!/usr/bin/env python3
"""Wire Idaho into cities.json (Idaho Geospatial Office / IGNIS hub)."""
import json, os

ROOT = "/opt/data/civic-data-explainers"
cities = json.load(open(os.path.join(ROOT, "cities.json")))

if any(c["id"] == "idaho" for c in cities):
    print("Idaho already in cities.json")
else:
    idaho = {
        "id": "idaho",
        "name": "Idaho",
        "hub_url": "https://gis.idaho.gov/",
        "gov_url": "https://www.idaho.gov",
        "state": "ID",
        "active": True,
        "model": None,
        "min_score": 0,
        "content_dir": "hugo-site/content/idaho",
        "static_dir": "hugo-site/static/idaho",
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
    cities.append(idaho)
    json.dump(cities, open(os.path.join(ROOT, "cities.json"), "w"), indent=2)
    print(f"Added Idaho to cities.json ({len(cities)} cities total)")
