import re

path_env = "alembic/env.py"
with open(path_env, "r") as f:
    content = f.read()

# Add configuracion to schema list
content = content.replace('"public", "administracion", "catastro", "comercial", "core", "contratacion"', '"public", "administracion", "catastro", "comercial", "core", "contratacion", "configuracion"')

with open(path_env, "w") as f:
    f.write(content)
