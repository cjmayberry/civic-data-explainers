#!/usr/bin/env python3
"""Scan all 50 state capitals' data portals with comprehensive URL patterns.

Most city portals are either:
1. Socrata cloud (data.cityname.gov) — but the actual domain varies
2. CKAN self-hosted (cityname.gov/data or data.cityname.gov)
3. ArcGIS Hub (hub.arcgis.com or cityname.maps.arcgis.com)
4. data.gov state-level catalog

We cast a wide net with known domain patterns for each capital.
"""
import json, urllib.parse, urllib.request, ssl, re
from concurrent.futures import ThreadPoolExecutor, as_completed

ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

CAPITALS = [
    {"id": "montpeliervt", "name": "Montpelier", "state": "VT", "state_short": "vt"},
    {"id": "carsoncitynv", "name": "Carson City", "state": "NV", "state_short": "nv"},
    {"id": "boisecity", "name": "Boise", "state": "ID", "state_short": "id"},
    {"id": "salt_lake_city", "name": "Salt Lake City", "state": "UT", "state_short": "ut"},
    {"id": "phoenixaz", "name": "Phoenix", "state": "AZ", "state_short": "az"},
    {"id": "littlerockar", "name": "Little Rock", "state": "AR", "state_short": "ar"},
    {"id": "saccounty", "name": "Sacramento", "state": "CA", "state_short": "ca"},
    {"id": "denverco", "name": "Denver", "state": "CO", "state_short": "co"},
    {"id": "hartfordct", "name": "Hartford", "state": "CT", "state_short": "ct"},
    {"id": "doverde", "name": "Dover", "state": "DE", "state_short": "de"},
    {"id": "atlantaga", "name": "Atlanta", "state": "GA", "state_short": "ga"},
    {"id": "honoluluhi", "name": "Honolulu", "state": "HI", "state_short": "hi"},
    {"id": "providence", "name": "Providence", "state": "RI", "state_short": "ri"},
    {"id": "springfieldil", "name": "Springfield", "state": "IL", "state_short": "il"},
    {"id": "indianapolis", "name": "Indianapolis", "state": "IN", "state_short": "in"},
    {"id": "deshielles", "name": "Des Moines", "state": "IA", "state_short": "ia"},
    {"id": "wichita", "name": "Wichita", "state": "KS", "state_short": "ks"},
    {"id": "frankfortky", "name": "Frankfort", "state": "KY", "state_short": "ky"},
    {"id": "batonrouge", "name": "Baton Rouge", "state": "LA", "state_short": "la"},
    {"id": "augustame", "name": "Augusta", "state": "ME", "state_short": "me"},
    {"id": "annapolismd", "name": "Annapolis", "state": "MD", "state_short": "md"},
    {"id": "bostonma", "name": "Boston", "state": "MA", "state_short": "ma"},
    {"id": "bozemanmt", "name": "Bozeman", "state": "MT", "state_short": "mt"},
    {"id": "omaha", "name": "Omaha", "state": "NE", "state_short": "ne"},
    {"id": "casperwy", "name": "Casper", "state": "WY", "state_short": "wy"},
    {"id": "trentonnj", "name": "Trenton", "state": "NJ", "state_short": "nj"},
    {"id": "santafe", "name": "Santa Fe", "state": "NM", "state_short": "nm"},
    {"id": "raleigh", "name": "Raleigh", "state": "NC", "state_short": "nc"},
    {"id": "bismarcknd", "name": "Bismarck", "state": "ND", "state_short": "nd"},
    {"id": "columbusoh", "name": "Columbus", "state": "OH", "state_short": "oh"},
    {"id": "okc", "name": "Oklahoma City", "state": "OK", "state_short": "ok"},
    {"id": "portlandor", "name": "Portland", "state": "OR", "state_short": "or"},
    {"id": "harrisburgpa", "name": "Harrisburg", "state": "PA", "state_short": "pa"},
    {"id": "nashvilletn", "name": "Nashville", "state": "TN", "state_short": "tn"},
    {"id": "austintx", "name": "Austin", "state": "TX", "state_short": "tx"},
    {"id": "richmondva", "name": "Richmond", "state": "VA", "state_short": "va"},
    {"id": "olympiawa", "name": "Olympia", "state": "WA", "state_short": "wa"},
    {"id": "charlestonwv", "name": "Charleston", "state": "WV", "state_short": "wv"},
    {"id": "madisonwi", "name": "Madison", "state": "WI", "state_short": "wi"},
    {"id": "juneau", "name": "Juneau", "state": "AK", "state_short": "ak"},
    {"id": "carsoncty", "name": "Carson City", "state": "NV", "state_short": "nv"},
]

def fetch(url, timeout=10):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Hermes-Scan/1.0"})
        resp = urllib.request.urlopen(req, timeout=timeout, context=ssl_ctx)
        return resp.status, resp.read().decode("utf-8", errors="replace")
    except:
        return 0, None

def generate_patterns(cap):
    """Generate all possible data portal URLs for a capital."""
    name = cap["name"].lower().replace(" ", "")
    state_short = cap["state_short"]
    patterns = []
    
    # Socrata cloud
    patterns.append(f"https://data.{name}.gov")
    patterns.append(f"https://{name}.gov")
    patterns.append(f"https://data.{name}.com")
    
    # CKAN self-hosted
    patterns.append(f"https://data.{name}.gov")
    
    # data.gov state filter
    # (handled separately)
    
    # ArcGIS Hub
    patterns.append(f"https://hub.arcgis.com/search?q={urllib.parse.quote(cap['name'])}")
    patterns.append(f"https://{name}.maps.arcgis.com")
    
    # City .gov with /data
    city_domains = {
        "montpelier": "montpeliervt.org",
        "carson": "carson.org",
        "boise": "cityofboise.org",
        "salt_lake_city": "slc.gov",
        "phoenix": "phoenix.gov",
        "little_rock": "littlerock.gov",
        "sacramento": "saccounty.net",  # county hosts it
        "denver": "denvergov.org",
        "hartford": "hartford.gov",
        "dover": "cityofdover.com",
        "atlanta": "atlantaga.gov",
        "honolulu": "honolulu.gov",
        "providence": "providenceri.gov",
        "springfield": "springfield.il.gov",
        "indianapolis": "indy.gov",
        "des_moines": "dsm.city",
        "wichita": "wichita.gov",
        "frankfort": "frankfort-ky.org",
        "baton_rouge": "brgov.com",
        "augusta": "augustamaine.gov",
        "annapolis": "annapolis.gov",
        "boston": "boston.gov",
        "bozeman": "bozeman.net",
        "omaha": "omahagov.net",
        "casper": "casperwyoming.com",
        "trenton": "trentonnj.org",
        "santa_fe": "santafenm.gov",
        "raleigh": "raleighnc.gov",
        "bismarck": "bismarcknd.gov",
        "columbus": "columbus.gov",
        "oklahoma_city": "okc.gov",
        "portland": "portlandoregon.gov",
        "harrisburg": "harrisburgpa.gov",
        "nashville": "nashville.gov",
        "austin": "austintexas.gov",
        "richmond": "richmondgov.com",
        "olympia": "olympiawa.gov",
        "charleston": "charlestonwv.gov",
        "madison": "cityofmadison.com",
        "juneau": "juneau.org",
    }
    
    domain_key = name.replace("city", "").replace(" ", "")
    
    for city_domain in [city_domains.get(domain_key) or city_domains.get(name)]:
        if city_domain:
            patterns.append(f"https://data.{city_domain}")
            patterns.append(f"https://{city_domain}/data")
    
    return patterns

def scan_capital(cap):
    result = {
        "id": cap["id"],
        "name": cap["name"],
        "state": cap["state"],
        "api_type": None,
        "url": None,
        "dataset_count": 0,
    }
    
    patterns = generate_patterns(cap)
    
    for url in patterns:
        status, content = fetch(url)
        if status != 200:
            continue
            
        # CKAN check
        s, c = fetch(f"{url}/api/3/action/package_search?rows=5")
        if s == 200 and '"result"' in (c or ""):
            result["api_type"] = "CKAN"
            result["url"] = url
            try:
                data = json.loads(c)
                result["dataset_count"] = data["result"]["count"]
            except:
                pass
            return result
        
        # Socrata check
        s, c = fetch(f"{url}/api/catalog/search?q=&offset=0&limit=5")
        if s == 200 and '"results"' in (c or ""):
            result["api_type"] = "Socrata"
            result["url"] = url
            try:
                data = json.loads(c)
                result["dataset_count"] = data.get("result", {}).get("total", 0)
            except:
                pass
            return result
    
    # Fall back to data.gov
    s, c = fetch(f"https://catalog.data.gov/api/3/action/package_search?q=&fq=organization:{cap['state'].lower()}_state&rows=5")
    if s == 200 and '"result"' in (c or ""):
        result["api_type"] = "data.gov (CKAN proxy)"
        result["url"] = "https://catalog.data.gov"
        try:
            data = json.loads(c)
            result["dataset_count"] = data["result"]["count"]
        except:
            pass
        return result
    
    return result

results = []
with ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(scan_capital, c) for c in CAPITALS]
    for f in as_completed(futures):
        results.append(f.result())

print("=== CAPITAL DATA PORTAL SCAN (REFINED) ===")
found = 0
for r in sorted(results, key=lambda x: (x["state"], x["name"])):
    if r["api_type"]:
        found += 1
        count = f", {r['dataset_count']} datasets" if r['dataset_count'] else ""
        print(f"{r['state']:3s} | {r['name']:18s} | {r['api_type']:25s} | {r['url']}{count}")
    else:
        print(f"{r['state']:3s} | {r['name']:18s} | — NOT FOUND")

print(f"\nTotal: {len(results)} capitals | {found} API endpoints found")
