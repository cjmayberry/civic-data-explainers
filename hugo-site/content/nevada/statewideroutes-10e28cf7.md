---
title: "StatewideRoutes"
date: "2026-08-02"
description: "Read Only LRS service for GeoHUB."
teaser: "Read Only LRS service for GeoHUB."
tags: ["LRS", "Location Referencing", "Statewideroutes", "Milepost Calibrated Routes", "Geohub LRS", "Geohub_LRS"]
categories: ["Transportation"]
cover: "covers/statewideroutes-10e28cf7--transportation--placeholder.svg"
source_url: "https://services1.arcgis.com/9Y4hSlLf13E9S0Eo/arcgis/rest/services/Geohub_LRS/FeatureServer/0"
license: ""
dataset_id: "https://www.arcgis.com/home/item.html?id=10e28cf7674647319249204bdade6f27&sublayer=0"
city: "nevada"
site_url: "https://civic-data-explainers.pages.dev"
draft: false
---

## What this tracks  
This dataset records Nevada's statewide road network, including route identifiers and jurisdictional details.

## Why it matters to you  
Knowing which agency maintains a specific road helps you report potholes or flooding correctly — Lyon County (code LY) handles "B ST," while NDOT manages state routes. Trucking companies can verify weight limits by checking **SystemType** before planning routes through Nevada. Residents can identify which roads get winter maintenance first by their jurisdiction code.

## How to read this data  
**RouteID** — A unique identifier like "100002LY" combining route number (100002) and county code (LY).  
**RouteNameFull** — The complete road name, such as "B ST" for local streets or "US-50" for highways.  
**JurisdictionCode** — Three-digit codes like "040" showing which government entity manages the road (state, county, or city).  
**CountyCode** — Two-letter abbreviations like "LY" for Lyon County, indicating where the road is located.  

## Try it yourself  
Look up your daily commute route by searching for its name in **RouteNameFull** to see which agency maintains it — this determines who to call about road hazards.
