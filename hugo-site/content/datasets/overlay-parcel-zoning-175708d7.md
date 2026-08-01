---
title: "Overlay Parcel Zoning"
date: "2026-06-09"
description: "This dataset can used to view areas with special zoning considerations within the City of Oklahoma City."
teaser: "This dataset tracks special zoning areas in Oklahoma City that have additional rules beyond standard zoning"
tags: ["oklahoma city", "zoning", "zones", "subdivision", "boundary", "boundaries", "overlay", "parcel", "special", "zngdswl"]
categories: ["Licensing"]
cover: "covers/overlay-parcel-zoning-175708d7--licensing--map_real_geometry.svg"
source_url: "https://utility.arcgis.com/usrsvcs/servers/175708d7ab7148109d1b9d27c82008d8/rest/services/OpenData/Licensing_Zoning/FeatureServer/1"
license: "custom"
dataset_id: "175708d7ab7148109d1b9d27c82008d8"
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
    description: "Text description of zoning class"
  - field: "Shape"
    description: "Geographic data in state plane coordinates (WKID 103512)"
  - field: "Area"
    description: "Approximate area of feature in US square feet"
  - field: "Length"
    description: "Approximate length of perimeter of feature in US feet"
---

## What this is  
This dataset tracks special zoning areas in Oklahoma City that have additional rules beyond standard zoning.

## Why it matters to you  
Special zoning overlays can affect what you're allowed to build on a property, whether you can open certain types of businesses, or what renovations require extra permits. For example, a historic district overlay might restrict exterior changes to a home, while an economic development overlay could offer tax breaks for specific business types. These rules directly impact property values and what you can do with land you own.

## How to read this data  
- **Zoning Class**: Short code (like "HD" for Historic District) showing the overlay type  
- **Description**: Plain-English explanation of what the zoning overlay means  
- **Area**: Size of the specially-zoned area in square feet  
- **Full Case**: Reference number for the original planning decision, if you need to look up details  

## Where this leaves you  
While this data shows where special zoning exists, you'll need to cross-reference it with a property map or your parcel number to see if a specific address falls within one of these areas. The zoning codes themselves require additional research to understand all their restrictions.
