import json, os, collections

base = "/opt/data/civic-data-explainers"
content_root = os.path.join(base, "hugo-site/content")
static_root = os.path.join(base, "hugo-site/static")

cities_with_content = sorted([d for d in os.listdir(content_root)
                              if os.path.isdir(os.path.join(content_root, d))])

print("CONTENT DIRS:", cities_with_content)
print()

results = {}
for city in cities_with_content:
    cdir = os.path.join(content_root, city)
    pages = [f for f in os.listdir(cdir) if f.endswith(".md") and f != "_index.md"]
    # find manifest
    man = None
    cand = os.path.join(static_root, city, "manifest.json")
    if os.path.exists(cand):
        man = cand
    nd = len(pages)
    row = {"pages": nd, "manifest": man}
    if man:
        with open(man) as fh:
            m = json.load(fh)
        ds = m.get("datasets", [])
        row["datasets"] = len(ds)
        img = collections.Counter()
        inquiry = 0
        needs_review = 0
        schema_null = 0
        content_status = collections.Counter()
        for d in ds:
            isrc = d.get("image_status") or d.get("image_source") or "none"
            img[isrc] += 1
            if d.get("inquiry_enabled"):
                inquiry += 1
            cs = d.get("content_status")
            content_status[cs] += 1
            if cs == "needs_review":
                needs_review += 1
            if d.get("schema") is None:
                schema_null += 1
        row["datasets"] = len(ds)
        row["image_dist"] = dict(img)
        row["inquiry"] = inquiry
        row["needs_review"] = needs_review
        row["schema_null"] = schema_null
        row["content_status"] = dict(content_status)
        ga = m.get("generated_at")
        row["generated_at"] = ga
    results[city] = row

for city, r in results.items():
    print(f"=== {city} ===")
    print(f"  pages={r['pages']} manifest={r['manifest']}")
    if "datasets" in r:
        print(f"  datasets={r['datasets']} inquiry={r['inquiry']} needs_review={r['needs_review']} schema_null={r['schema_null']}")
        print(f"  image_dist={r['image_dist']}")
        print(f"  content_status={r['content_status']}")
        print(f"  generated_at={r['generated_at']}")
    print()
