import os

env_path = "alembic/env.py"
with open(env_path, "r") as f:
    content = f.read()

# Add include_object logic
include_logic = """
def include_object(object, name, type_, reflected, compare_to):
    if type_ == "table" and name in [
        "spatial_ref_sys", "geography_columns", "geometry_columns", 
        "raster_columns", "raster_overviews", "bg", "counties", 
        "county_lookup", "cousub", "direction_lookup", "edges", 
        "faces", "featnames", "geocode_settings", "geocode_settings_default", 
        "loader_lookups", "loader_platform", "loader_variables", "node", 
        "place", "place_lookup", "pointg", "secondary_unit_lookup", 
        "state", "state_lookup", "street_type_lookup", "topology", 
        "tract", "zip_lookup", "zip_lookup_all", "zip_lookup_base", 
        "zip_state", "zip_state_loc", "layer"
    ]:
        return False
    return True

"""

content = content.replace("context.configure(", include_logic + "context.configure(\n    include_object=include_object,")
with open(env_path, "w") as f:
    f.write(content)
