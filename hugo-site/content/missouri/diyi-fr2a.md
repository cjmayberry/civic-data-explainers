---
title: "DHSS WIC Data"
date: "2026-08-02"
description: "WIC Household ID"
teaser: "WIC Household ID"
categories: ["Default"]
cover: "covers/diyi-fr2a--default--placeholder.svg"
source_url: "https://data.mo.gov/resource/diyi-fr2a.json"
license: ""
dataset_id: "diyi-fr2a"
city: "missouri"
site_url: "https://data.mo.gov"
draft: false
dictionary:
  - field: "co_agency_fk"
    description: "Local Agency ID"
  - field: "countyname"
    description: "County the municipality is located in per United States Census Bureau data"
  - field: "population_2022"
    description: "Year of United States Census Bureau data used to determine a municipality’s population"
  - field: "municipality_name"
    description: "Municipality the household is located in per United States Census Bureau data"
  - field: "net_benefit"
    description: "Total benefit amount redeemed by the household during the state fiscal year"
  - field: "applicant_zip"
    description: "Zip code where the household is located"
  - field: "applicant_state"
    description: "State where the household is located"
  - field: "applicant_city"
    description: "City where the household is located"
  - field: "county"
    description: "County where the household is located"
  - field: "ts_orig_reg_pk_householdid"
    description: "WIC Household ID"
---

## What this tracks  
This dataset records the total value of WIC benefits redeemed by enrolled households in Missouri during state fiscal year 2025, broken down by county and municipality.  

## Why it matters to you  
If you're a parent or caregiver in Missouri, this data shows which areas have higher WIC participation, helping you gauge local demand for nutrition assistance. Small business owners—like grocery stores or pharmacies—can use it to identify underserved areas where expanding WIC-approved product offerings might benefit the community and attract customers. For example, a Lamar grocer might notice their town’s high redemption totals and decide to stock more WIC-eligible formula.  

## How to read this data  
**county** — The Missouri county where the household is located (e.g., "BARTON").  
**applicant_city** — The city of residence for the WIC recipient (e.g., "LAMAR").  
**net_benefit** — The total annual WIC benefits redeemed by the household in dollars (e.g., "1390.24").  
**population_2022** — The municipality’s population, if over 1,000 (e.g., "4298").  

## Try it yourself  
Search the dataset for your ZIP code to see the average WIC benefit amounts in your area—this could help you estimate local need if you run a business serving families.
