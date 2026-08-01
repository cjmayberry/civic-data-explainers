import sys
sys.path.insert(0, ".")
from extract_catalog import split_description_sections, parse_data_dictionary

with open("/tmp/sample_description.txt") as f:
    desc = f.read()

sections = split_description_sections(desc)
print("=== SECTIONS DETECTED ===")
for k, v in sections.items():
    display = v[:80] + "..." if len(v) > 80 else v
    print(f"{k}: {display}")

print()
print("=== DATA DICTIONARY PARSED ===")
dd = parse_data_dictionary(sections.get("Data Dictionary", ""))
for field in dd:
    print(f"  {field['field']!r} -> {field['description']!r}")

print()
print(f"# {len(sections)} sections, {len(dd)} fields parsed")
