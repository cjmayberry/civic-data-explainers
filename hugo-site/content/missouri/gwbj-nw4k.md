---
title: "Home Health - Out of State Providers"
date: "2026-08-02"
description: ""
teaser: ""
tags: ["Health"]
categories: ["Other"]
cover: "covers/gwbj-nw4k--other--placeholder.svg"
source_url: "https://data.mo.gov/resource/gwbj-nw4k.json"
license: ""
dataset_id: "gwbj-nw4k"
city: "missouri"
site_url: "https://data.mo.gov"
draft: false
dictionary:
  - field: "admin"
    description: ""
  - field: "phone"
    description: ""
  - field: "zip"
    description: ""
  - field: "state"
    description: ""
  - field: "facilities_county"
    description: ""
  - field: "city"
    description: ""
  - field: "address"
    description: ""
  - field: "facname"
    description: ""
  - field: "ownership4profit"
    description: ""
  - field: "ownershiphospbased"
    description: ""
  - field: "ownershipdistrict"
    description: ""
  - field: "ownershipnonpcorp"
    description: ""
  - field: "ownershipcity"
    description: ""
  - field: "ownershipcounty"
    description: ""
  - field: "factype"
    description: ""
  - field: "ownershipfacbased"
    description: ""
  - field: "ownershipinptfac"
    description: ""
  - field: "servicearea_county"
    description: ""
  - field: "partialcountydetails"
    description: ""
  - field: "fid"
    description: ""
  - field: "licnumber"
    description: ""
  - field: "licyrexpires"
    description: ""
---

## What this tracks  
This dataset lists home health providers physically located in Missouri but certified through another state's CMS program.

## Why it matters to you  
If you're comparing home health options for aging parents in Kansas City, this reveals providers that meet Missouri's location requirements but operate under different state regulations. The **ownership4profit** field tells you whether a provider is for-profit (✓) before you schedule consultations. Families in Jackson County can use the **servicearea_county** field to see which agencies serve their specific area despite the out-of-state certification.

## How to read this data  
**facname** — Provider name like "Aquinas/Carondelet Home Health"  
**address** — Physical location such as "1600 Genessee Street, Ste 325"  
**licyrexpires** — When the license renewals are due (e.g., "2027-05-31")  
**servicearea_county** — Where they're authorized to provide care (like "CASS" for Cass County)  

## Try it yourself  
Search the dataset for your county in the **servicearea_county** field to find providers near you that accept out-of-state certifications.
