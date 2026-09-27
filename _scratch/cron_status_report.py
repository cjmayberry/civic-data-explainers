import json, os, glob

repo = "/opt/data/civic-data-explainers"
with open(os.path.join(repo, "cities.json")) as f:
    cities = json.load(f)

print("TOTAL cities in cities.json:", len(cities))
active = [c for c in cities if c.get("active")]
print("ACTIVE:", len(active), [c["id"] for c in active])
print("ACOG in cities.json?", any(c["id"]=="acog" for c in cities))

print("\n--- PER CITY ---")
for c in cities:
    cid = c["id"]
    mpath = os.path.join(repo, "hugo-site/static", cid, "manifest.json")
    n_ds = None
    real = ph = inquiry = needs = null = 0
    imgstat = {}
    if os.path.exists(mpath):
        with open(mpath) as f:
            m = json.load(f)
        ds = m.get("datasets", [])
        n_ds = len(ds)
        for d in ds:
            istat = (d.get("image_status") or d.get("image_source") or "").lower()
            imgstat[istat] = imgstat.get(istat,0)+1
            if "placeholder" in istat: ph += 1
            else: real += 1
            if d.get("inquiry_enabled"): inquiry += 1
            if d.get("content_status")=="needs_review": needs += 1
            if d.get("schema") is None: null += 1
    else:
        n_ds = "NO-MANIFEST"
    cdir = os.path.join(repo, "hugo-site/content", cid)
    npages = 0
    if os.path.isdir(cdir):
        npages = len([p for p in glob.glob(os.path.join(cdir,"*.md")) if not os.path.basename(p).startswith("_index")])
    print(f"{cid:12} ds={str(n_ds):12} pages={npages:4} real={real:3} ph={ph:3} inq={inquiry:3} needs={needs:3} null={null:3} img={imgstat}")

# okc manifest check
print("\n--- okc static dir ---")
okc_static = os.path.join(repo, "hugo-site/static/okc")
if os.path.isdir(okc_static):
    print(sorted(os.listdir(okc_static))[:20])
print("\n--- acog ---")
acog_static = os.path.join(repo, "hugo-site/static/acog")
print("acog static manifest:", os.path.exists(acog_static+"/manifest.json"))
print("acog public manifest:", os.path.exists(os.path.join(repo,"public/acog/manifest.json")))
