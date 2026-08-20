#!/usr/bin/env python3
"""Fix all county pages: add draft: false, fix state name in teaser."""
import os

ROOT = "/opt/data/civic-data-explainers"
CONTENT = os.path.join(ROOT, "hugo-site/content")

state_names = {
    "newmexico": "New Mexico",
    "idaho": "Idaho",
    "utah": "Utah",
}

fixed = 0
for state, state_name in state_names.items():
    state_dir = os.path.join(CONTENT, state)
    for fname in sorted(os.listdir(state_dir)):
        if not fname.endswith('.md'):
            continue
        path = os.path.join(state_dir, fname)
        with open(path) as f:
            content = f.read()
        
        # Check if draft: false is present
        if 'draft: false' not in content:
            # Insert draft: false after site_url line
            content = content.replace(
                'site_url: "https://civic-data-explainers.pages.dev"',
                'site_url: "https://civic-data-explainers.pages.dev"\ndraft: false'
            )
            with open(path, "w") as f:
                f.write(content)
            fixed += 1
        
        # Fix state name in teaser
        if f", {state} —" in content or f",{state}—" in content:
            content = content.replace(
                f", {state} —", f", {state_name} —"
            ).replace(
                f",{state}—", f", {state_name} —"
            ).replace(
                f"County, {state} —", f"County, {state_name} —"
            ).replace(
                f"County,{state} —", f"County, {state_name} —"
            )
            with open(path, "w") as f:
                f.write(content)

print(f"Fixed {fixed} county pages (added draft: false, corrected state names)")
