---
title: "Adopted Streets"
date: "2026-06-09"
description: "This dataset can be used to view Oklahoma City streets that have been adopted through the adopt-a-city street program."
teaser: "This dataset tracks which Oklahoma City streets have been adopted by organizations through the adopt-a-city-street program"
tags: ["okc", "oklahoma city", "adopt", "adopeted", "streets"]
categories: ["Transportation"]
cover: "covers/adopted-streets-0ad77166--transportation--placeholder.svg"
inquiry_enabled: true
inquiry_search: "Adopted_Street"
inquiry_field: "Adopting_Organization"
inquiry_label: "Is your street adopted — and by whom?"
source_url: "https://utility.arcgis.com/usrsvcs/servers/0ad7716656324cf7844fd2e1ffe1f6be/rest/services/OpenData/Transportation/FeatureServer/2"
geojson_url: "https://utility.arcgis.com/usrsvcs/servers/0ad7716656324cf7844fd2e1ffe1f6be/rest/services/OpenData/Transportation/FeatureServer/2/query?where=1%3D1&f=geojson&outSR=4326&resultRecordCount=1500"
license: "custom"
dataset_id: "0ad7716656324cf7844fd2e1ffe1f6be"
city: "okc"
site_url: "https://open-okc.hub.arcgis.com"
map_link: "https://open-okc.hub.arcgis.com/datasets/0ad7716656324cf7844fd2e1ffe1f6be_2"
maintained_by: "This dataset is maintained by the Public Works Department of the City of Oklahoma City."
draft: false
dictionary:
  - field: "ObjectID"
    description: "Numeric unique identifier with no special meaning"
  - field: "Street"
    description: "Street name including from and to information"
  - field: "Adopted"
    description: "Organization who has adopted street"
  - field: "Shape"
    description: "Geographic data in state plane coordinates (WKID 103512)"
  - field: "Length"
    description: "Approximate length of feature in US feet"
---









## What this is  
This dataset tracks which Oklahoma City streets have been adopted by organizations through the adopt-a-city-street program.

## Why it matters to you  
Adopted streets often receive extra attention for litter cleanup and maintenance. If you're deciding where to open a business, volunteer for cleanup, or report a problem like potholes, knowing which streets have active adopters helps predict how quickly issues might get addressed. Neighborhood groups also use this to coordinate with existing adopters or claim unadopted stretches.

## How to read this data  
- **Street**: The name and block range (e.g., "Main St from 1st to 5th Ave")  
- **Adopted**: The group responsible for upkeep (e.g., a business or nonprofit)  
- **Length**: How long the adopted stretch is (in feet)  

## Try it yourself  
Search the dataset for your street or neighborhood—if it’s unadopted, you might qualify to "claim" it through the city’s program. If already adopted, note the responsible organization to contact about maintenance needs.
