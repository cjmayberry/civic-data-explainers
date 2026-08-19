---
title: "GreenAndAmpt SSURGO"
date: "2026-08-02"
description: "Green and Ampt"
teaser: "Green and Ampt"
tags: ["NDOT", "GeoHub"]
categories: ["Transportation"]
cover: "covers/greenandampt-ssurgo-9056af09--transportation--placeholder.svg"
source_url: "https://gis.dot.nv.gov/agsphs/rest/services/GeoHub/GreenAndAmpt_SSURGO/MapServer/0"
license: ""
dataset_id: "https://www.arcgis.com/home/item.html?id=9056af0914294e84a627bc05e19f6218&sublayer=0"
city: "nevada"
site_url: "https://civic-data-explainers.pages.dev"
map_link: "https://geohub-ndot.hub.arcgis.com/datasets/NDOT::greenandampt-ssurgo"
geojson_url: "https://gis.dot.nv.gov/agsphs/rest/services/GeoHub/GreenAndAmpt_SSURGO/MapServer/0/query?where=1%3D1&f=geojson&outSR=4326&resultRecordCount=1500"
draft: false
---

## What this is

GreenAndAmpt SSURGO is a spatial dataset from the Nevada Department of Transportation (NDOT) GeoHub that associates Green-Ampt infiltration parameters with SSURGO (Soil Survey Geographic Database) soil polygons for Nevada. The Green-Ampt model is a physical infiltration equation used in hydrologic modeling, and this layer maps those parameters onto the Detailed Soil Survey units provided by the USDA Natural Resources Conservation Service.

## Why it matters to you

If you're working on stormwater management, pavement drainage design, flood modeling, or any project where water infiltration rates matter, this layer gives you physically-based infiltration parameters tied to mapped soil units. Rather than using generic assumptions, you can reference the Green-Ampt parameters for the specific soil type at your site — which matters for accurately estimating how quickly water will soak into the ground versus running off.

## How to read this data

Each polygon represents a SSURGO soil map unit with associated Green-Ampt infiltration parameters. The layer is most useful when you overlay it with your site or watershed of interest and read off the parameters for the soil units you're working with. The parameters feed directly into hydrologic models that predict runoff, infiltration, and drainage behavior.

## Where this leaves you

This is a soil-based layer — the parameters are tied to mapped soil polygons, not to street addresses. To use it for a specific site, identify the soil unit at your location on the map and reference the associated Green-Ampt parameters for that unit. For engineered projects, a site-specific soil investigation may still be warranted in addition to the SSURGO-level data.

## Look it up yourself

Open the map and zoom to your site or watershed. The soil polygons show SSURGO map units with Green-Ampt parameters. Identify the polygon covering your area and reference the associated infiltration values for your hydrologic modeling or drainage analysis. For project-specific engineering, consult a geotechnical or civil engineer and reference the NRCS SSURGO database for the most detailed soil documentation.
