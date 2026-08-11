#!/usr/bin/env python3
"""Nightly state+capital add — orchestrates a full jurisdiction build headlessly.

For one jurisdiction (state or capital): extract catalog -> curate (bounded,
resident-facing) -> scaffold -> wire into the site (cities.json + layouts +
_index) -> pipeline stages (manifest/introspect/draft/covers) -> build.

SAFETY (the "never leave the repo broken" rule):
  - A jurisdiction is only kept (in cities.json + content + layouts) if its
    pipeline actually DRAFTS content (content_status != stub). Anything that
    fails is ROLLED BACK so no undrafted section ever renders as junk.
  - The orchestrator only commits+pushes when at least one jurisdiction
    drafted and the site builds; otherwise it writes a report and keeps the
    repo clean for a retry the next night.

Usage:
  python3 pipeline/nightly_add.py --registry data/jurisdictions.json --commit
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORT = "/opt/data/Ocean/outputs/reports/civic-nightly-build-latest.md"
LEDGER = "/opt/data/Ocean/outputs/reports/civic-nightly-ledger.md"
PIPELINE_TIMEOUT = 900

def sh(cmd, timeout=900):
    return subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, timeout=timeout)

def rollback(city):
    """Remove a half-added jurisdiction so no undrafted section leaks to the site."""
    cf = os.path.join(ROOT, "cities.json")
    cities = json.load(open(cf)); cities = [c for c in cities if c["id"] != city]
    json.dump(cities, open(cf, "w"), indent=2, ensure_ascii=False)
    rcf = os.path.join(ROOT, "hugo-site", "data", "cities.json")
    rc = json.load(open(rcf)); rc.pop(city, None)
    json.dump(rc, open(rcf, "w"), indent=2, ensure_ascii=False)
    for d in (f"hugo-site/content/{city}", f"hugo-site/static/{city}", f"hugo-site/layouts/{city}"):
        p = os.path.join(ROOT, d)
        if os.path.isdir(p):
            shutil.rmtree(p)

def extract(portal_url, out_catalog):
    r = sh(["python3", "extractor/extract_catalog.py", portal_url], timeout=300)
    if r.returncode != 0:
        # RSS fast-path may fail on malformed XML -> retry with DCAT data.json
        r = sh(["python3", "extractor/extract_catalog.py", portal_url, "--format", "dcat"], timeout=300)
    if r.returncode != 0:
        raise RuntimeError(f"extract failed (rss+dcat): {(r.stderr or r.stdout)[-400:]}")
    s = r.stdout.find("[")
    open(out_catalog, "w").write(r.stdout[s:] if s >= 0 else r.stdout)
    return len(json.load(open(out_catalog)))

def curate(catalog, out, cap):
    r = sh(["python3", "pipeline/curate.py", "--catalog", catalog, "--out", out, "--cap", str(cap)])
    if r.returncode != 0:
        raise RuntimeError(f"curate failed: {r.stderr[-400:]}")
    return r.stdout.strip()

def scaffold(cat, city, out_dir, static_dir):
    r = sh(["python3", "content/scaffold_city.py", "--catalog", cat, "--city", city,
            "--site-url", "https://civic-data-explainers.pages.dev",
            "--out", os.path.join(ROOT, out_dir), "--static-out", os.path.join(ROOT, static_dir)])
    if r.returncode != 0:
        raise RuntimeError(f"scaffold failed: {r.stderr[-400:]}")
    import glob
    return len(glob.glob(os.path.join(ROOT, out_dir, "*.md")))

def wire(city, name, hub, gov, state, level):
    cf = os.path.join(ROOT, "cities.json")
    cities = json.load(open(cf))
    if not any(c["id"] == city for c in cities):
        cities.append({"id": city, "name": name, "hub_url": hub, "gov_url": gov,
                       "state": state, "active": True, "model": None, "min_score": 0,
                       "content_dir": f"hugo-site/content/{city}",
                       "static_dir": f"hugo-site/static/{city}", "category_map": {}})
        json.dump(cities, open(cf, "w"), indent=2, ensure_ascii=False)
    rcf = os.path.join(ROOT, "hugo-site", "data", "cities.json")
    rc = json.load(open(rcf))
    if city not in rc:
        rc[city] = {"name": name, "short": name.split()[-1], "hub": hub, "gov": gov,
                    "center": [0, 0], "blurb": f"{name} open-data explainers."}
        json.dump(rc, open(rcf, "w"), indent=2, ensure_ascii=False)
    template = "missouri" if level == "state" else "okc"
    for f in ("single.html", "list.html"):
        src = os.path.join(ROOT, "hugo-site", "layouts", template, f)
        dst = os.path.join(ROOT, "hugo-site", "layouts", city, f)
        if os.path.exists(src) and not os.path.exists(dst):
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(src, dst)
    idx = os.path.join(ROOT, f"hugo-site/content/{city}/_index.md")
    if not os.path.exists(idx):
        open(idx, "w").write(f"---\ntitle: \"{name} explainers\"\ndraft: false\n---\n")

def run_pipeline(city):
    r = sh(["python3", "pipeline/run.py", "cities.json", "--city", city,
            "--model", "deepseek/deepseek-chat-v3-0324"], timeout=PIPELINE_TIMEOUT)
    return r.returncode

def section_drafted(city):
    mpath = os.path.join(ROOT, f"hugo-site/static/{city}/manifest.json")
    if not os.path.exists(mpath):
        return False, 0
    data = json.load(open(mpath))
    entries = data if isinstance(data, list) else data.get("datasets", [])
    drafted = sum(1 for e in entries if (e.get("content_status") or "") in ("drafted", "published"))
    return drafted > 0, drafted

def add_one(city, name, portal, hub, gov, state, level, cap, dry_draft):
    cat = os.path.join(ROOT, f"{city}_catalog.json")
    cur = f"/tmp/{city}_curated.json"
    steps = []
    try:
        n = extract(portal, cat); steps.append(f"extracted {n}")
        curate(cat, cur, cap); steps.append(f"curated≤{cap}")
        ns = scaffold(cur, city, f"hugo-site/content/{city}", f"hugo-site/static/{city}")
        steps.append(f"scaffolded {ns}")
        wire(city, name, hub, gov, state, level); steps.append("wired")
        if not dry_draft:
            rc = run_pipeline(city); steps.append(f"pipeline exit {rc}")
            ok_d, nd = section_drafted(city)
            if not ok_d:
                rollback(city)
                return False, f"{', '.join(steps)} — NOT DRAFTED (rolled back)"
            steps.append(f"{nd} drafted")
        return True, ", ".join(steps)
    except Exception as e:
        rollback(city)
        return False, f"ERROR: {e} (rolled back)"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--registry"); ap.add_argument("--commit", action="store_true")
    ap.add_argument("--dry-draft", action="store_true"); ap.add_argument("--cap", type=int, default=120)
    args = ap.parse_args()

    if not args.registry:
        ap.error("--registry required")
    reg = json.load(open(args.registry))
    queue = reg["queue"]
    state = next((c for c in queue if c["level"] == "state" and c.get("status") == "pending"), None)
    capital = None
    if state:
        capital = next((c for c in queue if c.get("parent") == state["id"] and c.get("status") == "pending"), None)
    rows, errors, drafted = [], [], []
    for j in ([state, capital] if state else []):
        if not j or not j.get("portal_url"):
            errors.append(f"{j['id'] if j else '?'}: no portal_url — skip"); continue
        ok, d = add_one(j["id"], j["name"], j["portal_url"], j.get("hub_url") or j["portal_url"],
                        j.get("gov_url") or "", j.get("state", "US"), j["level"],
                        args.cap if j["level"] == "state" else max(60, args.cap // 2), args.dry_draft)
        rows.append((j["id"], ok, d))
        if ok:
            drafted.append(j["id"]); j["status"] = "live"

    # Build + commit ONLY if something drafted (or dry-draft plumbing test)
    do_commit = args.commit and (drafted or args.dry_draft)
    if do_commit:
        b = sh(["bash", "build.sh"], timeout=300)
        if b.returncode != 0:
            errors.append(f"build failed: {b.stderr[-400:]}")
            do_commit = False
    if do_commit:
        json.dump(reg, open(args.registry, "w"), indent=2, ensure_ascii=False)
        write_report(rows, errors)
        sh(["git", "add", "-A"]); sh(["git", "commit", "-m", f"nightly add: {', '.join(drafted)}"])
        sh(["git", "push"])
    else:
        write_report(rows, errors)
    print("\n".join(f"{c}: {'OK' if ok else 'FAIL'} — {d}" for c, ok, d in rows))
    if errors: print("\n".join("ERR: " + e for e in errors))

def write_report(rows, errors):
    os.makedirs(os.path.dirname(REPORT), exist_ok=True)
    lines = [f"# Civic Nightly Build — {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}"]
    lines += [f"- **{c}**: {'✅' if ok else '❌'} {d}" for c, ok, d in rows]
    if errors:
        lines.append("\n## Errors\n" + "\n".join(f"- {e}" for e in errors))
    open(REPORT, "w").write("\n".join(lines) + "\n")
    with open(LEDGER, "a") as f:
        f.write(f"- {datetime.now(timezone.utc).isoformat()} | " + "; ".join(
            f"{c}:{'ok' if ok else 'FAIL'}" for c, ok, _ in rows) + "\n")

if __name__ == "__main__":
    main()
