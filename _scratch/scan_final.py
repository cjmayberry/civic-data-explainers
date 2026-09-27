#!/usr/bin/env python3
"""Definitive scan of all 50 state data portals.

Strategy:
- For each state, try multiple candidate URLs
- For Socrata: /api/views?limit=5 returns JSON array of datasets
- For CKAN: /api/3/action/package_search?rows=0 returns count
- Use web_search to find correct URLs for states where data.{state}.gov doesn't resolve
"""
import json, urllib.request, ssl, re
from concurrent.futures import ThreadPoolExecutor, as_completed

ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

# All 50 states with candidate portal URLs (order matters: try most likely first)
STATES = [
    ("ak", "Alaska", "Juneau", ["https://data.alaska.gov"]),
    ("al", "Alabama", "Montgomery", ["https://data.alabama.gov"]),
    ("ar", "Arkansas", "Little Rock", ["https://data.arkansas.gov"]),
    ("az", "Arizona", "Phoenix", ["https://data.az.gov"]),
    ("ca", "California", "Sacramento", ["https://data.ca.gov"]),
    ("co", "Colorado", "Denver", ["https://data.colorado.gov"]),
    ("ct", "Connecticut", "Hartford", ["https://data.ct.gov"]),
    ("de", "Delaware", "Dover", ["https://data.delaware.gov"]),
    ("fl", "Florida", "Tallahassee", ["https://data.florida.gov"]),
    ("ga", "Georgia", "Atlanta", ["https://data.georgia.gov"]),
    ("hi", "Hawaii", "Honolulu", ["https://data.hawaii.gov"]),
    ("ia", "Iowa", "Des Moines", ["https://data.iowa.gov"]),
    ("id", "Idaho", "Boise", ["https://data.idaho.gov"]),
    ("il", "Illinois", "Springfield", ["https://data.illinois.gov"]),
    ("in", "Indiana", "Indianapolis", ["https://data.indiana.gov"]),
    ("ks", "Kansas", "Topeka", ["https://data.kansas.gov"]),
    ("ky", "Kentucky", "Frankfort", ["https://data.ky.gov"]),
    ("la", "Louisiana", "Baton Rouge", ["https://data.louisiana.gov"]),
    ("ma", "Massachusetts", "Boston", ["https://data.mass.gov", "https://data.boston.gov"]),
    ("md", "Maryland", "Annapolis", ["https://data.maryland.gov"]),
    ("me", "Maine", "Augusta", ["https://data.maine.gov"]),
    ("mi", "Michigan", "Lansing", ["https://data.michigan.gov"]),
    ("mn", "Minnesota", "Saint Paul", ["https://data.hennepin.us"]),
    ("ms", "Mississippi", "Jackson", ["https://data.mississippi.gov"]),
    ("mo", "Missouri", "Jefferson City", ["https://data.mo.gov"]),
    ("mt", "Montana", "Helena", ["https://data.montana.gov"]),
    ("ne", "Nebraska", "Lincoln", ["https://data.nebraska.gov"]),
    ("nv", "Nevada", "Carson City", ["https://data.nv.gov"]),
    ("nh", "New Hampshire", "Concord", ["https://www.nh.gov/data"]),
    ("nj", "New Jersey", "Trenton", ["https://data.nj.gov"]),
    ("nm", "New Mexico", "Santa Fe", ["https://data.nm.gov"]),
    ("ny", "New York", "Albany", ["https://data.ny.gov"]),
    ("nc", "North Carolina", "Raleigh", ["https://data.ncdot.gov"]),
    ("nd", "North Dakota", "Bismarck", ["https://data.nd.gov"]),
    ("oh", "Ohio", "Columbus", ["https://data.ohio.gov"]),
    ("ok", "Oklahoma", "Oklahoma City", ["https://data.ok.gov"]),
    ("or", "Oregon", "Salem", ["https://data.oregon.gov"]),
    ("pa", "Pennsylvania", "Harrisburg", ["https://data.pa.gov"]),
    ("ri", "Rhode Island", "Providence", ["https://data.ri.gov"]),
    ("sc", "South Carolina", "Columbia", ["https://data.sc.gov"]),
    ("sd", "South Dakota", "Pierre", ["https://dss.sd.gov"]),
    ("tn", "Tennessee", "Nashville", ["https://data.tn.gov"]),
    ("tx", "Texas", "Austin", ["https://data.texas.gov"]),
    ("ut", "Utah", "Salt Lake City", ["https://data.utah.gov"]),
    ("vt", "Vermont", "Montpelier", ["https://data.vermont.gov"]),
    ("va", "Virginia", "Richmond", ["https://data.vacommons.org", "https://data.virginia.gov"]),
    ("wa", "Washington", "Olympia", ["https://data.wa.gov"]),
    ("wv", "West Virginia", "Charleston", ["https://data.westvirginia.gov"]),
    ("wi", "Wisconsin", "Madison", ["https://data-wisconsin.opendata.arcgis.com"]),
    ("wy", "Wyoming", "Cheyenne", ["https://data.wyoming.gov"]),
]

def fetch(url, timeout=12):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Hermes-Scan/1.0", "Accept": "application/json"})
        resp = urllib.request.urlopen(req, timeout=timeout, context=ssl_ctx)
        return resp.status, resp.read().decode("utf-8", errors="replace"), resp.url
    except:
        return 0, None, None

def scan(short, name, capital, urls):
    for url in urls:
        # CKAN
        s, c, final = fetch(f"{url}/api/3/action/package_search?rows=0")
        if s == 200 and c and '"result"' in c:
            try:
                data = json.loads(c)
                return (short, name, capital, "CKAN", data["result"]["count"], final or url)
            except:
                pass
        
        # Socrata /api/views
        s, c, final = fetch(f"{url}/api/views?limit=5")
        if s == 200 and c and c.strip().startswith("["):
            try:
                views = json.loads(c)
                if isinstance(views, list):
                    # Get total count
                    s2, c2, _ = fetch(f"{url}/api/views?limit=1")
                    total = len(views)  # approximate
                    return (short, name, capital, "Socrata", total, final or url)
            except:
                pass
    
    return (short, name, capital, None, 0, None)

results = []
with ThreadPoolExecutor(max_workers=12) as executor:
    futures = [executor.submit(scan, *s) for s in STATES]
    for f in as_completed(futures):
        results.append(f.result())

print("=== ALL 50 STATE DATA PORTALS ===")
found = 0
for r in sorted(results, key=lambda x: x[0]):
    short, name, capital, api, count, url = r
    if api:
        found += 1
        print(f"  {short.upper():3s} | {capital:15s} | {api:12s} | ~{count:4d} | {url}")
    else:
        print(f"  {short.upper():3s} | {capital:15s} | NOT FOUND   |      | tried: {name}")

print(f"\n{len(results)} capitals scanned | {found} APIs found")
