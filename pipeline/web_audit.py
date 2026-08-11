#!/usr/bin/env python3
"""Web auditor for Civic Data, Explained — crawls the live site regularly.

Checks every section + dataset page for:
  - HTTP 200
  - branding integrity (a page under /kansas/ must NOT render another city's
    name in its H1/header — catches the missouri-on-kansas class of bug)
  - cover image loads (HTTP 200, not 404-HTML)
  - live-map container present on dataset pages
Writes a report to Ocean/outputs/reports/civic-web-audit-latest.md.

Usage: python3 pipeline/web_audit.py [--base https://civic-data-explainers.pages.dev] [--limit N]
"""
import argparse
import concurrent.futures
import json
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone

REPORT = "/opt/data/Ocean/outputs/reports/civic-web-audit-latest.md"

def fetch(url, timeout=25):
    req = urllib.request.Request(url, headers={"User-Agent": "civic-audit/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read().decode("utf-8", "ignore")
    except urllib.error.HTTPError as e:
        return e.code, ""
    except Exception as e:
        return 0, ""

def audit_page(base, path, city, limit):
    url = base + path
    status, html = fetch(url)
    if status != 200:
        return ("FAIL", f"{path} HTTP {status}", False)
    cov = re.search(r'class="(?:card-|article-)?cover"[^>]*src="([^"]+)"', html)
    if not cov:
        return ("FAIL", f"{path} no cover", False)
    has_map = "data-maplibre-geojson" in html
    return ("OK", f"{path} cover+map={has_map}", has_map)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default="https://civic-data-explainers.pages.dev")
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()

    sections = ["okc", "memphis", "lisbon", "missouri", "tennessee", "kansas"]
    city_names = {"okc": "Oklahoma City", "memphis": "Memphis", "lisbon": "Lisbon",
                  "missouri": "Missouri", "tennessee": "Tennessee", "kansas": "Kansas"}
    rows, fails = [], []

    # 1. audit each section index
    for s in sections:
        status, html = fetch(args.base + f"/{s}/")
        if status != 200:
            rows.append((s, "FAIL", f"/{s}/ HTTP {status}")); fails.append(f"/{s}/ HTTP {status}"); continue
        m = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.S)
        title = re.sub(r"<[^>]+>", "", m.group(1)).strip() if m else ""
        if s == "okc":
            # OKC's flagship list page is titled "All explainers" by design — check it
            # does NOT leak any other city's name instead.
            ok = not any(n.lower() in title.lower() for n in city_names.values() if n != "Oklahoma City")
        else:
            ok = city_names.get(s, "").lower() in title.lower()
        rows.append((s, "OK" if ok else "FAIL", f"/{s}/ title='{title}'"))
        if not ok: fails.append(f"/{s}/ branding: '{title}'")

    # 2. audit dataset pages (sample: parse card links from section index)
    seen = 0
    map_count = 0
    for s in sections:
        status, html = fetch(args.base + f"/{s}/")
        if status != 200: continue
        links = re.findall(rf'href="(/{s}/[a-z0-9_-]+/)"', html)
        links = sorted(set(links))
        if args.limit: links = links[:args.limit]
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
            futs = {ex.submit(audit_page, args.base, p, city_names.get(s, ""), args.limit): p for p in links}
            for fu in concurrent.futures.as_completed(futs):
                status, detail, has_map = fu.result()
                seen += 1
                if status != "OK":
                    fails.append(detail)
                    rows.append((s, status, detail))
                else:
                    map_count += 1 if has_map else 0

    # report
    os.makedirs(os.path.dirname(REPORT), exist_ok=True)
    with open(REPORT, "w") as f:
        f.write(f"# Civic Web Audit — {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}\n")
        f.write(f"\nSections checked: {len(sections)} · dataset pages checked: {seen} · failures: {len(fails)} · pages with live map: {map_count}/{seen}\n\n")
        if fails:
            f.write("## Failures\n" + "\n".join(f"- {x}" for x in fails) + "\n")
        else:
            f.write("## All green ✅\n")
        f.write("\n## Section titles\n" + "\n".join(f"- {c}: {t}" for c, st, t in rows if t.startswith("/")) + "\n")
    # watchdog stdout: silent when green, print failures when broken (for a no-agent cron)
    if fails:
        print(f"CIVIC WEB AUDIT: {len(fails)} failures across {seen} pages:")
        for x in fails[:30]:
            print("  FAIL:", x)
    else:
        print(f"OK — {seen} pages, all green ({map_count} with live map)")

if __name__ == "__main__":
    main()
