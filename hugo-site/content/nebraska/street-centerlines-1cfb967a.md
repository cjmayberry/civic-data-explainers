---
title: "Street Centerlines"
date: "2026-08-02"
description: "These data represent 911-valid civic address ranges in the state of Nebraska. This layer is utilized in Next Generation 911 for both geospatial call routing and location validation functions. Creation and maintenance of "
teaser: "These data represent 911-valid civic address ranges in the state of Nebraska. This layer is utilized in Next Generation 911 for both geospatial call routing and location…"
tags: ["transportation", "location"]
categories: ["Transportation"]
cover: "covers/street-centerlines-1cfb967a--transportation--placeholder.svg"
source_url: "https://gis.ne.gov/Enterprise/rest/services/Street_Centerlines/FeatureServer"
license: ""
dataset_id: "https://www.arcgis.com/home/item.html?id=1cfb967a70dd4b0abee9d38249c06b0a&sublayer=0"
city: "nebraska"
site_url: "https://civic-data-explainers.pages.dev"
draft: false
---

## What this tracks  
This dataset records official street address ranges across Nebraska, used by 911 systems to validate and route emergency calls.

## Why it matters to you  
When you call 911 in Nebraska, this data ensures responders can find your exact location. If you're opening a business, it confirms your address exists in emergency systems. For rural residents, it verifies whether your property has a recognized address for mail delivery or emergency services. The data also shows which municipality (like Harrisburg) officially maintains your road.

## How to read this data  
**ST_NAME** — The base street name (e.g., "Road 67") without directional prefixes.  
**ADDR_LF** and **ADDR_LT** — The low and high house numbers on the left side of the street (e.g., 3600-3798).  
**PARITY_L** — Whether left-side addresses are even (E) or odd (O) numbers.  
**MSAG_COM_L** — The city or community name used in 911 systems (e.g., "Harrisburg"), which may differ from postal addresses.  

## Try it yourself  
Contact your county's Public Safety Answering Point to verify if your home address appears correctly in this 911 system, especially if you've recently moved or built a new structure.
