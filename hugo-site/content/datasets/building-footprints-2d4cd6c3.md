---
title: "Building Footprints"
date: "2026-06-09"
description: "This dataset can be used to view building footprints derived from aerial planimetric data collected in 2020."
teaser: "Every building in OKC, drawn from the sky in 2020 — and the honest limits of aerial data."
tags: [" oklahoma city", "buildings", "footprints", "addresses", "planimetrics", "2020"]
categories: ["Infrastructure"]
cover: "covers/building-footprints-2d4cd6c3--infrastructure--placeholder.svg"
source_url: "https://utility.arcgis.com/usrsvcs/servers/2d4cd6c3279f48f394329f3367069c61/rest/services/OpenData/Infrastructure_Planimetrics/FeatureServer/2"
license: "custom"
dataset_id: "2d4cd6c3279f48f394329f3367069c61"
city: "oklahoma-city"
site_url: "https://open-okc.hub.arcgis.com"
draft: false
dictionary:
  - field: "ObjectID"
    description: "Numeric unique identifier with no special meaning"
  - field: "Elevation"
    description: "Elevation above sea level in US feet"
  - field: "Shape"
    description: "Geographic data in state plane coordinates (WKID 103512)"
  - field: "Area"
    description: "Approximate area of feature in US square feet"
  - field: "Length"
    description: "Approximate length of perimeter of feature in US feet"
map_link: "https://open-okc.hub.arcgis.com/datasets/2d4cd6c3279f48f394329f3367069c61_2"
maintained_by: "This dataset is maintained by the Information Technology Department of the City of Oklahoma City."
---









## What this is

The footprint of every building in Oklahoma City — captured from aerial imagery collected in **2020** — with its elevation above sea level.

## Why it matters to you

This is the dataset that makes flood-risk maps, solar-potential calculators, and "how much of my lot is covered by structure?" questions answerable. It's also a time capsule: the data was collected in 2020, so every building built since then is invisible to it. Understanding *when* data was collected is a civic superpower — most arguments about "the data is wrong" turn out to be "the data is old."

## How to read this data

- **Elevation** — height above sea level in feet. Combine with flood zone maps to understand your property's drainage reality.
- **Area** — the building's footprint in square feet. This is the "building coverage" number that matters for lot-coverage rules.
- **Shape** — the actual outline. The data comes from aerial imagery, so outlines may not perfectly match what's on the ground.

## Try it yourself

Find your own home's footprint and check its Area. Now count how many new buildings near you went up after 2020 — anything newer simply won't be in this dataset. That's your reminder to always check a dataset's collection date before trusting it.
