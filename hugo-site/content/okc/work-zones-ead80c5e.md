---
title: "Work Zones"
date: "2026-06-10"
description: "This dataset can be used to view information on active work zones within the City of Oklahoma City.  It includes information about related closures such as streets, lanes, and sidewalks."
teaser: "This dataset tracks active construction and repair work zones across Oklahoma City streets, including lane, road, and sidewalk closures"
tags: ["okc", "oklahoma city", "roads", "streets", "lanes", "right of way", "right-of-way", "closures"]
categories: ["Transportation"]
cover: "covers/work-zones-ead80c5e--transportation--placeholder.svg"
inquiry_enabled: true
inquiry_search: "Worklocation"
inquiry_field: "Worktype"
inquiry_label: "Check for active work near a street"
inquiry_extra: ["Startdate", "Enddate"]
source_url: "https://utility.arcgis.com/usrsvcs/servers/ead80c5e4e4e4c719359217f704a0c4c/rest/services/OpenData/Transportation/FeatureServer/5"
license: "custom"
dataset_id: "ead80c5e4e4e4c719359217f704a0c4c"
city: "okc"
site_url: "https://open-okc.hub.arcgis.com"
map_link: "https://open-okc.hub.arcgis.com/datasets/ead80c5e4e4e4c719359217f704a0c4c_5"
maintained_by: "This dataset is maintained by the Development Services Department of the City of Oklahoma City."
draft: false
dictionary:
  - field: "ObjectID"
    description: "Numeric unique identifier with no special meaning"
  - field: "Work Type"
    description: "Type of work being performed"
  - field: "Start Date"
    description: "Work start date based on issued permit"
  - field: "End Date"
    description: "Work end date based on issued permit"
  - field: "Location"
    description: "Location where work is being performed"
  - field: "Work Zone Number"
    description: "Alphanumeric number associated with work zone"
  - field: "North Bound"
    description: "indicates number of north bound lanes closed (if lane closure)"
  - field: "South Bound"
    description: "indicates number of south bound lanes closed (if lane closure)"
  - field: "East Bound"
    description: "indicates number of east bound lanes closed (if lane closure)"
  - field: "West Bound"
    description: "indicates number of west bound lanes closed (if lane closure)"
  - field: "Road Closure"
    description: "Indicates if the entire road will be closed"
  - field: "Lane Closure"
    description: "Indicates if lanes will be closed"
  - field: "Sidewalk Closure"
    description: "Indicates if sidewalks will be closed. Right-of-way"
  - field: "Work"
    description: "Indicates if work is being performed in the right-of-way"
  - field: "Shape"
    description: "Geographic data in state plane coordinates (WKID 103512)"
---









## What this is  
This dataset tracks active construction and repair work zones across Oklahoma City streets, including lane, road, and sidewalk closures.

## Why it matters to you  
Work zones directly impact your daily commutes, business deliveries, and street accessibility. Knowing where and when lanes are closed helps you:  
- Reroute to avoid delays when driving to work  
- Check if sidewalk closures affect foot traffic to your storefront  
- Plan alternate routes for trash pickup or moving trucks  

## How to read this data  
Key fields to check:  
- **Work Type**: What’s being done (e.g., “utility repair,” “resurfacing”)  
- **Start/End Date**: When disruptions are expected (compare these to your schedule)  
- **Road/Lane Closure**: “Yes” means full or partial roadblocks (check North/South/East/West Bound for lane-specific impacts)  
- **Sidewalk Closure**: Critical for pedestrians and businesses with foot traffic  

## Try it yourself  
Search the dataset for your street or neighborhood. If you see active work zones:  
- Note the end date to anticipate delays  
- Check if closures affect your usual routes to school, work, or deliveries  
- Report errors (like outdated end dates) to the city’s public works department
