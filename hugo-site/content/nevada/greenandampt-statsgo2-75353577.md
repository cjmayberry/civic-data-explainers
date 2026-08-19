---
title: "GreenAndAmpt STATSGO2"
date: "2026-08-02"
description: "GeoHub"
teaser: "GeoHub"
tags: ["NDOT", "GeoHub"]
categories: ["Transportation"]
cover: "covers/greenandampt-statsgo2-75353577--transportation--placeholder.svg"
source_url: "https://gis.dot.nv.gov/agsphs/rest/services/GeoHub/GreenAndAmpt_STATSGO2/MapServer/0"
license: ""
dataset_id: "https://www.arcgis.com/home/item.html?id=753535770c5c47ef8ae11b34e96398b7&sublayer=0"
city: "nevada"
site_url: "https://civic-data-explainers.pages.dev"
map_link: "https://geohub-ndot.hub.arcgis.com/datasets/NDOT::greenandampt-statsgo2"
geojson_url: "https://gis.dot.nv.gov/agsphs/rest/services/GeoHub/GreenAndAmpt_STATSGO2/MapServer/0/query?where=1%3D1&f=geojson&outSR=4326&resultRecordCount=1500"
draft: false
---

## What this is

GreenAndAmpt STATSGO2 is a spatial dataset from the Nevada Department of Transportation (NDOT) GeoHub that associates Green-Ampt infiltration parameters with STATSGO2 (State Soil Geographic Database) soil polygons for Nevada. STATSGO2 is the generalized, statewide-scale companion to SSURGO — it provides soil information at a coarser resolution suitable for regional and statewide analyses where the detailed SSURGO survey units are not available or not needed.

## Why it matters to you

If you're doing statewide or regional hydrologic analysis, watershed-scale modeling, or broad transportation-planning work in Nevada, STATSGO2 gives you Green-Ampt infiltration parameters across the entire state at a resolution that's appropriate for large-area studies. It's the right layer when you need statewide coverage and can accept the generalized soil boundaries that come with STATSGO2 rather than the more detailed SSURGO units.

## How to read this data

Each polygon represents a STATSGO2 soil association or map unit with associated Green-Ampt parameters. The layer is most useful at regional and statewide scales — overlay it with your study area, read off the infiltration parameters for the soil units present, and use them as input to your hydrologic or drainage model. The parameters are appropriate for regional modeling where site-specific precision is less critical than statewide coverage.

## Where this leaves you

STATSGO2 is a generalized soil layer — its polygons represent broad soil associations rather than precise survey boundaries. For a specific site, SSURGO (the more detailed layer) would be more appropriate if available; STATSGO2 is the right choice when you need statewide coverage or are working at a scale where the generalization is acceptable.

## Look it up yourself

Open the map and zoom to your region of interest. The soil polygons show STATSGO2 map units with Green-Ampt parameters. For statewide or regional analyses, use the layer directly. For site-specific work, check whether the more detailed SSURGO layer (GreenAndAmpt SSURGO) is available for your area and prefer that where possible.
