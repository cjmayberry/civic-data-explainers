---
title: "City Boundaries"
date: "2026-06-09"
description: "This dataset can be used to determine the boundary of the City of Oklahoma City and used for comparison to address information or other location-based datasets."
teaser: "This dataset shows the exact boundary lines of Oklahoma City"
tags: [" oklahoma city", "boundary", "boundaries", "city", "jurisdiction"]
categories: ["Government"]
cover: "covers/city-boundaries-8699b841--government--map_real_geometry.png"
source_url: "https://utility.arcgis.com/usrsvcs/servers/8699b8414ebd476e87db5486f116b00a/rest/services/OpenData/Government_Boundaries/FeatureServer/1"
license: "custom"
dataset_id: "8699b8414ebd476e87db5486f116b00a"
city: "Oklahoma City"
site_url: "https://open-okc.hub.arcgis.com"
draft: false
dictionary:
  - field: "ObjectID"
    description: "Numeric unique identifier with no special meaning"
  - field: "City Name"
    description: "Name of city"
  - field: "City FIPS"
    description: "Numeric code used to identitfy a geographic region based on the Federal Information Processing Standards (FIPS) of the United States governement"
  - field: "Shape"
    description: "Geographic data in state plane coordinates (WKID 103512)"
  - field: "Area"
    description: "Approximate area of feature in US square feet"
  - field: "Length"
    description: "Approximate length of perimeter of feature in US feet"
---



## What this is  
This dataset shows the exact boundary lines of Oklahoma City.

## Why it matters to you  
Knowing where city limits fall affects real decisions: whether a property qualifies for city services (like trash pickup), which police department responds to 911 calls, or whether a business needs to file taxes with the city or county. Developers also check these boundaries to confirm zoning rules before buying land.

## How to read this data  
- **City Name**: Confirms this is Oklahoma City’s boundary (useful when comparing to other cities’ datasets).  
- **City FIPS**: A government code that helps link this map to other datasets like census or tax records.  
- **Area/Length**: Technical measurements (in feet) used by planners—most residents can ignore these.  

## Where this leaves you  
While you can’t look up specific addresses here, this dataset helps other tools verify if locations fall inside city limits. Check your water bill or local zoning maps to confirm your address’s status.
