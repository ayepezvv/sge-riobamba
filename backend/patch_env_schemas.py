import re

path = "/home/ayepez/.openclaw/workspace/sge/backend/alembic/env.py"
with open(path, "r") as f:
    content = f.read()

new_logic = """def include_object(object, name, type_, reflected, compare_to):
    if type_ == "table":
        # Incluir explícitamente nuestras tablas
        if name in [
            "users", "roles", "permissions", "role_permission", "audit_logs", 
            "redes", "sectores", "rutas", "barrios", "calles", "parametros_sistema", 
            "ciudadanos", "referencias_ciudadanos",
            "predios", "acometidas", "cuentas", "medidores", "historial_medidor_cuenta", "historial_tarifa_cuenta"
        ]:
            return True
        return False
    return True

def include_name(name, type_, parent_names):
    if type_ == "schema":
        return name in ["administracion", "catastro", "comercial", "core"]
    return True"""

# replace include_object and add include_name
content = re.sub(r"def include_object.*?return True", new_logic, content, flags=re.DOTALL)

# Add include_schemas=True and include_name to context.configure
content = content.replace('include_object=include_object\n    )', 'include_object=include_object,\n        include_schemas=True,\n        include_name=include_name\n    )')

with open(path, "w") as f:
    f.write(content)
