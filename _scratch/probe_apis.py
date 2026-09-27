#!/usr/bin/env python3
import json, urllib.request, ssl, re
from concurrent.futures import ThreadPoolExecutor, as_completed

ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

def fetch(url, timeout=12):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        resp = urllib.request.urlopen(req, timeout=timeout, context=ssl_ctx)
        return resp.status, resp.read().decode("utf-8", errors="replace")[:5000]
    except:
        return 0, None

def get_count(url):
    s, c = fetch(f"{url}/api/3/action/package_search?rows=0")
    if s == 200 and c and '"result"' in c[:200]:
        m = re.search(r'"count"\s*:\s*(\d+)', c)
        if m: return "CKAN", int(m.group(1))
    s, c = fetch(f"{url}/api/search?q=&rows=0")
    if s == 200 and c and '"count"' in c[:200]:
        m = re.search(r'"count"\s*:\s*(\d+)', c)
        if m: return "Socrata", int(m.group(1))
    s, c = fetch(f"{url}/api/views?limit=1")
    if s == 200 and c and c.strip().startswith("["):
        return "Socrata", "?"
    s, c = fetch(f"{url}/api/v3/search?q=*&rows=5")
    if s == 200 and c and '"total"' in c:
        m = re.search(r'"total"\s*:\s*(\d+)', c)
        if m: return "ArcGIS", int(m.group(1))
    return None, 0

candidates = {
    "AK": ["https://gis.data.alaska.gov"],
    "AL": ["https://data-algeohub.opendata.arcgis.com"],
    "AR": ["https://data.arkansas.gov"],
    "DE": ["https://data.delaware.gov"],
    "FL": ["https://data.florida.gov"],
    "GA": ["https://data.georgia.gov"],
    "IA": ["https://data.iowa.gov"],
    "ID": ["https://data.idaho.gov"],
    "IN": ["https://data.indiana.gov"],
    "KS": ["https://data.kansas.gov"],
    "KY": ["https://data.ky.gov"],
    "LA": ["https://data.louisiana.gov"],
    "MD": ["https://data.maryland.gov"],
    "ME": ["https://data.maine.gov"],
    "MN": ["https://data.hennepin.us"],
    "MS": ["https://data.mississippi.gov"],
    "MT": ["https://data.montana.gov"],
    "NC": ["https://data.ncdot.gov"],
    "ND": ["https://data.nd.gov"],
    "NE": ["https://data.nebraska.gov"],
    "NM": ["https://data.nm.gov"],
    "NV": ["https://data.nv.gov"],
    "OH": ["https://data.ohio.gov"],
    "RI": ["https://data.ri.gov"],
    "SC": ["https://data.sc.gov"],
    "SD": ["https://data.sd.gov"],
    "TN": ["https://data.tn.gov"],
    "UT": ["https://data.utah.gov"],
    "WI": ["https://data-wisconsin.opendata.arcgis.com"],
    "WV": ["https://data.westvirginia.gov"],
    "WY": ["https://data.wyoming.gov"],
}

all_pairs = []
for state, urls in candidates.items():
    for url in urls:
        all_pairs.append((state, url))

def test_pair(state, url):
    api, count = get_count(url)
    if api:
        return (state, url, api, count)
    return (state, url, None, 0)

results = []
with ThreadPoolExecutor(max_workers=20) as ex:
    futs = {ex.submit(test_pair, s, u): (s, u) for s, u in all_pairs}
    for f in as_completed(futs, timeout=120):
        results.append(f.result())

found = {}
for state, url, api, count in results:
    if api and state not in found:
        found[state] = (url, api, count)
        print(f"  {state:3s} | {api:12s} | {count} | {url}")

print(f"\n{len(found)}/31 states found")
