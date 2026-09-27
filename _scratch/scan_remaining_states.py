#!/usr/bin/env python3
"""Scan remaining 38 states with redirect-following + alternative URL patterns."""
import json, urllib.request, ssl
from concurrent.futures import ThreadPoolExecutor, as_completed

ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

# The 38 states that didn't respond
STATES_TO_FIX = [
    ("ak", "Alaska", "Juneau", ["https://data.alaska.gov", "https://doas.alaska.gov", "https://dhss.alaska.gov"]),
    ("al", "Alabama", "Montgomery", ["https://data.alabama.gov", "https://data.aap.state.al.us"]),
    ("ar", "Arkansas", "Little Rock", ["https://data.arkansas.gov"]),
    ("az", "Arizona", "Phoenix", ["https://data.az.gov", "https://azgeo-open-data-agic.hub.arcgis.com"]),
    ("de", "Delaware", "Dover", ["https://data.delaware.gov", "https://delaware.gov"]),
    ("fl", "Florida", "Tallahassee", ["https://www.data.fl.gov", "https://data.florida.gov", "https://www.florida.gov/opendata"]),
    ("ga", "Georgia", "Atlanta", ["https://data.georgia.gov", "https://dataga.data.gov"]),
    ("hi", "Hawaii", "Honolulu", ["https://data.hawaii.gov", "https://planning.hawaii.gov"]),
    ("ia", "Iowa", "Des Moines", ["https://data.iowa.gov", "https://iowa.gov"]),
    ("id", "Idaho", "Boise", ["https://data.idaho.gov"]),
    ("in", "Indiana", "Indianapolis", ["https://data.indiana.gov", "https://www.in.gov/igov/data"]),
    ("ks", "Kansas", "Topeka", ["https://data.kansas.gov"]),
    ("ky", "Kentucky", "Frankfort", ["https://data.ky.gov", "https://www.ky.gov"]),
    ("la", "Louisiana", "Baton Rouge", ["https://data.louisiana.gov"]),
    ("ma", "Massachusetts", "Boston", ["https://data.mass.gov", "https://data.boston.gov"]),
    ("md", "Maryland", "Annapolis", ["https://data.maryland.gov", "https://maryland.maps.arcgis.com"]),
    ("me", "Maine", "Augusta", ["https://data.maine.gov", "https://www.maine.gov"]),
    ("mi", "Michigan", "Lansing", ["https://www.michigan.gov/midata", "https://data.michigan.gov"]),
    ("mn", "Minnesota", "Saint Paul", ["https://mn.gov/governor-support-service/data", "https://data.hennepin.us"]),
    ("ms", "Mississippi", "Jackson", ["https://data.mississippi.gov", "https://www.dor.ms.gov"]),
    ("mt", "Montana", "Helena", ["https://data.montana.gov"]),
    ("nc", "North Carolina", "Raleigh", ["https://data.ncdot.gov"]),
    ("nd", "North Dakota", "Bismarck", ["https://data.nd.gov", "https://www.nd.gov"]),
    ("ne", "Nebraska", "Lincoln", ["https://data.nebraska.gov"]),
    ("nh", "New Hampshire", "Concord", ["https://www.nh.gov/data", "https://data.nh.gov"]),
    ("nm", "New Mexico", "Santa Fe", ["https://data.nm.gov"]),
    ("nv", "Nevada", "Carson City", ["https://data.nv.gov"]),
    ("ny", "New York", "Albany", ["https://data.ny.gov"]),
    ("oh", "Ohio", "Columbus", ["https://data.ohio.gov"]),
    ("ri", "Rhode Island", "Providence", ["https://data.ri.gov"]),
    ("sc", "South Carolina", "Columbia", ["https://data.sc.gov"]),
    ("sd", "South Dakota", "Pierre", ["https://dss.sd.gov", "https://sddoh.sd.gov"]),
    ("tn", "Tennessee", "Nashville", ["https://data.tn.gov"]),
    ("ut", "Utah", "Salt Lake City", ["https://data.utah.gov"]),
    ("va", "Virginia", "Richmond", ["https://data.vacommons.org", "https://data.virginia.gov"]),
    ("wi", "Wisconsin", "Madison", ["https://data-wisconsin.opendata.arcgis.com"]),
    ("wv", "West Virginia", "Charleston", ["https://data.westvirginia.gov"]),
    ("wy", "Wyoming", "Cheyenne", ["https://data.wyoming.gov"]),
]

def fetch(url, timeout=12):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        resp = urllib.request.urlopen(req, timeout=timeout, context=ssl_ctx)
        return resp.status, resp.read().decode("utf-8", errors="replace"), resp.url
    except:
        return 0, None, None

def scan(short, name, capital, urls):
    result = {"short": short, "capital": capital, "api_type": None, "count": 0, "url_used": None}
    
    for url in urls:
        # Try CKAN
        s, c, final = fetch(f"{url}/api/3/action/package_search?rows=0")
        if s == 200 and c and '"result"' in c:
            try:
                data = json.loads(c)
                result["api_type"] = "CKAN"
                result["count"] = data["result"].get("count", 0)
                result["url_used"] = final or url
                return result
            except:
                pass
        
        # Try Socrata catalog
        s, c, final = fetch(f"{url}/api/catalog/search?q=&offset=0&limit=0")
        if s == 200 and c and '"total"' in c:
            try:
                data = json.loads(c)
                result["api_type"] = "Socrata"
                result["count"] = data.get("result", {}).get("total", 0)
                result["url_used"] = final or url
                return result
            except:
                pass
        
        # Try Socrata /api/views
        s, c, final = fetch(f"{url}/api/views")
        if s == 200 and c and c.startswith("["):
            try:
                views = json.loads(c)
                if isinstance(views, list):
                    result["api_type"] = "Socrata"
                    result["count"] = len(views)
                    result["url_used"] = final or url
                    return result
            except:
                pass
    
    return result

results = []
with ThreadPoolExecutor(max_workers=8) as executor:
    futures = [executor.submit(scan, *s) for s in STATES_TO_FIX]
    for f in as_completed(futures):
        results.append(f.result())

print("=== STATES WITH API FOUND ===")
found = 0
for r in sorted(results, key=lambda x: x["short"]):
    if r["api_type"]:
        found += 1
        print(f"  {r['short'].upper():3s} | {r['capital']:15s} | {r['api_type']:12s} | {r['count']:6d} | {r['url_used']}")
    else:
        print(f"  {r['short'].upper():3s} | {r['capital']:15s} | — NOT FOUND")

print(f"\n{len(results)} states scanned | {found} APIs found")
