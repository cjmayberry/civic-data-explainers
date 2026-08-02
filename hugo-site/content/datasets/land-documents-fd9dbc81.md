---
title: "Land Documents"
date: "2026-07-28"
description: "This dataset can be used to view land document information such as deeds, easements, and ordinances."
teaser: "This dataset tracks legal land documents like deeds, easements, and ordinances filed with the city"
tags: ["okc", "oklahoma city", "land", "documents", "property", "deeds", "ordinances"]
categories: ["Infrastructure"]
cover: "covers/land-documents-fd9dbc81--infrastructure--map_real_geometry.png"
map_data: "img/data/land-documents-fd9dbc81.geojson"
inquiry_enabled: true
inquiry_search: "Address"
inquiry_field: "IndexType"
inquiry_label: "Check documents recorded at an address"
inquiry_extra: ["Number", "Grantor"]
source_url: "https://utility.arcgis.com/usrsvcs/servers/fd9dbc810c9e4b3b8eb17887b796f0e5/rest/services/OpenData/Licensing_Subdivision/FeatureServer/8"
license: "custom"
dataset_id: "fd9dbc810c9e4b3b8eb17887b796f0e5"
city: "oklahoma-city"
site_url: "https://open-okc.hub.arcgis.com"
draft: false
dictionary:
  - field: "ObjectID"
    description: "Numeric unique identifier with no special meaning"
  - field: "Document Type"
    description: "Type of land document"
  - field: "Document Number"
    description: "Identifying number of document"
  - field: "Location"
    description: "Description of area the document applies to"
  - field: "Address"
    description: "Address, if any, associated with document"
  - field: "Grantor"
    description: "Grantor of legal document"
  - field: "Reference"
    description: "Ordinance or case number, if any, associated with document"
  - field: "Shape"
    description: "Geographic data in state plane coordinates (WKID 103512)"
---







## What this is  
This dataset tracks legal land documents like deeds, easements, and ordinances filed with the city.  

## Why it matters to you  
These records affect property rights, construction plans, and neighborhood changes. For example:  
- If you’re buying a home, checking for easements (like utility access) could reveal hidden limits on your property.  
- A new ordinance might block a business expansion you’re planning.  
- Deeds show who legally owns or transfers land—key for disputes or development.  

## How to read this data  
Key fields include:  
- **Document Type**: Tells you if it’s a deed (ownership transfer), easement (shared rights), or ordinance (local law).  
- **Location/Address**: Where the document applies—compare to your property or area of interest.  
- **Grantor**: Who signed over rights (e.g., a seller or government agency).  

## Try it yourself  
Search the dataset for your address or street to see:  
- Active easements (like sidewalks or pipelines crossing your land).  
- Recent ordinances that might affect renovations or zoning.  
- Past deeds to trace property ownership history.
