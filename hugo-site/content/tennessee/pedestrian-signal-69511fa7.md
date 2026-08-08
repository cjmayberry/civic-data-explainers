---
title: "Pedestrian Signal"
date: "2026-08-02"
description: "ADA-related infrastructure. Includes layers for Pedestrian Signals, Crosswalks, Specialty Pavement Markings, Curb Ramps, and Sidewalks. ADA-related infrastructure. Includes layers for Pedestrian Signals, Crosswalks, Spec"
teaser: "ADA-related infrastructure. Includes layers for Pedestrian Signals, Crosswalks, Specialty Pavement Markings, Curb Ramps, and Sidewalks. ADA-related infrastructure.…"
tags: []
categories: ["Default"]
cover: "covers/pedestrian-signal-69511fa7--default--cover_only.svg"
source_url: "https://services2.arcgis.com/nf3p7v7Zy4fTOh6M/arcgis/rest/services/ADA_Asset_Data/FeatureServer"
license: ""
dataset_id: "https://www.arcgis.com/home/item.html?id=69511fa73a584e2bb37acfa85b177fa5&sublayer=1"
city: "tennessee"
site_url: "https://geodata.tn.gov"
draft: false
---

## What this tracks  
This dataset records ADA-compliant pedestrian infrastructure across Tennessee, including curb ramps, crosswalks, and accessibility features like truncated dome tiles.

## Why it matters to you  
If you use a wheelchair or walk with mobility aids, this data tells you which intersections have properly sloped ramps (under 8.33%) and detectable warning tiles before you plan a route. Small businesses can check if their storefronts meet accessibility standards by comparing their curb ramps' **RAMP_SLOPE_PCT** and **TRUNCATED_DOME_PRESENCE** against ADA requirements. Cities use this to prioritize repairs where ramps exceed slope limits or lack safety features.

## How to read this data  
**FEATURE_DESCRIPTION** — Type of infrastructure (e.g., "Driveway", "Curb Ramp").  
**RAMP_SLOPE_PCT** — Steepness of ramps; ADA requires under 8.33% (sample: 7.7).  
**TRUNCATED_DOME_PRESENCE** — Whether tactile warning tiles exist (2 = present).  
**COUNTY_NAME** — Location county (sample: "Bedford").  

## Try it yourself  
Look up your nearest intersection using the **STREETSMART_URL** field to see if curb ramps have tactile domes and safe slopes.
