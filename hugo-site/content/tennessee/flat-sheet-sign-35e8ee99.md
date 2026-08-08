---
title: "Flat Sheet Sign"
date: "2026-08-02"
description: "This layer is a cartographic representation of where flat sheet signs have been installed on all interstates, state routes, TDOT maintained state park roads, and locally owned NHS routes. This information was collected u"
teaser: "This layer is a cartographic representation of where flat sheet signs have been installed on all interstates, state routes, TDOT maintained state park roads, and locally…"
tags: ["Flatsheet Signs", "Tennessee"]
categories: ["Transportation"]
cover: "covers/flat-sheet-sign-35e8ee99--transportation--cover_only.svg"
source_url: "https://services2.arcgis.com/nf3p7v7Zy4fTOh6M/arcgis/rest/services/Flat_Sheet_Sign/FeatureServer"
license: ""
dataset_id: "https://www.arcgis.com/home/item.html?id=35e8ee994d234e09a9583bbaf553a5cf"
city: "tennessee"
site_url: "https://geodata.tn.gov"
draft: false
---

## What this tracks  
This dataset records the locations and details of flat sheet road signs installed along Tennessee interstates, state routes, and TDOT-maintained roads.

## Why it matters to you  
Knowing where these signs are located helps you anticipate roadside information before road trips—like scenic route markers or historical trail indicators. For small businesses near highways, this reveals what directional signage exists to guide customers to your location. The condition data alerts TDOT when signs need maintenance, which affects nighttime visibility for drivers.

## How to read this data  
**FEAT_DESC** — Describes the sign's purpose, like "Tennessee Scenic Parkway (Lower Case Text / Bird)" or "Trail of Tears" historical markers.  
**LOC_DESC** — Placement relative to the road, with values like "Right" indicating which side of the roadway the sign is on.  
**LOG_MILE** — The mile marker where the sign is located (e.g., 0.28 means just over a quarter-mile from the route's start).  
**CONDITION** — Rates sign durability on a scale (3 in the sample suggests adequate condition).  

## Try it yourself  
Check if your county (like Lawrence County in the sample) has scenic route signs by filtering the dataset for your **COUNTY_NAME**, then look for **FEAT_DESC** values mentioning parks or trails.
