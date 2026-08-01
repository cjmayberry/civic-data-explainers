---
title: "Emergency Responses"
date: "2026-06-03"
description: "This dataset can be used to view select police and fire responses within the City of Oklahoma City."
teaser: "A live-updated list of recent police and fire emergency calls in Oklahoma City"
tags: [" oklahoma city", "police", "ems", "wrecks", "auto", "automobile", "car", "crash"]
categories: ["Public Safety"]
cover: "covers/emergency-responses-01c97e29--public-safety--map_real_geometry.svg"
source_url: "https://utility.arcgis.com/usrsvcs/servers/01c97e2928134efc93157d99f2d23047/rest/services/OpenData/Public_Safety/FeatureServer/0"
license: "custom"
dataset_id: "01c97e2928134efc93157d99f2d23047"
city: "Oklahoma City"
site_url: "https://open-okc.hub.arcgis.com"
draft: false
dictionary:
  - field: "ObjectID"
    description: "Numeric unique identifier with no special meaning"
  - field: "Call Type"
    description: "Type of police or fire call"
  - field: "Description"
    description: "Description of police or fire call"
  - field: "Location"
    description: "Approximate location of call"
  - field: "Reported On"
    description: "Date and time call was reported"
  - field: "Shape"
    description: "Geographic data in state plane coordinates (WKID 103512)"
---

## What this is  
A live-updated list of recent police and fire emergency calls in Oklahoma City.

## Why it matters to you  
This data shows where first responders are being dispatched right now. You might use it to:  
- Check if a siren you just heard was near your home or workplace  
- See if emergency activity is clustered in certain areas over time  
- Understand what types of incidents (car crashes, medical calls, etc.) are most common in your neighborhood  

## How to read this data  
Key fields explained:  
- **Call Type**: Broad category like "Traffic Collision" or "Medical Emergency"  
- **Location**: Approximate street or intersection (not exact addresses)  
- **Reported On**: When the call came in (updates every 5 minutes)  

## Try it yourself  
1. Scan recent calls near your home by searching the map for your street  
2. Look for patterns — do certain call types appear repeatedly at particular times?  
3. Compare different neighborhoods by filtering the "Location" field  

*(Note: Locations are approximate and delayed by 5-15 minutes for responder safety.)*
