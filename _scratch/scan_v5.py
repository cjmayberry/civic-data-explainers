#!/usr/bin/env python3
"""Final comprehensive scan of all 50 state data portals.

Strategy: try the correct full domain for each state, then probe for
CKAN (/api/3/action/package_search) and Socrata (/api/views) APIs.
Many states use Socrata cloud (data.{domain}.gov) or CKAN.
"""
import json, urllib.request, ssl
from concurrent.futures import ThreadPoolExecutor, as_completed

ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

# Correct full URLs for all 50 state data portals
# Based on known patterns + earlier web research
PORTALS = [
    ("AK", "Juneau", ["https://data.alaska.gov", "https://gis.data.alaska.gov"]),
    ("AL", "Montgomery", ["https://data.alabama.gov"]),
    ("AR", "Little Rock", ["https://data.arkansas.gov", "https://gis.arkansas.gov"]),
    ("AZ", "Phoenix", ["https://data.az.gov", "https://phoenixopendata.com"]),
    ("CA", "Sacramento", ["https://data.ca.gov"]),
    ("CO", "Denver", ["https://data.colorado.gov"]),
    ("CT", "Hartford", ["https://data.ct.gov"]),
    ("DE", "Dover", ["https://data.delaware.gov"]),
    ("FL", "Tallahassee", ["https://data.florida.gov", "https://geodata.floridagio.gov"]),
    ("GA", "Atlanta", ["https://data.georgia.gov", "https://dataga.data.gov"]),
    ("HI", "Honolulu", ["https://opendata.hawaii.gov", "https://data.hawaii.gov"]),
    ("IA", "Des Moines", ["https://data.iowa.gov"]),
    ("ID", "Boise", ["https://data.idaho.gov", "https://data.citiesandcounties.org"]),
    ("IL", "Springfield", ["https://data.illinois.gov"]),
    ("IN", "Indianapolis", ["https://data.indy.gov"]),
    ("KS", "Topeka", ["https://data.kansas.gov"]),
    ("KY", "Frankfort", ["https://data.ky.gov"]),
    ("LA", "Baton Rouge", ["https://data.louisiana.gov"]),
    ("MA", "Boston", ["https://data.boston.gov", "https://data.mass.gov"]),
    ("MD", "Annapolis", ["https://data.maryland.gov"]),
    ("ME", "Augusta", ["https://data.maine.gov"]),
    ("MI", "Lansing", ["https://data.michigan.gov"]),
    ("MN", "Saint Paul", ["https://data.hennepin.us"]),
    ("MS", "Jackson", ["https://data.mississippi.gov"]),
    ("MO", "Jefferson City", ["https://data.mo.gov"]),
    ("MT", "Helena", ["https://data.montana.gov"]),
    ("NE", "Lincoln", ["https://data.nebraska.gov"]),
    ("NV", "Carson City", ["https://data.nv.gov"]),
    ("NH", "Concord", ["https://www.nh.gov/data", "https://data.nh.gov"]),
    ("NJ", "Trenton", ["https://data.nj.gov"]),
    ("NM", "Santa Fe", ["https://data.nm.gov"]),
    ("NY", "Albany", ["https://data.ny.gov"]),
    ("NC", "Raleigh", ["https://data.ncdot.gov", "https://data.raleighnc.gov"]),
    ("ND", "Bismarck", ["https://data.nd.gov"]),
    ("OH", "Columbus", ["https://data.ohio.gov"]),
    ("OK", "Oklahoma City", ["https://data.ok.gov"]),
    ("OR", "Salem", ["https://data.oregon.gov"]),
    ("PA", "Harrisburg", ["https://data.pa.gov"]),
    ("RI", "Providence", ["https://data.ri.gov"]),
    ("SC", "Columbia", ["https://data.sc.gov"]),
    ("SD", "Pierre", ["https://data.sd.gov", "https://dss.sd.gov"]),
    ("TN", "Nashville", ["https://data.tn.gov", "https://data.nashville.gov"]),
    ("TX", "Austin", ["https://data.texas.gov"]),
    ("UT", "Salt Lake City", ["https://data.slc.gov", "https://data.utah.gov"]),
    ("VT", "Montpelier", ["https://data.vermont.gov"]),
    ("VA", "Richmond", ["https://data.virginia.gov", "https://data.vacommons.org"]),
    ("WA", "Olympia", ["https://data.wa.gov"]),
    ("WI", "Madison", ["https://data-wisconsin.opendata.arcgis.com"]),
    ("WV", "Charleston", ["https://data.westvirginia.gov"]),
    ("WY", "Cheyenne", ["https://data.wyoming.gov"]),
]

def fetch(url, timeout=12):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        resp = urllib.request.urlopen(req, timeout=timeout, context=ssl_ctx)
        resp.read(100)  # consume
        return resp.status, resp.url
    except:
        return 0, None

def fetch_content(url, timeout=12):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        resp = urllib.request.urlopen(req, timeout=timeout, context=ssl_ctx)
        return resp.status, resp.read().decode("utf-8", errors="replace")[:5000], resp.url
    except:
        return 0, None, None

def probe(state, capital, urls):
    for url in urls:
        final = url
        # Try CKAN
        s, c, f = fetch_content(f"{url}/api/3/action/package_search?rows=0")
        if s == 200 and c and '"result"' in c:
            try:
                data = json.loads(c)
                return (state, capital, "CKAN", data["result"]["count"], f or url)
            except:
                pass
        
        # Try Socrata /api/views (returns JSON array)
        s, c, f = fetch_content(f"{url}/api/views")
        if s == 200 and c and c.strip().startswith("["):
            try:
                views = json.loads(c)
                if isinstance(views, list):
                    datasets = [v for v in views if isinstance(v, dict) and v.get("assetType") == "dataset"]
                    return (state, capital, "Socrata", len(datasets), f or url)
            except:
                pass
        
        # Try ArcGIS Hub /api/v3/search
        s, c, f = fetch_content(f"{url}/api/v3/search?q=*&rows=5")
        if s == 200 and c and '"total"' in c:
            try:
                data = json.loads(c)
                return (state, capital, "ArcGIS Hub", data.get("total", 0), f or url)
            except:
                pass
    
    return (state, capital, None, 0, None)

results = []
with ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(probe, *p) for p in PORTALS]
    for f in as_completed(futures):
        results.append(f.result())

print("=== ALL 50 STATES — API PROBE RESULTS ===")
found = 0
for state, capital, api, count, url in sorted(results):
    if api:
        found += 1
        print(f"  {state:3s} | {capital:15s} | {api:14s} | {count:6d} | {url}")
    else:
        print(f"  {state:3s} | {capital:15s} | NOT FOUND     |      | tried URLs")

print(f"\n{len(results)} states | {found} APIs found")
