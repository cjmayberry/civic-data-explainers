---
title: "Garage Sales"
date: "2026-06-03"
description: "This dataset can be used to determine current and upcoming garage sales within the City of Oklahoma City."
teaser: "A list of current and upcoming garage sales in Oklahoma City, including what types of items are being sold"
tags: [" oklahoma city", "garage", "yard", "sales", "permits"]
categories: ["Licensing"]
cover: "covers/garage-sales-a2b13b6d--licensing--map_real_geometry.png"
map_data: "img/data/garage-sales-a2b13b6d.geojson"
source_url: "https://utility.arcgis.com/usrsvcs/servers/a2b13b6db7804ea98482ca085e2783db/rest/services/OpenData/Licensing_Permits/FeatureServer/0"
license: "custom"
dataset_id: "a2b13b6db7804ea98482ca085e2783db"
city: "Oklahoma City"
site_url: "https://open-okc.hub.arcgis.com"
draft: false
dictionary:
  - field: "ObjectID"
    description: "Numeric unique identifier with no special meaning"
  - field: "Address"
    description: "Address if garage sale"
  - field: "Permit Date"
    description: "Starting date of issued permit"
  - field: "Appliances"
    description: "Yes/No indicator if this item type is being sold"
  - field: "Baby Kid Items"
    description: "Yes/No indicator if this item type is being sold"
  - field: "Clothing"
    description: "Yes/No indicator if this item type is being sold"
  - field: "Electronics"
    description: "Yes/No indicator if this item type is being sold"
  - field: "Entertainment"
    description: "Yes/No indicator if this item type is being sold"
  - field: "Fitness Equipment"
    description: "Yes/No indicator if this item type is being sold"
  - field: "Furniture"
    description: "Yes/No indicator if this item type is being sold"
  - field: "Hobbies"
    description: "Yes/No indicator if this item type is being sold"
  - field: "Kitchen Items"
    description: "Yes/No indicator if this item type is being sold"
  - field: "Lawn Tools"
    description: "Yes/No indicator if this item type is being sold"
  - field: "Household Items"
    description: "Yes/No indicator if this item type is being sold"
  - field: "Sporting Goods"
    description: "Yes/No indicator if this item type is being sold"
  - field: "All Categories"
    description: "list of all item categories being sold"
  - field: "Shape"
    description: "Geographic data in state plane coordinates (WKID 103512)"
---

## What this is  
A list of current and upcoming garage sales in Oklahoma City, including what types of items are being sold.

## Why it matters to you  
If you're looking for secondhand deals or want to declutter your home by hosting your own sale, this data helps you:  
- Find nearby garage sales selling items you need (like baby gear or furniture)  
- Scout competition before planning your own sale  
- Avoid permit conflicts if hosting multiple sales on the same block  

## How to read this data  
Key fields to check:  
- **Address**: Where the sale is happening  
- **Permit Date**: When the sale starts  
- **All Categories**: A quick list of what's being sold (e.g., "Electronics, Furniture")  
- **Specific item fields** (like "Baby Kid Items"): "Yes" means those items are available  

## Try it yourself  
Search the dataset for sales near your address this weekend. Look for sales listing "Furniture" or "Electronics" if you’re bargain-hunting, or check if your street already has a sale planned before applying for your own permit.
