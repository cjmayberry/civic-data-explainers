#!/usr/bin/env python3
"""Fully fix brace syntax in state list.html templates.

The gen_state_scaffolding.py generated files with a mix of single and double braces:
- { define → {{ define
- { $var := → {{ $var :=
- { if → {{ if
- { range → {{ range
- { .Field } → {{ .Field }}
- { printf → {{ printf
- { with → {{ with
- { end } → {{ end }}
- {{ end }} (already correct, leave as-is)

Strategy: replace ALL single-brace expressions with double-brace equivalents.
"""

import os
import glob
import re

LAYOUTS = "/opt/data/civic-data-explainers/hugo-site/layouts"

def fix_list_html(content):
    """Fix all single-brace Hugo template syntax."""
    # Order matters: handle longer patterns first to avoid partial matches

    # 1. { define "main" } → {{ define "main" }}
    content = content.replace("{ define ", "{{ define ")

    # 2. { $var := ... } → {{ $var := ... }}  (variable assignments)
    # Match: { $name := ... }  where } is the closing brace
    content = re.sub(r'\{\s*\$(\w+)\s*:=\s*([^}]*)\}', r'{{ $\1 := \2 }}', content)

    # 3. { if ... } → {{ if ... }}
    content = re.sub(r'\{\s*if\s+([^}]*)\}', r'{{ if \1 }}', content)

    # 4. { range ... } → {{ range ... }}
    content = re.sub(r'\{\s*range\s+([^}]*)\}', r'{{ range \1 }}', content)

    # 5. { with ... } → {{ with ... }}
    content = re.sub(r'\{\s*with\s+([^}]*)\}', r'{{ with \1 }}', content)

    # 6. { .Field | ... } → {{ .Field | ... }}  (expression interpolation)
    # Match: { <expression> } where expression contains Hugo template syntax
    content = re.sub(r'\{\s*([^}]*?)\s*\}', r'{{ \1 }}', content)

    # 7. { end } → {{ end }}  (but NOT {{ end }} which is already correct)
    content = re.sub(r'(?<!\{\{\{)\{\s*end\s*\}', '{{ end }}', content)

    return content

fixed = 0
for path in glob.glob(f"{LAYOUTS}/*/list.html"):
    with open(path) as f:
        content = f.read()

    new_content = fix_list_html(content)

    if new_content != content:
        with open(path, "w") as f:
            f.write(new_content)
        fixed += 1
        rel = os.path.relpath(path, LAYOUTS)
        print(f"Fixed: {rel}")

print(f"\nTotal fixed: {fixed}")

# Show a sample fix
sample_path = f"{LAYOUTS}/alabama/list.html"
with open(sample_path) as f:
    sample = f.read()
print(f"\n=== {sample_path} after fix ===")
print(sample)
