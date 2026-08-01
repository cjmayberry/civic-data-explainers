---
title: "Fire Stations"
date: "2026-06-03"
description: "This dataset can be used to view the location of fire stations within the City of Oklahoma City."
teaser: "The response-time backbone: where OKC’s fire stations sit — and what “Facility Name” really is."
tags: ["OKC", "Fire", "oklahoma city", "stations", "oklahoma city"]
categories: ["Public Safety"]
cover: "covers/fire-stations-7f57d399--public-safety--map_real_geometry.png"
map_data: "img/data/fire-stations-7f57d399.geojson"
source_url: "https://utility.arcgis.com/usrsvcs/servers/7f57d399cbd1468d877a8411205a671d/rest/services/OpenData/Public_Safety/FeatureServer/4"
license: "custom"
dataset_id: "7f57d399cbd1468d877a8411205a671d"
city: "Oklahoma City"
site_url: "https://open-okc.hub.arcgis.com"
draft: false
dictionary:
  - field: "ObjectID"
    description: "Numeric unique identifier with no special meaning"
  - field: "Facility Name"
    description: "Numeric identifier of fire station"
  - field: "Facility Address"
    description: "Address of fire station"
  - field: "Shape"
    description: "Geographic data in state plane coordinates (WKID 103512)"
---






## What this is

The locations of Oklahoma City fire stations — the fixed points the entire emergency response system is built around.

## Why it matters to you

Emergency response is a geometry problem: minutes are saved or lost based on where stations sit relative to where people live and work. This dataset is the anchor for that calculation — planners use station locations to model response times and decide where the next station should go. For you, it answers a practical question: how far is the nearest station from your home or business? (That number shows up in insurance pricing, too.)

## How to read this data

- **Facility Name** — despite the name, the catalog notes this is a *numeric identifier* of the station, not a friendly name. A good reminder to read field descriptions instead of assuming.
- **Facility Address** — where the station is. Cross-reference with ward and zoning maps and you can see how public safety facilities are distributed across the city.

## Try it yourself

Find the nearest station to your home and estimate the drive time. Then check the gaps — which part of town looks farthest from any station? That's where response times are longest, and it's the kind of observation this dataset exists to make.
