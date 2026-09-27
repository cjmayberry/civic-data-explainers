import json, os
from collections import Counter

base = "/opt/data/civic-data-explainers"
manifest_map = {
    "okc": f"{base}/hugo-site/static/img/manifest.json",
    "memphis": f"{base}/hugo-site/static/memphis/manifest.json",
    "lisbon": f"{base}/hugo-site/static/lisbon/manifest.json",
    "missouri": f"{base}/hugo-site/static/missouri/manifest.json",
    "tennessee": f"{base}/hugo-site/static/tennessee/manifest.json",
}

for city, path in manifest_map.items():
    print(f"\n===== {city} =====")
    if not os.path.exists(path):
        print("MANIFEST MISSING:", path)
        continue
    m = json.load(open(path))
    ds = m.get("datasets", [])
    print(f"generated_at: {m.get('generated_at')}")
    print(f"datasets: {len(ds)}")
    if ds:
        print("sample entry keys:", sorted(ds[0].keys()))
    img = Counter(str(d.get("image_status")) for d in ds)
    cs = Counter(str(d.get("content_status")) for d in ds)
    inquiry = sum(1 for d in ds if d.get("inquiry_enabled"))
    schema_null = sum(1 for d in ds if d.get("schema") is None)
    print("image_status:", dict(img))
    print("content_status:", dict(cs))
    print("inquiry_enabled:", inquiry)
    print("schema_null:", schema_null)
    cdir = f"{base}/hugo-site/content/{city}"
    if os.path.isdir(cdir):
        pages = [f for f in os.listdir(cdir) if f.endswith(".md")]
        idx = sum(1 for p in pages if p == "_index.md")
        print(f"content md pages: {len(pages)} (incl _index: {idx}, datasets: {len(pages)-idx})")

# broader: count active cities in cities.json and how many have manifests + content
print("\n===== BROADER =====")
cities = json.load(open(f"{base}/cities.json"))
active = [c for c in cities if c.get("active")]
print(f"active cities in cities.json: {len(active)}")
for c in active:
    cid = c["id"]
    mp = f"{base}/hugo-site/static/{cid}/manifest.json"
    if cid == "okc":
        mp = f"{base}/hugo-site/static/img/manifest.json"
    has_m = os.path.exists(mp)
    cd = f"{base}/hugo-site/content/{cid}"
    npages = len([f for f in os.listdir(cd) if f.endswith('.md')]) if os.path.isdir(cd) else 0
    print(f"  {cid:12s} manifest={'Y' if has_m else 'N'} content_pages={npages}")
