---
title: "Food Pantry List"
date: "2026-08-02"
description: ""
teaser: ""
tags: ["Social Services"]
categories: ["Other"]
cover: "covers/eb3y-vtsa--other--placeholder.svg"
source_url: "https://data.mo.gov/resource/eb3y-vtsa.json"
license: ""
dataset_id: "eb3y-vtsa"
city: "missouri"
site_url: "https://data.mo.gov"
draft: false
dictionary:
  - field: ":@computed_region_ny2h_ckbz"
    description: ""
  - field: "location_zip"
    description: ""
  - field: "location_state"
    description: ""
  - field: "location_city"
    description: ""
  - field: "additional_address_info"
    description: ""
  - field: "location_address"
    description: ""
  - field: "hours_of_operation"
    description: ""
  - field: "phone_number"
    description: ""
  - field: "county"
    description: ""
  - field: "agency_name"
    description: ""
  - field: "location"
    description: ""
  - field: ":@computed_region_c8ar_jsdj"
    description: ""
  - field: ":@computed_region_ikxf_gfzr"
    description: ""
---

## What this tracks  
This dataset lists food pantries in Missouri, including their locations, hours, and contact information.

## Why it matters to you  
If you're facing food insecurity in Missouri, this data helps you find the nearest pantry without calling multiple places. A small business owner might check pantry hours before donating perishable goods to ensure they're open for drop-off. Families can plan visits around the limited operating hours (like "2nd Fri 3:30-5:30") to avoid wasted trips.

## How to read this data  
**agency_name** — The pantry's name (e.g., "Zalma General Baptist Food Pantry").  
**hours_of_operation** — When to visit (e.g., "2nd Fri 3:30-5:30" means only open one afternoon per month).  
**location** — Full address with GPS coordinates (e.g., 9369 Maple Street, Zalma, MO 63787).  
**phone_number** — Direct contact (e.g., 573-225-3615) to confirm inventory or requirements.  

## Try it yourself  
Search the dataset for pantries near your ZIP code using the `human_address` field, then call the **phone_number** to ask about eligibility or current stock.
