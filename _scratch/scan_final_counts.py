#!/usr/bin/env python3
"""Get dataset counts for all 50 state portals using regex extraction."""
import json, re, urllib.request, ssl
from concurrent.futures import ThreadPoolExecutor, as_completed

ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

def fetch_url(url, timeout=25):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        resp = urllib.request.urlopen(req, timeout=timeout, context=ssl_ctx)
        return resp.status, resp.read().decode("utf-8", errors="replace")[:5000]
    except:
        return 0, None

def get_count(url):
    """Probe for API type + dataset count."""
    # Try CKAN first
    s, c = fetch_url(f"{url}/api/3/action/package_search?rows=0")
    if s == 200 and c and '"result"' in c:
        m = re.search(r'"count"\s*:\s*(\d+)', c)
        if m:
            return "CKAN", int(m.group(1))
    
    # Try Socrata /api/search (newer endpoint)
    s, c = fetch_url(f"{url}/api/search?q=&rows=0")
    if s == 200 and c:
        m = re.search(r'"count"\s*:\s*(\d+)', c)
        if m:
            return "Socrata", int(m.group(1))
    
    # Try Socrata /api/views (older endpoint, returns JSON array)
    s, c = fetch_url(f"{url}/api/views?limit=1")
    if s == 200 and c and c.strip().startswith("["):
        return "Socrata", "?"
    
    # Try ArcGIS Hub
    s, c = fetch_url(f"{url}/api/v3/search?q=*&rows=5")
    if s == 200 and c and '"total"' in c:
        m = re.search(r'"total"\s*:\s*(\d+)', c)
        if m:
            return "ArcGIS-Hub", int(m.group(1))
    
    return None, 0

# All confirmed + candidate URLs for 50 states
PORTALS = {
    "AK": ["https://gis.data.alaska.gov", "https://data.alaska.gov"],
    "AL": ["https://data-algeohub.opendata.arcgis.com", "https://data.alabama.gov"],
    "AR": ["https://data.arkansas.gov"],
    "AZ": ["https://phoenixopendata.com", "https://data.az.gov", "https://azgeo-open-data-agic.hub.arcgis.com"],
    "CA": ["https://data.ca.gov"],
    "CO": ["https://data.colorado.gov"],
    "CT": ["https://data.ct.gov"],
    "DE": ["https://data.delaware.gov", "https://de-firstmap-delaware.hub.arcgis.com"],
    "FL": ["https://data.florida.gov"],
    "GA": ["https://data.georgia.gov"],
    "HI": ["https://opendata.hawaii.gov"],
    "IA": ["https://data.iowa.gov"],
    "ID": ["https://data.idaho.gov", "https://data.citiesandcounties.org"],
    "IL": ["https://data.illinois.gov"],
    "IN": ["https://data.indiana.gov", "https://data.indy.gov"],
    "KS": ["https://data.kansas.gov"],
    "KY": ["https://data.ky.gov"],
    "LA": ["https://data.louisiana.gov"],
    "MA": ["https://data.boston.gov"],
    "MD": ["https://data.maryland.gov", "https://maryland.maps.arcgis.com"],
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
    "TN": ["https://data.tn.gov"],
    "TX": ["https://data.texas.gov"],
    "UT": ["https://data.slc.gov", "https://data.utah.gov"],
    "VT": ["https://data.vermont.gov"],
    "VA": ["https://data.virginia.gov"],
    "WA": ["https://data.wa.gov"],
    "WI": ["https://data-wisconsin.opendata.arcgis.com", "https://data.wisconsin.gov"],
    "WV": ["https://data.westvirginia.gov"],
    "WY": ["https://data.wyoming.gov"],
}

def scan_state(state, urls):
    for url in urls:
        api, count = get_count(url)
        if api:
            return (state, url, api, count)
    return (state, None, None, 0)

results = []
with ThreadPoolExecutor(max_workers=15) as executor:
    futures = {executor.submit(scan_state, s, us): s for s, us in PORTALS.items()}
    for fut in as_completed(futures, timeout=120):
        results.append(fut.result())

print("=== FINAL: ALL 50 STATE PORTAL SCAN ===")
found = 0
total_datasets = 0
for state, url, api, count in sorted(results):
    if api:
        found += 1
        if isinstance(count, int):
            total_datasets += count
        c = str(count)
    else:
        c = "-"
    print(f"  {state:3s} | {api or 'NOT FOUND':14s} | {c:>10} | {url or 'N/A'}")

print(f"\n{found}/50 states | {total_datasets} total datasets (CKAN+Socrata only)")
