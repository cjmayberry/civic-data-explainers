---
title: "Sidewalks"
date: "2026-06-09"
description: "This dataset can be used to view sidewalks maintained by the City of Oklahoma City and the funding source if available."
teaser: "The walkability map: every city-maintained sidewalk in OKC — and which ones were paid for with bonds."
tags: ["okc", "oklahoma city", "sidewalks"]
categories: ["Transportation"]
cover: "covers/sidewalks-bc31068e--transportation--map_real_geometry.png"
source_url: "https://utility.arcgis.com/usrsvcs/servers/bc31068e20ed4b2fa1265bb810b1de23/rest/services/OpenData/Transportation/FeatureServer/1"
license: "custom"
dataset_id: "bc31068e20ed4b2fa1265bb810b1de23"
city: "Oklahoma City"
site_url: "https://open-okc.hub.arcgis.com"
draft: false
dictionary:
  - field: "ObjectID"
    description: "Numeric unique identifier with no special meaning"
  - field: "Sidewalk Funding"
    description: "Funding, if known, associated with sidewalk"
  - field: "Shape"
    description: "Geographic data in state plane coordinates (WKID 103512)"
  - field: "Length"
    description: "Approximate length of perimeter of feature in US feet"
  - field: "Area"
    description: "Approximate area of feature in US square feet"
---




## What this is

Every sidewalk maintained by the City of Oklahoma City, mapped with its funding source where known.

## Why it matters to you

Sidewalks are the most used piece of city infrastructure you never think about — until one is missing. This dataset shows which sidewalks exist and, crucially, *who paid for them*. That funding field is the story of how OKC builds walkable neighborhoods: many newer sidewalks were paid for with GO Bond money, which means they were voted on by residents like you. If a sidewalk gap is breaking up your walk to school or the bus stop, this map shows you're not imagining it — the city's own data confirms what's missing.

## How to read this data

- **Sidewalk Funding** — the funding source (GO Bond or other initiatives). The catalog is honest: this is generally only filled in for *newer* sidewalks, so an empty field doesn't mean "no sidewalk" — it means "no funding record."
- **Length** — the length of the sidewalk segment in feet. Chain segments together to measure a whole route.

## Try it yourself

Trace the route from your home to the nearest school or bus stop on the sidewalk map. Count the gaps. If you find one, that's a specific, data-backed request you can take to your council member — city decisions run on documented needs, and this dataset is the documentation.
