---
title: "Elevation Contours"
date: "2026-06-09"
description: "This dataset can be used to view elevation contours derived from lidar planimetric data collected in 2020."
teaser: "This dataset shows elevation lines across the city, marking how high the land is above sea level"
tags: ["oklahoma city", "elevation", "countours", "planimetrics", "2020"]
categories: ["Infrastructure"]
cover: "covers/elevation-contours-1e61c575--infrastructure--map_real_geometry.png"
source_url: "https://utility.arcgis.com/usrsvcs/servers/1e61c57573004a83a6f1694aa0e94f84/rest/services/OpenData/Infrastructure_Planimetrics/FeatureServer/3"
license: "custom"
dataset_id: "1e61c57573004a83a6f1694aa0e94f84"
city: "Oklahoma City"
site_url: "https://open-okc.hub.arcgis.com"
draft: false
dictionary:
  - field: "ObjectID"
    description: "Numeric unique identifier with no special meaning"
  - field: "Elevation"
    description: "Elevation above sea level in US feet"
  - field: "Contour Type"
    description: "Indicates if the contour line is primary or intermediate"
  - field: "Shape"
    description: "Geographic data in state plane coordinates (WKID 103512)"
  - field: "Length"
    description: "Approximate length of feature in US feet"
---





## What this is  
This dataset shows elevation lines across the city, marking how high the land is above sea level.

## Why it matters to you  
Elevation affects flood risks, construction costs, and even where water flows during heavy rain. If you're buying property, building a home, or planning landscaping, these contours show where water might pool or drain. Builders use this to calculate foundation needs, and gardeners use it to predict which plants will thrive.

## How to read this data  
- **Elevation**: The height in feet above sea level (higher numbers = steeper hills)  
- **Contour Type**: "Primary" lines mark major elevation changes (like every 10 feet), while "intermediate" lines show smaller steps  
- **Length**: How long each elevation line runs—longer lines mean flatter areas at that height  

## Where this leaves you  
While you can't look up your exact address, these contours help visualize the city's hills and valleys. For precise elevation at a specific property, you'd need a surveyor to combine this with more detailed data.
