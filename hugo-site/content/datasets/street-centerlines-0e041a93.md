---
title: "Street Centerlines"
date: "2026-06-09"
description: "This dataset may be used to determine location and other attributes of the streets located within the City of Oklahoma City."
teaser: "The invisible skeleton under every address in OKC — updated daily, used by 911, delivery apps, and you."
tags: [" oklahoma city", "streets", "intersections", "centerlines"]
categories: ["Transportation"]
cover: "covers/street-centerlines-0e041a93--transportation--map_real_geometry.png"
source_url: "https://utility.arcgis.com/usrsvcs/servers/0e041a931ede4d38a9d23c5301708662/rest/services/OpenData/Transportation_Streets/FeatureServer/5"
license: "custom"
dataset_id: "0e041a931ede4d38a9d23c5301708662"
city: "Oklahoma City"
site_url: "https://open-okc.hub.arcgis.com"
draft: false
dictionary:
  - field: "ObjectID"
    description: "Numeric unique identifier with no special meaning"
  - field: "Street Class"
    description: "Oklahoma City classification of street"
  - field: "CFCC"
    description: "Street classification based on Census Feature Class Codes"
  - field: "Full Street Name"
    description: "Full street name associated with underlying street code"
  - field: "Street Prefix"
    description: "Prefix direction of street"
  - field: "Street Name"
    description: "Name of street without prefix or suffix"
  - field: "Street Suffix"
    description: "Suffix type of street"
  - field: "Left From Address"
    description: "Numeric starting address range for left side of street"
  - field: "Left To Address"
    description: "Numeric ending address range for left side of street"
  - field: "Right From Address"
    description: "Numeric starting address range for right side of street"
  - field: "Right To Address"
    description: "Numeric ending address range for left right of street"
  - field: "Oneway"
    description: "Indicates the flow of traffic on street segment"
  - field: "Lanes"
    description: "Number of lanes associated with street segment"
  - field: "Shape"
    description: "Geographic data in state plane coordinates (WKID 103512)"
  - field: "Length"
    description: "Approximate length of feature in US feet"
---






## What this is

Every street in Oklahoma City, drawn as a single center line with the street's full name, classification, and the address ranges on each side. It updates **daily**.

## Why it matters to you

When a delivery driver finds your house, when 911 locates a caller, when a map app routes around a closed road — they're all reading address ranges off a dataset like this one. It's also why some streets are "NW 23rd" and others are "Broadway": the dataset separates prefix, name, and suffix so every address in the city can be assembled consistently. If your address doesn't resolve in an app, the problem often traces back to a gap in centerline data.

## How to read this data

- **Full Street Name** — the assembled name, e.g. "N Walker Ave".
- **Street Class** — the city's classification of the road, from neighborhood streets up to major arterials. Higher classes carry more traffic and usually get plowed and repaved first.
- **Left From / Left To Address** — the address range on the left side of the street. Odd/even numbering conventions mean one side of the street carries one range and the other carries another; this is how mapping systems guess which side a house is on.

## Try it yourself

Look up your own street, then compare the **Left To Address** and **Right To Address** ranges. See how the numbering works? Now find a brand-new street — it'll be there, because this dataset refreshes every single day.
