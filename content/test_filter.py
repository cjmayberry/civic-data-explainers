import sys
sys.path.insert(0, ".")
from draft_content import filter_teaching_worthy

# Synthetic records exercising each branch. Field values are made up to
# probe the filter, not pulled from the real feed.
records = [
    {  # should PASS: zoning, clean dict, daily cadence, cross-city keyword
        "type": "Dataset", "title": "Straight Zoning",
        "topics": ["Land Use"], "update_interval": "Daily",
        "data_dictionary": [{"field": "ZONING", "description": "x"}] * 4,
    },
    {  # should FAIL: utility keyword (trash) even though dict is clean
        "type": "Dataset", "title": "My Trash Day",
        "topics": ["Public Works"], "update_interval": "Every 5 minutes",
        "data_dictionary": [{"field": "ROUTE", "description": "x"}] * 4,
    },
    {  # should FAIL: heavy GIS keyword
        "type": "Dataset", "title": "Survey Monument Control Points",
        "topics": ["Infrastructure"], "update_interval": "Daily",
        "data_dictionary": [{"field": "X", "description": "y"}] * 5,
    },
    {  # should FAIL: not cross-city (no matching keyword) even though clean+cadence
        "type": "Dataset", "title": "Airport Boundary",
        "topics": ["Facilities"], "update_interval": "Daily",
        "data_dictionary": [{"field": "X", "description": "y"}] * 4,
    },
    {  # should PASS: thin dict (1 field) but real cadence + cross-city -- OR logic
        "type": "Dataset", "title": "Council Ward Boundaries",
        "topics": ["Government"], "update_interval": "Weekly",
        "data_dictionary": [{"field": "WARD", "description": "x"}],
    },
    {  # should PASS: as-needed cadence but clean dict + cross-city -- OR logic
        "type": "Dataset", "title": "Public Infrastructure Projects",
        "topics": ["Infrastructure"], "update_interval": "As needed",
        "data_dictionary": [{"field": "BUDGET", "description": "x"}] * 6,
    },
    {  # should FAIL: it's an Application, not a Dataset
        "type": "Application", "title": "Zoning Map Viewer",
        "topics": ["Land Use"], "update_interval": "Daily",
        "data_dictionary": [{"field": "X", "description": "y"}] * 5,
    },
]

expected_pass = {
    "Straight Zoning", "Council Ward Boundaries", "Public Infrastructure Projects",
}
expected_fail = {
    "My Trash Day", "Survey Monument Control Points", "Airport Boundary",
    "Zoning Map Viewer",
}

result = filter_teaching_worthy(records)
actual_pass = {r["title"] for r in result}

print(f"Passed filter: {sorted(actual_pass)}")
print(f"Expected pass: {sorted(expected_pass)}")

if actual_pass == expected_pass:
    print("\nALL CASES CORRECT")
else:
    missing = expected_pass - actual_pass
    extra = actual_pass - expected_pass
    if missing:
        print(f"\nMISSING (should have passed, didn't): {missing}")
    if extra:
        print(f"\nUNEXPECTED (shouldn't have passed, did): {extra}")
    sys.exit(1)
