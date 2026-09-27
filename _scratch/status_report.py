import os, json, glob

base = "/opt/data/civic-data-explainers"

def find_manifest(city):
    cands = [
        f"{base}/hugo-site/static/{city}/manifest.json",
        f"{base}/hugo-site/content/{city}/manifest.json",
        f"{base}/public/{city}/manifest.json",
    ]
    for c in cands:
        if os.path.exists(c):
            return c
    return None

cities = ["okc","memphis","lisbon","missouri","tennessee","acog"]
print("=== MANIFEST LOCATIONS ===")
for city in cities:
    print(city, find_manifest(city))

print("\n=== PER-CITY STATS ===")
for city in cities:
    mpath = find_manifest(city)
    content_dir = f"{base}/hugo-site/content/{city}"
    pages = [f for f in os.listdir(content_dir) if f.endswith('.md')] if os.path.isdir(content_dir) else []
    n_pages = len(pages)
    # counts from content frontmatter
    needs_review = 0
    schema_null = 0
    inquiry = 0
    image_real = 0
    image_placeholder = 0
    if mpath:
        with open(mpath) as f:
            m = json.load(f)
        ds = m.get("datasets", [])
        n_ds = len(ds)
        for d in ds:
            cs = d.get("content_status","")
            if "needs_review" in cs:
                needs_review += 1
            sch = d.get("schema")
            if sch is None:
                schema_null += 1
            if d.get("inquiry_enabled"):
                inquiry += 1
            isrc = d.get("image_status") or d.get("image_source") or ""
            if isrc == "placeholder":
                image_placeholder += 1
            else:
                image_real += 1
        print(f"{city}: manifest_ds={n_ds} pages={n_pages} inquiry={inquiry} needs_review={needs_review} schema_null={schema_null} img_placeholder={image_placeholder} img_other={image_real}")
    else:
        print(f"{city}: NO MANIFEST. pages={n_pages}")

# cities.json check
with open(f"{base}/cities.json") as f:
    txt = f.read()
print("\nacog in cities.json:", '"id": "acog"' in txt)
import re
ids = re.findall(r'"id":\s*"([a-z0-9]+)"', txt)
print("total city ids in cities.json:", len(ids))
print("active flag count:", txt.count('"active": true'))

# ACOG: content dir stubs
acog_dir = f"{base}/hugo-site/content/acog"
if os.path.isdir(acog_dir):
    acog_pages = [f for f in os.listdir(acog_dir) if f.endswith('.md')]
    print(f"\nACOG content dir: {len(acog_pages)} md files")
    # sample frontmatter content_status
    nr = 0
    for f in acog_pages[:50]:
        with open(os.path.join(acog_dir,f)) as fh:
            head = fh.read(400)
        if "needs_review" in head or "stub" in head.lower():
            nr += 1
    print(f"ACOG sample needs_review/stub among first 50: {nr}")
