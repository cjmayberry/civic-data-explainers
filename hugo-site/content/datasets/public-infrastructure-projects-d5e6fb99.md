---
title: "Public Infrastructure Projects"
date: "2026-07-30"
description: "This dataset can be used to view public infrastructure projects related to streets, bridges, traffic, drainage, parks, and facility improvements within the City of Oklahoma City."
teaser: "How OKC plans and pays for the streets, bridges and parks around you — and why “planned” and “actual” are two different dates."
tags: ["okc", "oklahoma city", "projects", "bonds", "parks", "bridges", "drainage", "intersections", "streets", "buildings", "facility", "police", "fire", "bond", "penny"]
categories: ["Infrastructure"]
cover: "covers/public-infrastructure-projects-d5e6fb99--infrastructure--placeholder.svg"
source_url: "https://services5.arcgis.com/2mOVdIcRtNH2JsSF/arcgis/rest/services/Infrastructure_Projects_OD/FeatureServer"
license: "custom"
dataset_id: "d5e6fb99125c44a6b5165336607fe199"
city: "oklahoma-city"
site_url: "https://open-okc.hub.arcgis.com"
draft: false
featured: true
dictionary:
  - field: "ObjectID"
    description: "Numeric unique identifier with no special meaning"
  - field: "Project Name"
    description: "Short name of Project"
  - field: "Description"
    description: "Additional project details"
  - field: "Project Type"
    description: "General type of project"
  - field: "Planned Start Date"
    description: "Estimated project start date"
  - field: "Planned End Date"
    description: "Estimated project end date"
  - field: "Estimated Budget"
    description: "Estimated project cost in USD"
  - field: "Department Responsible"
    description: "Department, if any, responsible for project management"
  - field: "Project Phase"
    description: "Current phase of project"
  - field: "Actual Start Date"
    description: "Date project actually started"
  - field: "Actual End Date"
    description: "Date project actually ended"
  - field: "Expenditures"
    description: "Actual amount spent of on project in USD"
  - field: "Notes"
    description: "Additional comments about project"
  - field: "Funding sources"
    description: "Source(s) of funds for project"
  - field: "Ward"
    description: "Council ward impacted by project"
  - field: "Project Category"
    description: "Category of project"
  - field: "Project Section"
    description: "Subcategory of project"
  - field: "Project Location"
    description: "Text description of area where work is being performed"
  - field: "Shape"
    description: "Geographic data in Web Mercator coordinates"
map_link: "https://open-okc.hub.arcgis.com/datasets/d5e6fb99125c44a6b5165336607fe199_0"
maintained_by: "This dataset is maintained by the Public Works Department of the City of Oklahoma City."
---









## What this is

This is the city's public to-do list for major construction: every street, bridge, drainage, park and traffic project Oklahoma City has planned or underway, with a budget and a schedule attached.

## Why it matters to you

That orange cone on your commute started as a row in this dataset. If you want to know why a street is torn up, when a project near you is supposed to finish, or whether the city is actually spending what it promised on a neighborhood bond project, this is the ledger to check. For small businesses, a "Planned End Date" can mean the difference between a normal summer and a summer of detoured customers — worth knowing before you lease, hire, or stock inventory.

## How to read this data

- **Project Phase** — where a project sits in its life: planning, design, under construction, or complete. Filter for "under construction" to see what's actively affecting streets today.
- **Planned Start Date / Planned End Date** — the city's estimate. Treat these as a forecast, not a promise.
- **Actual Start Date** — when work really began. The gap between planned and actual is the single most honest number in city infrastructure: compare them and you'll see how realistic the estimates were.
- **Estimated Budget** — the sticker price in USD. Note the word "estimated" — the dataset is honest about it.

## Try it yourself

Open the data service, filter **Project Phase = "under construction"** in your part of town, and check the gap between Planned and Actual Start Date. Pick the project with the biggest gap and ask yourself: what would make a city's schedule slip by that much?
