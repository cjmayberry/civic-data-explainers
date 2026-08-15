---
title: "PredictiveNitrateModelNDEE"
date: "2026-08-02"
description: "The model predictions represent the probability that nitrate concentrations will exceed certain threshold values in private domestic wells based on a limited set of model inputs. In this layer, threshold values of 3 mg/L"
teaser: "The model predictions represent the probability that nitrate concentrations will exceed certain threshold values in private domestic wells based on a limited set of…"
tags: ["health", "environment"]
categories: ["Health"]
cover: "covers/predictivenitratemodelndee-de8bc4eb--health--placeholder.svg"
source_url: "https://gis.ne.gov/agencyext/rest/services/PredictiveNitrateModelNDEE/FeatureServer"
license: ""
dataset_id: "https://www.arcgis.com/home/item.html?id=de8bc4eb82de4f8ebeb430498a6a3aa5&sublayer=0"
city: "nebraska"
site_url: "https://civic-data-explainers.pages.dev"
draft: false
---

## What this tracks  
This dataset predicts the probability that nitrate levels in private wells across Nebraska exceed safe drinking water thresholds (3 mg/L, 5 mg/L, and 10 mg/L).

## Why it matters to you  
If you rely on a private well in Nebraska, this data helps you decide whether to test your water for nitrates—a common contaminant linked to health risks. A high prediction probability (like 0.71 for the 3 mg/L threshold) suggests your well water may need treatment. Farmers can also use this to assess runoff risks before expanding fertilizer use near vulnerable areas.

## How to read this data  
**GBM_BKD_Prediction** — Probability (0–1) that nitrate exceeds 3 mg/L (background level). Sample: 0.71 means a 71% chance.  
**GBM_ELE_Prediction** — Probability for 5 mg/L (elevated level). Sample: 0.33 means a 33% chance.  
**GBM_MCL_Prediction_Binary** — Binary flag (0 or 1) for 10 mg/L (federal safety limit). Sample: 1 means likely unsafe.  

## Try it yourself  
Check your Nebraska address in the [NDEE’s groundwater quality map](https://deq-iis.ne.gov/zs/) to see predicted nitrate risks for nearby wells.
