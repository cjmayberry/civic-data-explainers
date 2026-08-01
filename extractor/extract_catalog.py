#!/usr/bin/env python3
"""
Generic catalog extractor — ArcGIS Hub (RSS + DCAT data.json) and CKAN portals.

Three source formats, one normalized output schema:

  rss   — ArcGIS Hub RSS 2.0 feed at <site>/api/feed/rss/2.0 (default, the
          original mechanism, verified on open-okc, gis-okdot, gisdata-occokc).
  dcat  — ArcGIS Hub DCAT feed at <site>/data.json (project-open-data v1.1
          catalog.jsonld). Richer: publisher, formats, license, spatial,
          keywords. Use when RSS is disabled or you need distribution formats.
  ckan  — CKAN portal /api/3/action/package_search (e.g. data.ok.gov, which
          migrated off Socrata to CKAN 2.9 / OpenGov in 2026 — all legacy
          Socrata endpoints are dead).

Format auto-detection from the URL (explicit --format overrides):
  "data.json" in url            -> dcat
  "/api/3/action" in url        -> ckan
  otherwise                     -> rss

Usage:
    python3 extract_catalog.py https://open-okc.hub.arcgis.com > catalog.json
    python3 extract_catalog.py https://gis-okdot.opendata.arcgis.com --format dcat --pretty
    python3 extract_catalog.py https://data.ok.gov/api/3/action/package_search --pretty

Output: JSON array of records, one per catalog item. Every record carries the
common schema below so downstream stages (build_manifest.py, redraft.py,
fetch_images.py) don't care which source produced it:

  title, link, guid, type, featured, topics,
  pub_date_iso, maintained_by,
  suitable_use, limitations_on_use, update_interval,
  data_dictionary (list of {field, description}),
  description_raw, structure_detected,
  source ("rss" | "dcat" | "ckan"),
  formats (list of distribution formats),
  service_url (ArcGIS REST / datastore URL when the source exposes one),
  scope ("county" for LiDAR/NAIP/imagery-type records that must never be
         pulled at full-state scale — TBs; everything else "state")
"""
import sys
import json
import re
import argparse
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

RSS_FEED_PATH = "/api/feed/rss/2.0"
DCAT_FEED_PATH = "/data.json"
CKAN_SEARCH_PATH = "/api/3/action/package_search"
CKAN_PAGE_SIZE = 100  # CKAN's max rows per request

# Matches the section-heading convention OKC uses inside <description>.
# Sections run in this order when present; any subset may appear.
SECTION_HEADERS = [
    "Suitable Use",
    "Limitations on Use",
    "Data Dictionary",
    "Update Interval",
    "Maintained By",
    "Contact",
]

# LiDAR / NAIP / imagery-style records are only sane at county scale.
# If a record's title/description matches, flag scope=county so no pipeline
# stage attempts a full-state pull (verified: full-state 3DEP/NAIP = TBs).
COUNTY_SCOPE_RE = re.compile(
    r"\b(lidar|naip|orthoimagery|orthophoto|aerial imagery|3dep|elevation "
    r"model|dem|dsm|dtm|imagery mosaic)\b",
    re.I,
)


USER_AGENT = "civic-data-pipeline/1.0"


def http_get(url: str, timeout: int = 60) -> bytes:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": USER_AGENT},
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def strip_html(text: str) -> str:
    if not text:
        return ""
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def iso_or_none(raw: str) -> str | None:
    """Best-effort parse of a datetime string to ISO-8601 UTC."""
    if not raw:
        return None
    try:
        dt = datetime.fromisoformat(raw.replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc).isoformat()
    except ValueError:
        return None


def detect_format(site_url: str) -> str:
    if "data.json" in site_url:
        return "dcat"
    if "/api/3/action" in site_url:
        return "ckan"
    return "rss"


# --------------------------------------------------------------------------
# RSS (ArcGIS Hub /api/feed/rss/2.0)
# --------------------------------------------------------------------------

def fetch_rss(site_url: str, timeout: int = 30) -> bytes:
    """Fetch the RSS feed for a given ArcGIS Hub site root URL."""
    site_url = site_url.rstrip("/")
    feed_url = f"{site_url}{RSS_FEED_PATH}"
    try:
        return http_get(feed_url, timeout)
    except Exception as e:
        raise ValueError(
            f"RSS fetch failed for {feed_url} ({e}). If this is a CKAN portal "
            f"(e.g. data.ok.gov), pass --format ckan and/or the "
            f"/api/3/action/package_search URL."
        ) from e


def split_description_sections(description: str) -> dict:
    """
    Best-effort split of an OKC-style description blob into named sections.
    Returns {} if the structure isn't detected -- caller should fall back
    to treating the whole description as unstructured prose in that case.

    OKC's actual format: headers appear verbatim WITHOUT colons, concatenated.
    Example: "Suitable Use This dataset... Limitations on Use This dataset..."
    We match headers as word boundaries, then slice between consecutive headers.
    """
    if not description:
        return {}

    alternation = "|".join(re.escape(h) for h in SECTION_HEADERS)
    # Match headers as word boundaries (no colons in live feed)
    header_re = re.compile(rf"\b({alternation})\b")
    matches = list(header_re.finditer(description))
    if not matches:
        return {}

    sections = {}
    for i, m in enumerate(matches):
        header = m.group(1)
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(description)
        body = description[start:end].strip()
        sections[header] = body

    return sections


def parse_data_dictionary(dd_text: str) -> list:
    """
    OKC's Data Dictionary section is a run of 'Field Name - Description.'
    pairs with no other delimiter. This is a heuristic parse -- it looks
    for '<Capitalized Field Name> - ' as the split point. Imperfect on
    edge cases (field names containing ' - ' themselves) but good enough
    for a rough draft; treat output as a starting point to hand-check,
    not ground truth.
    """
    if not dd_text:
        return []
    # Split on ". <Word starting field> - " pattern -- field names are
    # Title Case runs before the first standalone hyphen.
    field_pattern = re.compile(r"([A-Z][A-Za-z0-9_/ ]{1,40}?)\s+-\s+")
    matches = list(field_pattern.finditer(dd_text))
    fields = []
    for i, m in enumerate(matches):
        name = m.group(1).strip()
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(dd_text)
        desc = dd_text[start:end].strip().rstrip(".")
        if name and desc:
            fields.append({"field": name, "description": desc})
    return fields


def parse_rss_item(item: ET.Element) -> dict:
    title = (item.findtext("title") or "").strip()
    link = (item.findtext("link") or "").strip()
    guid = (item.findtext("guid") or "").strip()
    pub_date_raw = (item.findtext("pubDate") or "").strip()
    description = (item.findtext("description") or "").strip()
    categories = [c.text.strip() for c in item.findall("category") if c.text]

    item_type = "Application" if "Application" in categories else (
        "Dataset" if "Dataset" in categories else "Unknown"
    )
    featured = "Featured" in categories
    # Everything else in categories minus the type/featured markers is a
    # topical category (Infrastructure, Public Safety, etc.)
    topics = [
        c for c in categories
        if c not in ("Dataset", "Application", "Featured",
                      "Open Data Type", "Open Data Category")
    ]

    sections = split_description_sections(description)
    data_dictionary = parse_data_dictionary(sections.get("Data Dictionary", ""))

    return {
        "title": title,
        "link": link,
        "guid": guid,
        "type": item_type,
        "featured": featured,
        "topics": topics,
        "pub_date_iso": iso_or_none(pub_date_raw),
        "update_interval": sections.get("Update Interval", "").strip() or None,
        "maintained_by": sections.get("Maintained By", "").strip() or None,
        "suitable_use": sections.get("Suitable Use", "").strip() or None,
        "limitations_on_use": sections.get("Limitations on Use", "").strip() or None,
        "data_dictionary": data_dictionary,
        "description_raw": description,
        "structure_detected": bool(sections),
    }


def extract_rss(site_url: str) -> list:
    raw = fetch_rss(site_url)
    root = ET.fromstring(raw)
    channel = root.find("channel")
    if channel is None:
        raise ValueError("No <channel> found -- is this a valid RSS 2.0 feed?")
    items = channel.findall("item")
    return [parse_rss_item(item) for item in items]


# --------------------------------------------------------------------------
# DCAT (ArcGIS Hub /data.json — project-open-data v1.1 catalog.jsonld)
# --------------------------------------------------------------------------

def fetch_dcat(site_url: str, timeout: int = 60) -> bytes:
    site_url = site_url.rstrip("/")
    if site_url.endswith(".json"):
        feed_url = site_url  # caller already passed the data.json URL
    else:
        feed_url = f"{site_url}{DCAT_FEED_PATH}"
    return http_get(feed_url, timeout)


def parse_dcat_item(rec: dict) -> dict:
    title = strip_html(rec.get("title") or "")
    link = rec.get("landingPage") or ""
    guid = rec.get("identifier") or link
    desc_html = rec.get("description") or ""
    description = strip_html(desc_html)

    keywords = rec.get("keyword") or []
    topics = [strip_html(k) for k in keywords if strip_html(k)]
    # themes are coarse (nearly always "geospatial"); keywords are the
    # real topical tags on ArcGIS Hub DCAT feeds.
    themes = [strip_html(t) for t in (rec.get("theme") or []) if strip_html(t)]

    publisher = (rec.get("publisher") or {}).get("name") or ""
    maintained_by = strip_html(publisher) or None

    distributions = rec.get("distribution") or []
    formats = []
    service_url = None
    for dist in distributions:
        fmt = (dist.get("format") or "").strip()
        if fmt and fmt not in formats:
            formats.append(fmt)
        url = (dist.get("accessURL") or "").strip()
        if url and "GeoServices" in fmt:
            service_url = url
    if not service_url:
        for dist in distributions:
            url = (dist.get("accessURL") or "").strip()
            if url and ("FeatureServer" in url or "MapServer" in url
                        or "ImageServer" in url):
                service_url = url
                break

    modified = iso_or_none(rec.get("modified") or "")
    issued = iso_or_none(rec.get("issued") or "")

    return {
        "title": title,
        "link": link,
        "guid": guid,
        "type": "Dataset",
        "featured": False,
        "topics": topics or themes,
        "pub_date_iso": issued or modified,
        "update_interval": None,
        "maintained_by": maintained_by,
        "suitable_use": None,
        "limitations_on_use": None,
        "data_dictionary": [],
        "description_raw": description,
        "structure_detected": False,
        "access_level": rec.get("accessLevel"),
        "license": rec.get("license"),
        "spatial": rec.get("spatial"),
        "formats": formats,
        "service_url": service_url,
    }


def extract_dcat(site_url: str) -> list:
    raw = fetch_dcat(site_url)
    catalog = json.loads(raw)
    datasets = catalog.get("dataset") or []
    return [parse_dcat_item(rec) for rec in datasets]


# --------------------------------------------------------------------------
# CKAN (/api/3/action/package_search)
# --------------------------------------------------------------------------

def ckan_search(base_url: str, start: int = 0, rows: int = CKAN_PAGE_SIZE) -> dict:
    sep = "&" if "?" in base_url else "?"
    url = f"{base_url}{sep}start={start}&rows={rows}"
    raw = http_get(url)
    payload = json.loads(raw)
    if not payload.get("success"):
        raise ValueError(f"CKAN search failed: {payload.get('error')}")
    return payload["result"]


def parse_ckan_item(rec: dict, base_url: str) -> dict:
    title = strip_html(rec.get("title") or "")
    name = rec.get("name") or ""
    link = f"{base_url.split('/api/3/action')[0]}/dataset/{name}"
    guid = rec.get("id") or name
    description = strip_html(rec.get("notes") or "")

    topics = [t.get("name") for t in (rec.get("tags") or []) if t.get("name")]
    topics += [g.get("title") or g.get("name")
               for g in (rec.get("groups") or [])
               if g.get("title") or g.get("name")]

    org = rec.get("organization") or {}
    maintained_by = org.get("title") or org.get("name") or None

    resources = rec.get("resources") or []
    formats = []
    service_url = None
    for res in resources:
        fmt = (res.get("format") or "").strip()
        if fmt and fmt not in formats:
            formats.append(fmt)
        if not service_url and res.get("datastore_active"):
            url = (res.get("url") or "").strip()
            if url:
                service_url = url
    if not service_url:
        for res in resources:
            url = (res.get("url") or "").strip()
            if url and ("datastore" in url.lower()
                        or "api" in url.lower()):
                service_url = url
                break

    return {
        "title": title,
        "link": link,
        "guid": guid,
        "type": "Dataset",
        "featured": False,
        "topics": topics,
        "pub_date_iso": iso_or_none(rec.get("metadata_modified") or ""),
        "update_interval": None,
        "maintained_by": maintained_by,
        "suitable_use": None,
        "limitations_on_use": None,
        "data_dictionary": [],
        "description_raw": description,
        "structure_detected": False,
        "access_level": "public" if not rec.get("private") else "private",
        "license": rec.get("license_title"),
        "spatial": None,
        "formats": formats,
        "service_url": service_url,
    }


def extract_ckan(base_url: str) -> list:
    # base_url may be the portal root (https://data.ok.gov) or a full
    # package_search URL. Normalize to the action URL.
    if "/api/3/action/package_search" not in base_url:
        action_url = base_url.rstrip("/") + CKAN_SEARCH_PATH
    else:
        action_url = base_url.split("?")[0]

    records = []
    start = 0
    while True:
        result = ckan_search(action_url, start=start)
        results = result.get("results") or []
        if not results:
            break
        records.extend(parse_ckan_item(r, action_url) for r in results)
        count = result.get("count", 0)
        start += len(results)
        if start >= count or len(results) < CKAN_PAGE_SIZE:
            break
    return records


# --------------------------------------------------------------------------
# Common post-processing
# --------------------------------------------------------------------------

def extract(site_url: str, fmt: str | None = None) -> list:
    fmt = fmt or detect_format(site_url)
    if fmt == "dcat":
        return extract_dcat(site_url)
    if fmt == "ckan":
        return extract_ckan(site_url)
    if fmt == "rss":
        return extract_rss(site_url)
    raise ValueError(f"Unknown format: {fmt}")


def finalize(records: list, fmt: str) -> list:
    """Fill provenance/scope/formats fields that live in parse helpers."""
    out = []
    for rec in records:
        rec = dict(rec)
        rec["source"] = fmt
        rec["scope"] = "county" if COUNTY_SCOPE_RE.search(
            f"{rec['title']} {rec['description_raw']}"
        ) else "state"
        # formats/service_url are set per-format; normalize key presence
        rec.setdefault("formats", [])
        rec.setdefault("service_url", None)
        out.append(rec)
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("site_url", help="ArcGIS Hub site root, CKAN portal root, "
                                         "data.json URL, or package_search URL")
    parser.add_argument("--format", dest="fmt", choices=["rss", "dcat", "ckan"],
                        help="Override auto-detection (rss|dcat|ckan)")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output")
    args = parser.parse_args()

    fmt = args.fmt or detect_format(args.site_url)
    records = extract(args.site_url, fmt)
    records = finalize(records, fmt)

    indent = 2 if args.pretty else None
    print(json.dumps(records, indent=indent, ensure_ascii=False))

    structured_count = sum(1 for r in records if r["structure_detected"])
    county_count = sum(1 for r in records if r["scope"] == "county")
    print(
        f"# {len(records)} items via {fmt}; {structured_count} had "
        f"OKC-style section structure; {county_count} flagged county-scope",
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()
