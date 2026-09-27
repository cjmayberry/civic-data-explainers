#!/usr/bin/env python3
"""Final scan: find data portal URLs via web_search + verify API accessibility.

For each state, searches the web for its official open data portal,
then tests CKAN/Socrata/ArcGIS API endpoints.
"""
import json, urllib.request, ssl
from hermes_tools import web_search

ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

def fetch(url, timeout=15):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        resp = urllib.request.urlopen(req, timeout=timeout, context=ssl_ctx)
        return resp.status, resp.read().decode("utf-8", errors="replace")[:5000], resp.url
    except:
        return 0, None, None

def probe_api(url):
    """Test a URL for CKAN, Socrata, or ArcGIS APIs."""
    # CKAN
    s, c, _ = fetch(f"{url}/api/3/action/package_search?rows=0")
    if s == 200 and c and '"result"' in c:
        try:
            data = json.loads(c)
            return "CKAN", data["result"]["count"]
        except:
            pass
    
    # Socrata /api/views
    s, c, _ = fetch(f"{url}/api/views")
    if s == 200 and c and c.strip().startswith("["):
        try:
            views = json.loads(c)
            datasets = [v for v in views if isinstance(v, dict) and v.get("assetType") == "dataset"]
            return "Socrata", len(datasets)
        except:
            pass
    
    # Socrata catalog
    s, c, _ = fetch(f"{url}/api/catalog/search?q=&limit=0")
    if s == 200 and c and '"total"' in c:
        try:
            data = json.loads(c)
            return "Socrata", data.get("result", {}).get("total", 0)
        except:
            pass
    
    # ArcGIS Hub
    s, c, _ = fetch(f"{url}/api/v3/search?q=*&rows=5")
    if s == 200 and c and '"total"' in c:
        try:
            data = json.loads(c)
            return "ArcGIS", data.get("total", 0)
        except:
            pass
    
    return None, 0

# Already confirmed APIs:
# CKAN: CA, OK, VA
# Socrata: CO, CT, IL, MI, MO, NJ, NY, OR, PA, TX, VT, WA
# ArcGIS Hub: AK, AL, AZ, DE(was Socrata but down), WI
# Confirmed non-data: many states use state gov sites without data portals

# States to search for: all 50 minus confirmed 19
already_have = {"CA", "CO", "CT", "IL", "MA", "MI", "MO", "NJ", "NY", "OK", "OR", 
                "PA", "TX", "VA", "VT", "WA"}

states_to_search = [
    ("Alaska", "AK"), ("Arizona", "AZ"), ("Arkansas", "AR"),
    ("Delaware", "DE"), ("Florida", "FL"), ("Georgia", "GA"),
    ("Hawaii", "HI"), ("Iowa", "IA"), ("Idaho", "ID"),
    ("Indiana", "IN"), ("Kansas", "KS"), ("Kentucky", "KY"),
    ("Louisiana", "LA"), ("Maryland", "MD"), ("Maine", "ME"),
    ("Minnesota", "MN"), ("Mississippi", "MS"), ("Montana", "MT"),
    ("North Carolina", "NC"), ("North Dakota", "ND"), ("Nebraska", "NE"),
    ("New Hampshire", "NH"), ("New Mexico", "NM"), ("Nevada", "NV"),
    ("Ohio", "OH"), ("Rhode Island", "RI"), ("South Carolina", "SC"),
    ("South Dakota", "SD"), ("Tennessee", "TN"), ("Utah", "UT"),
    ("Wisconsin", "WI"), ("West Virginia", "WV"), ("Wyoming", "WY"),
    ("Alabama", "AL"), ("Arkansas", "AR"),
]

results = []
for state_name, state_short in states_to_search:
    if state_short in already_have:
        continue
    try:
        res = web_search(f"{state_name} official open data portal site:domain.gov OR data.gov", limit=3)
        urls = [r["url"] for r in res.get("data", {}).get("web", [])]
        for url in urls[:3]:
            api, count = probe_api(url)
            if api:
                results.append((state_short, state_name, url, api, count))
                print(f"  {state_short:3s} | {state_name:15s} | {api:12s} | {count:6d} | {url}")
                break
        else:
            results.append((state_short, state_name, None, None, 0))
            print(f"  {state_short:3s} | {state_name:15s} | NOT FOUND   |      | searched {len(urls)} results")
    except Exception as e:
        results.append((state_short, state_name, None, None, 0))
        print(f"  {state_short:3s} | {state_name:15s} | ERROR       |      | {str(e)[:80]}")

print(f"\nTotal: {len(results)} states scanned")
found = sum(1 for r in results if r[3])
print(f"New APIs found: {found}")
