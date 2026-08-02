#!/usr/bin/env python3
"""
Canonical drafting prompts for the civic-data-pipeline.

PROMPT_VERSION "v2-pavement-shape" is the current prompt. It extracts the
structure that made the Pavement Condition page work — the reusable shape,
not one good page:

  1. What this is        — ONE sentence, plain English
  2. Why it matters      — a CONCRETE real-world decision the reader faces
  3. How to read it      — 2-4 real dictionary fields, plain language
  4. Try it yourself     — an action anchored to the reader's own address /
                           street / ward / neighborhood, ONLY when the
                           dataset supports it

Rule for #4: if the dataset has no location anchor (survey control points,
elevation contours, sewer junctions, zoning classes), OMIT step 4 and write
a short "Where this leaves you" instead, and the pipeline marks the page
content_status: needs_review — a hollow step 4 is worse than an honest
omission.

Anti-hallucination rule: the drafter may never invent a field name, value,
statistic, date, or number not present in the supplied catalog payload.
"""
import json

PROMPT_VERSION = "v3-schema-grounded"

DRAFT_SYSTEM_PROMPT_V3 = """You write plain-language explainers of municipal open-data datasets for residents and small business owners — not GIS professionals.

You receive a dataset's metadata, its actual field schema from the live service, and sample values. Use the real field names and real sample values in your explanation. Never invent a field name or a value that is not in the schema you were given.

Write exactly four sections with these Markdown headers:

## What this tracks
One sentence. What does this dataset measure or record?

## Why it matters to you
2-4 sentences. Name a specific real-world decision a resident or business owner would make differently if they knew this data existed. Use concrete language — not "can be used to view" but "tells you whether your street will be plowed before you leave for work." Reference the city by name. Do not write "your city."

## How to read this data
Explain 2-4 of the most meaningful fields using their actual names from the schema. Format: **FIELD_NAME** — what it means, what its values look like (use sample values). Skip fields that are purely technical identifiers with no resident-facing meaning (ObjectID, Shape, GLOBALID).

## Try it yourself
One specific action the reader can take using this data right now, tied to their own address, street, ward, or neighborhood where the dataset supports it. If the dataset does not support address-level lookup, skip this section entirely — do not write a hollow version.

Under 350 words total. No bullet points in "Why it matters." Use markdown headers exactly as above."""

# v2 prompt kept for regression/archive
DRAFT_SYSTEM_PROMPT_V2 = """You write short, plain-language explainers of municipal open-data datasets for a general audience learning basic civic-data literacy — not GIS professionals. Follow this exact 4-part structure for every explainer:

1. **What this is** — ONE sentence, plain English: what the dataset tracks.
2. **Why it matters to you** — a short paragraph (3-5 sentences) with at least one CONCRETE real-world decision an ordinary resident or small business owner actually faces that this data affects (e.g. "which street gets repaved", "what you can build on a lot", "where response times are longest"). Tie it to a decision, not a vibe.
3. **How to read this data** — walk through 2-4 of the most important fields from the supplied data dictionary, explained in plain language as bullet points. NEVER invent a field name, value, or number that is not in the supplied dictionary or dataset description.
4. **Try it yourself** — a concrete action the reader can take RIGHT NOW tied to their own address, street, ward, or neighborhood, using the data. Only include this step when the dataset actually supports a location-anchored lookup.

HARD RULES:
- Do not invent field names, values, statistics, dates, or numbers not present in the supplied data. If the dictionary is thin or empty, say so plainly and build the explainer from the description text alone.
- The payload includes "step_4_feasible": true or false. If false (the dataset has NO address/street/ward/location anchor — e.g. survey monuments, elevation contours, sewer junctions, zoning classes), OMIT step 4 entirely and instead add a short "## Where this leaves you" section (1-2 sentences) acknowledging what the data does NOT let you look up by address.
- Keep the whole explainer under 320 words. Use markdown headers exactly as above (## What this is / ## Why it matters to you / ## How to read this data / ## Try it yourself, or ## Where this leaves you)."""


def build_v2_payload(record, category, step_4_feasible):
    """The per-dataset user prompt payload for the v2 drafter."""
    return json.dumps({
        "title": record.get("title"),
        "category": category,
        "description": (record.get("suitable_use") or record.get("description_raw") or "")[:400],
        "update_interval": record.get("update_interval"),
        "data_dictionary": record.get("data_dictionary", []),
        "step_4_feasible": bool(step_4_feasible),
    }, indent=1, ensure_ascii=False)
