#!/usr/bin/env python3
"""Search for portal URLs for the 32 states with no API found."""
import json, urllib.request, ssl
from hermes_tools import web_search
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

def fetch(url, timeout=15):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        resp = urllib.request.urlopen(req, timeout=timeout, context=ssl_ctx)
        return resp.status, resp.read().decode("utf-8", errors="replace")[:5000]
    except:
        return 0, None

def probe(url):
    """Try CKAN, Socrata, ArcGIS Hub."""
    # CKAN
    s, c = fetch(f"{url}/api/3/action/package_search?rows=0")
    if s == 200 and c and '"result"' in c:
        m = json.loads(c[:200]) if c else {}
        if "result" in c[:200]:
            import re
            count_m = re.search(r'"count"\s*:\s*(\d+)', c)
            if count_m:
                return "CKAN", int(count_m.group(1))
    
    # Socrata /api/search
    s, c = fetch(f"{url}/api/search?q=&rows=0")
    if s == 200 and c and '"count"' in c:
        import re
        m = re.search(r'"count"\s*:\s*(\d+)', c)
        if m:
            return "Socrata", int(m.group(1))
    
    # Socrata /api/views
    s, c = fetch(f"{url}/api/views?limit=1")
    if s == 200 and c and c.strip().startswith("["):
        return "Socrata", "?"
    
    # ArcGIS
    s, c = fetch(f"{url}/api/v3/search?q=*&rows=5")
    if s == 200 and c and '"total"' in c:
        import re
        m = re.search(r'"total"\s*:\s*(\d+)', c)
        if m:
            return "ArcGIS", int(m.group(1))
    
    return None, 0

missing_states = [
    "Alaska", "Alabama", "Arkansas", "Delaware", "Florida", "Georgia",
    "Iowa", "Idaho", "Indiana", "Kansas", "Kentucky", "Louisiana",
    "Maryland", "Maine", "Minnesota", "Mississippi", "Montana",
    "North Carolina", "North Dakota", "Nebraska", "New Hampshire",
    "New Mexico", "Nevada", "Ohio", "Rhode Island", "South Carolina",
    "South Dakota", "Tennessee", "Utah", "Wisconsin", "West Virginia", "Wyoming",
]

found = {}
for state in missing_states:
    try:
        res = web_search(f"{state} state government open data portal", limit=3)
        urls = [r["url"] for r in res.get("data", {}).get("web", [])]
        for url in urls[:3]:
            api, count = probe(url)
            if api:
                found[state] = (url, api, count)
                print(f"  {state[:6]:6s} | {api:12s} | {count} | {url}")
                break
        else:
            print(f"  {state[:6]:6s} | NOT FOUND | searched {len(urls)} URLs")
    except Exception as e:
        print(f"  {state[:6]:6s} | ERROR     | {str(e)[:60]}")
    time.sleep(0.5)

print(f"\n{len(found)}/{len(missing_states)} additional states found")
