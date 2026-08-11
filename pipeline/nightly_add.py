#!/usr/bin/env python3
"""Nightly state+capital add — orchestrates a full jurisdiction build headlessly.

For one jurisdiction (state or capital): extract catalog -> curate (bounded,
resident-facing) -> scaffold -> wire into the site (cities.json + layouts +
_index) -> pipeline stages (manifest/introspect/draft/covers) -> build.
The `--registry` driver pops the next (state, capital) pair from
data/jurisdictions.json and runs both, then commits+pushes and writes the
report. Runs with zero user interaction (plain python, no approval gate).

Usage:
  python3 pipeline/nightly_add.py --city kansas --catalog kansas_catalog.json --cap 120 --level state
  python3 pipeline/nightly_add.py --registry data/jurisdictions.json --dry-draft
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORT = "/opt/data/Ocean/outputs/reports/civic-nightly-build-latest.md"
LEDGER = "/opt/data/Ocean/outputs/reports/civic-nightly-ledger.md"

def sh(cmd, timeout=400):
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, timeout=timeout)
    return r

def extract(portal_url, out_catalog):
    r = sh(["python3", "extractor/extract_catalog.py", portal_url])
    if r.returncode != 0:
        raise RuntimeError(f"extract failed: {r.stderr[-500:]}")
    # extractor prints JSON to stdout; strip any non-JSON log tail
    data = r.stdout
    # find the JSON array
    s = data.find("[")
    open(out_catalog, "w").write(data[s:] if s >= 0 else data)
    n = len(json.load(open(out_catalog)))
    return n

def curate(catalog, out, cap):
    r = sh(["python3", "pipeline/curate.py", "--catalog", catalog, "--out", out, "--cap", str(cap)])
    if r.returncode != 0:
        raise RuntimeError(f"curate failed: {r.stderr[-500:]}")
    return r.stdout.strip()

def scaffold(cat, city, out_dir, static_dir):
    r = sh(["python3", "content/scaffold_city.py", "--catalog", cat, "--city", city,
            "--site-url", "https://civic-data-explainers.pages.dev",
            "--out", os.path.join(ROOT, out_dir), "--static-out", os.path.join(ROOT, static_dir)])
    if r.returncode != 0:
        raise RuntimeError(f"scaffold failed: {r.stderr[-500:]}")
    import glob
    return len(glob.glob(os.path.join(ROOT, out_dir, "*.md")))

def wire(city, name, hub, gov, state, level):
    """Add the city to root + render cities.json, copy layouts, write _index."""
    # root cities.json
    cf = os.path.join(ROOT, "cities.json")
    cities = json.load(open(cf))
    if not any(c["id"] == city for c in cities):
        cities.append({"id": city, "name": name, "hub_url": hub, "gov_url": gov,
                       "state": state, "active": True, "model": None, "min_score": 0,
                       "content_dir": f"hugo-site/content/{city}",
                       "static_dir": f"hugo-site/static/{city}", "category_map": {}})
        json.dump(cities, open(cf, "w"), indent=2, ensure_ascii=False)
    # render cities.json (hugo-site/data)
    rcf = os.path.join(ROOT, "hugo-site", "data", "cities.json")
    rc = json.load(open(rcf))
    if city not in rc:
        rc[city] = {"name": name, "short": name.split()[-1], "hub": hub, "gov": gov,
                    "center": [0, 0], "blurb": f"{name} open-data explainers."}
        json.dump(rc, open(rcf, "w"), indent=2, ensure_ascii=False)
    # layouts: copy a template city's single/list
    template = "missouri" if level == "state" else "okc"
    for f in ("single.html", "list.html"):
        src = os.path.join(ROOT, "hugo-site", "layouts", template, f)
        dst = os.path.join(ROOT, "hugo-site", "layouts", city, f)
        if os.path.exists(src) and not os.path.exists(dst):
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(src, dst)
    # _index.md (fixes pluralized section title)
    idx = os.path.join(ROOT, f"hugo-site/content/{city}/_index.md")
    if not os.path.exists(idx):
        open(idx, "w").write(f"---\ntitle: \"{name} explainers\"\ndraft: false\n---\n")

def run_pipeline(city, catalog, cmap_empty_ok=True):
    # manifest -> introspect -> draft -> covers via run.py for this city
    r = sh(["python3", "pipeline/run.py", "cities.json", "--city", city,
            "--model", "deepseek/deepseek-chat-v3-0324"])
    return r.returncode

def build():
    env = dict(os.environ)
    return sh(["bash", "build.sh"]).returncode

def write_report(rows, errors):
    os.makedirs(os.path.dirname(REPORT), exist_ok=True)
    lines = [f"# Civic Nightly Build — {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}"]
    for city, ok, detail in rows:
        lines.append(f"- **{city}**: {'✅' if ok else '❌'} {detail}")
    if errors:
        lines.append("\n## Errors\n" + "\n".join(f"- {e}" for e in errors))
    lines.append("\n## Next up\nSee data/jurisdictions.json queue.")
    open(REPORT, "w").write("\n".join(lines) + "\n")
    with open(LEDGER, "a") as f:
        f.write(f"- {datetime.now(timezone.utc).isoformat()} | " + "; ".join(
            f"{c}:{'ok' if ok else 'FAIL'}" for c, ok, _ in rows) + "\n")

def add_one(city, name, portal, hub, gov, state, level, cap, dry_draft):
    detail = []
    cat = os.path.join(ROOT, f"{city}_catalog.json")
    cur = f"/tmp/{city}_curated.json"
    out_dir = f"hugo-site/content/{city}"
    static_dir = f"hugo-site/static/{city}"
    try:
        n = extract(portal, cat)
        detail.append(f"extracted {n}")
        cur_msg = curate(cat, cur, cap)
        detail.append(f"curated->{cap}")
        ns = scaffold(cur, city, out_dir, static_dir)
        detail.append(f"scaffolded {ns} stubs")
        wire(city, name, hub, gov, state, level)
        detail.append("wired")
        if not dry_draft:
            rc = run_pipeline(city, cur)
            detail.append(f"pipeline exit {rc}")
        return True, ", ".join(detail)
    except Exception as e:
        return False, f"ERROR: {e}"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--city"); ap.add_argument("--name"); ap.add_argument("--portal")
    ap.add_argument("--hub"); ap.add_argument("--gov"); ap.add_argument("--state")
    ap.add_argument("--level", default="state"); ap.add_argument("--cap", type=int, default=120)
    ap.add_argument("--registry"); ap.add_argument("--dry-draft", action="store_true")
    ap.add_argument("--commit", action="store_true")
    args = ap.parse_args()

    if args.registry:
        reg = json.load(open(args.registry))
        queue = reg["queue"]
        # pop next state + its capital
        state = next((c for c in queue if c["level"] == "state" and c.get("status") == "pending"), None)
        capital = None
        if state:
            capital = next((c for c in queue if c.get("parent") == state["id"] and c.get("status") == "pending"), None)
        rows, errors = [], []
        for j in ([state, capital] if state else []):
            if not j or not j.get("portal_url"):
                errors.append(f"{j['id'] if j else '?'}: no portal_url — skip")
                continue
            ok, d = add_one(j["id"], j["name"], j["portal_url"], j["hub_url"] or j["portal_url"],
                            j["gov_url"] or "", j.get("state","US"), j["level"],
                            args.cap if j["level"] == "state" else max(60, args.cap // 2), args.dry_draft)
            rows.append((j["id"], ok, d))
            if ok:
                j["status"] = "live"
        if args.commit:
            json.dump(reg, open(args.registry, "w"), indent=2, ensure_ascii=False)
            write_report(rows, errors)
            sh(["git", "add", "-A"]); sh(["git", "commit", "-m", "nightly add"]);
            sh(["git", "push"])
        print("\n".join(f"{c}: {'OK' if ok else 'FAIL'} — {d}" for c, ok, d in rows))
        if errors: print("\n".join(errors))
    else:
        ok, d = add_one(args.city, args.name, args.portal, args.hub or args.portal,
                        args.gov or "", args.state or "US", args.level, args.cap, args.dry_draft)
        print(("OK — " if ok else "FAIL — ") + d)

if __name__ == "__main__":
    main()
