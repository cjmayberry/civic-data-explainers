#!/usr/bin/env python3
"""Extract Nevada catalog from NDOT GeoHub via DCAT (gets service_urls)."""
import json, subprocess, sys

ROOT = "/opt/data/civic-data-explainers"
url = "https://geohub-ndot.hub.arcgis.com/"

print(f"Extracting Nevada via DCAT from {url}...", flush=True)
r = subprocess.run(
    ["python3", "extractor/extract_catalog.py", url, "--format", "dcat"],
    capture_output=True, text=True, cwd=ROOT, timeout=300
)
if r.returncode != 0:
    print(f"ERROR: {r.stderr}", file=sys.stderr)
    sys.exit(r.returncode)

cat = json.loads(r.stdout)
json.dump(cat, open(f"{ROOT}/nevada_catalog.json", "w"), indent=2)
print(f"Saved nevada_catalog.json: {len(cat)} records", flush=True)

# Summary
su = sum(1 for r in cat if r.get("service_url"))
print(f"With service_url: {su}/{len(cat)}", flush=True)
print(f"Without service_url: {len(cat) - su}/{len(cat)}", flush=True)
print(f"Source: {set(r.get('source','?') for r in cat)}", flush=True)
print(f"Structure detected: {sum(1 for r in cat if r.get('structure_detected'))}", flush=True)
