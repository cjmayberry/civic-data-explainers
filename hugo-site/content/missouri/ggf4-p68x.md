---
title: "BackflowTesters"
date: "2026-08-02"
description: ""
teaser: ""
categories: ["Default"]
cover: "covers/ggf4-p68x--default--placeholder.svg"
source_url: "https://data.mo.gov/resource/ggf4-p68x.json"
license: ""
dataset_id: "ggf4-p68x"
city: "missouri"
site_url: "https://data.mo.gov"
draft: false
dictionary:
  - field: "expr1011"
    description: ""
  - field: "county"
    description: ""
  - field: "region"
    description: ""
  - field: "forhire"
    description: ""
  - field: "first_name"
    description: ""
  - field: "last_name"
    description: ""
  - field: "expr1012"
    description: ""
  - field: "expr1007"
    description: ""
  - field: "id_number"
    description: ""
  - field: "expiration"
    description: ""
  - field: "certified"
    description: ""
  - field: "expr1008"
    description: ""
  - field: "expr1009"
    description: ""
  - field: "expr1010"
    description: ""
---

## What this tracks  
This dataset lists certified backflow prevention device testers in Missouri who are available for hire to inspect and maintain backflow prevention systems.

## Why it matters to you  
If you own a business or property in Missouri with an irrigation system, commercial kitchen, or other plumbing that requires backflow prevention devices, this data helps you find licensed professionals to test your devices. Annual backflow testing is legally required for many properties — using an uncertified tester could result in fines or water service interruptions. The list tells you whether a tester near you is currently certified and when their certification expires.

## How to read this data  
**first_name** + **last_name** — The tester's full name (e.g., Jake Gaal).  
**forhire** — Whether the tester is currently available for work (sample value: True).  
**expr1012** — The tester's phone number (sample: 314-241-8023).  
**expr1008** — The tester's business address (sample: 1544 South 3rd Street, St. Louis, MO 63104).  

## Try it yourself  
Search the dataset for testers in your Missouri ZIP code by filtering on the **expr1010** (ZIP code) field to find local professionals.
