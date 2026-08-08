---
title: "Sidewalks"
date: "2026-08-02"
description: "ADA-related infrastructure. Includes layers for Pedestrian Signals, Crosswalks, Specialty Pavement Markings, Curb Ramps, and Sidewalks. ADA-related infrastructure. Includes layers for Pedestrian Signals, Crosswalks, Spec"
teaser: "ADA-related infrastructure. Includes layers for Pedestrian Signals, Crosswalks, Specialty Pavement Markings, Curb Ramps, and Sidewalks. ADA-related infrastructure.…"
tags: ["T", "D", "O", ",", "e", "n", "s", "p", "a", "r", "t", "m", "o", "f", "i", "A", "M", "g", "v", "I", "y", "C", "w", "l", "k", "u", "b", "P", "d", "S", "c"]
categories: ["Default"]
cover: "covers/sidewalks-69511fa7--default--cover_only.svg"
source_url: "https://services2.arcgis.com/nf3p7v7Zy4fTOh6M/arcgis/rest/services/ADA_Asset_Data/FeatureServer"
license: ""
dataset_id: "https://www.arcgis.com/home/item.html?id=69511fa73a584e2bb37acfa85b177fa5&sublayer=3"
city: "tennessee"
site_url: "https://geodata.tn.gov"
draft: false
---

## What this tracks  
This dataset records ADA-compliant sidewalk features across Tennessee, including curb ramps, crosswalks, and pedestrian signals.

## Why it matters to you  
If you use a wheelchair or walk with mobility aids, this data tells you whether a specific intersection has properly sloped ramps (under 8.33%) and detectable warning domes before you plan a route. Business owners can check if their storefront meets accessibility standards by reviewing the **RAMP_SLOPE_PCT** and **TRUNCATED_DOME_PRESENCE** values nearby.

## How to read this data  
**FEATURE_DESCRIPTION** — Identifies the type of infrastructure, like "Driveway" or "Curb Ramp" (sample value: "Driveway").  
**RAMP_SLOPE_PCT** — Measures ramp steepness; ADA requires under 8.33% (sample: 7.7%).  
**TRUNCATED_DOME_PRESENCE** — Indicates tactile warning domes for the visually impaired (sample: 2, likely meaning "present").  
**LOCATION_DESCRIPTION** — Side of the road the feature is on, like "Right" (sample: "Right").  

## Try it yourself  
Look up your nearest intersection using the **STREETSMART_URL** field to see if curb ramps meet accessibility standards. The link provides a street-level view with measurement tools.
