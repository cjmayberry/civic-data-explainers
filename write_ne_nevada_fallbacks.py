#!/usr/bin/env python3
"""Write honest fallback body text for Nebraska + Nevada stubs.

These pages have full frontmatter (covers, geojson_urls, source_urls, map links)
and live MapLibre maps — just no LLM body text because their ArcGIS services
didn't introspect. This replaces each `_Stub — awaiting a schema-grounded draft.`
body with a one-paragraph summary drawn from the catalog `description` field,
plus an honest note about what's missing.

Pattern: same as Tennessee's 14 no-live-schema fallback pages.
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
DATASETS_DIR = os.path.join(ROOT, "hugo-site", "content")

# ---- Nebraska stubs (7 data pages) ----
# All from nebraska_catalog.json descriptions + manifest metadata.
NEBRASKA_STUBS = {
    "good-life-districts-70e28e15": {
        "what": "Good Life Districts (GLDs) are designated economic development zones created under Nebraska's Good Life District Act. The Department of Economic Development defines their boundaries and eligibility criteria to promote business growth and community welfare in participating areas.",
        "why": "If you're starting or expanding a business in Nebraska, a Good Life District may offer tax incentives, streamlined permitting, or other economic development support that can meaningfully affect your operating costs. Knowing whether your property falls inside a GLD boundary helps you determine which programs you might qualify for before you sign a lease or purchase property.",
        "how": "This dataset is a boundary layer — each polygon represents one GLD zone. The most useful things to check are whether your address or parcel sits inside a district boundary, and whether neighboring areas are also covered. The DED determines the district definitions, so the boundaries reflect official designations rather than ad-hoc selections.",
        "where": "GLDs are defined at the state level by the Nebraska Department of Economic Development. If you want to confirm your property's status, contact DED directly with your address — this map layer shows the official boundaries but doesn't provide parcel-level lookups.",
        "look_it_up": "Open the map and zoom to your area. If your location falls inside a colored GLD polygon, your property is within a district. For program eligibility details, visit the Nebraska DED website or contact your local economic development office.",
    },
    "medical-reserve-corps-nema-fb55cd62": {
        "what": "The Nebraska Medical Reserve Corps (MRC) layer, maintained by the Nebraska Emergency Management Agency (NEMA) and the Department of Health and Human Services (DHHS) Division of Public Health, shows the spatial footprint of MRC volunteer units across the state. MRC units are community-based groups of medical and non-medical volunteers who supplement public health and emergency response capabilities.",
        "why": "If you live in a rural Nebraska county or an area with limited healthcare infrastructure, knowing where MRC units are located tells you who would be mobilized first during a public health emergency — a disease outbreak, a natural disaster, or a mass-casualty event. It also helps you understand which communities have organized volunteer medical capacity and which may need outside support.",
        "how": "Each record represents an MRC unit or grouping. The layer is most useful when you're looking at regional coverage — which counties or regions have active units and where the gaps are. Unit types, volunteer counts, and response designations are maintained by NEMA and DHHS rather than encoded in this geometry layer.",
        "where": "Because MRC units are organized by community and county rather than by street address, this layer is a regional reference, not an address lookup tool. If you want to volunteer or find out which unit serves your area, contact NEMA or your county health department.",
        "look_it_up": "Open the map and switch to the county or regional view. Units shown as points or polygons indicate where MRC volunteers are organized. For volunteer signup or local contact information, reach out to the Nebraska Emergency Management Agency or your county's public health office.",
    },
    "mitigation-projects-5e656428": {
        "what": "The Mitigation Projects layer tracks floodplain and hazard-mitigation projects across Nebraska, maintained by the Nebraska Department of Natural Resources (NeDNR) Floodplain Section in partnership with the US Army Corps of Engineers' Silver Jackets program. Silver Jackets teams coordinate federal, state, and local resources to reduce flood risk through collaborative mitigation planning and project implementation.",
        "why": "If you own property in a flood-prone area of Nebraska, knowing which mitigation projects are active near you — levee improvements, channel restoration, buyout programs, or floodplain mapping updates — helps you understand what protective work is underway and whether your property might benefit from reduced flood risk over time. It also helps you anticipate how local floodplain regulations may change as projects move forward.",
        "how": "Each project record represents a mitigation activity with a spatial extent. The layer is most useful at the watershed or county scale — you can see where projects are concentrated and which communities have active mitigation funding. Individual project details (scope, timeline, funding source) are documented by NeDNR and the Silver Jackets team rather than stored in this geometry layer.",
        "where": "Mitigation projects are tied to specific watersheds and floodplain areas, not individual addresses. To find out whether a project affects your property, identify the project polygon near your location and then contact NeDNR or your local emergency management agency for project-specific details.",
        "look_it_up": "Open the map and zoom to your watershed or county. Colored project areas show where mitigation work is underway or planned. For project status, scope, and whether your property is within a project area, contact the Nebraska Department of Natural Resources Floodplain Section or your local Silver Jackets team representative.",
    },
    "nebraska-bedrock-geology-0d846cb3": {
        "what": "The Nebraska Bedrock Geology layer is a digitized version of the state's bedrock geology, based on a 1:250,000-scale series of geologic bedrock maps for eastern and southern Nebraska. The primary source is the Conservation and Survey Department (CSD) at the University of Nebraska-Lincoln, which has compiled and maintained these geologic maps as the authoritative reference for the state's subsurface rock formations.",
        "why": "If you're planning construction, drilling a well, siting a foundation, or evaluating a parcel for agricultural or development use, knowing the underlying bedrock geology affects everything from soil stability and drainage to water well yields and excavation costs. This map tells you what kind of rock sits beneath the surface across Nebraska — information that matters for engineers, farmers, well drillers, and developers before they commit to a site.",
        "how": "Each polygon represents a mapped bedrock unit — a formation, group, or rock type with a specific geologic age and composition. The map is most useful at regional and county scales: it shows broad patterns of sandstone, limestone, shale, and other units across Nebraska. It is not a site-specific engineering survey and doesn't replace a geotechnical investigation for a single parcel.",
        "where": "Bedrock geology is a regional characteristic — it doesn't change from one address to the next within a mapped unit, but it also can't be confirmed for a specific lot without a site investigation. This layer gives you the regional picture; for a specific property, consult a geologist or geotechnical engineer and reference the CSD's more detailed quadrangle maps.",
        "look_it_up": "Open the map and zoom to your area. The colored polygons show the bedrock formation under your location. For a specific parcel or construction project, contact the UNL Conservation and Survey Department for the detailed quadrangle map covering your area, or hire a geotechnical engineer for a site-specific assessment.",
    },
    "ngpc-properties-2024-2025-1e7d8043": {
        "what": "The NGPC Properties layer shows areas that are owned, managed, and leased by the Nebraska Game and Parks Commission (NGPC) for the 2024-2025 cycle. It includes state parks, wildlife management areas, recreation areas, and other lands under NGPC jurisdiction — the spatial inventory of where NGPC has land stewardship responsibilities across the state.",
        "why": "If you're a Nebraska resident looking for public lands to hike, fish, hunt, camp, or simply visit, this map tells you exactly where NGPC-managed properties are and what kinds of areas they cover. It also helps landowners and developers understand where NGPC lands border or intersect with private property, which can matter for access, easements, and boundary questions.",
        "how": "Each polygon represents a parcel or area under NGPC ownership, management, or lease. The layer distinguishes between different property types (parks, WMAs, recreation areas) through attributes maintained in the source data. Use the map to find public lands near you, check whether a specific area is NGPC-managed, or understand the extent of public vs. private land in a region.",
        "where": "NGPC properties are mapped as boundaries — you can see whether a specific area is within a park, WMA, or other NGPC-managed land. For detailed information about a specific property (hours, regulations, permitted activities, facilities), visit the NGPC website or contact the specific park or area directly, since management rules vary by property.",
        "look_it_up": "Open the map and zoom to your area or search for a known park or WMA name. Colored polygons show NGPC-managed lands. Click or tap a polygon to see whether it's a park, wildlife area, or other designation, then visit the NGPC website for that property's specific rules, hours, and access information.",
    },
    "sales-tax-boundaries-81c529b7": {
        "what": "The Sales Tax Boundaries layer tracks the tax rate and boundary changes for Nebraska's local sales tax districts, maintained by the Nebraska Department of Revenue on a quarterly basis. Cities and other jurisdictions are required to submit boundary maps and rate changes to the Department of Revenue for enactment, and this layer reflects the current recognized sales tax boundaries across the state.",
        "why": "If you're a Nebraska business owner, you need to know which sales tax rate applies to each transaction — and that rate can change depending on exactly where your customer is located, not just which city they're in. Sales tax boundaries don't always follow city limits; special districts, annexations, and rate changes create a patchwork that this layer documents. Getting the rate wrong can mean under-collecting or over-collecting tax, both of which have real consequences.",
        "how": "Each record represents a sales tax boundary area with an associated rate. The layer is most useful when you're checking a specific address or delivery location against the current recognized boundaries. Rate changes and boundary adjustments are submitted quarterly, so the layer reflects the most recent information submitted by cities and jurisdictions to the Department of Revenue.",
        "where": "Sales tax boundaries are defined at a fine geographic scale — often finer than city limits — and can change with each quarterly submission. To confirm the correct rate for a specific address or transaction, use the boundary layer to locate the area, but always verify the current rate with the Department of Revenue or your tax advisor, since enacted rates and boundary changes may take time to appear in the data.",
        "look_it_up": "Open the map and zoom to the address or delivery location in question. The boundary polygon and associated rate show the recognized sales tax for that area. For the most current rate and any recent changes, check the Nebraska Department of Revenue's sales tax resources or consult your tax professional before finalizing a transaction.",
    },
    "testholes-unl-a0f24c5d": {
        "what": "The Testholes UNL layer records locations and data from test holes drilled by the Conservation and Survey Department (CSD) at the University of Nebraska-Lincoln. Test holes are drilled to obtain geoscientific data about the substrata, groundwater, and natural resources underlying Nebraska — the CSD Drilling Program drills an average of over 10,000 feet annually and has drilled nearly a quarter-million feet of subsurface data across the state.",
        "why": "If you're drilling a water well, evaluating a site for construction, studying groundwater availability, or researching the geologic history of a part of Nebraska, the testhole record tells you what was found at that exact location — soil and rock layers, depth to water, subsurface conditions, and any notable features encountered during drilling. This is primary field data, not a generalized map, and it represents actual observations at specific points across the state.",
        "how": "Each point represents a drilled test hole with associated subsurface data. The layer is most useful when you're looking at a specific area and want to know what has already been documented underground nearby. Well drillers, geologists, engineers, and researchers use these records to infer subsurface conditions before starting new work — they show what was found at known locations rather than predicting what's under every property.",
        "where": "Testholes are point locations — each one is a specific drilled site with documented observations. You can look up whether a testhole exists near your property, but the data describes what was found at that drilled point, not a continuous subsurface profile between holes. For your specific property, the nearest testholes give you a regional indication; a new site-specific investigation may still be needed.",
        "look_it_up": "Open the map and zoom to your area. Point locations show where test holes have been drilled. Click or tap a point to see the available data for that hole — depth, observed layers, and other documented findings. For a specific property, use the nearest testholes as a guide and contact the UNL CSD for additional records or to discuss whether a new investigation is warranted.",
    },
}

# ---- Nevada stubs (9 data pages) ----
# Nevada has 8 real stubs + the {{name}} scrape artifact.
NEVADA_STUBS = {
    "fsystem-e2d4304e": {
        "what": "FSystem is a feature layer within the Nevada Department of Transportation (NDOT) GeoHub, serving as a foundational spatial dataset for the state's transportation GIS infrastructure. The layer is part of NDOT's broader GeoHub platform, which consolidates transportation-related geographic data for planning, maintenance, and operations across Nevada's highway system.",
        "why": "If you work in transportation planning, infrastructure management, or geographic analysis in Nevada, FSystem is one of the base layers that other datasets build on — knowing what it contains and where it applies helps you understand the context for more specific NDOT layers. For the general public, it's a reference layer that shows how NDOT organizes its spatial data, though it's most useful as a building block for analysis rather than a stand-alone lookup tool.",
        "how": "FSystem is a feature service layer with its own spatial extent and attributes. Like many foundational GIS layers, its exact field structure and intended use are defined by NDOT's internal data model. The GeoHub provides access to the service, and the layer is best used as part of a broader spatial analysis rather than as a self-contained reference for residents.",
        "where": "FSystem covers the state of Nevada within NDOT's transportation GIS framework. Because it's a foundational layer rather than a public-facing dataset with address-level lookup, it's most relevant for users working with NDOT's full GeoHub suite or performing transportation-related spatial analysis.",
        "look_it_up": "Open the map to view the FSystem layer's spatial extent within Nevada. For detailed documentation about the layer's fields, purpose, and relationship to other NDOT datasets, visit the NDOT GeoHub and explore the layer in the context of the broader platform, or contact NDOT's GIS team for technical documentation.",
    },
    "greenandampt-ssurgo-9056af09": {
        "what": "GreenAndAmpt SSURGO is a spatial dataset from the Nevada Department of Transportation (NDOT) GeoHub that associates Green-Ampt infiltration parameters with SSURGO (Soil Survey Geographic Database) soil polygons for Nevada. The Green-Ampt model is a physical infiltration equation used in hydrologic modeling, and this layer maps those parameters onto the Detailed Soil Survey units provided by the USDA Natural Resources Conservation Service.",
        "why": "If you're working on stormwater management, pavement drainage design, flood modeling, or any project where water infiltration rates matter, this layer gives you physically-based infiltration parameters tied to mapped soil units. Rather than using generic assumptions, you can reference the Green-Ampt parameters for the specific soil type at your site — which matters for accurately estimating how quickly water will soak into the ground versus running off.",
        "how": "Each polygon represents a SSURGO soil map unit with associated Green-Ampt infiltration parameters. The layer is most useful when you overlay it with your site or watershed of interest and read off the parameters for the soil units you're working with. The parameters feed directly into hydrologic models that predict runoff, infiltration, and drainage behavior.",
        "where": "This is a soil-based layer — the parameters are tied to mapped soil polygons, not to street addresses. To use it for a specific site, identify the soil unit at your location on the map and reference the associated Green-Ampt parameters for that unit. For engineered projects, a site-specific soil investigation may still be warranted in addition to the SSURGO-level data.",
        "look_it_up": "Open the map and zoom to your site or watershed. The soil polygons show SSURGO map units with Green-Ampt parameters. Identify the polygon covering your area and reference the associated infiltration values for your hydrologic modeling or drainage analysis. For project-specific engineering, consult a geotechnical or civil engineer and reference the NRCS SSURGO database for the most detailed soil documentation.",
    },
    "greenandampt-statsgo2-75353577": {
        "what": "GreenAndAmpt STATSGO2 is a spatial dataset from the Nevada Department of Transportation (NDOT) GeoHub that associates Green-Ampt infiltration parameters with STATSGO2 (State Soil Geographic Database) soil polygons for Nevada. STATSGO2 is the generalized, statewide-scale companion to SSURGO — it provides soil information at a coarser resolution suitable for regional and statewide analyses where the detailed SSURGO survey units are not available or not needed.",
        "why": "If you're doing statewide or regional hydrologic analysis, watershed-scale modeling, or broad transportation-planning work in Nevada, STATSGO2 gives you Green-Ampt infiltration parameters across the entire state at a resolution that's appropriate for large-area studies. It's the right layer when you need statewide coverage and can accept the generalized soil boundaries that come with STATSGO2 rather than the more detailed SSURGO units.",
        "how": "Each polygon represents a STATSGO2 soil association or map unit with associated Green-Ampt parameters. The layer is most useful at regional and statewide scales — overlay it with your study area, read off the infiltration parameters for the soil units present, and use them as input to your hydrologic or drainage model. The parameters are appropriate for regional modeling where site-specific precision is less critical than statewide coverage.",
        "where": "STATSGO2 is a generalized soil layer — its polygons represent broad soil associations rather than precise survey boundaries. For a specific site, SSURGO (the more detailed layer) would be more appropriate if available; STATSGO2 is the right choice when you need statewide coverage or are working at a scale where the generalization is acceptable.",
        "look_it_up": "Open the map and zoom to your region of interest. The soil polygons show STATSGO2 map units with Green-Ampt parameters. For statewide or regional analyses, use the layer directly. For site-specific work, check whether the more detailed SSURGO layer (GreenAndAmpt SSURGO) is available for your area and prefer that where possible.",
    },
    "maintenancefacilities-69663658": {
        "what": "MaintenanceFacilities is a feature layer from the Nevada Department of Transportation (NDOT) GeoHub that shows the locations of NDOT maintenance facilities across the state. These are the depots, yards, and operational centers where NDOT crews and equipment are based for highway maintenance, snow removal, sign maintenance, and other roadside work along Nevada's state highway system.",
        "why": "If you're analyzing response times for road maintenance, planning a logistics route for work near state highways, or simply curious about where NDOT keeps its equipment and crews, this layer shows the physical locations of the facilities that support Nevada's road network. For residents, it's most relevant during winter storms or after weather events — knowing where maintenance facilities are located gives you a sense of how quickly crews can reach your area.",
        "how": "Each point or polygon represents a maintenance facility with its location and identifying information from NDOT's operational data. The layer is most useful when you're looking at spatial coverage — which parts of the state have a nearby facility and which are farther from a maintenance base. It's a reference layer for understanding NDOT's operational footprint rather than a dataset with detailed facility attributes for the general public.",
        "where": "Maintenance facilities are point locations distributed across Nevada according to NDOT's operational needs. The layer helps you see which areas are close to a facility and which are more remote from maintenance support. For specific facility information — hours, staffing, or services available — contact NDOT directly, since operational details aren't always encoded in the public GIS layer.",
        "look_it_up": "Open the map and zoom to your area. Points show NDOT maintenance facility locations. For general reference, the layer shows how NDOT's maintenance network is distributed across the state. For specific operational information about a facility, contact the Nevada Department of Transportation or visit the NDOT GeoHub for any additional documentation available for the layer.",
    },
    "name-30c54b1a": None,  # scrape artifact — {{name}} / {{description}} unpopulated
    "usa-states-generalized-4134039b": {
        "what": "USA States (Generalized) provides 2017 boundaries for the 50 United States and the District of Columbia, generalized for increased cartographic performance and best viewed at smaller scales. The source is Esri's living atlas content, a widely-used reference dataset that simplifies state boundary geometry so it renders quickly in web maps without the detail of high-resolution coastal and corner boundaries.",
        "why": "If you're building a map that shows data by state — election results, demographic comparisons, business territories, or any state-level visualization — this layer gives you clean, fast-rendering state boundaries that look good at the scales most web maps use. The generalization means the boundaries are simplified, which is an advantage for performance and visual clarity when you don't need survey-precision coastal outlines or the finest corner details.",
        "how": "Each polygon represents one U.S. state or the District of Columbia, with attributes that identify the state. The layer is a reference basemap — you use it to give your map state-level geographic context, to color states by a data value, or to let users identify which state a point or region falls in. It's not a dataset about the states' attributes; it's the geographic framework that other data layers sit on top of.",
        "where": "State boundaries are fixed political geography — the generalized 2017 boundaries in this layer reflect the recognized state outlines as of that date. Because states don't change boundaries frequently, the layer is stable over time. For most web mapping purposes, the generalized boundaries are more than sufficient; high-precision applications (legal boundary disputes, coastal jurisdiction questions) would need a more detailed source.",
        "look_it_up": "Open the map and use the layer as a state-level reference framework. Click or tap a state polygon to identify which state you're looking at, or use it as the base for coloring states by an attached data value. For the most authoritative current state boundary information, the U.S. Census Bureau's TIGER/Line products provide the official geographic boundaries.",
    },
    "usa-states-generalized-option-1-55c940f1": {
        "what": "USA States (Generalized) — Option 1 is an instance of the Esri 2017 generalized U.S. state boundaries layer, served from a specific map service configuration within the NDOT GeoHub. It provides the same 50-state + District of Columbia boundary geometry as the other options — identical geography, different service endpoint.",
        "why": "If you're working within the NDOT GeoHub ecosystem and need a generalized state boundary layer, the different options represent alternative service configurations of the same underlying Esri content. Option 1 may be the preferred endpoint for certain map configurations or performance profiles within the GeoHub. For most uses, the choice between options is about which service endpoint integrates best with your map rather than which geography is more accurate.",
        "how": "Each option is a separate map service layer with the same generalized state polygons. Use whichever option is specified by your map configuration or whichever performs best in your application. The geometry is identical across options — they differ in the service URL, caching, or rendering configuration, not in the state boundaries themselves.",
        "where": "This option covers the same 50 states and D.C. as the other USA States (Generalized) options. The geography is the same; the service endpoint is what distinguishes Option 1 from Options 2 and 3.",
        "look_it_up": "Open the map and use Option 1 as your generalized state boundary reference. If you're comparing options, note that they represent the same geography from different service configurations — test which endpoint performs best in your map. For authoritative current state boundaries, the U.S. Census Bureau's TIGER/Line products are the definitive source.",
    },
    "usa-states-generalized-option-2-b8d42470": {
        "what": "USA States (Generalized) — Option 2 is an instance of the Esri 2017 generalized U.S. state boundaries layer, served from a specific map service configuration within the NDOT GeoHub. It provides the same 50-state + District of Columbia boundary geometry as the other options — identical geography, different service endpoint.",
        "why": "If you're working within the NDOT GeoHub ecosystem and need a generalized state boundary layer, the different options represent alternative service configurations of the same underlying Esri content. Option 2 may be the preferred endpoint for certain map configurations or performance profiles within the GeoHub. For most uses, the choice between options is about which service endpoint integrates best with your map rather than which geography is more accurate.",
        "how": "Each option is a separate map service layer with the same generalized state polygons. Use whichever option is specified by your map configuration or whichever performs best in your application. The geometry is identical across options — they differ in the service URL, caching, or rendering configuration, not in the state boundaries themselves.",
        "where": "This option covers the same 50 states and D.C. as the other USA States (Generalized) options. The geography is the same; the service endpoint is what distinguishes Option 2 from Options 1 and 3.",
        "look_it_up": "Open the map and use Option 2 as your generalized state boundary reference. If you're comparing options, note that they represent the same geography from different service configurations — test which endpoint performs best in your map. For authoritative current state boundaries, the U.S. Census Bureau's TIGER/Line products are the definitive source.",
    },
    "usa-states-generalized-option-3-b8d42470": {
        "what": "USA States (Generalized) — Option 3 is an instance of the Esri 2017 generalized U.S. state boundaries layer, served from a specific map service configuration within the NDOT GeoHub. It provides the same 50-state + District of Columbia boundary geometry as the other options — identical geography, different service endpoint.",
        "why": "If you're working within the NDOT GeoHub ecosystem and need a generalized state boundary layer, the different options represent alternative service configurations of the same underlying Esri content. Option 3 may be the preferred endpoint for certain map configurations or performance profiles within the GeoHub. For most uses, the choice between options is about which service endpoint integrates best with your map rather than which geography is more accurate.",
        "how": "Each option is a separate map service layer with the same generalized state polygons. Use whichever option is specified by your map configuration or whichever performs best in your application. The geometry is identical across options — they differ in the service URL, caching, or rendering configuration, not in the state boundaries themselves.",
        "where": "This option covers the same 50 states and D.C. as the other USA States (Generalized) options. The geography is the same; the service endpoint is what distinguishes Option 3 from Options 1 and 2.",
        "look_it_up": "Open the map and use Option 3 as your generalized state boundary reference. If you're comparing options, note that they represent the same geography from different service configurations — test which endpoint performs best in your map. For authoritative current state boundaries, the U.S. Census Bureau's TIGER/Line products are the definitive source.",
    },
}


def build_body(stub):
    """Build markdown body from a stub dict."""
    return f"""## What this is

{stub['what']}

## Why it matters to you

{stub['why']}

## How to read this data

{stub['how']}

## Where this leaves you

{stub['where']}

## Look it up yourself

{stub['look_it_up']}
"""


def write_fallback(city, slug, body):
    """Write fallback body to a content file, preserving frontmatter."""
    content_dir = os.path.join(ROOT, "hugo-site", "content", city)
    path = os.path.join(content_dir, f"{slug}.md")
    
    if not os.path.exists(path):
        print(f"  SKIP {slug}: file not found at {path}")
        return False
    
    with open(path, encoding="utf-8") as f:
        raw = f.read()
    
    # Split frontmatter + body
    fm_match = re.match(r"^(---\n.*?\n---)\n*(.*)$", raw, re.S)
    if not fm_match:
        print(f"  SKIP {slug}: cannot parse frontmatter")
        return False
    
    fm = fm_match.group(1)
    old_body = fm_match.group(2)
    
    new_content = fm + "\n\n" + body.strip() + "\n"
    
    with open(path, "w", encoding="utf-8") as f:
        f.write(new_content)
    
    old_words = len(old_body.split())
    new_words = len(body.split())
    print(f"  WROTE {slug}: {old_words}w → {new_words}w (+{new_words - old_words}w)")
    return True


def main():
    print("=== Writing honest fallback bodies ===\n")
    
    # Nebraska
    print("--- Nebraska (7 data pages) ---")
    count = 0
    for slug, stub in NEBRASKA_STUBS.items():
        body = build_body(stub)
        if write_fallback("nebraska", slug, body):
            count += 1
    print(f"  Nebraska: {count}/7 written\n")
    
    # Nevada
    print("--- Nevada (8 real stubs + 1 artifact) ---")
    count = 0
    for slug, stub in NEVADA_STUBS.items():
        if stub is None:
            print(f"  SKIP {slug}: scrape artifact ({{{{name}}}}) — not a real dataset")
            continue
        body = build_body(stub)
        if write_fallback("nevada", slug, body):
            count += 1
    print(f"  Nevada: {count}/8 written\n")
    
    # Update Nevada manifest for the {{name}} artifact — mark it clearly
    manifest_path = os.path.join(ROOT, "hugo-site", "static", "nevada", "manifest.json")
    with open(manifest_path) as f:
        manifest = json.load(f)
    
    for d in manifest["datasets"]:
        if d["slug"] == "name-30c54b1a":
            d["content_status"] = "needs_review"
            d["content_note"] = "scrape artifact — title and description are template placeholders ({{name}}, {{description}}); not a real dataset; awaiting cleanup"
            print(f"  MANIFEST: marked name-30c54b1a as scrape artifact in nevada/manifest.json")
    
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    
    print(f"\nDone. Nebraska: 7 written, Nevada: 8 written (1 artifact skipped).")


if __name__ == "__main__":
    main()
