import json, os, glob

BASE = "/opt/data/civic-data-explainers"
cities = ["okc", "memphis", "lisbon", "missouri", "tennessee", "acog"]

def find_manifest(city):
    for p in [
        f"{BASE}/hugo-site/static/{city}/manifest.json",
        f"{BASE}/public/{city}/manifest.json",
    ]:
        if os.path.exists(p):
            return p
    return None

print("=== MANIFEST / CONTENT AUDIT ===")
for city in cities:
    mpath = find_manifest(city)
    content_dir = f"{BASE}/hugo-site/content/{city}"
    n_content = 0
    if os.path.isdir(content_dir):
        n_content = len([f for f in os.listdir(content_dir) if f.endswith(".md")])
    if not mpath:
        print(f"\n## {city}: NO manifest found (content pages={n_content})")
        continue
    m = json.load(open(mpath))
    ds = m.get("datasets", [])
    print(f"\n## {city}: manifest={mpath}")
    print(f"  datasets={len(ds)}  content_pages={n_content}")
    # distributions
    from collections import Counter
    img = Counter()
    inq = 0
    needs_review = 0
    schema_null = 0
    statuses = Counter()
    for d in ds:
        img[d.get("image_status","?")] += 1
        if d.get("inquiry_enabled"): inq += 1
        cs = d.get("content_status","?")
        statuses[cs] += 1
        if cs == "needs_review": needs_review += 1
        sch = d.get("schema")
        if sch is None: schema_null += 1
    print(f"  image_status={dict(img)}")
    print(f"  inquiry_enabled={inq}")
    print(f"  content_status={dict(statuses)}")
    print(f"  needs_review={needs_review}  schema_null={schema_null}")

# extras: newer cities present in static/content but not in the 6-list
print("\n=== OTHER CITIES PRESENT ===")
for d in sorted(os.listdir(f"{BASE}/hugo-site/content")):
    if d in cities: continue
    if os.path.isdir(f"{BASE}/hugo-site/content/{d}"):
        n = len([f for f in os.listdir(f"{BASE}/hugo-site/content/{d}") if f.endswith(".md")])
        mp = f"{BASE}/hugo-site/static/{d}/manifest.json"
        has_m = os.path.exists(mp)
        mlen = len(json.load(open(mp)).get("datasets",[])) if has_m else 0
        print(f"  {d}: content_pages={n} manifest={'yes('+str(mlen)+')' if has_m else 'no'}")
