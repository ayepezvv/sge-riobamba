import re

path = "alembic/env.py"
with open(path, "r") as f:
    content = f.read()

new_func = """def include_object(object, name, type_, reflected, compare_to):
    if type_ == "table" and object.schema == "tiger":
        return False
    if type_ == "table" and object.schema == "topology":
        return False
    if type_ == "table" and name in [
        'spatial_ref_sys', 'layer', 'topology', 'pagc_gaz', 'pagc_lex', 'pagc_rules',
        'tabblock', 'zcta5', 'zip_lookup', 'countysub_lookup', 'zip_state', 'featnames',
        'edges', 'addr', 'county', 'zip_lookup_base', 'county_lookup', 'loader_variables',
        'direction_lookup', 'state_lookup', 'place_lookup', 'secondary_unit_lookup',
        'zip_lookup_all', 'geocode_settings_default', 'tabblock20', 'zip_state_loc',
        'cousub', 'state', 'addrfeat', 'street_type_lookup', 'loader_lookuptables',
        'faces', 'place', 'geocode_settings', 'tract', 'bg', 'loader_platform'
    ]:
        return False
    return True"""

content = re.sub(r'def include_object.*?return True', new_func, content, flags=re.DOTALL)

with open(path, "w") as f:
    f.write(content)
