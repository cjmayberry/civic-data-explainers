import json, os, glob

REPO = "/opt/data/civic-data-explainers"
with open(os.path.join(REPO, "cities.json")) as f:
    cities = json.load(f)
active = [c for c in cities if c.get("active")]

for c in active:
    cid = c["id"]
    mpath = os.path.join(REPO, c["static_dir"], "manifest.json")
    cpath = os.path.join(REPO, c["content_dir"])
    if not os.path.exists(mpath):
        continue
    m = json.load(open(mpath))
    ds = m["datasets"]
    # exact content_status distribution
    cs = {}
    for d in ds:
        v = d.get("content_status", "?")
        cs[v] = cs.get(v, 0) + 1
    # slug vs file cross-check
    man_slugs = set(d.get("slug") for d in ds)
    mds = glob.glob(os.path.join(cpath, "*.md"))
    file_slugs = set(os.path.basename(x)[:-3] for x in mds if not os.path.basename(x).startswith("_index"))
    missing_files = man_slugs - file_slugs
    missing_manifest = file_slugs - man_slugs
    print(f"### {cid}: content_status={cs}")
    if missing_files:
        print(f"    manifest slugs WITHOUT a content file: {sorted(missing_files)}")
    if missing_manifest:
        print(f"    content files WITHOUT manifest entry: {sorted(missing_manifest)}")
