---
title: "Hotel Motel Tax"
date: "2026-06-09"
description: "This dataset can be to determine hotels that have an active license issued by the City of Oklahoma City."
teaser: "This dataset tracks hotels and motels with active tax licenses in Oklahoma City"
tags: ["oklahoma city", "hotels", "motels", "tax", "license", "certificate", "revenue"]
categories: ["Finance"]
cover: "covers/hotel-motel-tax-b6e78aa9--finance--map_real_geometry.png"
map_data: "img/data/hotel-motel-tax-b6e78aa9.geojson"
inquiry_enabled: true
inquiry_search: "LegalName"
inquiry_field: "Sector"
inquiry_label: "Check a hotel/motel registration"
inquiry_extra: ["Address", "Certificate"]
source_url: "https://utility.arcgis.com/usrsvcs/servers/b6e78aa9a14c494f827ea0f24418cac7/rest/services/OpenData/Finance/FeatureServer/3"
license: "custom"
dataset_id: "b6e78aa9a14c494f827ea0f24418cac7"
city: "Oklahoma City"
site_url: "https://open-okc.hub.arcgis.com"
draft: false
dictionary:
  - field: "ObjectID"
    description: "Numeric unique identifier with no special meaning"
  - field: "Legal Name"
    description: "Name of business entity that certificate is issued to"
  - field: "Address"
    description: "House number and full street name associated with issued certificate"
  - field: "Certificate"
    description: "Number associated with issued certificate"
  - field: "Sector"
    description: "Sector (NW, NE, SW, SE, Central) within the City of Oklahoma City"
  - field: "Shape"
    description: "Geographic data in state plane coordinates (WKID 103512)"
---







## What this is  
This dataset tracks hotels and motels with active tax licenses in Oklahoma City.

## Why it matters to you  
When traveling or booking accommodations, you might want to verify if a hotel is properly licensed by the city. This data also helps small businesses (like nearby restaurants or tour operators) identify licensed hotels to partner with for promotions or referrals. The city uses this to ensure tax compliance and track tourism activity.

## How to read this data  
- **Legal Name**: The official business name of the hotel/motel (e.g., "Sunset Inn LLC").  
- **Address**: The exact street address where the business operates.  
- **Certificate**: The unique license number issued by the city (e.g., "HM-2023-0456").  
- **Sector**: Which part of the city the hotel is in (NW, NE, SW, SE, or Central).  

## Try it yourself  
Search the dataset for hotels near your neighborhood or an upcoming event venue by filtering for the **Sector** field (e.g., "Central" for downtown). Check if a hotel you’re considering has a valid license by matching its name or address.
