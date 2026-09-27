#!/usr/bin/env python3
"""Find and verify all 50 state data portals via web search + API probe."""
import json, urllib.request, ssl, time
from hermes_tools import web_search
from concurrent.futures import ThreadPoolExecutor

ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

def fetch(url, timeout=20):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (X11)"})
        resp = urllib.request.urlopen(req, timeout=timeout, context=ssl_ctx)
        return resp.status, resp.read().decode("utf-8", errors="replace")[:50000]
    except:
        return 0, None

def fetch_json(url, timeout=20):
    s, c = fetch(url, timeout)
    if s == 200 and c:
        try:
            return json.loads(c)
        except:
            pass
    return None

def probe_api(url):
    """Probe for CKAN, Socrata, or ArcGIS Hub API."""
    # CKAN
    data = fetch_json(f"{url}/api/3/action/package_search?rows=0")
    if data and "result" in data:
        return "CKAN", data["result"]["count"]
    
    # Socrata /api/views?limit=1 (quick check)
    data = fetch_json(f"{url}/api/views?limit=1")
    if data and isinstance(data, list):
        return "Socrata", "?"
    
    # Socrata /api/views (no limit — works for small portals)
    data = fetch_json(f"{url}/api/views")
    if data and isinstance(data, list):
        datasets = [v for v in data if isinstance(v, dict) and v.get("assetType") == "dataset"]
        return "Socrata", len(datasets)
    
    return None, 0

# First, find the correct portal URLs for states we don't have yet
# Use web_search to find each state's data portal
states_without_api = [
    "Alaska", "Arizona", "Arkansas", "Delaware", "Florida", "Georgia",
    "Hawaii", "Iowa", "Idaho", "Indiana", "Kansas", "Kentucky", "Louisiana",
    "Maryland", "Maine", "Michigan", "Minnesota", "Mississippi", "Montana",
    "North Carolina", "North Dakota", "Nebraska", "New Hampshire", "New Mexico",
    "Nevada", "Ohio", "Rhode Island", "South Carolina", "South Dakota",
    "Tennessee", "Utah", "Wisconsin", "West Virginia", "Wyoming",
]

results = []
for state_name in states_without_api:
    try:
        res = web_search(f"{state_name} official open data portal", limit=3)
        for r in res.get("data", {}).get("web", []):
            url = r["url"]
            api, count = probe_api(url)
            if api:
                results.append((state_name, url, api, count))
                print(f"  {state_name:20s} | {api:12s} | {count} | {url}")
                break
        else:
            results.append((state_name, None, None, 0))
            print(f"  {state_name:20s} | NOT FOUND | | searched")
    except Exception as e:
        results.append((state_name, None, None, 0))
        print(f"  {state_name:20s} | ERROR     | {str(e)[:80]}")
    time.sleep(1)  # Rate limit

print(f"\n{len(results)} states scanned")
