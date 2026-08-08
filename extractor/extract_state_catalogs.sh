#!/usr/bin/env bash
# Refresh every catalog the pipeline can consume from one command.
# Writes: okc_catalog.json (RSS), odot_catalog.json + occ_catalog.json (DCAT),
#         okgov_catalog.json (CKAN).
# Usage: bash extractor/extract_state_catalogs.sh   (from repo root)
set -euo pipefail
cd "$(dirname "$0")/.."

PY=python3
EX=extractor/extract_catalog.py

echo "== OKC (ArcGIS Hub RSS) =="
$PY "$EX" https://open-okc.hub.arcgis.com > okc_catalog.json
echo "== ODOT (ArcGIS Hub DCAT data.json) =="
$PY "$EX" https://gis-okdot.opendata.arcgis.com/data.json > odot_catalog.json
echo "== OCC (ArcGIS Hub DCAT data.json) =="
$PY "$EX" https://gisdata-occokc.opendata.arcgis.com/data.json > occ_catalog.json
echo "== data.ok.gov (CKAN package_search) =="
$PY "$EX" https://data.ok.gov/api/3/action/package_search > okgov_catalog.json
echo "== ACOG (ArcGIS Hub RSS; needs scaffold_city.py for service URLs) =="
$PY "$EX" https://acog-maps-and-data-acog.hub.arcgis.com > acog_catalog.json
echo "== Missouri (Socrata discovery API) =="
$PY "$EX" https://data.mo.gov/api/catalog/v1 > mo_catalog.json

echo
echo "Done. Record counts:"
for f in okc_catalog.json odot_catalog.json occ_catalog.json okgov_catalog.json acog_catalog.json mo_catalog.json; do
  n=$($PY -c "import json;print(len(json.load(open('$f'))))")
  echo "  $f: $n"
done
