#!/usr/bin/env python3
"""Bulk scan all 50 state data portals for API type + dataset counts.

Tests each state's data portal URL for:
1. Socrata Catalog API (/api/catalog/search)
2. Socrata Views API (/api/views)  
3. CKAN API (/api/3/action/package_search)
"""
import json, urllib.request, ssl
from concurrent.futures import ThreadPoolExecutor, as_completed

ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

# All 50 states + DC with their known data portal URLs
# Sources: official state data portals, web research
STATES = [
    ("al", "Alabama", "Montgomery", "https://data.alabama.gov"),
    ("ak", "Alaska", "Juneau", "https://data.alaska.gov"),
    ("az", "Arizona", "Phoenix", "https://data.az.gov"),
    ("ar", "Arkansas", "Little Rock", "https://data.arkansas.gov"),
    ("ca", "California", "Sacramento", "https://data.ca.gov"),
    ("co", "Colorado", "Denver", "https://data.colorado.gov"),
    ("ct", "Connecticut", "Hartford", "https://data.ct.gov"),
    ("de", "Delaware", "Dover", "https://data.delaware.gov"),
    ("fl", "Florida", "Tallahassee", "https://www.data.fl.gov"),
    ("ga", "Georgia", "Atlanta", "https://data.georgia.gov"),
    ("hi", "Hawaii", "Honolulu", "https://data.hawaii.gov"),
    ("id", "Idaho", "Boise", "https://data.idaho.gov"),
    ("il", "Illinois", "Springfield", "https://data.illinois.gov"),
    ("in", "Indiana", "Indianapolis", "https://data.indiana.gov"),
    ("ia", "Iowa", "Des Moines", "https://data.iowa.gov"),
    ("ks", "Kansas", "Topeka", "https://data.kansas.gov"),
    ("ky", "Kentucky", "Frankfort", "https://data.ky.gov"),
    ("la", "Louisiana", "Baton Rouge", "https://data.louisiana.gov"),
    ("me", "Maine", "Augusta", "https://data.maine.gov"),
    ("md", "Maryland", "Annapolis", "https://data.maryland.gov"),
    ("ma", "Massachusetts", "Boston", "https://data.mass.gov"),
    ("mi", "Michigan", "Lansing", "https://www.michigan.gov/midata"),
    ("mn", "Minnesota", "Saint Paul", "https://mn.gov/governor-support-service/data"),
    ("ms", "Mississippi", "Jackson", "https://data.mississippi.gov"),
    ("mo", "Missouri", "Jefferson City", "https://data.mo.gov"),
    ("mt", "Montana", "Helena", "https://data.montana.gov"),
    ("ne", "Nebraska", "Lincoln", "https://data.nebraska.gov"),
    ("nv", "Nevada", "Carson City", "https://data.nv.gov"),
    ("nh", "New Hampshire", "Concord", "https://www.nh.gov/data"),
    ("nj", "New Jersey", "Trenton", "https://data.nj.gov"),
    ("nm", "New Mexico", "Santa Fe", "https://data.nm.gov"),
    ("ny", "New York", "Albany", "https://data.ny.gov"),
    ("nc", "North Carolina", "Raleigh", "https://data.ncdot.gov"),
    ("nd", "North Dakota", "Bismarck", "https://data.nd.gov"),
    ("oh", "Ohio", "Columbus", "https://data.ohio.gov"),
    ("ok", "Oklahoma", "Oklahoma City", "https://data.ok.gov"),
    ("or", "Oregon", "Salem", "https://data.oregon.gov"),
    ("pa", "Pennsylvania", "Harrisburg", "https://data.pa.gov"),
    ("ri", "Rhode Island", "Providence", "https://data.ri.gov"),
    ("sc", "South Carolina", "Columbia", "https://data.sc.gov"),
    ("sd", "South Dakota", "Pierre", "https://dss.sd.gov"),
    ("tn", "Tennessee", "Nashville", "https://data.tn.gov"),
    ("tx", "Texas", "Austin", "https://data.texas.gov"),
    ("ut", "Utah", "Salt Lake City", "https://data.utah.gov"),
    ("vt", "Vermont", "Montpelier", "https://data.vermont.gov"),
    ("va", "Virginia", "Richmond", "https://data.vacommons.org"),
    ("wa", "Washington", "Olympia", "https://data.wa.gov"),
    ("wv", "West Virginia", "Charleston", "https://data.westvirginia.gov"),
    ("wi", "Wisconsin", "Madison", "https://data-wisconsin.opendata.arcgis.com"),
    ("wy", "Wyoming", "Cheyenne", "https://data.wyoming.gov"),
]

def fetch(url, timeout=15):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Hermes-Scan/1.0", "Accept": "application/json"})
        resp = urllib.request.urlopen(req, timeout=timeout, context=ssl_ctx)
        return resp.status, resp.read().decode("utf-8", errors="replace")
    except:
        return 0, None

def scan_state(short, name, capital, url):
    result = {
        "short": short,
        "state": name[:2],
        "capital": capital,
        "api_type": None,
        "dataset_count": 0,
        "url": url,
        "api_url": None,
    }
    
    # 1. Try Socrata /api/catalog/search
    s, c = fetch(f"{url}/api/catalog/search?q=&offset=0&limit=5")
    if s == 200 and c:
        try:
            data = json.loads(c)
            total = data.get("result", {}).get("total", 0)
            if "results" in data or total > 0:
                result["api_type"] = "Socrata"
                result["dataset_count"] = total
                result["api_url"] = f"{url}/api/catalog/search"
                return result
        except:
            pass
    
    # 2. Try CKAN /api/3/action/package_search
    s, c = fetch(f"{url}/api/3/action/package_search?rows=0")
    if s == 200 and c and '"result"' in c:
        try:
            data = json.loads(c)
            if "result" in data:
                result["api_type"] = "CKAN"
                result["dataset_count"] = data["result"].get("count", 0)
                result["api_url"] = f"{url}/api/3/action/package_search"
                return result
        except:
            pass
    
    # 3. Try Socrata /api/views
    s, c = fetch(f"{url}/api/views")
    if s == 200 and c and c.startswith("["):
        try:
            views = json.loads(c)
            if isinstance(views, list):
                result["api_type"] = "Socrata (views)"
                result["dataset_count"] = len(views)
                result["api_url"] = f"{url}/api/views"
                return result
        except:
            pass
    
    return result

results = []
with ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(scan_state, *s) for s in STATES]
    for f in as_completed(futures):
        results.append(f.result())

print("=== ALL 50 STATE DATA PORTALS ===")
found = 0
for r in sorted(results, key=lambda x: x["short"]):
    if r["api_type"]:
        found += 1
        count = f", {r['dataset_count']} datasets" if r['dataset_count'] else ""
        print(f"  {r['short'].upper():3s} | {r['capital']:15s} | {r['api_type']:20s} | {r['dataset_count']} datasets | {r['api_url']}")
    else:
        print(f"  {r['short'].upper():3s} | {r['capital']:15s} | — NOT FOUND | {r['url']}")

print(f"\nTotal: {len(results)} states | {found} APIs found")
