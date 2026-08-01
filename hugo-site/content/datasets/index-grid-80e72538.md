---
title: "Index Grid"
date: "2026-06-09"
description: "This dataset can be used to find out the fire index grid numbers for approximate square mile sections within the City of Oklahoma City."
teaser: "This dataset tracks numbered grid squares (about 1 mile wide) used by Oklahoma City’s fire department to organize the city into sections"
tags: ["okc", "oklahoma city", "grids", "fire", "index", "surveys", "boundary", "boundaries"]
categories: ["Infrastructure"]
cover: "covers/index-grid-80e72538--infrastructure--map_real_geometry.png"
source_url: "https://utility.arcgis.com/usrsvcs/servers/80e725387d8848baa12f2374843043e3/rest/services/OpenData/Infrastructure_Survey/FeatureServer/2"
license: "custom"
dataset_id: "80e725387d8848baa12f2374843043e3"
city: "Oklahoma City"
site_url: "https://open-okc.hub.arcgis.com"
draft: false
dictionary:
  - field: "ObjectID"
    description: "Numeric unique identifier with no special meaning"
  - field: "Fire Index Grid"
    description: "Numeric value for grid"
  - field: "Shape"
    description: "Geographic data in state plane coordinates (WKID 103512)"
  - field: "Length"
    description: "Approximate length of perimeter of feature in US feet"
  - field: "Area"
    description: "Approximate area of feature in US square feet"
---





## What this is  
This dataset tracks numbered grid squares (about 1 mile wide) used by Oklahoma City’s fire department to organize the city into sections.  

## Why it matters to you  
Emergency responders use these grid numbers to coordinate calls and track incident locations. While most residents won’t need this daily, knowing your grid helps if you’re reporting a fire or major emergency—dispatchers may ask for it to pinpoint your area faster. Neighborhood groups or businesses planning safety drills might also use these grids to align with city response protocols.  

## How to read this data  
- **Fire Index Grid**: The number assigned to your ~1-square-mile section of the city (e.g., "Grid 42").  
- **Shape/Area**: Technical geographic details (like boundary lines and size) used for mapping systems.  

## Where this leaves you  
This data doesn’t let you look up your grid by typing in an address here—you’d need a separate city map or tool to match your location to a grid number.
