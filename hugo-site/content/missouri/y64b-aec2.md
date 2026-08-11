---
title: "Oil and Gas Permits"
date: "2026-08-02"
description: ""
teaser: ""
tags: ["Natural Resources"]
categories: ["Environment"]
cover: "covers/y64b-aec2--environment--placeholder.svg"
source_url: "https://data.mo.gov/resource/y64b-aec2.json"
license: ""
dataset_id: "y64b-aec2"
city: "missouri"
site_url: "https://data.mo.gov"
draft: false
dictionary:
  - field: "rangedir"
    description: ""
  - field: "apiwebaddress"
    description: ""
  - field: ":@computed_region_ikxf_gfzr"
    description: ""
  - field: "location_1_city"
    description: ""
  - field: "county"
    description: ""
  - field: "range"
    description: ""
  - field: "wellno"
    description: ""
  - field: "countycode"
    description: ""
  - field: "location_1_address"
    description: ""
  - field: ":@computed_region_c8ar_jsdj"
    description: ""
  - field: "township"
    description: ""
  - field: ":@computed_region_ny2h_ckbz"
    description: ""
  - field: "location_1_state"
    description: ""
  - field: "location_1"
    description: ""
  - field: "status"
    description: ""
  - field: "ogcnumber"
    description: ""
  - field: "coname"
    description: ""
  - field: "leasename"
    description: ""
  - field: "id"
    description: ""
  - field: "section"
    description: ""
  - field: "location_1_zip"
    description: ""
---


## What this tracks  
This dataset records oil and gas drilling permits issued in Missouri, including well locations and operator details.

## Why it matters to you  
If you're buying rural property in Bates County, this data tells you whether active or abandoned wells exist on the land — critical for assessing potential environmental liabilities. For nearby residents, the status field reveals whether old wells were properly abandoned, which affects groundwater safety. Farmers can check if active drilling permits exist near their fields, which may impact land use agreements.

## How to read this data  
**status** — Current condition of the well, like "Abandoned" (permanently sealed) or potentially "Active".  
**coname** — The operating company, e.g., "GARRETT & MCLAUGHLIN", useful for contacting operators about legacy wells.  
**location_1** — GPS coordinates (e.g., 38.32796, -94.57552) to pinpoint wells on a map relative to your property.  
**leasename** — Landowner name ("LONG, C. L.") for verifying historical agreements.  

## Try it yourself  
Search the [Missouri DNR portal](http://www.dnr.mo.gov/geology/geosrv/ogc/permits/) using your township (41), range (33W), and section (28) to find permits near your land.
