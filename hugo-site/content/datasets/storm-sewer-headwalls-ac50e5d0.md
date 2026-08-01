---
title: "Storm Sewer Headwalls"
date: "2026-06-03"
description: "This dataset can be used to determine storm sewer headwall locations and related attributes within the City of Oklahoma City."
teaser: "A map of storm sewer headwalls (the concrete structures where storm drains meet pipes) across Oklahoma City"
tags: [" oklahoma city", "storm", "sewer", "headwalls", "conrete", "earthen", "grass", "channels", "flumes", "gabion", "baskets", "grated inlets", "rip rap", "slop wall"]
categories: ["Infrastructure"]
cover: "covers/storm-sewer-headwalls-ac50e5d0--infrastructure--map_real_geometry.svg"
source_url: "https://utility.arcgis.com/usrsvcs/servers/ac50e5d0600e428d8618b5e2dc48782d/rest/services/OpenData/Infrastructure_Hydrology/FeatureServer/1"
license: "custom"
dataset_id: "ac50e5d0600e428d8618b5e2dc48782d"
city: "Oklahoma City"
site_url: "https://open-okc.hub.arcgis.com"
draft: false
dictionary:
  - field: "ObjectID"
    description: "Numeric unique identifier with no special meaning"
  - field: "Sub Type"
    description: "Type of headwall"
  - field: "Project Number"
    description: "Public Works project number associated with headwall"
  - field: "Location"
    description: "Text description of location"
  - field: "Comments"
    description: "Comments related to headwall"
  - field: "Shape"
    description: "Geographic data in state plane coordinates (WKID 103512)"
---

## What this is  
A map of storm sewer headwalls (the concrete structures where storm drains meet pipes) across Oklahoma City.

## Why it matters to you  
Headwalls prevent erosion where stormwater enters pipes. If one fails near your property, it could cause flooding or sinkholes. This data helps:  
- Neighbors report clogged or damaged headwalls after heavy rain  
- Developers check drainage infrastructure before building  
- Homebuyers assess flood risks near a property  

## How to read this data  
Key fields in the dataset:  
- **Sub Type**: What kind of headwall (e.g., "concrete box", "pipe end")  
- **Location**: Written description like "SW corner of 12th St & Western Ave"  
- **Project Number**: Links to construction records if repairs were done  

## Try it yourself  
[Open the map](https://www.okc.gov/departments/planning/gis-maps/gis-data) and search your street name in the "Location" field to find headwalls near you. Note any with "Comments" about maintenance needs.  

*(Word count: 175)*
