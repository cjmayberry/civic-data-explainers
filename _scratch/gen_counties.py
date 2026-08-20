#!/usr/bin/env python3
"""Generate county pages for New Mexico, Idaho, and Utah.

Each county gets a minimal Hugo markdown file so the state's card grid
shows something before real datasets are wired in.
"""
import json, os

ROOT = "/opt/data/civic-data-explainers"
CONTENT = os.path.join(ROOT, "hugo-site/content")

counties = {
    "newmexico": {
        "name": "New Mexico",
        "counties": [
            "Bernalillo", "Catron", "Chaves", "Cibola", "Colfax", "Curry",
            "De Baca", "Doña Ana", "Eddy", "Esmeralda", "Grant", "Guadalupe",
            "Harding", "Hidalgo", "Lea", "Luna", "McKinley", "Mora",
            "Otero", "Quay", "Rio Arriba", "Roosevelt", "Sandoval", "San Juan",
            "San Miguel", "Santa Fe", "Sierra", "Socorro", "Taos", "Torrance",
            "Union", "Valencia",
        ],
    },
    "idaho": {
        "name": "Idaho",
        "counties": [
            "Ada", "Adams", "Bannock", "Bear Lake", "Benewah", "Boise",
            "Bonner", "Boundary", "Butte", "Camas", "Canyon", "Caribou",
            "Cassia", "Clark", "Clearwater", "Custer", "Douglas", "Elmore",
            "Franklin", "Fremont", "Gem", "Gooding", "Idaho", "Jefferson",
            "Jerome", "Kootenai", "Latah", "Lemhi", "Lewis", "Lincoln",
            "Madison", "Minidoka", "Nez Perce", "Oneida", "Owyhee", "Payette",
            "Power", "Shoshone", "Teton", "Twin Falls", "Valley", "Washington",
            "Wayne", "Wright",
        ],
    },
    "utah": {
        "name": "Utah",
        "counties": [
            "Beaver", "Box Elder", "Cache", "Carbon", "Daggett", "Davis",
            "Duchesne", "Emery", "Garfield", "Grand", "Iron", "Juab", "Kane",
            "Millard", "Morgan", "Piute", "Rich", "Salt Lake", "San Juan",
            "Sanpete", "Sevier", "Summit", "Tooele", "Uintah", "Utah",
            "Wasatch", "Washington", "Wayne", "Weber",
        ],
    },
}

written = 0
for state, info in counties.items():
    state_name = info["name"]
    county_list = info["counties"]
    state_dir = os.path.join(CONTENT, state)
    os.makedirs(state_dir, exist_ok=True)
    for county in county_list:
        slug = county.lower().replace(" ", "-")
        path = os.path.join(state_dir, f"{slug}.md")
        if not os.path.exists(path):
            md = f"""---
title: "{county} County"
date: "2026-08-18"
teaser: "{county} County, {state_name} — open data explainers"
categories: ["County"]
city: "{state}"
site_url: "https://civic-data-explainers.pages.dev"
draft: false
---
"""
            with open(path, "w") as f:
                f.write(md)
            written += 1

print(f"Wrote {written} county pages across NM/ID/UT")
