---
title: "Zonas reguladas de estacionamento na via pública | Regulated on-street parking zones"
date: "2026-08-06"
description: "The geographic boundaries of Lisbon's regulated on-street parking zones (ZEDL and ZAAC)."
teaser: "The boundaries of Lisbon's regulated on-street parking zones (ZEDL / ZAAC) as polygons."
tags: ["Limites geográficos", "ZAAC", "ZEDL", "On-Street Parking"]
categories: ["Transportation"]
cover: "covers/parkingregulatedzonespaces--transportation--placeholder.svg"
source_url: "https://dados.emel.pt/api/3/action/datastore_search?resource_id=387eb395-34d5-4944-892b-4c56f07ec329"
geojson_url: "/lisbon/geojson/parkingregulatedzonespaces.geojson"
license: "Creative Commons - Atribuição e Compartilha Igual (CC BY-SA)"
dataset_id: "ebfade18-c14c-4e3f-b006-9d0c232ae209"
city: "lisbon"
site_url: "https://civic-data-explainers.pages.dev"
map_link: "https://dados.emel.pt/dataset/parkingregulatedzonespaces"
maintained_by: "EMEL"
draft: false
---


## What this tracks  
The geographic limits of Lisbon's regulated on-street parking zones — the ZEDL (Zonas de Estacionamento de Duração Limitada, limited-duration parking) and ZAAC (Zonas de Acesso Automóvel Condicionado, restricted vehicle access) areas — as map polygons.

## Why it matters to you  
If you drive in Lisbon, this dataset is the difference between a ticket and a legal park. **zona** is the zone code ("001", "003"…), **zonaNR** gives the zone a human-readable name ("Berna / Valbom", "Parque"…), and **coordenadas** holds the polygon that defines exactly where the rules apply. A zone number is only useful if you can see its boundary — this dataset is the boundary.

## How to read this data  
**zona** — the official zone identifier (e.g. "001").  \n**zonaNR** — the zone's name (e.g. "Berna / Valbom"), useful when talking to EMEL or contesting a ticket.  \n**coordenadas** — a GeoJSON Polygon of the zone's boundary, for maps and navigation apps.

## Try it yourself  
Open the [parking zones in EMEL's data portal](https://dados.emel.pt/dataset/parkingregulatedzonespaces), find your street's **zona**, and cross-check it against the [parking areas dataset](https://dados.emel.pt/dataset/parkingzone) to see which tariff and time limit applies there.
