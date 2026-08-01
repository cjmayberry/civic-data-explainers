#!/usr/bin/env python3
"""
Content drafter for the civic-data-pipeline.

Takes catalog JSON from extract_catalog.py, filters to datasets worth
teaching from, and drafts a plain-language explainer per dataset by
calling out to a model -- via Hermes's own model_registry routing proxy,
NOT a hardcoded provider. This script does not know or care which model
answers; that's Hermes's job. Point HERMES_ENDPOINT at your FastAPI
routing proxy.

The filter encodes four criteria (cadence, clean dictionary, cross-city
pattern, no heavy-GIS lift) worked out by hand against OKC's specific
catalog. The threshold values below (e.g. "at least 3 dictionary fields")
are reasonable starting points, not tuned constants -- adjust once you
see how they perform against a second city's catalog, since a threshold
picked from one example is a guess with one data point behind it.

Usage:
    python3 draft_content.py catalog.json --hermes-endpoint http://localhost:8000/v1/chat/completions > drafts.json
    python3 draft_content.py catalog.json --dry-run   # filter only, no model calls, inspect what would be drafted
"""
import sys
import json
import argparse
import urllib.request

# Datasets whose *pattern* (not exact schema) recurs across most US
# municipal ArcGIS Hub sites -- used for the cross-city-generalizes filter.
# This is a heuristic keyword list built from what's common in municipal
# GIS practice generally, not verified against a second city's actual
# catalog -- expect to refine this list once you run the pipeline
# elsewhere and see what does/doesn't transfer.
LIKELY_CROSS_CITY_KEYWORDS = [
    "zoning", "street centerline", "parcel", "plat", "council", "ward",
    "district", "infrastructure project", "pavement", "tif", "tax increment",
    "land use", "address point", "subdivision",
]

# Datasets that are live-utility facts rather than teaching material --
# excluded even if they otherwise pass the cadence/dictionary filters.
# ("no lesson to teach, just a fact to look up" -- see prior discussion)
UTILITY_KEYWORDS = [
    "trash", "garbage", "recycl", "emergency response", "911", "garage sale",
    "hotel motel tax", "work zone", "road closure", "bulky waste",
]

# Datasets needing real GIS tooling to be legible -- excluded regardless
# of other scores.
HEAVY_GIS_KEYWORDS = [
    "survey monument", "control point", "vegetation", "elevation",
    "contour", "impervious surface", "sewer junction", "headwall",
    "storm sewer node",
]

DRAFT_SYSTEM_PROMPT = """You write short, plain-language explainers of \
municipal open-data datasets for a general audience learning basic web \
publishing and civic-data literacy -- not GIS professionals. Given a \
dataset's title, category, and data dictionary, write:

1. A one-sentence plain-English summary of what the dataset tracks.
2. A short paragraph (3-5 sentences) explaining why this matters to an \
ordinary resident or small business owner, with at least one concrete \
example scenario.
3. A "How to read this data" section that walks through 2-4 of the most \
important fields from the data dictionary, explained in plain language.

Do not invent field names or values not present in the supplied data \
dictionary. If the data dictionary is empty or thin, say so plainly \
rather than filling in plausible-sounding fields. Keep the total \
response under 300 words. Output as markdown with the three sections \
as headers."""


def passes_utility_filter(record: dict) -> bool:
    """True if this is a live-fact lookup, not teaching material -- excluded."""
    text = (record["title"] + " " + " ".join(record.get("topics", []))).lower()
    return not any(kw in text for kw in UTILITY_KEYWORDS)


def passes_heavy_gis_filter(record: dict) -> bool:
    """True if this doesn't require real GIS tooling to be legible."""
    text = (record["title"] + " " + " ".join(record.get("topics", []))).lower()
    return not any(kw in text for kw in HEAVY_GIS_KEYWORDS)


def has_clean_dictionary(record: dict, min_fields: int = 3) -> bool:
    """True if there's enough structured field data to teach from."""
    return len(record.get("data_dictionary", [])) >= min_fields


def has_real_cadence(record: dict) -> bool:
    """
    True if update_interval suggests an actual recurring cadence rather
    than 'as needed' / empty / unknown. Matches on interval words rather
    than a fixed list of exact strings, since cadence phrasing varies.
    """
    interval = (record.get("update_interval") or "").lower()
    if not interval or "as needed" in interval:
        return False
    return any(w in interval for w in [
        "minute", "hour", "daily", "day", "week", "month", "quarter",
    ])


def likely_cross_city(record: dict) -> bool:
    """True if the title/topics suggest a pattern common to other cities."""
    text = record["title"].lower()
    return any(kw in text for kw in LIKELY_CROSS_CITY_KEYWORDS)


def filter_teaching_worthy(records: list) -> list:
    """
    Applies the four-part filter. A record needs: not a pure utility
    lookup, not heavy-GIS, AND (clean dictionary OR real cadence) AND
    likely cross-city relevance. The OR on dictionary/cadence is
    deliberate -- Public Infrastructure Projects has a rich dictionary
    but 'as needed' cadence, and Street Centerlines has both -- requiring
    AND on every criterion would have wrongly dropped the infrastructure
    projects dataset in the original manual pass.
    """
    out = []
    for r in records:
        if r["type"] != "Dataset":
            continue
        if not passes_utility_filter(r):
            continue
        if not passes_heavy_gis_filter(r):
            continue
        if not (has_clean_dictionary(r) or has_real_cadence(r)):
            continue
        if not likely_cross_city(r):
            continue
        out.append(r)
    return out


def call_hermes(endpoint: str, record: dict, model: str = None) -> str:
    """
    Calls the Hermes model_registry routing proxy with a draft request.
    Assumes an OpenAI-compatible /v1/chat/completions shape, since that's
    the common convention for a FastAPI routing proxy in front of mixed
    providers -- adjust the payload shape if your actual proxy contract
    differs, this wasn't tested against your specific registry.
    """
    user_content = json.dumps({
        "title": record["title"],
        "topics": record.get("topics", []),
        "update_interval": record.get("update_interval"),
        "data_dictionary": record.get("data_dictionary", []),
    }, indent=2)

    payload = {
        "messages": [
            {"role": "system", "content": DRAFT_SYSTEM_PROMPT},
            {"role": "user", "content": f"Dataset:\n{user_content}"},
        ],
    }
    if model:
        payload["model"] = model

    req = urllib.request.Request(
        endpoint,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        result = json.loads(resp.read())

    # OpenAI-compatible response shape assumed here.
    return result["choices"][0]["message"]["content"]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("catalog_json", help="Path to JSON output from extract_catalog.py")
    parser.add_argument("--hermes-endpoint", help="URL of Hermes's chat-completions endpoint")
    parser.add_argument("--model", help="Optional model override to pass through to Hermes's router")
    parser.add_argument("--dry-run", action="store_true", help="Only run the filter, print what would be drafted, make no model calls")
    args = parser.parse_args()

    with open(args.catalog_json) as f:
        records = json.load(f)

    worthy = filter_teaching_worthy(records)

    if args.dry_run:
        print(f"# {len(worthy)} of {len(records)} items pass the teaching-worthy filter:", file=sys.stderr)
        for r in worthy:
            print(f"  - {r['title']} (interval: {r.get('update_interval')}, "
                  f"{len(r.get('data_dictionary', []))} dict fields)", file=sys.stderr)
        print(json.dumps(worthy, indent=2, ensure_ascii=False))
        return

    if not args.hermes_endpoint:
        print("Error: --hermes-endpoint is required unless --dry-run is set", file=sys.stderr)
        sys.exit(1)

    drafts = []
    for r in worthy:
        try:
            draft_text = call_hermes(args.hermes_endpoint, r, model=args.model)
            drafts.append({"source": r, "draft_markdown": draft_text})
            print(f"# drafted: {r['title']}", file=sys.stderr)
        except Exception as e:
            print(f"# FAILED on {r['title']}: {e}", file=sys.stderr)
            drafts.append({"source": r, "draft_markdown": None, "error": str(e)})

    print(json.dumps(drafts, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
