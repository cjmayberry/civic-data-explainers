#!/usr/bin/env python3
"""
Converts drafts.json (output of content/draft_content.py) into Hugo
content files under content/datasets/<slug>.md, each with frontmatter
matching what layouts/datasets/single.html expects.

This is the connective piece between the drafting step and the Hugo
build -- without it you have valid JSON and a valid Hugo site with no
path between them.

Usage:
    python3 to_hugo_content.py drafts.json --site-url https://open-okc.hub.arcgis.com --city "Oklahoma City" --out ../hugo-site/content/datasets
"""
import sys
import json
import re
import argparse
from pathlib import Path

import yaml  # PyYAML -- install with: pip install pyyaml --break-system-packages


def slugify(title: str) -> str:
    slug = title.lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    return slug.strip("-")


def draft_to_page(draft: dict, site_url: str, city: str) -> tuple:
    source = draft["source"]
    body = draft.get("draft_markdown")

    if not body:
        # A failed draft (see draft_content.py's error handling) --
        # still worth a stub page rather than silently dropping it,
        # so the gap is visible in the built site instead of just
        # vanishing from the list.
        body = (
            f"*Draft generation failed for this dataset "
            f"({draft.get('error', 'unknown error')}). Source data is "
            f"available below; explainer text pending.*"
        )

    frontmatter = {
        "title": source["title"],
        "source_city": city,
        "source_link": source.get("link", ""),
        "update_interval": source.get("update_interval") or "Unknown",
        "topics": source.get("topics", []),
        "data_dictionary": source.get("data_dictionary", []),
        "draft": bool(draft.get("error")),  # Hugo can filter these out of listings if desired
    }

    slug = slugify(source["title"])
    content = "---\n" + yaml.safe_dump(frontmatter, sort_keys=False, allow_unicode=True) + "---\n\n" + body + "\n"
    return slug, content


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("drafts_json", help="Path to drafts.json from draft_content.py")
    parser.add_argument("--site-url", required=True, help="Source ArcGIS Hub site URL, for reference")
    parser.add_argument("--city", required=True, help="Human-readable city name for the source_city field")
    parser.add_argument("--out", required=True, help="Output directory (Hugo's content/datasets/)")
    args = parser.parse_args()

    with open(args.drafts_json) as f:
        drafts = json.load(f)

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    written = 0
    failed = 0
    for draft in drafts:
        slug, content = draft_to_page(draft, args.site_url, args.city)
        path = out_dir / f"{slug}.md"
        path.write_text(content, encoding="utf-8")
        written += 1
        if draft.get("error"):
            failed += 1

    print(f"# Wrote {written} pages to {out_dir} ({failed} marked draft/failed)", file=sys.stderr)


if __name__ == "__main__":
    main()
