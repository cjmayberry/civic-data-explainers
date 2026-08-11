---
title: "KDHE TMDL Stream"
date: "2026-08-02"
description: "This item is updated weekly (disreguard the ArcGIS Online dates). This web app provides general information about Total Maximum Daily Loads (TMDLs) of pollutants in Kansas waterways identified as impaired. Section 303(d)"
teaser: "This item is updated weekly (disreguard the ArcGIS Online dates). This web app provides general information about Total Maximum Daily Loads (TMDLs) of pollutants in…"
categories: ["Default"]
cover: "covers/kdhe-tmdl-stream-910998e2--default--placeholder.svg"
source_url: "https://maps.kdhe.ks.gov/kdhe_oits/rest/services/Reference/TMDL_vw_external/FeatureServer/4"
geojson_url: "https://maps.kdhe.ks.gov/kdhe_oits/rest/services/Reference/TMDL_vw_external/FeatureServer/4/query?where=1%3D1&f=geojson&outSR=4326&resultRecordCount=1500"
license: ""
dataset_id: "https://www.arcgis.com/home/item.html?id=910998e2e4ec4fc69d3359e8a146095e&sublayer=4"
city: "kansas"
site_url: "https://civic-data-explainers.pages.dev"
draft: false
---

## What this tracks  
This dataset records pollution levels and water quality issues in Kansas streams, identifying which waterways exceed safe limits for specific contaminants.

## Why it matters to you  
If you fish in Kansas streams, this data tells you whether your favorite spot has high E. coli levels that could make the water unsafe for swimming. Farmers can check if nearby streams have nitrate or pesticide contamination that might affect irrigation plans. The "High" values in fields like **BIOLOGY** or **E_COLI** signal where KDHE has documented significant water quality problems.

## How to read this data  
**STREAM_NAME** — Identifies the waterway, with values like "Unnamed Stream" for smaller tributaries.  
**E_COLI** — Shows fecal contamination levels, with "High" indicating unsafe bacterial counts. Sample reports like "WolfCrFCB.pdf" (linked in **ECBURL**) provide detailed test results.  
**BIOLOGY** — Rates overall aquatic health, where "High" means severe ecosystem impairment. The linked **BIOURL** report explains specific issues like fish population declines.  

## Try it yourself  
Search for streams near your property using the **BASIN** field (e.g., "MISSOURI RIVER BASIN") and check their **E_COLI** status before planning recreational use.
