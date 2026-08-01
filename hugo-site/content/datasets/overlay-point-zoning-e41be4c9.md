---
title: "Overlay Point Zoning"
date: "2026-06-03"
description: "This dataset can used to view locations with special zoning considerations within the City of Oklahoma City."
teaser: "This dataset tracks locations in Oklahoma City with special zoning rules that override standard zoning codes"
tags: ["oklahoma city", "zoning", "zones", "subdivision", "boundary", "boundaries", "overlay", "point", "special", "zngdswl"]
categories: ["Licensing"]
cover: "covers/overlay-point-zoning-e41be4c9--licensing--map_real_geometry.png"
map_data: "img/data/overlay-point-zoning-e41be4c9.geojson"
source_url: "https://utility.arcgis.com/usrsvcs/servers/e41be4c9bd794c2db35270448da83c82/rest/services/OpenData/Licensing_Zoning/FeatureServer/0"
license: "custom"
dataset_id: "e41be4c9bd794c2db35270448da83c82"
city: "Oklahoma City"
site_url: "https://open-okc.hub.arcgis.com"
draft: false
dictionary:
  - field: "ObjectID"
    description: "Numeric unique identifier with no special meaning"
  - field: "Zoning Class"
    description: "Abbreviated zoning code"
  - field: "Full Case"
    description: "Planning case number associated with area (if any)"
  - field: "Description"
    description: "Text description of specific zoning that applies"
  - field: "Ordinance Number"
    description: "City ordinance reference number (if any)"
  - field: "Shape"
    description: "Geographic data in state plane coordinates (WKID 103512)"
---





## What this is  
This dataset tracks locations in Oklahoma City with special zoning rules that override standard zoning codes.

## Why it matters to you  
Special zoning can determine what you're allowed to build or operate on a property. If you're buying land to open a business, adding a structure to your home, or contesting a neighbor's construction plans, these overlay zones could change what's legally permitted—even if the base zoning seems to allow it. For example, a historic district overlay might block vinyl siding, or a floodplain overlay could require elevated foundations.

## How to read this data  
- **Zoning Class**: Short code (like "H" for historic or "FP" for floodplain) showing the type of special zoning.  
- **Description**: Plain-English details (e.g., "Design Review Overlay: Exterior changes require approval").  
- **Ordinance Number**: Reference to the city law that created this exception—useful for looking up official rules.  

## Where this leaves you  
This data doesn't let you search by address, but you can cross-reference it with a zoning map to spot overlaps near your property. Check the city’s main zoning dataset first to see if overlays apply to your area.
