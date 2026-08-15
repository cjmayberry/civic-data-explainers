---
title: "Ramp"
date: "2026-08-02"
description: "Feature service for collecting field data using the ArcGIS for Collector app. Enabled for offline-editing."
teaser: "Feature service for collecting field data using the ArcGIS for Collector app. Enabled for offline-editing."
tags: ["Nevada", "transportation", "NDOT", "ADA", "American", "Disability", "feature", "collection", "right of way"]
categories: ["Transportation"]
cover: "covers/ramp-ee16995a--transportation--placeholder.svg"
source_url: "https://services1.arcgis.com/9Y4hSlLf13E9S0Eo/arcgis/rest/services/PROD/FeatureServer/0"
license: ""
dataset_id: "https://www.arcgis.com/home/item.html?id=ee16995a65df43578cd87c72f3256fc9&sublayer=0"
city: "nevada"
site_url: "https://civic-data-explainers.pages.dev"
draft: false
---

## What this tracks  
This dataset records measurements and compliance details of ADA-accessible ramps at intersections across Nevada, including slope angles, landing dimensions, and inspection status.  

## Why it matters to you  
If you use a wheelchair or walk with mobility aids, this data tells you whether ramps on your commute meet accessibility standards. A business owner can check if their storefront’s nearby ramps are **Compliant** before planning renovations, avoiding costly retrofits later. Residents can identify non-compliant ramps (like those with steep **RampSlopeCenter** values) to report to Nevada’s transportation department for prioritization.  

## How to read this data  
**RampSlopeCenter** — The steepness of the ramp’s middle section (e.g., 6.3% means it rises 6.3 inches per 100 inches horizontally). Lower values are safer.  
**ComplianceStatus** — Whether the ramp meets ADA standards (e.g., "Compliant" or needs repair).  
**LandingWidth** — Flat space at the ramp’s top/bottom (e.g., 4.3 feet). Wider landings are easier to navigate.  
**DWS_Width** — Tactile warning strip coverage (e.g., "DWS spans full width of ramp" means better visibility for visually impaired pedestrians).  

## Try it yourself  
Look up your nearest intersection in Nevada’s [ADA ramp map](https://gis.ndot.maps.arcgis.com/) to see if its ramps are marked "Compliant" or need upgrades.
