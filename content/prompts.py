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

PROMPT_VERSION = "v2-pavement-shape"

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
