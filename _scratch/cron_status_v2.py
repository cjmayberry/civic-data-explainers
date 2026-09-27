import json, os

base = "/opt/data/civic-data-explainers"
cities = ["okc","memphis","lisbon","missouri","tennessee","acog"]

for c in cities:
    manifest_path = os.path.join(base, f"hugo-site/static/{c}/manifest.json")
    content_dir = os.path.join(base, f"hugo-site/content/{c}")
    print(f"\n===== {c} =====")
    if os.path.exists(manifest_path):
        m = json.load(open(manifest_path))
        ds = m.get("datasets", [])
        print(f"manifest exists: datasets={len(ds)}")
        img = {}
        inq = 0
        nr = 0
        schema_null = 0
        for d in ds:
            s = d.get("image_status")
            img[s] = img.get(s,0)+1
            if d.get("inquiry_enabled"): inq += 1
            if d.get("content_status") == "needs_review": nr += 1
            if d.get("schema") is None: schema_null += 1
        print(f"  image_status: {img}")
        print(f"  inquiry_enabled: {inq}")
        print(f"  content_status=needs_review: {nr}")
        print(f"  schema null: {schema_null}")
    else:
        print(f"  manifest MISSING at {manifest_path}")
    if os.path.isdir(content_dir):
        files = [f for f in os.listdir(content_dir) if f.endswith(".md")]
        print(f"  content md files: {len(files)}")
    else:
        print(f"  content dir MISSING: {content_dir}")
