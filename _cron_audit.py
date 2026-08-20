import json, os, glob

REPO = "/opt/data/civic-data-explainers"
with open(os.path.join(REPO, "cities.json")) as f:
    cities = json.load(f)

active = [c for c in cities if c.get("active")]
print(f"ACTIVE CITIES IN cities.json: {len(active)} -> {[c['id'] for c in active]}")
print()

rows = []
for c in active:
    cid = c["id"]
    mpath = os.path.join(REPO, c["static_dir"], "manifest.json")
    cpath = os.path.join(REPO, c["content_dir"])
    n_manifest = "NO MANIFEST"
    n_pages = "NO CONTENT"
    img_dist = {}
    inquiry = 0
    needs_review = 0
    schema_null = 0
    generated_at = "?"
    content_models = {}
    if os.path.exists(mpath):
        with open(mpath) as f:
            m = json.load(f)
        ds = m.get("datasets", [])
        n_manifest = len(ds)
        generated_at = m.get("generated_at", "?")
        for d in ds:
            st = d.get("image_status") or d.get("image_source") or "?"
            img_dist[st] = img_dist.get(st, 0) + 1
            if d.get("inquiry_enabled") in (True, "true", 1, "1"):
                inquiry += 1
            if d.get("content_status") == "needs_review":
                needs_review += 1
            sch = d.get("schema")
            if sch is None:
                schema_null += 1
            cm = d.get("content_model") or d.get("content_status")
            content_models[cm] = content_models.get(cm, 0) + 1
    if os.path.isdir(cpath):
        mds = [x for x in glob.glob(os.path.join(cpath, "*.md")) if not os.path.basename(x).startswith("_index")]
        n_pages = len(mds)
    rows.append((cid, n_manifest, n_pages, img_dist, inquiry, needs_review, schema_null, generated_at, content_models))
    print(f"### {cid}")
    print(f"  manifest datasets: {n_manifest} | content pages: {n_pages} | inquiry_enabled: {inquiry} | needs_review: {needs_review} | schema_null: {schema_null}")
    print(f"  image_status dist: {img_dist}")
    print(f"  content_model dist: {content_models}")
    print(f"  generated_at: {generated_at}")
    print()

# ACOG explicit check
print("=== ACOG ===")
print("  in cities.json:", any(c['id']=='acog' for c in cities))
print("  content/acog exists:", os.path.isdir(os.path.join(REPO,"hugo-site/content/acog")))
print("  static/acog exists:", os.path.isdir(os.path.join(REPO,"hugo-site/static/acog")))
