---
title: "SalesTaxBoundaries"
date: "2026-08-02"
description: "Is a view of SalesTaxBoundaries_GIS updated through the execute procedure in SSMS and used to publish to the portal. Department of Revenue tracks tax rate and boundary changes on a quarterly basis. Cities are required to"
teaser: "Is a view of SalesTaxBoundaries_GIS updated through the execute procedure in SSMS and used to publish to the portal. Department of Revenue tracks tax rate and boundary…"
tags: ["boundaries"]
categories: ["Government"]
cover: "covers/salestaxboundaries-cd16ed82--government--placeholder.svg"
source_url: "https://gis.ne.gov/agency3/rest/services/SalesTaxWebLayerREV/FeatureServer/0"
license: ""
dataset_id: "https://www.arcgis.com/home/item.html?id=cd16ed82de544e8a93c2541ba889cbef&sublayer=0"
city: "nebraska"
site_url: "https://civic-data-explainers.pages.dev"
draft: false
---

## What this tracks  
This dataset records sales tax rates and boundaries across Nebraska, including state, county, and city-level rates.

## Why it matters to you  
If you run a business in Nebraska, this data tells you exactly what sales tax rate to charge customers based on your location. For example, a coffee shop owner in Omaha would use this to confirm whether their baked goods are taxed at the general rate (5.5%) or a lower food/drug rate. Residents can also check if moving just outside city limits would reduce their sales tax burden on major purchases.

## How to read this data  
**TotalRate** — The combined sales tax percentage you'll pay. Sample value: 5.5 means 5.5% tax.  
**FoodDrugTaxRateIntrastate** — Lower rate applied to qualifying grocery items. Sample value: 0.055 means 5.5%.  
**CityName** — Which municipality's rates apply. Sample value: "Nebraska" indicates state-wide rates.  

## Try it yourself  
Check the current sales tax rate for your Nebraska address by cross-referencing the CityName field with your municipality's boundaries in the dataset.
