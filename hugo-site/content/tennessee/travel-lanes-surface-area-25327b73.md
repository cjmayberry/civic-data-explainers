---
title: "Travel Lanes Surface Area"
date: "2026-08-02"
description: "This layer is a cartographic representation of where travel lanes exist on all interstates, state routes, TDOT maintained state park roads, and locally owned NHS routes. This information was collected using vehicle mount"
teaser: "This layer is a cartographic representation of where travel lanes exist on all interstates, state routes, TDOT maintained state park roads, and locally owned NHS routes.…"
tags: ["Travel Lane Surface Area, Tennessee"]
categories: ["Transportation"]
cover: "covers/travel-lanes-surface-area-25327b73--transportation--placeholder.svg"
source_url: "https://services2.arcgis.com/nf3p7v7Zy4fTOh6M/arcgis/rest/services/Travel_Lanes_Surface_Area/FeatureServer"
license: ""
dataset_id: "https://www.arcgis.com/home/item.html?id=25327b73e77a4f42980d394a788422fb"
city: "tennessee"
site_url: "https://geodata.tn.gov"
draft: false
---


## What this tracks  
This dataset maps the exact locations and dimensions of travel lanes on Tennessee interstates, state routes, and select locally maintained roads.

## Why it matters to you  
If you're planning a trucking route through Shelby County, this data tells you whether specific ramps (like concrete on-ramps) can accommodate your vehicle's width. Small businesses shipping oversized loads can check **WIDTH** values to avoid routes with narrow lanes. Commuters can also identify ramp locations (**FEAT_DESC**) to anticipate merge points during construction season.

## How to read this data  
**FEAT_DESC** — Describes the lane type, like "Concrete On-Ramp" or "Main Travel Lane."  
**WIDTH** — Lane width in feet (sample: 11.25 ft). Critical for large vehicles.  
**ROUTE** — Highway identifier (sample: I0240 for I-240).  
**LOC_DESC** — Position relative to the road (sample: "Right" for right-side lanes).  

## Try it yourself  
Check the width of the nearest interstate on-ramp by searching [TDOT's map](https://www.tn.gov/tdot.html) for your exit number (**EXIT_** field, e.g., "0016").
