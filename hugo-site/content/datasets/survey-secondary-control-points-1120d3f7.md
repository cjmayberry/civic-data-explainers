---
title: "Survey Secondary Control Points"
date: "2026-06-22"
description: "This dataset can be used to find out information on secondary survey control points for the City of Oklahoma City."
teaser: "A dataset of permanent survey markers (called \"secondary control points\") that help map and measure Oklahoma City accurately"
tags: ["okc", "oklahoma city", "surveys", "control", "points", "monuments"]
categories: ["Infrastructure"]
cover: "covers/survey-secondary-control-points-1120d3f7--infrastructure--map_real_geometry.png"
map_data: "img/data/survey-secondary-control-points-1120d3f7.geojson"
source_url: "https://utility.arcgis.com/usrsvcs/servers/1120d3f72fe64245a799851598fb83c6/rest/services/OpenData/Infrastructure_Survey/FeatureServer/1"
license: "custom"
dataset_id: "1120d3f72fe64245a799851598fb83c6"
city: "Oklahoma City"
site_url: "https://open-okc.hub.arcgis.com"
draft: false
dictionary:
  - field: "ObjectID"
    description: "Numeric unique identifier with no special meaning"
  - field: "Station number"
    description: "Station number associated with monument"
  - field: "Easting"
    description: "East coordinate base on datum (WKID 103512)"
  - field: "Northing"
    description: "North coordinate base on datum (WKID 103512)"
  - field: "Elevation"
    description: "Elevation above sea level in US feet"
  - field: "Code"
    description: "Code associated with monument"
  - field: "Description"
    description: "Additional comments about location of monument"
  - field: "Source"
    description: "Entity providing information on monument"
  - field: "Material Code"
    description: "Code for material of monument"
  - field: "Size Code"
    description: "Code used for size of monument"
  - field: "Shape"
    description: "Geographic data in state plane coordinates (WKID 103512)"
---







## What this is  
A dataset of permanent survey markers (called "secondary control points") that help map and measure Oklahoma City accurately.

## Why it matters to you  
These markers are the hidden reference points that ensure construction projects, property surveys, and infrastructure work align correctly. If a developer builds a new shopping center or the city repairs a bridge, surveyors use these markers to verify locations down to the inch. Errors in these points could mean misplaced property lines or misaligned roads.

## How to read this data  
Key fields include:  
- **Station number**: A unique ID for each survey marker (like "OKC-456").  
- **Easting/Northing**: Precise coordinates in Oklahoma’s state plane system (not latitude/longitude).  
- **Elevation**: Height above sea level in feet—critical for floodplain maps or grading land.  
- **Description**: Notes like "in sidewalk near NW 23rd & Walker" to help locate the physical marker.  

## Where this leaves you  
This dataset doesn’t support address lookups, but professionals use it to anchor legal surveys and engineering plans. If you’re disputing a property line, your surveyor would reference these points.
