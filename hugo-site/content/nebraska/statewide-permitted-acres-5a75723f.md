---
title: "Statewide Permitted Acres"
date: "2026-08-02"
description: "The Nebraska Department of Natural Resources (NeDNR) uses spatial representations of Certified Acres (CA), or areas of land which can legally be irrigated for groundwater use, surface water use, or a mix of the two (comi"
teaser: "The Nebraska Department of Natural Resources (NeDNR) uses spatial representations of Certified Acres (CA), or areas of land which can legally be irrigated for…"
tags: ["farming", "inlandWaters"]
categories: ["Environment"]
cover: "covers/statewide-permitted-acres-5a75723f--environment--placeholder.svg"
source_url: "https://dweegis.nebraska.gov/weegis/rest/services/Statewide_Permitted_Acres/FeatureServer"
geojson_url: "https://dweegis.nebraska.gov/weegis/rest/services/Statewide_Permitted_Acres/FeatureServer/0/query?where=1%3D1&f=geojson&outSR=4326&resultRecordCount=1500"
license: ""
dataset_id: "https://www.arcgis.com/home/item.html?id=5a75723fe7b346728e4102f995e69548&sublayer=0"
city: "nebraska"
site_url: "https://civic-data-explainers.pages.dev"
draft: false
---

## What this tracks  
This dataset records legally permitted irrigation areas in Nebraska, distinguishing between groundwater, surface water, and mixed-use permits.

## Why it matters to you  
If you're a farmer or landowner in Nebraska, this data tells you whether nearby properties are legally permitted to irrigate—and with what water sources. For example, if you're considering purchasing land in the North Platte NRD, checking **PermitType** reveals whether existing water rights are tied to surface water (like rivers) or groundwater (wells), which affects long-term water availability. It also helps small agricultural businesses anticipate local water-use regulations.

## How to read this data  
**PermitType** — Specifies the water source allowed for irrigation (sample: "Surface Water").  
**NRDs** — The Natural Resources District managing the permit (sample: "NPNRD" for North Platte).  
**ModeledAcres** — The estimated irrigable land area in acres (sample: 20.45).  
**CentroidLat/Long** — Approximate center point of the permitted area (sample: 41.8474, -103.9797).  

## Try it yourself  
Search your county’s NRD name in the dataset to see permitted irrigation acres near your property. For example, look for "NPNRD" to find North Platte NRD parcels.
