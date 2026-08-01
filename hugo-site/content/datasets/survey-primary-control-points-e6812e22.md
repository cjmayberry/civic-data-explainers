---
title: "Survey Primary Control Points"
date: "2026-06-22"
description: "This dataset can be used to find out information on primary survey control points for the City of Oklahoma City."
teaser: "A map of permanent survey markers that help engineers and builders measure land accurately across Oklahoma City"
tags: ["okc", "oklahoma city", "surveys", "control", "points", "monuments"]
categories: ["Infrastructure"]
cover: "covers/survey-primary-control-points-e6812e22--infrastructure--map_real_geometry.png"
map_data: "img/data/survey-primary-control-points-e6812e22.geojson"
source_url: "https://utility.arcgis.com/usrsvcs/servers/e6812e2241ba4ff68d77edd95ad049b8/rest/services/OpenData/Infrastructure_Survey/FeatureServer/0"
license: "custom"
dataset_id: "e6812e2241ba4ff68d77edd95ad049b8"
city: "Oklahoma City"
site_url: "https://open-okc.hub.arcgis.com"
draft: false
dictionary:
  - field: "ObjectID"
    description: "Numeric unique identifier with no special meaning"
  - field: "Status"
    description: "Status of monument as of last inspection"
  - field: "Station number"
    description: "Station number associated with monument"
  - field: "Condition"
    description: "Condition of monument as of last inspection"
  - field: "Description"
    description: "Comments related to monument"
  - field: "Material"
    description: "Abbreviated material code"
  - field: "Contractor"
    description: "Contractor used to set or verify monument"
  - field: "Datum"
    description: "Datum used to derive location (X Y coordinates)"
  - field: "Date Set"
    description: "Date, if known, when monument was set"
  - field: "Monument Type"
    description: "Type of monument"
  - field: "X Coordinate"
    description: "X coordinate based on specified datum"
  - field: "Y Coordinate"
    description: "Y coordinate based on specified datum"
  - field: "Shape"
    description: "Geographic data in state plane coordinates (WKID 103512)"
---



## What this is  
A map of permanent survey markers that help engineers and builders measure land accurately across Oklahoma City.

## Why it matters to you  
These metal or concrete markers (called "monuments") are the foundation for all property surveys and construction projects. When a developer builds a new shopping center or when your neighbor puts up a fence, surveyors use these exact points to confirm boundary lines. If markers go missing or get damaged, it can delay construction projects and even lead to property disputes.

## How to read this data  
Key fields include:  
- **Status**: Whether the marker is currently usable (like "Active" or "Destroyed")  
- **Condition**: Physical state (like "Good" or "Needs Repair")  
- **Monument Type**: What it’s made of (e.g., "Brass Disk" or "Steel Rod")  
- **X/Y Coordinates**: Precise map locations (for professionals with GIS tools)  

## Where this leaves you  
This isn’t something you’d look up for your home address—it’s specialized infrastructure for surveyors. But if you ever see a metal disk stamped "OKC CONTROL" in a sidewalk, now you know it’s part of the city’s measurement backbone.
