#!/usr/bin/env python3
"""Scan data.gov + CKAN + Socrata + ArcGIS Hub for all 50 state capitals."""
import json, urllib.parse, urllib.request, ssl
from concurrent.futures import ThreadPoolExecutor, as_completed

ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

CAPITALS = [
    ("Alabama", "Montgomery", "al"),
    ("Alaska", "Juneau", "ak"),
    ("Arizona", "Phoenix", "az"),
    ("Arkansas", "Little Rock", "ar"),
    ("California", "Sacramento", "ca"),
    ("Colorado", "Denver", "co"),
    ("Connecticut", "Hartford", "ct"),
    ("Delaware", "Dover", "de"),
    ("Florida", "Tallahassee", "fl"),
    ("Georgia", "Atlanta", "ga"),
    ("Hawaii", "Honolulu", "hi"),
    ("Idaho", "Boise", "id"),
    ("Illinois", "Springfield", "il"),
    ("Indiana", "Indianapolis", "in"),
    ("Iowa", "Des Moines", "ia"),
    ("Kansas", "Topeka", "ks"),
    ("Kentucky", "Frankfort", "ky"),
    ("Louisiana", "Baton Rouge", "la"),
    ("Maine", "Augusta", "me"),
    ("Maryland", "Annapolis", "md"),
    ("Massachusetts", "Boston", "ma"),
    ("Michigan", "Lansing", "mi"),
    ("Minnesota", "Saint Paul", "mn"),
    ("Mississippi", "Jackson", "ms"),
    ("Missouri", "Jefferson City", "mo"),
    ("Montana", "Helena", "mt"),
    ("Nebraska", "Lincoln", "ne"),
    ("Nevada", "Carson City", "nv"),
    ("New Hampshire", "Concord", "nh"),
    ("New Jersey", "Trenton", "nj"),
    ("New Mexico", "Santa Fe", "nm"),
    ("New York", "Albany", "ny"),
    ("North Carolina", "Raleigh", "nc"),
    ("North Dakota", "Bismarck", "nd"),
    ("Ohio", "Columbus", "oh"),
    ("Oklahoma", "Oklahoma City", "ok"),
    ("Oregon", "Salem", "or"),
    ("Pennsylvania", "Harrisburg", "pa"),
    ("Rhode Island", "Providence", "ri"),
    ("South Carolina", "Columbia", "sc"),
    ("South Dakota", "Pierre", "sd"),
    ("Tennessee", "Nashville", "tn"),
    ("Texas", "Austin", "tx"),
    ("Utah", "Salt Lake City", "ut"),
    ("Vermont", "Montpelier", "vt"),
    ("Virginia", "Richmond", "va"),
    ("Washington", "Olympia", "wa"),
    ("West Virginia", "Charleston", "wv"),
    ("Wisconsin", "Madison", "wi"),
    ("Wyoming", "Cheyenne", "wy"),
]

def fetch(url, timeout=20):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Hermes-Scan/1.0"})
        resp = urllib.request.urlopen(req, timeout=timeout, context=ssl_ctx)
        return 200, resp.read().decode("utf-8", errors="replace")
    except:
        return 0, None

def try_data_gov(capital, state_short):
    """Search data.gov for datasets matching the capital."""
    q = urllib.parse.quote(capital + " " + state_short)
    url = f"https://catalog.data.gov/api/3/action/package_search?q={q}&rows=0"
    s, c = fetch(url)
    if s == 200 and c and '"result"' in c:
        try:
            data = json.loads(c)
            count = data["result"]["count"]
            if count > 0:
                # Also try to find the organization
                url2 = f"https://catalog.data.gov/api/3/action/package_search?q={q}&rows=5&facet=organization"
                s2, c2 = fetch(url2)
                org = None
                if s2 == 200 and c2:
                    try:
                        data2 = json.loads(c2)
                        orgs = data2["result"].get("facets", {}).get("organization", {})
                        if orgs:
                            org = list(orgs.keys())[0]
                    except:
                        pass
                return {"api": "data.gov CKAN", "count": count, "org": org, "url": "https://catalog.data.gov"}
        except:
            pass
    return None

def try_socrata(capital):
    """Try Socrata catalog API for common city domains."""
    domains = [
        f"data.{capital.lower().replace(' ', '')}.gov",
        f"data.{capital.lower()}.gov",
    ]
    # Common Socrata domain mappings
    socrata_map = {
        "oklahoma city": "data.okc.gov",
        "salt lake city": "data.slc.gov",
        "saint paul": "data.spjimmy.org",
        "new york": "data.cityofnewyork.us",
        "los angeles": "data.lacounty.gov",
    }
    
    if capital.lower() in socrata_map:
        domains.insert(0, socrata_map[capital.lower()])
    
    for domain in domains:
        url = f"https://{domain}/api/catalog/search?q=&offset=0&limit=5"
        s, c = fetch(url)
        if s == 200 and c and '"results"' in c:
            try:
                data = json.loads(c)
                total = data["result"].get("total", 0)
                if total > 0:
                    return {"api": "Socrata", "count": total, "url": f"https://{domain}"}
            except:
                pass
    return None

def scan_capital(state_name, capital, state_short):
    result = {
        "state": state_name[:3],
        "capital": capital,
        "api_type": None,
        "dataset_count": 0,
        "org": None,
        "url": None,
    }
    
    # 1. data.gov
    dg = try_data_gov(capital, state_short)
    if dg:
        result["api_type"] = dg["api"]
        result["dataset_count"] = dg["count"]
        result["org"] = dg.get("org")
        result["url"] = dg["url"]
    
    # 2. Socrata (if data.gov didn't find enough)
    if not result["api_type"]:
        sc = try_socrata(capital)
        if sc:
            result["api_type"] = sc["api"]
            result["dataset_count"] = sc["count"]
            result["url"] = sc["url"]
    
    return result

results = []
with ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(scan_capital, *c) for c in CAPITALS]
    for f in as_completed(futures):
        results.append(f.result())

print("=== CAPITAL SCAN: data.gov + Socrata ===")
found = 0
for r in sorted(results, key=lambda x: x["state"]):
    if r["api_type"]:
        found += 1
        print(f"{r['state']} | {r['capital']:15s} | {r['api_type']:18s} | {r['dataset_count']} datasets | {r['url']}")
    else:
        print(f"{r['state']} | {r['capital']:15s} | — NOT FOUND")

print(f"\nTotal: {len(results)} capitals | {found} found APIs")
