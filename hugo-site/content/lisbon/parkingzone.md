---
title: "Áreas reguladas de estacionamento na via pública | Regulated on-street parking areas"
date: "2026-08-06"
description: "Lisbon's regulated on-street parking areas with their tariff, time limits and parking type."
teaser: "Every regulated on-street parking area in Lisbon — tariff color, time window, and parking type."
tags: ["Tarifas", "Áreas de estacionamento", "On-Street Parking"]
categories: ["Transportation"]
cover: "covers/parkingzone--transportation--placeholder.svg"
source_url: "https://dados.emel.pt/api/3/action/datastore_search?resource_id=c5bc37d0-16cc-44fb-b362-bca921d25314"
license: "Creative Commons - Atribuição e Compartilha Igual (CC BY-SA)"
dataset_id: "cf8487d1-c781-4838-9d09-d1a3f85710ef"
city: "lisbon"
site_url: "https://civic-data-explainers.pages.dev"
map_link: "https://dados.emel.pt/dataset/parkingzone"
maintained_by: "EMEL"
draft: false
---


## What this tracks  
Every regulated on-street parking area in Lisbon — 11 fields per area covering the tariff product, rate code, time window, and parking type, with the area drawn as a polygon.

## Why it matters to you  
This is the "what does it cost and for how long" half of Lisbon parking. **Tarifa** is the color band ("Amarela" = yellow), **Horario** is the paid window ("2ª A 6ª 9-19H" = Monday–Friday 9am–7pm in the sample), and **Tipo_Estacionamento** tells you the rule ("Rotativo" = rotating/limited, "Bolsa de Residentes" = residents' bays). Park in a yellow "Rotativo" area outside its window and you're fine — inside it, you're paying or ticketed.

## How to read this data  
**Produto** — the tariff product name (e.g. "AmarelaRotação", "Exclusivo para residentes").  \n**Tarifa** — the rate band color (e.g. "Amarela", "Verde").  \n**Horario** — when the charge applies (e.g. "2ª A 6ª 9-19H" or "24 HORAS").  \n**Tipo_Estacionamento** — the parking rule (e.g. "Rotativo", "Bolsa de Residentes").  \n**GeoJSONCoordinates** — the area's boundary for mapping.

## Try it yourself  
Open the [parking areas in EMEL's data portal](https://dados.emel.pt/dataset/parkingzone) and find your usual parking spot. Check **Horario** first — a "24 HORAS" area is always paid, while a weekday-hours zone may be free exactly when you need it.
