---
title: "Storm Sewer Junctions"
date: "2026-06-03"
description: "This dataset can be used to determine storm sewer junctions, such as inlet boxes, junction boxes, and manholes, within the City of Oklahoma City."
teaser: "A map of storm sewer connection points like drain inlets and manholes across Oklahoma City"
tags: [" oklahoma city", "storm", "sewer", "junction", "conrete", "earthen", "grass", "channels", "flumes", "gabion", "baskets", "grated inlets", "rip rap", "slop wall"]
categories: ["Infrastructure"]
cover: "covers/storm-sewer-junctions-35d63012--infrastructure--map_real_geometry.svg"
source_url: "https://utility.arcgis.com/usrsvcs/servers/35d63012d1534c67899f79ad75a53ca1/rest/services/OpenData/Infrastructure_Hydrology/FeatureServer/0"
license: "custom"
dataset_id: "35d63012d1534c67899f79ad75a53ca1"
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
A map of storm sewer connection points like drain inlets and manholes across Oklahoma City.

## Why it matters to you  
When heavy rain hits, these junctions determine where water pools or flows. Knowing their locations helps you:  
- Report flooding risks near your property  
- Check if new construction might block drainage  
- Understand why certain streets flood repeatedly  

## How to read this data  
Key fields include:  
- **Sub Type**: What kind of junction it is (e.g., inlet box, manhole)  
- **Location**: A written description of where it’s placed (e.g., "NW corner of 5th and Hudson")  
- **Project Number**: Links the junction to a city construction project (if applicable)  

## Try it yourself  
Search the map for junctions near your home or business—note any that are clogged or damaged, and report them to Public Works with the **ObjectID** for faster service.  

*(Note: "Shape" field is for GIS professionals and won’t help most residents.)*
