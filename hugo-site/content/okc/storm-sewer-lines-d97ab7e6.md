---
title: "Storm Sewer Lines"
date: "2026-06-09"
description: "This dataset can be used to determine storm sewer lines, such as channels, flumes, gabion baskets, inlets, rip rap, and pipes, within the City of Oklahoma City."
teaser: "The hidden plumbing under OKC streets — how stormwater gets from your curb to the river."
tags: [" oklahoma city", "storm", "sewer", "lines", "conrete", "earthen", "grass", "channels", "flumes", "gabion", "baskets", "grated inlets", "rip rap", "slop wall"]
categories: ["Infrastructure"]
cover: "covers/storm-sewer-lines-d97ab7e6--infrastructure--placeholder.svg"
source_url: "https://utility.arcgis.com/usrsvcs/servers/d97ab7e67970441c95e41e2211cbcd24/rest/services/OpenData/Infrastructure_Hydrology/FeatureServer/2"
license: "custom"
dataset_id: "d97ab7e67970441c95e41e2211cbcd24"
city: "okc"
site_url: "https://open-okc.hub.arcgis.com"
map_link: "https://open-okc.hub.arcgis.com/datasets/d97ab7e67970441c95e41e2211cbcd24_2"
maintained_by: "This dataset is maintained by the Public Works Department of the City of Oklahoma City."
draft: false
dictionary:
  - field: "ObjectID"
    description: "Numeric unique identifier with no special meaning"
  - field: "Sub Type"
    description: "Type of sewer line"
  - field: "Project Number"
    description: "Public Works project number associated with storm sewer line"
  - field: "Material"
    description: "Material used for storm sewer line"
  - field: "Line Name"
    description: "Name of storm sewer line (if any)"
  - field: "Nominal Size"
    description: "Size of storm sewer line (if applicable)"
  - field: "Location"
    description: "Text description of location"
  - field: "Upstream Invert"
    description: "The elevation of the structure at inflow"
  - field: "Downstream Invert"
    description: "The elevation of the structure at outflow"
  - field: "Slope"
    description: "Slope of the storm sewer line as a percentage"
  - field: "Comments"
    description: "Comments related to junction"
  - field: "Shape"
    description: "Geographic data in state plane coordinates (WKID 103512)"
  - field: "Length"
    description: "Approximate length of feature in US feet"
---











## What this is

The storm sewer network — the pipes, channels, flumes, and inlets that carry rainwater from streets and neighborhoods out of the city. Every line with its material, size, slope, and elevation.

## Why it matters to you

Storm sewers are why your street doesn't become a river in a downpour. When they fail, you get flooding — and the flood doesn't care about property lines. This dataset is how engineers find where the weak points are: an undersized pipe, a too-gentle slope, a line in the wrong material. For homeowners in flood-prone areas, knowing where the storm infrastructure is (and reading its size and slope) explains a lot about why water behaves the way it does on your street.

## How to read this data

- **Material** — what the pipe is made of. Old materials corrode faster; this field is a first clue to a line's age and health.
- **Nominal Size** — the pipe's diameter. This is the capacity number: bigger pipes move more water.
- **Slope** — the gradient as a percentage. Water flows because of slope — too little and the pipe silts up, too much and it scours.
- **Upstream / Downstream Invert** — the elevation of the pipe at each end. Compare them and you get the drop that drives the flow.

## Try it yourself

Find the storm line nearest your home and note its size and slope. Next heavy rain, watch where the water actually goes — then see if your observations match what the data says the system should do. That's field-checking, and it's how the pros do it.
