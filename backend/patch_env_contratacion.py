import re
path = "alembic/env.py"
with open(path, "r") as f:
    content = f.read()

# Update table inclusions
new_tables = '"predios", "acometidas", "cuentas", "medidores", "historial_medidor_cuenta", "historial_tarifa_cuenta", "tipo_proceso", "plantilla_documento", "proceso_contratacion", "documento_generado"'
content = re.sub(r'"predios".*"historial_tarifa_cuenta"', new_tables, content)

# Update schema inclusions
content = content.replace('"comercial", "core"]', '"comercial", "core", "contratacion"]')

with open(path, "w") as f:
    f.write(content)
