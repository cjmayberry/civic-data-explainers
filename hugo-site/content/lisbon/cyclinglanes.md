---
title: "Rede ciclável | Cycling Network"
date: "2026-08-06"
description: "The cycling network of Lisbon: each segment's location, width, length, lane type and surface condition."
teaser: "Every cycle lane segment in Lisbon — location, width, length, lane type, and surface condition."
tags: ["Rede ciclável", "Cycling"]
categories: ["Transportation"]
cover: "covers/cyclinglanes--transportation--placeholder.svg"
source_url: "https://dados.emel.pt/api/3/action/datastore_search?resource_id=f084da97-b3e8-49dc-83b3-93975bdaa2c1"
license: "Creative Commons - Atribuição e Compartilha Igual (CC BY-SA)"
dataset_id: "4f2d47a7-1ec4-41f9-8894-76695f728bc2"
city: "lisbon"
site_url: "https://civic-data-explainers.pages.dev"
map_link: "https://dados.emel.pt/dataset/cyclinglanes"
maintained_by: "EMEL"
draft: false
---


## What this tracks  
This dataset maps Lisbon's cycling network segment by segment — 119 segments in the live service — with each one's location, width, length, lane type, and pavement quality.

## Why it matters to you  
If you cycle in Lisbon, the width and pavement-quality fields tell you what to expect before you ride a route. **largura** (2.2–2.6 m in the sample) separates comfortable lanes from tight ones, and **pavQualidade** flags stretches where the surface may be rougher. The **freguesia** (parish) field lets you see how the network is distributed across neighborhoods — useful when choosing where to live or asking your parish council where the gaps are.

## How to read this data  
**localizacao** — where the segment runs (e.g. "Vela Latina (Avenida Brasilia)", "Avenida Infante Dom Henrique").  \n**largura** — lane width in meters (2.6 in the sample); **comprimento** — segment length in meters (112.2 in the sample).  \n**hierarquia** — the segment's role in the network ("Local" vs "Principal"), which hints at how connected a route is.  \n**pavQualidade** — surface condition ("Bom", "Muito Bom"…), worth checking before planning a fast commute.  \n**situacao** — "Operacional" means the segment is in service today.

## Try it yourself  
Open the [cycling network in EMEL's own data portal](https://dados.emel.pt/dataset/cyclinglanes) and look at your parish (**freguesia**). If a route you ride shows up as "Local" with a low **largura**, you have a concrete, citable data point for asking about an upgrade.
