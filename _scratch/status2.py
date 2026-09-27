import os, json
# OKC manifest locations
for p in ["hugo-site/static/okc/manifest.json","public/okc/manifest.json","hugo-site/content/okc/manifest.json"]:
    print("OKC manifest", p, os.path.exists(p))
# ACOG
acog_pub = os.listdir("public/acog")
acog_dirs = [f for f in acog_pub if os.path.isdir(os.path.join("public/acog", f))]
print("ACOG public pages:", len(acog_dirs))
print("ACOG content dir exists:", os.path.isdir("hugo-site/content/acog"))
# 50-state expansion manifest coverage
states = [d for d in os.listdir("hugo-site/content") if os.path.isdir("hugo-site/content/" + d)]
have_manifest = [d for d in states if os.path.exists("hugo-site/static/" + d + "/manifest.json")]
print("content cities:", len(states))
print("with manifest:", len(have_manifest), sorted(have_manifest))
# OKC frontmatter stats
okc_dir = "hugo-site/content/okc"
pages = [f for f in os.listdir(okc_dir) if f.endswith(".md")]
inquiry = 0; real_img = 0; ph_img = 0; nr = 0
for f in pages:
    t = open(okc_dir + "/" + f).read(2000)
    if "inquiry_enabled: true" in t: inquiry += 1
    if "image_status: placeholder" in t: ph_img += 1
    elif "image_status:" in t: real_img += 1
    if "needs_review" in t: nr += 1
print("OKC: pages=%d inquiry=%d placeholder=%d other_img=%d needs_review=%d" % (len(pages), inquiry, ph_img, real_img, nr))
