---
title: "Specialty Pavement Markings"
date: "2026-08-02"
description: "ADA-related infrastructure. Includes layers for Pedestrian Signals, Crosswalks, Specialty Pavement Markings, Curb Ramps, and Sidewalks. ADA-related infrastructure. Includes layers for Pedestrian Signals, Crosswalks, Spec"
teaser: "ADA-related infrastructure. Includes layers for Pedestrian Signals, Crosswalks, Specialty Pavement Markings, Curb Ramps, and Sidewalks. ADA-related infrastructure.…"
tags: ["T", "D", "O", ",", "e", "n", "s", "p", "a", "r", "t", "m", "o", "f", "i", "A", "M", "g", "v", "I", "y", "C", "w", "l", "k", "u", "b", "P", "d", "S", "c"]
categories: ["Transportation"]
cover: "covers/specialty-pavement-markings-69511fa7--transportation--cover_only.svg"
source_url: "https://services2.arcgis.com/nf3p7v7Zy4fTOh6M/arcgis/rest/services/ADA_Asset_Data/FeatureServer"
license: ""
dataset_id: "https://www.arcgis.com/home/item.html?id=69511fa73a584e2bb37acfa85b177fa5&sublayer=4"
city: "tennessee"
site_url: "https://geodata.tn.gov"
draft: false
---

## What this tracks  
This dataset records the locations and details of specialty pavement markings (like truncated domes and ramps) on Tennessee's interstates, state routes, and TDOT-maintained roads.  

## Why it matters to you  
If you rely on accessible routes—whether as a wheelchair user, a business owner ensuring ADA compliance, or a driver navigating unfamiliar exits—this data shows where tactile warnings and ramps exist. For example, a Nashville delivery driver could check ramp widths (**RAMP_WIDTH_FT**) before planning a route for a large truck, or a Chattanooga resident could verify if a crosswalk near their home has truncated domes (**TRUNCATED_DOME_PRESENCE**) for safer walking.  

## How to read this data  
**FEATURE_DESCRIPTION** — The type of pavement feature, like "Driveway" or "Curb Ramp" (sample: "Driveway").  
**LOCATION_DESCRIPTION** — Where the feature is placed relative to the road, such as "Right" or "Left" (sample: "Right").  
**TRUNCATED_DOME_PRESENCE** — Whether tactile warning domes are present (sample: "2" likely indicates yes/no; check the metadata for codes).  
**RAMP_SLOPE_PCT** — The incline of a ramp, critical for accessibility (sample: "7.7" means a 7.7% slope).  

## Try it yourself  
Look up your frequent commute route in the dataset using **ROUTE_NUMBER** (e.g., "SR010") to see if key intersections have accessible ramps or warnings.
