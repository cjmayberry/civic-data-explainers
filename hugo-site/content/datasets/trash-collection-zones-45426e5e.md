---
title: "Trash Collection Zones"
date: "2026-06-10"
description: "This dataset can be used to determine trash collection zones within the City of Oklahoma City."
teaser: "This dataset shows where and when trash gets picked up across Oklahoma City"
tags: ["oklahoma city", "trash", "waste", "pickup", "zones"]
categories: ["Infrastructure"]
cover: "covers/trash-collection-zones-45426e5e--infrastructure--map_real_geometry.png"
source_url: "https://utility.arcgis.com/usrsvcs/servers/45426e5e1b31489db9afea603870f724/rest/services/OpenData/Utilities/FeatureServer/1"
license: "custom"
dataset_id: "45426e5e1b31489db9afea603870f724"
city: "Oklahoma City"
site_url: "https://open-okc.hub.arcgis.com"
draft: false
dictionary:
  - field: "ObjectID"
    description: "Numeric unique identifier with no special meaning"
  - field: "Route"
    description: "Alphanumeric name of pickup route"
  - field: "Pickup Day"
    description: "Day of week/month that route normally runs"
  - field: "Service Provider"
    description: "Name of entity providing actually service"
  - field: "Shape"
    description: "Geographic data in state plane coordinates (WKID 103512)"
  - field: "Area"
    description: "Approximate area of feature in US square feet"
  - field: "Length"
    description: "Approximate length of perimeter of feature in US feet"
---



## What this is  
This dataset shows where and when trash gets picked up across Oklahoma City.

## Why it matters to you  
Knowing your trash collection zone answers practical questions like:  
- Which day to roll your bins to the curb  
- Who to call if pickup gets missed (city crew or private contractor)  
- Whether holiday schedules might delay your service  

## How to read this data  
Key fields to check:  
- **Route**: Identifies your neighborhood's pickup group (like "NW-12")  
- **Pickup Day**: Shows your collection day (e.g., "Every Tuesday" or "1st/3rd Friday")  
- **Service Provider**: Tells you whether the city or a company like Waste Management handles your area  

## Try it yourself  
1. Open the [interactive map](https://data.okc.gov/) (or your city's GIS portal)  
2. Type your address to see your zone's:  
   - Color-coded route area  
   - Next pickup date  
   - Provider contact info  

(Word count: 160)
