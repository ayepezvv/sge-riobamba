import sys
file_path = sys.argv[1]
with open(file_path, "r") as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if "op.create_index" in line and "schema=" not in line:
        if "permissions" in line or "roles" in line or "users" in line or "role_permission" in line:
            line = line.replace("], unique", "], schema='administracion', unique")
        elif "barrios" in line or "calles" in line or "ciudadanos" in line or "redes" in line or "referencias" in line or "sectores" in line or "rutas" in line:
            line = line.replace("], unique", "], schema='catastro', unique")
        elif "predios" in line or "acometidas" in line or "cuentas" in line or "medidores" in line or "historial" in line:
            line = line.replace("], unique", "], schema='comercial', unique")
        elif "audit_logs" in line or "parametros_sistema" in line:
            line = line.replace("], unique", "], schema='core', unique")
    new_lines.append(line)

with open(file_path, "w") as f:
    f.writelines(new_lines)
