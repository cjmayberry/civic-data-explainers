#!/usr/bin/env python3
"""
Definitive scan of all 50 state data portals.

Probe strategy per URL:
1. CKAN: /api/3/action/package_search?rows=0 → parse count
2. Socrata: /api/views?limit=1 → if JSON array, it's Socrata → get full count via /api/views
3. Socrata: /api/search?q=&rows=0 → parse count (newer Socrata)
4. ArcGIS Hub: /api/v3/search?q=*&rows=5 → parse total
Uses regex to extract counts from truncated JSON (avoids parse errors on large responses).
"""
import json, urllib.request, ssl, re
from concurrent.futures import ThreadPoolExecutor, as_completed

ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

def fetch(url, timeout=20):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0", "Accept": "*/*"})
        resp = urllib.request.urlopen(req, timeout=timeout, context=ssl_ctx)
        return resp.status, resp.read().decode("utf-8", errors="replace")[:50000]
    except:
        return 0, None

def probe(url):
    """Returns (api_type, count, final_url)."""
    # 1. CKAN
    s, c = fetch(f"{url}/api/3/action/package_search?rows=0")
    if s == 200 and c and '"result"' in c[:200]:
        m = re.search(r'"count"\s*:\s*(\d+)', c[:300])
        if m:
            return "CKAN", int(m.group(1)), url
    
    # 2. Socrata /api/views?limit=1 (quick probe)
    s, c = fetch(f"{url}/api/views?limit=1")
    if s == 200 and c and c.strip().startswith("["):
        # It's Socrata — now get full count
        s2, c2 = fetch(f"{url}/api/views", timeout=25)
        if s2 == 200 and c2 and c2.strip().startswith("["):
            try:
                views = json.loads(c2[:100000])
                if isinstance(views, list):
                    datasets = [v for v in views if isinstance(v, dict) and v.get("assetType") == "dataset"]
                    return "Socrata", len(datasets), url
            except:
                pass
        # Try Socrata search endpoint for count
        s3, c3 = fetch(f"{url}/api/search?q=&rows=0", timeout=20)
        if s3 == 200 and c3 and '"count"' in c3[:200]:
            m = re.search(r'"count"\s*:\s*(\d+)', c3[:300])
            if m:
                return "Socrata", int(m.group(1)), url
        return "Socrata", "?", url
    
    # 3. Socrata /api/search?q=&rows=0
    s, c = fetch(f"{url}/api/search?q=&rows=0")
    if s == 200 and c and '"count"' in c[:200]:
        m = re.search(r'"count"\s*:\s*(\d+)', c[:300])
        if m:
            return "Socrata", int(m.group(1)), url
    
    # 4. ArcGIS Hub /api/v3/search
    s, c = fetch(f"{url}/api/v3/search?q=*&rows=5")
    if s == 200 and c and '"total"' in c:
        m = re.search(r'"total"\s*:\s*(\d+)', c[:300])
        if m:
            return "ArcGIS-Hub", int(m.group(1)), url
    
    return None, 0, None

# All 50 states with their best candidate URLs
ALL = {
    "AL": ["https://data.alabama.gov"],
    "AK": ["https://gis.data.alaska.gov", "https://data.alaska.gov"],
    "AZ": ["https://data.az.gov", "https://phoenixopendata.com", "https://azgeo-open-data-agic.hub.arcgis.com"],
    "AR": ["https://data.arkansas.gov", "https://gis.arkansas.gov"],
    "CA": ["https://data.ca.gov"],
    "CO": ["https://data.colorado.gov"],
    "CT": ["https://data.ct.gov"],
    "DE": ["https://data.delaware.gov", "https://de-firstmap-delaware.hub.arcgis.com"],
    "FL": ["https://data.florida.gov", "https://geodata.floridagio.gov"],
    "GA": ["https://data.georgia.gov"],
    "HI": ["https://opendata.hawaii.gov", "https://data.hawaii.gov"],
    "IA": ["https://data.iowa.gov"],
    "ID": ["https://data.idaho.gov"],
    "IL": ["https://data.illinois.gov"],
    "IN": ["https://data.indiana.gov", "https://data.indy.gov"],
    "KS": ["https://data.kansas.gov"],
    "KY": ["https://data.ky.gov"],
    "LA": ["https://data.louisiana.gov"],
    "MA": ["https://data.boston.gov"],
    "MD": ["https://data.maryland.gov"],
    "ME": ["https://data.maine.gov"],
    "MI": ["https://data.michigan.gov"],
    "MN": ["https://data.hennepin.us"],
    "MS": ["https://data.mississippi.gov"],
    "MO": ["https://data.mo.gov"],
    "MT": ["https://data.montana.gov"],
    "NE": ["https://data.nebraska.gov"],
    "NV": ["https://data.nv.gov"],
    "NH": ["https://data.nh.gov", "https://www.nh.gov/data"],
    "NJ": ["https://data.nj.gov"],
    "NM": ["https://data.nm.gov"],
    "NY": ["https://data.ny.gov"],
    "NC": ["https://data.ncdot.gov", "https://data.raleighnc.gov"],
    "ND": ["https://data.nd.gov"],
    "OH": ["https://data.ohio.gov"],
    "OK": ["https://data.ok.gov"],
    "OR": ["https://data.oregon.gov"],
    "PA": ["https://data.pa.gov"],
    "RI": ["https://data.ri.gov"],
    "SC": ["https://data.sc.gov"],
    "SD": ["https://data.sd.gov", "https://dss.sd.gov"],
    "TN": ["https://data.tn.gov", "https://data.nashville.gov"],
    "TX": ["https://data.texas.gov"],
    "UT": ["https://data.slc.gov", "https://data.utah.gov"],
    "VT": ["https://data.vermont.gov"],
    "VA": ["https://data.virginia.gov"],
    "WA": ["https://data.wa.gov"],
    "WI": ["https://data-wisconsin.opendata.arcgis.com", "https://data.wisconsin.gov"],
    "WV": ["https://data.westvirginia.gov"],
    "WY": ["https://data.wyoming.gov"],
}

capitals = {"AL":"Montgomery","AK":"Juneau","AZ":"Phoenix","AR":"Little Rock",
    "CA":"Sacramento","CO":"Denver","CT":"Hartford","DE":"Dover","FL":"Tallahassee",
    "GA":"Atlanta","HI":"Honolulu","IA":"Des Moines","ID":"Boise","IL":"Springfield",
    "IN":"Indianapolis","KS":"Topeka","KY":"Frankfort","LA":"Baton Rouge",
    "MA":"Boston","MD":"Annapolis","ME":"Augusta","MI":"Lansing","MN":"Saint Paul",
    "MS":"Jackson","MO":"Jefferson City","MT":"Helena","NE":"Lincoln","NV":"Carson City",
    "NH":"Concord","NJ":"Trenton","NM":"Santa Fe","NY":"Albany","NC":"Raleigh",
    "ND":"Bismarck","OH":"Columbus","OK":"Oklahoma City","OR":"Salem","PA":"Harrisburg",
    "RI":"Providence","SC":"Columbia","SD":"Pierre","TN":"Nashville","TX":"Austin",
    "UT":"Salt Lake City","VT":"Montpelier","VA":"Richmond","WA":"Olympia","WI":"Madison",
    "WV":"Charleston","WY":"Cheyenne"}

# Build all (state, url) pairs
pairs = []
for state, urls in ALL.items():
    for url in urls:
        pairs.append((state, url))

results = {}
with ThreadPoolExecutor(max_workers=25) as ex:
    futs = {ex.submit(probe, u): (s, u) for s, u in pairs}
    for f in as_completed(futs, timeout=120):
        state, url = futs[f]
        try:
            api, count, final = f.result()
            if api and state not in results:
                results[state] = (url, api, count)
        except:
            pass

print("=== ALL 50 STATES — FINAL PORTAL SCAN ===")
found = 0
total = 0
for state in sorted(ALL.keys()):
    capital = capitals.get(state, "?")
    if state in results:
        found += 1
        url, api, count = results[state]
        if isinstance(count, int):
            total += count
            c = str(count)
        else:
            c = str(count)
        print(f"  {state:3s} | {capital:15s} | {api:12s} | {c:>6} | {url}")
    else:
        print(f"  {state:3s} | {capital:15s} | NOT FOUND   |      |")

print(f"\n{found}/50 states | {total} datasets (CKAN/Socrata counted)")
