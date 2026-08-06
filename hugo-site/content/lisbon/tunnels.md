---
title: "Túneis rodoviários geridos pela EMEL | Road tunnels managed by EMEL"
date: "2026-08-06"
description: "Lisbon's road tunnels managed by EMEL: location, access conditions (speed/height limits) and restrictions."
teaser: "Lisbon's EMEL-managed road tunnels — location, speed and height limits, and traffic restrictions."
tags: ["Túneis rodoviários", "Traffic"]
categories: ["Transportation"]
cover: "covers/tunnels--transportation--placeholder.svg"
source_url: "https://dados.emel.pt/api/3/action/datastore_search?resource_id=4991244d-b5ef-4eba-9da0-eb05fe1d53ff"
license: "Creative Commons - Atribuição e Compartilha Igual (CC BY-SA)"
dataset_id: "1787ba1c-ef6c-43f6-8ab9-b3602defe3c3"
city: "lisbon"
site_url: "https://civic-data-explainers.pages.dev"
map_link: "https://dados.emel.pt/dataset/tunnels"
maintained_by: "EMEL"
draft: false
---


## What this tracks  
The road tunnels managed by EMEL in Lisbon — each tunnel's location, parish, access conditions (speed and height limits), and current restrictions.

## Why it matters to you  
If you drive a van, a truck, or anything tall, the **condicaoAcesso** field is the safety-critical part of this dataset. The Túnel do Marquês, for example, allows max 50 km/h, max 3.8 m height, and bans heavy vehicles, dangerous goods, bicycles and pedestrians. Knowing a tunnel's height limit before you route through it saves you a scrape — or a fine.

## How to read this data  
**tunelID** — tunnel identifier (e.g. 1, 2).  \n**localizacao** — where the tunnel is (e.g. "Túnel do Marquês (debaixo da Avenida Eng.º Duarte Pacheco)").  \n**condicaoAcesso** — speed limit, max height, and vehicle restrictions (e.g. "Vel. Máx. 50 Km/h; Alt. Máx. 3.8m; proibido pesados…").  \n**pertubacoes** — link to current traffic restrictions ([condicionamentos-transito.cm-lisboa.pt](https://condicionamentos-transito.cm-lisboa.pt/)).  \n**freguesia** — the parish ("Campo de Ourique", "Areeiro" in the sample).

## Try it yourself  
Open the [tunnels in EMEL's data portal](https://dados.emel.pt/dataset/tunnels) and check the **condicaoAcesso** of the tunnels on your commute — the height limit in particular if you ever rent a van. Bookmark the **pertubacoes** link for the official word on closures.
