#!/usr/bin/env python3
"""Scan data.gov API for all 50 state capitals.

data.gov is CKAN-backed and aggregates datasets from every state and many cities.
The API supports facet filters by organization — perfect for finding which capitals
publish open data here.
"""
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

def fetch(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Hermes-Scan/1.0"})
        resp = urllib.request.urlopen(req, timeout=20, context=ssl_ctx)
        return 200, resp.read().decode("utf-8", errors="replace")
    except Exception as e:
        return 0, str(e)

def scan_capital(state_name, capital, state_short):
    """Search data.gov for datasets from this capital's org."""
    # Try: capital city name
    q = urllib.parse.quote(capital)
    url = f"https://catalog.data.gov/api/3/action/package_search?q={q}&fq=&rows=0&facet=...[truncated]