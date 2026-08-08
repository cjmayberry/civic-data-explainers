---
title: "Street Names"
date: "2026-06-03"
description: "This dataset can be used to view the street names and their associated street code within the City of Oklahoma City."
teaser: "A list of all street names in Oklahoma City with their official codes and directional prefixes/suffixes"
tags: [" oklahoma city", "streets", "intersections", "centerlines"]
categories: ["Transportation"]
cover: "covers/street-names-adea21af--transportation--placeholder.svg"
inquiry_enabled: true
inquiry_search: "StreetName"
inquiry_field: "StreetName"
inquiry_label: "Look up a street's official name"
inquiry_extra: ["StreetPrefix", "StreetSuffix"]
source_url: "https://utility.arcgis.com/usrsvcs/servers/adea21af99c740ec86870111a9881fc4/rest/services/OpenData/Transportation_Streets/FeatureServer/10"
geojson_url: "https://utility.arcgis.com/usrsvcs/servers/adea21af99c740ec86870111a9881fc4/rest/services/OpenData/Transportation_Streets/FeatureServer/10/query?where=1%3D1&f=geojson&outSR=4326&resultRecordCount=1500"
license: "custom"
dataset_id: "adea21af99c740ec86870111a9881fc4"
city: "okc"
site_url: "https://open-okc.hub.arcgis.com"
map_link: "https://open-okc.hub.arcgis.com/datasets/adea21af99c740ec86870111a9881fc4_10"
maintained_by: "This dataset is maintained by the Planning Department of the City of Oklahoma City."
draft: false
dictionary:
  - field: "ObjectID"
    description: "Numeric unique identifier with no special meaning"
  - field: "Street Code"
    description: "Numeric number associated with street name"
  - field: "Street Prefix"
    description: "Prefix direction of street"
  - field: "Street Name"
    description: "Name of street"
  - field: "Street Suffix"
    description: "Suffix type of street"
---









## What this is  
A list of all street names in Oklahoma City with their official codes and directional prefixes/suffixes.

## Why it matters to you  
Street codes are the hidden identifiers the city uses to track maintenance, permits, and emergency responses. When you report a pothole, request a streetlight repair, or check if your block is scheduled for repaving, city systems reference these codes. Knowing your street's official name format (including prefixes like "N" or "SW") ensures your service requests get routed correctly.

## How to read this data  
- **Street Code**: A unique number assigned to each street (e.g., "12345" for Main St)  
- **Street Prefix/Suffix**: Directional markers (like "NE" or "W") and road types (like "Ave" or "Blvd")  
- **Street Name**: The base name without prefixes/suffixes (e.g., "Main" in "NE Main St")  

## Try it yourself  
Look up your street in the dataset to find its official code and full formatted name. Next time you file a 311 request, use this exact format to avoid delays (e.g., "NE 23rd St" not "23rd Street Northeast").
