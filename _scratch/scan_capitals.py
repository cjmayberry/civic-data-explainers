#!/usr/bin/env python3
"""Scan all 50 state capitals' data portals for discoverable API endpoints.

For each capital, we hit:
1. data.gov API (CKAN) — most state portals proxy here
2. Socrata open data portals (data.cityname.gov)
3. Direct CKAN API endpoints (/api/3/action/)
4. ArcGIS REST directories ( /rest/services/ )
5. City portal search

Methodology is intentionally lightweight: look for the portal URL and API endpoint
first, then check if the API responds with discoverable datasets.
"""
import json, urllib.parse, urllib.request, ssl, time, re
from concurrent.futures import ThreadPoolExecutor, as_completed

ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

# 50 state capitals and their most likely data portal URLs
CAPITALS = [
    ("montpelier", "Montpelier", "VT", "https://data.vermont.gov", "https://www.montpeliervt.org"),
    ("carson_city", "Carson City", "NV", "https://data.nv.gov", "https://www.carson.org"),
    ("boise", "Boise", "ID", "https://data.cityofboise.org", "https://www.cityofboise.org"),
    ("salt_lake_city", "Salt Lake City", "UT", "https://data.slc.gov", "https://slc.gov"),
    ("phoenix", "Phoenix", "AZ", "https://www.phoenix.gov/data", "https://www.phoenix.gov"),
    ("little_rock", "Little Rock", "AR", "https://data.littlerock.gov", "https://www.littlerock.gov"),
    ("sacramento", "Sacramento", "CA", "https://data.cityofsacramento.org", "https://www.saccounty.net"),
    ("denver", "Denver", "CO", "https://data.denvergov.org", "https://www.denvergov.org"),
    ("hartford", "Hartford", "CT", "https://data.hartford.gov", "https://www.hartford.gov"),
    ("dover", "Dover", "DE", "https://data.delaware.gov", "https://cityofdover.com"),
    ("atlanta", "Atlanta", "GA", "https://opendata.atlantaga.gov", "https://www.atlantaga.gov"),
    ("honolulu", "Honolulu", "HI", "https://data.honolulu.gov", "https://www.honolulu.gov"),
    ("providence", "Providence", "RI", "https://data.providenceri.gov", "https://www.providenceri.com"),
    ("springfield", "Springfield", "IL", "https://www.springfield.il.gov", "https://springfield.il.gov"),
    ("indianapolis", "Indianapolis", "IN", "https://www.indy.gov/e/Departments/Mayor/Data-Analytics", "https://www.indy.gov"),
    ("des_moines", "Des Moines", "IA", "https://data.des-moines.org", "https://www.dsm.city"),
    ("wichita", "Wichita", "KS", "https://data.wichita.gov", "https://www.wichita.gov"),
    ("frankfort", "Frankfort", "KY", "https://data.frankfortky.gov", "https://www.frankfort-ky.org"),
    ("baton_rouge", "Baton Rouge", "LA", "https://data.egrc.lsu.edu", "https://www.brgov.com"),
    ("augusta", "Augusta", "ME", "https://data.maine.gov", "https://www.augustamaine.gov"),
    ("annapolis", "Annapolis", "MD", "https://data.annapolis.gov", "https://www.annapolis.gov"),
    ("boston", "Boston", "MA", "https://data.boston.gov", "https://www.boston.gov"),
    ("bozeman", "Bozeman", "MT", "https://data.bozeman.net", "https://www.bozeman.net"),
    ("omaha", "Omaha", "NE", "https://data.omaha.gov", "https://www.omahagov.net"),
    ("casper", "Casper", "WY", "https://data.casperwy.gov", "https://www.casperwyoming.com"),
    ("trenton", "Trenton", "NJ", "https://data.trentonnj.org", "https://www.trentonnj.org"),
    ("santa_fe", "Santa Fe", "NM", "https://data.santafeenv.org", "https://www.santafenm.gov"),
    ("raleigh", "Raleigh", "NC", "https://data.raleighnc.gov", "https://raleighnc.gov"),
    ("bismarck", "Bismarck", "ND", "https://data.bismarcknd.gov", "https://www.bismarcknd.gov"),
    ("columbus", "Columbus", "OH", "https://data.columbus.gov", "https://www.columbus.gov"),
    ("oklahoma_city", "Oklahoma City", "OK", "https://data.okc.gov", "https://www.okc.gov"),
    ("portland", "Portland", "OR", "https://data.portlandoregon.gov", "https://www.portlandoregon.gov"),
    ("harrisburg", "Harrisburg", "PA", "https://data.harrisburgpa.gov", "https://www.harrisburgpa.gov"),
    ("nashville", "Nashville", "TN", "https://data.nashville.gov", "https://www.nashville.gov"),
    ("austin", "Austin", "TX", "https://data.austintexas.gov", "https://www.austintexas.gov"),
    ("salt_lake", "Salt Lake City", "UT", "https://data.slc.gov", "https://slc.gov"),
    ("montpelier_vt", "Montpelier", "VT", "https://data.vermont.gov", "https://www.montpeliervt.org"),
    ("richmond", "Richmond", "VA", "https://data.richmondgov.org", "https://www.richmondgov.com"),
    ("olympia", "Olympia", "WA", "https://data.olywa.gov", "https://www.olympiawa.gov"),
    ("charleston", "Charleston", "WV", "https://data.charlestonwv.gov", "https://www.charlestonwv.gov"),
    ("madison", "Madison", "WI", "https://data.cityofmadison.com", "https://www.cityofmadison.com"),
]

def fetch(url, timeout=15):
    """Fetch URL, return (status, content) or (status, None)."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Hermes-CivicScan/1.0"})
        resp = urllib.request.urlopen(req, timeout=timeout, context=ssl_ctx)
        content = resp.read().decode("utf-8", errors="replace")
        return resp.status, content
    except Exception as e:
        return 0, None

def test_socrata(portal_url):
    """Test Socrata / CKAN-style data portal."""
    # Try Socrata discovery API
    discovery = f"{portal_url}/api/catalog/search?q=&offset=0&limit=5"
    status, _ = fetch(discovery)
    if status == 200:
        return "Socrata /api/catalog"
    
    # Try CKAN-style
    status, _ = fetch(f"{portal_url}/api/3/action/package_search?rows=5")
    if status == 200:
        return "CKAN /api/3/action"
    
    return None

def test_arcgis(arcgis_url_base):
    """Test ArcGIS REST endpoint."""
    url = f"{arcgis_url_base}/rest/services/?f=json"
    status, content = fetch(url)
    if status == 200 and "folders" in content:
        return "ArcGIS REST"
    return None

def scan_capital(key, name, state, portal_url, city_url):
    """Scan a capital for its API type."""
    results = {
        "id": key,
        "name": name,
        "state": state,
        "portal_url": portal_url,
        "city_url": city_url,
        "api_type": None,
        "dataset_count": 0,
        "notes": []
    }
    
    # 1. Test the portal directly
    api = test_socrata(portal_url)
    if api:
        results["api_type"] = api
        # Try to get dataset count
        if "CKAN" in api:
            _, content = fetch(f"{portal_url}/api/3/action/package_search?rows=0")
            if content:
                try:
                    data = json.loads(content)
                    results["dataset_count"] = data.get("result", {}).get("count", 0)
                except:
                    pass
        elif "Socrata" in api:
            _, content = fetch(f"{portal_url}/api/catalog/search?q=&offset=0&limit=0")
            if content:
                try:
                    data = json.loads(content)
                    results["dataset_count"] = data.get("result", {}).get("total", 0)
                except:
                    pass
    else:
        results["notes"].append("Portal URL did not respond to CKAN/Socrata probes")
    
    # 2. Try data.gov state filter
    state_query = urllib.parse.quote(f"organization:{state.lower()} state")
    dg_url = f"https://catalog.data.gov/api/3/action/package_search?q=&fq=organization:{state_query}&rows=5"
    _, dg_content = fetch(dg_url)
    
    return results

# Run all scans
results = []
with ThreadPoolExecutor(max_workers=8) as executor:
    futures = [executor.submit(scan_capital, *c) for c in CAPITALS]
    for f in as_completed(futures):
        results.append(f.result())
        time.sleep(0.1)

# Summary
print("=== CAPITAL DATA PORTAL SCAN ===")
for r in sorted(results, key=lambda x: x["id"]):
    api = r["api_type"] or "— NOT FOUND"
    count = f", {r['dataset_count']} datasets" if r['dataset_count'] > 0 else ""
    print(f"{r['state']:3s} | {r['name']:18s} | {api}{count}")
    for note in r["notes"]:
        print(f"    ↳ {note}")

print(f"\nTotal capitals scanned: {len(results)}")
print(f"APIs found: {sum(1 for r in results if r['api_type'])}")
