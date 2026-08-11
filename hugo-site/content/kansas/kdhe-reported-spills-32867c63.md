---
title: "KDHE Reported Spills"
date: "2026-08-02"
description: "Data is updated NIGHTLY via scripting (disregard the ArcGIS Online dates). This map service contains point data that represents spills reported to KDHE. The KDHE Spills Program works in conjunction with the Kansas Corpor"
teaser: "Data is updated NIGHTLY via scripting (disregard the ArcGIS Online dates). This map service contains point data that represents spills reported to KDHE. The KDHE Spills…"
categories: ["Default"]
cover: "covers/kdhe-reported-spills-32867c63--default--placeholder.svg"
source_url: "https://maps.kdhe.ks.gov/kdhe_doe/rest/services/BER/Spills_DASC/FeatureServer/0"
geojson_url: "https://maps.kdhe.ks.gov/kdhe_doe/rest/services/BER/Spills_DASC/FeatureServer/0/query?where=1%3D1&f=geojson&outSR=4326&resultRecordCount=1500"
license: ""
dataset_id: "https://www.arcgis.com/home/item.html?id=32867c632bfe4a4c844aadfcf75f2f27&sublayer=0"
city: "kansas"
site_url: "https://civic-data-explainers.pages.dev"
draft: false
---

## What this tracks  
This dataset records hazardous material spills reported to the Kansas Department of Health and Environment (KDHE), including details like location, materials involved, and cleanup status.  

## Why it matters to you  
If you're buying property near 3354 Rainbow Blvd in Kansas City, this data reveals past spills like transformer oil leaks that could affect soil or groundwater. Business owners can check whether suppliers (like the Board of Public Utilities) have recent spill records before signing contracts. Renters in Wyandotte County can see if their neighborhood has recurring issues, such as equipment failures contaminating local waterways.  

## How to read this data  
**SPILL_DATE** — When the spill occurred (e.g., 1358964000000, a Unix timestamp convertible to a readable date).  
**MATERIAL_COMBO** — The substance and quantity spilled (e.g., ".5 liter of electrical insulating oil/mineral oil").  
**CLEANUP_METHOD** — How the spill was addressed (e.g., "physical removal").  
**ADDRESS** — Exact spill location (e.g., "3354 Rainbow Blvd").  

## Try it yourself  
Search the [KDHE Spills map](https://maps.kdhe.ks.gov/) for your ZIP code (like 66103) to see active or historical spills near your home or workplace.
