---
title: "Bike Routes"
date: "2026-06-09"
description: "This dataset can be used to view current bike routes, including route type, within the City of Oklahoma City."
teaser: "OKC’s bike network, route by route — trail names, types, and what’s still in progress."
tags: ["okc", "oklahoma city", "bikes", "biking", "trails", "projects", "recreation"]
categories: ["Transportation"]
cover: "covers/bike-routes-5600dd31--transportation--map_real_geometry.png"
source_url: "https://utility.arcgis.com/usrsvcs/servers/5600dd31c2d545afb11eaa7f40d6eaa4/rest/services/OpenData/Transportation/FeatureServer/0"
license: "custom"
dataset_id: "5600dd31c2d545afb11eaa7f40d6eaa4"
city: "Oklahoma City"
site_url: "https://open-okc.hub.arcgis.com"
draft: false
dictionary:
  - field: "ObjectID"
    description: "Numeric unique identifier with no special meaning"
  - field: "Trail Name"
    description: "Name of trail if any"
  - field: "Trail Type"
    description: "Type of trail"
  - field: "Status"
    description: "Current status of trail"
  - field: "Shape"
    description: "Geographic data in state plane coordinates (WKID 103512)"
  - field: "Length"
    description: "Approximate length of feature in US feet"
---







## What this is

The city's current bike routes — including trail names, types, and status — mapped across Oklahoma City.

## Why it matters to you

If you're choosing where to live, work, or start a business, the bike network is a hidden amenity: routes connect parks, neighborhoods, and downtown, and Trail Type tells you whether you're on a shared street, a dedicated lane, or an off-road trail. For commuters, the Status field separates what's rideable today from what's still being built — the difference between a pleasant 15-minute ride and a surprise dead-end.

## How to read this data

- **Trail Name** — the route's name, if it has one. Named trails are usually the marquee routes with real investment behind them.
- **Trail Type** — what kind of facility it is. This determines who it's comfortable for: a family on cruisers vs. a commuter on a road bike.
- **Status** — current state (planned, under construction, or open). The catalog notes there can be a delay between completion and appearing here.

## Try it yourself

Plot a ride from your home to a destination you visit weekly using only routes marked open. Then look at what's planned near you — that's the network's future, and public comments on those projects actually shape them.
