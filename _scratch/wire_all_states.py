#!/usr/bin/env python3
"""Wire all 50 US states into cities.json. Skip already-present entries."""
import json

ROOT = "/opt/data/civic-data-explainers"
cities = json.load(open(f"{ROOT}/cities.json"))
existing = {c["id"] for c in cities}

# All 50 states: id, name, hub_url, gov_url, state_code
STATES = [
    ("alabama",       "Alabama",       "https://alabamagis.org/",          "https://www.alabama.gov",        "AL"),
    ("alaska",        "Alaska",        "https://ak.gov/",                  "https://www.alaska.gov",         "AK"),
    ("arizona",       "Arizona",       "https://azgeo.az.gov/",            "https://www.az.gov",             "AZ"),
    ("arkansas",      "Arkansas",      "https://gis.arkansas.gov/",        "https://www.arkansas.gov",       "AR"),
    ("california",    "California",    "https://data.ca.gov/",             "https://www.ca.gov",             "CA"),
    ("colorado",      "Colorado",      "https://coloradogis.org/",         "https://www.colorado.gov",       "CO"),
    ("connecticut",   "Connecticut",   "https://ct.gov/",                  "https://www.ct.gov",             "CT"),
    ("delaware",      "Delaware",      "https://de.gov/",                  "https://www.delaware.gov",       "DE"),
    ("florida",       "Florida",       "https://floridadisaster.org/gis/", "https://www.fl.gov",            "FL"),
    ("georgia",       "Georgia",       "https://georgiagis.org/",          "https://www.georgia.gov",        "GA"),
    ("hawaii",        "Hawaii",        "https://hawaii.gov/",              "https://www.hawaii.gov",         "HI"),
    ("idaho",         "Idaho",         "https://gis.idaho.gov/",           "https://www.idaho.gov",          "ID"),
    ("illinois",      "Illinois",      "https://gis.illinois.gov/",        "https://www.illinois.gov",       "IL"),
    ("indiana",       "Indiana",       "https://in.gov/gis/",              "https://www.in.gov",             "IN"),
    ("iowa",          "Iowa",          "https://iowamap.gov/",             "https://www.iowa.gov",           "IA"),
    ("kansas",        "Kansas",        "https://hub.kansasgis.org/",       "https://www.kansas.gov",         "KS"),
    ("kentucky",      "Kentucky",      "https://kygis.org/",               "https://www.kentucky.gov",       "KY"),
    ("louisiana",     "Louisiana",     "https://lagic.lsu.edu/",           "https://www.louisiana.gov",      "LA"),
    ("maine",         "Maine",         "https://maine.gov/",               "https://www.maine.gov",          "ME"),
    ("maryland",      "Maryland",      "https://geodata.md.gov/",          "https://www.maryland.gov",       "MD"),
    ("massachusetts", "Massachusetts", "https://mass.gov/",                "https://www.mass.gov",           "MA"),
    ("michigan",      "Michigan",      "https://gis-mi.com/",              "https://www.michigan.gov",       "MI"),
    ("minnesota",     "Minnesota",     "https://maps.dnr.state.mn.us/",    "https://www.mn.gov",             "MN"),
    ("mississippi",   "Mississippi",   "https://msgic.msstate.edu/",       "https://www.ms.gov",             "MS"),
    ("missouri",      "Missouri",      "https://data.mo.gov",              "https://www.mo.gov",             "MO"),
    ("montana",       "Montana",       "https://gis.mt.gov/",              "https://www.mt.gov",             "MT"),
    ("nebraska",      "Nebraska",      "https://www.nebraskamap.gov/",     "https://www.nebraska.gov",       "NE"),
    ("nevada",        "Nevada",        "https://geohub-ndot.hub.arcgis.com/", "https://ndot.nv.gov",         "NV"),
    ("newhampshire",  "New Hampshire","https://www.nh.gov/",               "https://www.nh.gov",             "NH"),
    ("newjersey",     "New Jersey",    "https://nj.gov/",                  "https://www.nj.gov",             "NJ"),
    ("newmexico",     "New Mexico",    "https://geodata.nm.gov/",          "https://www.newmexico.gov",      "NM"),
    ("newyork",       "New York",      "https://gis.ny.gov/",              "https://www.ny.gov",             "NY"),
    ("northcarolina", "North Carolina","https://ncdenr.org/",              "https://www.nc.gov",             "NC"),
    ("northdakota",   "North Dakota",  "https://www.nd.gov/",              "https://www.nd.gov",             "ND"),
    ("ohio",          "Ohio",          "https://gis.ohio.gov/",            "https://www.ohio.gov",           "OH"),
    ("oklahoma",      "Oklahoma",      "https://okgis.org/",               "https://www.ok.gov",             "OK"),
    ("oregon",        "Oregon",        "https://www.oregon.gov/",          "https://www.oregon.gov",         "OR"),
    ("pennsylvania",  "Pennsylvania",  "https://www.pa.gov/",              "https://www.pa.gov",             "PA"),
    ("rhodeisland",   "Rhode Island",  "https://ri.gov/",                  "https://www.ri.gov",             "RI"),
    ("southcarolina", "South Carolina","https://scgis.org/",               "https://www.sc.gov",             "SC"),
    ("southdakota",   "South Dakota",  "https://sd.gov/",                  "https://www.sd.gov",             "SD"),
    ("tennessee",     "Tennessee",     "https://geodata.tn.gov",           "https://www.tn.gov",             "TN"),
    ("texas",         "Texas",         "https://texas.gov/",               "https://www.texas.gov",          "TX"),
    ("utah",          "Utah",          "https://gis.utah.gov/",            "https://utah.gov",               "UT"),
    ("vermont",       "Vermont",       "https://vermont.gov/",             "https://www.vermont.gov",        "VT"),
    ("virginia",      "Virginia",      "https://www.virginia.gov/",        "https://www.virginia.gov",       "VA"),
    ("washington",    "Washington",    "https://wa.gov/",                  "https://www.wa.gov",             "WA"),
    ("westvirginia",  "West Virginia", "https://westvirginia.gov/",        "https://www.wv.gov",             "WV"),
    ("wisconsin",     "Wisconsin",     "https://wisconsin.gov/",           "https://www.wi.gov",             "WI"),
    ("wyoming",       "Wyoming",       "https://wyoming.gov/",             "https://www.wyoming.gov",        "WY"),
]

added = []
for cid, name, hub, gov, st in STATES:
    if cid in existing:
        continue
    cities.append({
        "id": cid,
        "name": name,
        "hub_url": hub,
        "gov_url": gov,
        "state": st,
        "active": True,
        "model": None,
        "min_score": 0,
        "content_dir": f"hugo-site/content/{cid}",
        "static_dir": f"hugo-site/static/{cid}",
        "category_map": {
            "boundaries": "Government",
            "transportation": "Transportation",
            "utilitiesCommunication": "Infrastructure",
            "environment": "Environment",
            "planningCadastre": "Government",
            "location": "Government",
            "farming": "Other",
            "inlandWaters": "Environment",
            "structure": "Infrastructure",
            "health": "Health",
            "biota": "Environment",
            "geoscientificInformation": "Environment",
            "society": "Other",
        },
    })
    added.append(cid)

json.dump(cities, open(f"{ROOT}/cities.json", "w"), indent=2)
print(f"Added {len(added)} states. Total cities.json entries: {len(cities)}")
print(f"Missing states (not wired): ", end="")
missing = [s[0] for s in STATES if s[0] not in {c['id'] for c in cities}]
print(missing if missing else "NONE")
