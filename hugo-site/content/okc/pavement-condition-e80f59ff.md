---
title: "Pavement Condition"
date: "2026-06-09"
description: "This dataset can be used to view information by the condition of Oklahoma City maintained streets based on pavement condition index (PCI)."
teaser: "The bumpiness report card: every OKC street scored on the Pavement Condition Index."
tags: ["okc", "oklahoma city", "streets", "pavement", "condition", "index", "roads", "surface", "pci"]
categories: ["Transportation"]
cover: "covers/pavement-condition-e80f59ff--transportation--placeholder.svg"
inquiry_enabled: true
inquiry_search: "XSTREET_NA"
inquiry_field: "PCICurrent"
inquiry_label: "Find your street's pavement score"
inquiry_extra: ["BEGDESC", "ENDDESC"]
source_url: "https://utility.arcgis.com/usrsvcs/servers/e80f59ff3b374307a28e634ac0a92c41/rest/services/OpenData/Transportation/FeatureServer/3"
license: "custom"
dataset_id: "e80f59ff3b374307a28e634ac0a92c41"
city: "okc"
site_url: "https://open-okc.hub.arcgis.com"
map_link: "https://open-okc.hub.arcgis.com/datasets/e80f59ff3b374307a28e634ac0a92c41_3"
geojson_url: "https://utility.arcgis.com/usrsvcs/servers/e80f59ff3b374307a28e634ac0a92c41/rest/services/OpenData/Transportation/FeatureServer/3/query?where=1%3D1&f=geojson&outSR=4326&resultRecordCount=1500"
maintained_by: "This dataset is maintained by the Public Works Department of the City of Oklahoma City."
draft: false
dictionary:
  - field: "ObjectID"
    description: "Numeric unique identifier with no special meaning"
  - field: "PCI"
    description: "Pavement condition index for street segment"
  - field: "Street Type"
    description: "Classification of street"
  - field: "Surface Type"
    description: "Type of surface of street"
  - field: "Street"
    description: "Name of street"
  - field: "From"
    description: "Starting position, typically a cross street, for street segment"
  - field: "To"
    description: "Ending position, typically a cross street, for street segment"
  - field: "Shape"
    description: "Geographic data in state plane coordinates (WKID 103512)"
  - field: "Length"
    description: "Approximate length of feature in US feet"
---












## What this is

A condition score for every street segment Oklahoma City maintains, based on the Pavement Condition Index (PCI) — the industry-standard rating of road health.

## Why it matters to you

PCI is the number behind the politics of potholes. Streets are scored on a scale (roughly 0–100), and cities use those scores to decide which streets get repaved and which get patched — because fixing a road when its score is 70 costs a fraction of rebuilding it when it's 20. If your street is rough, its PCI score is your evidence; if your street is newly smooth, the score will show the bump. This dataset is also the classic answer to "why did they pave THAT street and not mine?" — because it's a score, not a vibe.

## How to read this data

- **PCI** — the pavement condition index. Higher is better; a low PCI on your segment is the concrete number to quote in a service request.
- **Street Type** — the road's classification. Arterials get repaved on different cycles than neighborhood streets.
- **From / To** — the segment's boundaries, usually cross streets. A whole street isn't one entry — it's many segments, each with its own score.

## Try it yourself

Find your street and check the PCI of the segment right in front of your house. Then check the street one block over. The difference is your neighborhood's pavement story — and it's the exact data the city uses to pick winners and losers in the repaving queue.
