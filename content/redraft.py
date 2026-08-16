#!/usr/bin/env python3
"""
redraft.py — re-draft stub pages (all cities) against the v3 schema-grounded template.

Reads manifest.json v3 (category + schema source of truth) + each city's catalog,
re-drafts every stub page using prompts.DRAFT_SYSTEM_PROMPT_V3, then:
  - writes the new body into <content_dir>/<slug>.md
    (frontmatter rebuilt: canonical single category, cover, fixed description
     from suitable_use — repairs the old dictionary-text leak — teaser from
     the draft's one-sentence "what this is")
  - updates manifest.json content_status / content_model / last_updated
  - marks content_status: needs_review where the template doesn't fit cleanly
    (no step-4 anchor, thin dictionary, or validation flags a possible
    invented field)

Multi-city (Kansas, Nevada, Nebraska): one call per city, driven by pipeline/run.py.
Usage:
  python3 content/redraft.py --model upstage/solar-pro4:free --content-dir ... \
      --catalog ... --drafts ... --manifest ... --city-name ... --city-state ...
  python3 content/redraft.py --dry-run   # print the plan, call nothing
"""
import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
DATASETS_DIR = os.path.join(ROOT, "hugo-site", "content", "datasets")
MANIFEST_PATH = os.path.join(ROOT, "hugo-site", "static", "img", "manifest.json")
CATALOG_PATH = os.path.join(ROOT, "okc_catalog.json")
OUT_DRAFTS = os.path.join(ROOT, "drafts-v2.json")

from prompts import (DRAFT_SYSTEM_PROMPT_V2, DRAFT_SYSTEM_PROMPT_V3,
                     build_v2_payload, PROMPT_VERSION)  # noqa: E402

# Fields that let a reader anchor the "try it yourself" step to their own
# address / street / ward / neighborhood.
ANCHOR_RE = re.compile(
    r"address|street|ward|location|zip|segment|block|parcel|route|"
    r"intersection|neighbor|house|home", re.I)


def parse_frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m:
        return {}, text
    fm = {}
    for line in m.group(1).splitlines():
        if ":" not in line:
            continue
        key, _, raw = line.partition(":")
        key, raw = key.strip(), raw.strip()
        if raw.startswith("[") and raw.endswith("]"):
            fm[key] = json.loads(raw)
        elif raw.startswith('"') and raw.endswith('"'):
            fm[key] = json.loads(raw)
        elif raw == "true":
            fm[key] = True
        elif raw == "false":
            fm[key] = False
        else:
            fm[key] = raw
    return fm, m.group(2)


def yaml_str(s):
    return json.dumps(str(s), ensure_ascii=False)


def yaml_list(lst):
    return "[" + ", ".join(yaml_str(x) for x in lst) + "]"


def truncate(text, limit=170):
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= limit:
        return text
    cut = text[:limit]
    if " " in cut:
        cut = cut.rsplit(" ", 1)[0]
    return cut.rstrip(" ,;:-") + "…"


def build_frontmatter(fm, category, cover, description, teaser, dictionary):
    out = ["---"]
    for key in ("title", "date"):
        if key in fm:
            out.append(f"{key}: {yaml_str(fm[key])}")
    out.append(f"description: {yaml_str(description)}")
    out.append(f"teaser: {yaml_str(teaser)}")
    if "tags" in fm and fm["tags"]:
        out.append(f"tags: {yaml_list(fm['tags'])}")
    out.append(f"categories: {yaml_list([category])}")
    out.append(f"cover: {yaml_str(cover)}")
    for key in ("source_url", "license", "dataset_id", "city", "site_url"):
        if key in fm:
            out.append(f"{key}: {yaml_str(fm[key])}")
    out.append("draft: false")
    if dictionary:
        out.append("dictionary:")
        for item in dictionary:
            out.append(f"  - field: {yaml_str(item.get('field', ''))}")
            out.append(f"    description: {yaml_str(item.get('description', ''))}")
    out.append("---")
    return "\n".join(out)


def validate_draft(slug, title, body, dictionary, feasible):
    """Returns (needs_review, reason) — content checks, not style checks.
    `dictionary` may be a list of dicts ({field, description}) or a list of
    field-name strings (live schema)."""
    fields = set()
    for f in dictionary or []:
        if isinstance(f, dict):
            fields.add(re.sub(r"[^a-z0-9 ]", " ", (f.get("field") or "").lower()).strip())
        elif isinstance(f, str):
            fields.add(re.sub(r"[^a-z0-9 ]", " ", f.lower()).strip())
    issues = []

    if (("## What this is" not in body and "## What this tracks" not in body)
            or "## Why it matters to you" not in body):
        issues.append("missing required section (What this is / Why it matters)")
    if "## How to read this data" not in body:
        issues.append("missing How to read this data section")

    has_step4 = "## Try it yourself" in body
    has_leave = "## Where this leaves you" in body
    if feasible and not has_step4:
        issues.append("step-4 anchor exists but Try-it-yourself section missing")
    if not feasible and has_step4:
        issues.append("no step-4 anchor but Try-it-yourself section present (hollow step 4)")
    if not feasible and not has_leave and not has_step4:
        issues.append("neither Try it yourself nor Where this leaves you present")

    wc = len(body.split())
    if wc > 340:
        issues.append(f"over length ({wc} words)")

    # field check: any **Field** or capitalized name in the read section
    # that doesn't resolve to a real dictionary field
    read_sec = body.split("## How to read this data")[-1]
    for m in re.finditer(r"\*\*([^*]+)\*\*", read_sec):
        name = re.sub(r"[^a-z0-9 ]", " ", m.group(1).lower()).strip()
        if not name:
            continue
        ok = any(name == f or name in f or f in name for f in fields)
        if not ok and len(name) > 3:
            issues.append(f"possible invented field: '{m.group(1)}'")
            break  # one flag is enough

    if issues:
        return True, "; ".join(issues[:3])
    return False, None


def step4_feasible(record):
    dict_fields = [d.get("field", "") for d in (record.get("data_dictionary") or [])]
    if not dict_fields:
        return False
    return any(ANCHOR_RE.search(f) for f in dict_fields)


def build_v3_payload(d, rec, city):
    """Step 3 user prompt: city config + catalog meta + LIVE schema fields
    and samples. The schema is authoritative; catalog text is context only."""
    schema = d.get("schema") or {}
    fields = schema.get("fields") or []
    sample = schema.get("sample") or {}
    desc = (rec or {}).get("description_raw") or d.get("description") or ""
    desc = re.sub(r"<[^>]+>", " ", desc)
    lines = [
        f"City: {city['name']}, {city['state']}",
        f"Dataset: {d['title']}",
        f"Category: {d.get('display_category') or d.get('category') or ''}",
        f"Update interval: {(rec or {}).get('update_interval') or 'not stated'}",
        "Description from catalog: " + re.sub(r"\s+", " ", desc)[:500],
        "",
        "Schema fields:",
    ]
    for f in fields:
        name = f.get("name", "")
        if not name:
            continue
        alias = f.get("alias") or ""
        typ = f.get("type") or ""
        sv = sample.get(name)
        lines.append(f"  {name} ({alias}, {typ}): sample = {sv}")
    return "\n".join(lines)


def schema_has_anchor(schema):
    names = [f.get("name", "") for f in (schema or {}).get("fields", [])]
    return any(ANCHOR_RE.search(n) for n in names)


def strip_html(raw):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", raw or "")).strip()


def main():
    global DATASETS_DIR, CATALOG_PATH, OUT_DRAFTS, MANIFEST_PATH
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", default="upstage/solar-pro4:free",
                        help="model id (Nous primary; OpenRouter fallback)")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--only", help="comma list of slugs to re-draft (debug)")
    parser.add_argument("--apply-only", action="store_true",
                        help="skip drafting; apply drafts-v2.json to content files")
    parser.add_argument("--content-dir", default=DATASETS_DIR)
    parser.add_argument("--catalog", default=CATALOG_PATH)
    parser.add_argument("--drafts", default=OUT_DRAFTS)
    parser.add_argument("--manifest", default=MANIFEST_PATH)
    parser.add_argument("--city-name", default="Oklahoma City")
    parser.add_argument("--city-state", default="OK")
    parser.add_argument("--all", action="store_true",
                        help="target every dataset, not just stubs")
    args = parser.parse_args()
    DATASETS_DIR = args.content_dir
    CATALOG_PATH = args.catalog
    OUT_DRAFTS = args.drafts
    MANIFEST_PATH = args.manifest
    CITY_CONFIG = {"name": args.city_name, "state": args.city_state}

    with open(CATALOG_PATH) as f:
        catalog = json.load(f)
    by_title = {re.sub(r"\s+", " ", r["title"]).strip().lower(): r for r in catalog}
    with open(MANIFEST_PATH) as f:
        manifest = json.load(f)

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    targets = []
    for d in manifest["datasets"]:
        if not args.all and d["content_status"] != "stub":
            continue
        if args.only and d["slug"] not in args.only.split(","):
            continue
        targets.append(d)
    print(f"# {len(targets)} stub pages to re-draft (model={args.model}, prompt={PROMPT_VERSION})",
          file=sys.stderr)

    if args.dry_run:
        for d in sorted(targets, key=lambda x: x["slug"]):
            rec = by_title.get(d["title"].strip().lower())
            feas = step4_feasible(rec or {})
            print(f"  {'feasible ' if feas else 'NO-ANCHOR'} {d['slug']}")
        return

    # lazy import so --dry-run never needs keys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

    if args.apply_only:
        with open(OUT_DRAFTS) as f:
            saved = json.load(f)
        drafts_out = saved["drafts"]
        results = {"drafted": sum(1 for x in drafts_out if not x.get("needs_review")),
                   "needs_review": sum(1 for x in drafts_out if x.get("needs_review")),
                   "failed": sum(1 for x in drafts_out if x.get("error"))}
        print(f"# apply-only: {len(drafts_out)} drafts from {OUT_DRAFTS}", file=sys.stderr)
    else:
        from call_model import call_model
        drafts_out = []
        results = {"drafted": 0, "needs_review": 0, "failed": 0}
        for i, d in enumerate(sorted(targets, key=lambda x: x["slug"]), 1):
            slug = d["slug"]
            rec = by_title.get(d["title"].strip().lower())
            schema = d.get("schema") or {}
            if not schema:
                results["needs_review"] += 1
                reason = "no live schema — introspection failed or unavailable"
                drafts_out.append({"slug": slug, "body": None, "error": None,
                                   "needs_review": True, "reason": reason})
                print(f"  [{i}/{len(targets)}] {reason:14s} {slug}", file=sys.stderr)
                continue
            feas = schema_has_anchor(schema) or step4_feasible(rec or {})
            payload = build_v3_payload(d, rec, CITY_CONFIG)

            content, err = call_model(
                [
                    {"role": "system", "content": DRAFT_SYSTEM_PROMPT_V3},
                    {"role": "user", "content": payload},
                ],
                model="upstage/solar-pro4:free",  # Nous primary; OpenRouter fallback when Nous fails
                temperature=0.4, max_tokens=900,
                openrouter_model=args.model,
            )
            if err or not content:
                results["failed"] += 1
                print(f"  [{i}/{len(targets)}] FAIL {slug}: {err}", file=sys.stderr)
                drafts_out.append({"slug": slug, "body": None, "error": err,
                                   "needs_review": True, "reason": f"draft call failed: {err}"})
                continue

            body = content.strip()
            schema_fields = [f.get("name", "") for f in schema.get("fields", [])]
            dict_fields = (rec or {}).get("data_dictionary", [])
            needs_review, reason = validate_draft(slug, d["title"], body,
                                                  schema_fields or dict_fields, feas)
            if not feas and not needs_review:
                needs_review, reason = True, "no address/street/ward anchor — step-4 template doesn't fit cleanly"
            status = "needs_review" if needs_review else "drafted"
            results[status] += 1
            drafts_out.append({"slug": slug, "body": body, "error": None,
                               "needs_review": needs_review, "reason": reason})
            print(f"  [{i}/{len(targets)}] {status:14s} {slug} ({len(body.split())}w)"
                  + (f" — {reason}" if reason else ""), file=sys.stderr)

    # ---- write drafts json ----
    with open(OUT_DRAFTS, "w") as f:
        json.dump({
            "schema": 2,
            "city": "Oklahoma City",
            "prompt_version": PROMPT_VERSION,
            "content_model": f"openrouter/{args.model}/{PROMPT_VERSION}",
            "generated_at": now,
            "drafts": drafts_out,
        }, f, indent=2, ensure_ascii=False)

    # ---- apply: pages + manifest ----
    applied = 0
    by_slug = {d["slug"]: d for d in drafts_out}
    for d in manifest["datasets"]:
        draft = by_slug.get(d["slug"])
        if not draft:
            continue
        if not draft.get("body"):
            # failed/bodyless drafts must never overwrite an existing page
            continue
        path = os.path.join(DATASETS_DIR, d["slug"] + ".md")
        with open(path, encoding="utf-8") as f:
            raw = f.read()
        fm, _ = parse_frontmatter(raw)
        rec = by_title.get(d["title"].strip().lower())

        step1 = ""
        m = re.search(r"## What this is\s*\n+(.*?)(?:\n+## |\Z)", draft.get("body") or "", re.S)
        if m:
            step1 = re.sub(r"\s+", " ", m.group(1)).strip().rstrip(".")

        description = ((rec or {}).get("suitable_use") or "").strip() or fm.get("description", "")
        teaser = truncate(step1) if step1 else truncate(description, 170)
        dictionary = [{"field": x.get("field", ""), "description": x.get("description", "")}
                      for x in (rec or {}).get("data_dictionary", [])]

        new_fm = build_frontmatter(fm, d["category"], d.get("image_file") and f"covers/{d['image_file']}",
                                   description, teaser, dictionary)
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_fm + "\n\n" + (draft.get("body") or "").strip() + "\n")

        d["content_status"] = "needs_review" if (draft.get("needs_review") or draft.get("error")) else "drafted"
        d["content_model"] = "openrouter/" + args.model + "/" + PROMPT_VERSION
        d["last_updated"] = now
        applied += 1

    manifest["generated_at"] = now
    with open(MANIFEST_PATH, "w") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    print(json.dumps({"results": results, "applied_pages": applied,
                      "drafts_file": OUT_DRAFTS}, indent=2))


if __name__ == "__main__":
    main()
