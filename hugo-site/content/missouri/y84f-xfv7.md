---
title: "2015 State Budget Restrictions As of June 30, 2015"
date: "2026-08-02"
description: ""
teaser: ""
tags: ["Government Administration"]
categories: ["Government"]
cover: "covers/y84f-xfv7--government--placeholder.svg"
source_url: "https://data.mo.gov/resource/y84f-xfv7.json"
license: ""
dataset_id: "y84f-xfv7"
city: "missouri"
site_url: "https://data.mo.gov"
draft: false
dictionary:
  - field: "budget_fiscal_year"
    description: ""
  - field: "agency_name"
    description: ""
  - field: "released_amount"
    description: ""
  - field: "restricted_amount"
    description: ""
  - field: "fund_name"
    description: ""
---

Here is the YAML representation of the Missouri 2015 State Budget Restrictions dataset:

```yaml
name: 2015_state_budget_restrictions
title: 2015 State Budget Restrictions As of June 30, 2015
description: The data provided here details the State of Missouri's Budget Restrictions as of June 30, 2015.
category: Government
city: Missouri, MO
update_interval: Not stated
fields:
  - name: budget_fiscal_year
    title: Budget Fiscal Year
    type: integer
    description: The fiscal year for the budget data
    sample: 2015
  - name: agency_name
    title: Agency Name
    type: text
    description: The name of the government agency
    sample: AGRICULTURE
  - name: fund_name
    title: Fund Name
    type: text
    description: The name of the specific fund
    sample: AGRICULTURE BUSINESS DEVELOPMENT
  - name: restricted_amount
    title: Restricted Amount
    type: number
    description: The amount of restricted funds (in thousands of dollars)
    sample: 39
  - name: released_amount
    title: Released Amount
    type: number
    description: The amount of released funds (in thousands of dollars)
    sample: 39
```

Key notes:
1. The dataset contains financial restriction details for Missouri state agencies as of fiscal year 2015
2. All monetary amounts appear to be in thousands of dollars (based on the sample values)
3. The data is organized by agency and specific funds within agencies
4. The dataset tracks both restricted and released budget amounts
5. No update frequency is provided, suggesting this may be a one-time snapshot rather than regularly updated data
