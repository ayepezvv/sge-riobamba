import re

path = "/home/ayepez/.openclaw/workspace/sge/backend/alembic/env.py"
with open(path, "r") as f:
    content = f.read()

new_logic = """def include_object(object, name, type_, reflected, compare_to):
    if type_ == "table":
        # Incluir nuestras tablas explicitamente
        if name in ["users", "roles", "permissions", "role_permission", "audit_logs", "redes", "sectores", "rutas", "barrios", "calles", "parametros_sistema", "ciudadanos", "referencias_ciudadanos"]:
            return True
        # Excluir tablas de sistema postgis/tiger explícitamente
        if name in [
            "spatial_ref_sys", "geography_columns", "geometry_columns", 
            "raster_columns", "raster_overviews", "bg", "counties", 
            "county_lookup", "cousub", "direction_lookup", "edges", 
            "faces", "featnames", "geocode_settings", "geocode_settings_default", 
            "loader_lookups", "loader_platform", "loader_variables", "node", 
            "place", "place_lookup", "pointg", "secondary_unit_lookup", 
            "state", "state_lookup", "street_type_lookup", "topology", 
            "tract", "zip_lookup", "zip_lookup_all", "zip_lookup_base", 
            "zip_state", "zip_state_loc", "layer", "tabblock", "tabblock20",
            "county", "addr", "addrfeat", "zcta5", "pagc_gaz", "pagc_lex", "pagc_rules"
        ]:
            return False
        return False
    return True"""

content = re.sub(r"def include_object.*?return True", new_logic, content, flags=re.DOTALL)

with open(path, "w") as f:
    f.write(content)
