---
title: "Council Wards"
date: "2026-06-09"
description: "This dataset can be used to determine the council ward and council member for a given geographic region and is suitable for comparison to address information or other location-based datasets."
teaser: "The map that decides who speaks for you at city hall — and why ward boundaries quietly change."
tags: [" oklahoma city", "boundary", "boundaries", "city", "jurisdiction"]
categories: ["Government"]
cover: "covers/council-wards-666b9654--government--placeholder.svg"
source_url: "https://utility.arcgis.com/usrsvcs/servers/666b9654ab104ba7ac49870c66190e9c/rest/services/OpenData/Government_Boundaries/FeatureServer/2"
geojson_url: "https://utility.arcgis.com/usrsvcs/servers/666b9654ab104ba7ac49870c66190e9c/rest/services/OpenData/Government_Boundaries/FeatureServer/2/query?where=1%3D1&f=geojson&outSR=4326&resultRecordCount=1500"
license: "custom"
dataset_id: "666b9654ab104ba7ac49870c66190e9c"
city: "okc"
site_url: "https://open-okc.hub.arcgis.com"
map_link: "https://open-okc.hub.arcgis.com/datasets/666b9654ab104ba7ac49870c66190e9c_2"
maintained_by: "This dataset is maintained by the Information Technology Department of the City of Oklahoma City."
draft: false
dictionary:
  - field: "ObjectID"
    description: "Numeric unique identifier with no special meaning"
  - field: "Ward"
    description: "Numeric number of council ward"
  - field: "Council Member"
    description: "Name of current council member for ward"
  - field: "Shape"
    description: "Geographic data ward in state plane coordinates (WKID 103512)"
  - field: "Area"
    description: "Approximate area of feature in US square feet"
  - field: "Length"
    description: "Approximate length of perimeter of feature in US feet"
---











## What this is

Oklahoma City is divided into wards, and each ward elects one council member. This dataset is the official map of those boundaries and who currently represents each one.

## Why it matters to you

Every city service you care about — potholes, parks, zoning, police response — is filtered through your council member's office. When a street light is out for weeks, the person who can actually make it move is the ward representative. This dataset tells you which one is yours, and it's also the answer key for questions like "why is this development in my neighborhood?" — because land-use decisions live on a ward map too.

## How to read this data

- **Ward** — the number of the district (Oklahoma City has 8).
- **Council Member** — the current representative's name. This field changes with every election, so the dataset is only as current as its last update.
- **Area** — the size of the ward in square feet. Wards are drawn to be roughly equal in *population*, not in size — which is why some look huge and empty and others small and dense.

## Try it yourself

Find your address on the ward map and note the Ward number. Then look up when your council member's term ends and whether your ward is up for election this year — most people discover they vote for city council more often than they thought.
