#!/usr/bin/env python3
"""Efficient scan: use Socrata's domain discovery + CKAN/CKAN-style probes.

Key insight: Socrata has a public catalog at
https://socratadiscovery.blob.core.windows.net/socratadiscovery/ that lists
all known Socrata domains. But we can also just probe /api/views?limit=1 on
all candidate URLs in parallel.

Also: many state portals redirect data.state.gov to a specific domain.
We test all known patterns in parallel with short timeouts.
"""
import json, urllib.request, ssl
from concurrent.futures import ThreadPoolExecutor, as_completed

ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

def fetch(url, timeout=10):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        resp = urllib.request.urlopen(req, timeout=timeout, context=ssl_ctx)
        return resp.status, resp.read().decode("utf-8", errors="replace")[:20000], resp.url
    except:
        return 0, None, None

def fetch_json(url, timeout=10):
    s, c, f = fetch(url, timeout)
    if s == 200 and c:
        try:
            return json.loads(c), f
        except:
            pass
    return None, f

def probe(url):
    """Quick probe — returns (api_type, count, final_url)."""
    # CKAN (fast — rows=0)
    data, f = fetch_json(f"{url}/api/3/action/package_search?rows=0")
    if data and "result" in data:
        return "CKAN", data["result"]["count"], f or url
    
    # Socrata /api/views?limit=1 (fast probe)
    data, f = fetch_json(f"{url}/api/views?limit=1")
    if data and isinstance(data, list) and len(data) >= 1:
        # It's Socrata — get count
        s, c, f2 = fetch(f"{url}/api/views", timeout=20)
        if s == 200 and c and c.strip().startswith("["):
            try:
                views = json.loads(c)
                datasets = [v for v in views if isinstance(v, dict) and v.get("assetType") == "dataset"]
                return "Socrata", len(datasets), f2 or f or url
            except:
                pass
        return "Socrata", "?", f or url
    
    # ArcGIS Hub
    data, f = fetch_json(f"{url}/api/v3/search?q=*&rows=5")
    if data and "total" in data:
        return "ArcGIS-Hub", data["total"], f or url
    
    return None, 0, None

# All candidate URLs for all 50 states
# Try known patterns per state
ALL_CANDIDATES = {
    "AK": ["https://data.alaska.gov", "https://gis.data.alaska.gov"],
    "AL": ["https://data.alabama.gov"],
    "AR": ["https://data.arkansas.gov", "https://gis.arkansas.gov"],
    "AZ": ["https://data.az.gov", "https://phoenixopendata.com"],
    "CA": ["https://data.ca.gov"],
    "CO": ["https://data.colorado.gov"],
    "CT": ["https://data.ct.gov"],
    "DE": ["https://data.delaware.gov"],
    "FL": ["https://data.florida.gov", "https://www.data.fl.gov"],
    "GA": ["https://data.georgia.gov"],
    "HI": ["https://opendata.hawaii.gov", "https://data.hawaii.gov"],
    "IA": ["https://data.iowa.gov"],
    "ID": ["https://data.idaho.gov"],
    "IL": ["https://data.illinois.gov"],
    "IN": ["https://data.indiana.gov", "https://data.indy.gov"],
    "KS": ["https://data.kansas.gov"],
    "KY": ["https://data.ky.gov"],
    "LA": ["https://data.louisiana.gov"],
    "MA": ["https://data.boston.gov", "https://data.mass.gov"],
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
    "NC": ["https://data.ncdot.gov"],
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
    "WI": ["https://data-wisconsin.opendata.arcgis.com"],
    "WV": ["https://data.westvirginia.gov"],
    "WY": ["https://data.wyoming.gov"],
}

# Build all (state, url) pairs
all_pairs = []
for state, urls in ALL_CANDIDATES.items():
    for url in urls:
        all_pairs.append((state, url))

print(f"Testing {len(all_pairs)} candidate URLs in parallel...")

results = {}
with ThreadPoolExecutor(max_workers=20) as executor:
    future_to_state = {}
    for state, url in all_pairs:
        fut = executor.submit(probe, url)
        future_to_state[fut] = (state, url)
    
    for fut in as_completed(future_to_state, timeout=120):
        state, url = future_to_state[fut]
        try:
            api, count, final = fut.result()
            if api and state not in results:
                results[state] = (url, api, count)
        except:
            pass

# Print results
print("\n=== FINAL RESULTS (50 states) ===")
capitals = {"AK":"Juneau","AL":"Montgomery","AR":"Little Rock","AZ":"Phoenix",
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

found = 0
for state in sorted(ALL_CANDIDATES.keys()):
    capital = capitals.get(state, "?")
    if state in results:
        found += 1
        url, api, count = results[state]
        print(f"  {state:3s} | {capital:15s} | {api:12s} | {count} | {url}")
    else:
        print(f"  {state:3s} | {capital:15s} | NOT FOUND   |     |")

print(f"\n{len(results)}/50 states with APIs")
