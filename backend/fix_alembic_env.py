import re

path = "alembic/env.py"
with open(path, "r") as f:
    content = f.read()

old_func = """def include_object(object, name, type_, reflected, compare_to):
    if type_ == "table":
        if name in [
            "users", "roles", "permissions", "role_permission", "audit_logs", 
            "redes", "sectores", "rutas", "barrios", "calles", "parametros_sistema", 
            "ciudadanos", "referencias_ciudadanos",
            "predios", "acometidas", "cuentas", "medidores", "historial_medidor_cuenta", "historial_tarifa_cuenta", "tipo_proceso", "plantilla_documento", "proceso_contratacion", "documento_generado"
        ]:
            return True
        return False
    return True"""

new_func = """def include_object(object, name, type_, reflected, compare_to):
    # We ignore PostGIS internal tables
    if type_ == "table" and name in ['spatial_ref_sys', 'topology', 'layer', 'pagc_gaz', 'pagc_lex', 'pagc_rules']:
        return False
    return True"""

content = content.replace(old_func, new_func)

with open(path, "w") as f:
    f.write(content)
