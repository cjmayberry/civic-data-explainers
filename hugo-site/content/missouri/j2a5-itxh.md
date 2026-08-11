---
title: "DNR-WPP-Boil Order Report"
date: "2026-08-02"
description: ""
teaser: ""
tags: ["Regulatory"]
categories: ["Licensing"]
cover: "covers/j2a5-itxh--licensing--placeholder.svg"
source_url: "https://data.mo.gov/resource/j2a5-itxh.json"
license: ""
dataset_id: "j2a5-itxh"
city: "missouri"
site_url: "https://data.mo.gov"
draft: false
dictionary:
  - field: "county"
    description: ""
  - field: "geocoded_column"
    description: ""
  - field: "contaminant_of_concern"
    description: ""
  - field: "issue_date"
    description: ""
  - field: "geocoded_column_state"
    description: ""
  - field: "location"
    description: ""
  - field: "system_name"
    description: ""
  - field: "geocoded_column_zip"
    description: ""
  - field: ":@computed_region_ikxf_gfzr"
    description: "This column was automatically created in order to record in what polygon from the dataset 'Counties' (ikxf-gfzr) the point in column 'geocoded_column' is located. This enables the creation of region maps (choropleths) in the visualization canvas and data lens."
  - field: "geocoded_column_city"
    description: ""
  - field: ":@computed_region_ny2h_ckbz"
    description: "This column was automatically created in order to record in what polygon from the dataset 'School Districts' (ny2h-ckbz) the point in column 'geocoded_column' is located. This enables the creation of region maps (choropleths) in the visualization canvas and data lens."
  - field: "geocoded_column_address"
    description: ""
  - field: ":@computed_region_c8ar_jsdj"
    description: "This column was automatically created in order to record in what polygon from the dataset 'Missouri Counties' (c8ar-jsdj) the point in column 'geocoded_column' is located. This enables the creation of region maps (choropleths) in the visualization canvas and data lens."
  - field: "pws_id"
    description: ""
---


## What this tracks  
This dataset records active boil water orders issued to public water systems across Missouri.

## Why it matters to you  
If your water comes from a small public system (like a campground or grocery store), this data tells you whether you need to boil water before drinking it. For example, a Pittsburg resident using Alps Grocery's water system would see their July 2026 notice about chlorine failure here. Businesses serving food or drinks must check this to avoid health violations when their water source has contamination warnings.

## How to read this data  
**system_name** — The affected water provider (e.g., "Alps Grocery Pittsburg").  
**location** — Where the system operates (e.g., "25817 St Hwy 64, Pittsburg").  
**contaminant_of_concern** — Why boiling is needed (e.g., "Disinfectant pump failure/ No chlorine in system").  
**issue_date** — When the order took effect (e.g., "2026-07-13").  

## Try it yourself  
Search [your ZIP code or county](https://data.mo.gov/) to see current boil orders near you.
