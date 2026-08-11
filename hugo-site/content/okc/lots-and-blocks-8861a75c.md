---
title: "Lots and Blocks"
date: "2026-06-09"
description: "This dataset can be used to determine the lot and block number for a platted area within the City of Oklahoma City."
teaser: "This dataset tracks the official lot and block numbers for platted properties in Oklahoma City"
tags: [" oklahoma city", "plats", "subdivision", "lots", "blocks", "boundary", "boundaries"]
categories: ["Licensing"]
cover: "covers/lots-and-blocks-8861a75c--licensing--placeholder.svg"
source_url: "https://utility.arcgis.com/usrsvcs/servers/8861a75c02214e6dae3bf9c094fab65f/rest/services/OpenData/Licensing_Subdivision/FeatureServer/3"
license: "custom"
dataset_id: "8861a75c02214e6dae3bf9c094fab65f"
city: "okc"
site_url: "https://open-okc.hub.arcgis.com"
map_link: "https://open-okc.hub.arcgis.com/datasets/8861a75c02214e6dae3bf9c094fab65f_3"
geojson_url: "https://utility.arcgis.com/usrsvcs/servers/8861a75c02214e6dae3bf9c094fab65f/rest/services/OpenData/Licensing_Subdivision/FeatureServer/3/query?where=1%3D1&f=geojson&outSR=4326&resultRecordCount=1500"
maintained_by: "This dataset is maintained by the Planning Department of the City of Oklahoma City."
draft: false
dictionary:
  - field: "ObjectID"
    description: "Numeric unique identifier with no special meaning"
  - field: "Plat Name"
    description: "Name of plat associated with record"
  - field: "Block Number"
    description: "Numeric number for block"
  - field: "Lot Number"
    description: "Numeric number for lot"
  - field: "Shape"
    description: "Geographic data in state plane coordinates (WKID 103512)"
  - field: "Area"
    description: "Approximate area of feature in US square feet"
  - field: "Length"
    description: "Approximate length of perimeter of feature in US feet"
---










## What this is  
This dataset tracks the official lot and block numbers for platted properties in Oklahoma City.  

## Why it matters to you  
Every property in the city has a legal description tied to its plat (a map dividing land into lots and blocks). Knowing your lot and block helps when:  
- Verifying property boundaries for fences, additions, or disputes  
- Applying for building permits that require exact parcel identification  
- Researching zoning rules that apply to your specific lot  

## How to read this data  
Key fields include:  
- **Plat Name**: The official name of the subdivision map your lot belongs to (e.g., "Smith Addition")  
- **Block Number**: The numbered block within that plat (like a neighborhood grid)  
- **Lot Number**: Your parcel’s specific identifier within the block  

## Try it yourself  
Look up your address in the dataset to find:  
1. Your plat name (often referencing the original developer)  
2. Your block and lot numbers — key details for any property paperwork  

*(Note: The dataset includes area/length fields for surveyors, but most residents just need the plat, block, and lot numbers.)*
