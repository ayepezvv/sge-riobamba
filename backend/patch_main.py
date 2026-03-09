path = "/home/ayepez/.openclaw/workspace/sge/backend/app/main.py"
with open(path, "r") as f:
    content = f.read()

# Modify imports
old_import = "from app.api.routes import auth, users, roles, permissions, parametros, territorio, ciudadanos, comercial, contratacion"
new_import = "from app.api.routes import auth, users, roles, permissions, parametros, territorio, ciudadanos, comercial, contratacion, administrativo"
content = content.replace(old_import, new_import)

# Register router
old_register = 'app.include_router(contratacion.router, prefix="/api/contratacion", tags=["contratacion"])'
new_register = 'app.include_router(contratacion.router, prefix="/api/contratacion", tags=["contratacion"])\napp.include_router(administrativo.router, prefix="/api/administrativo", tags=["administrativo"])'
content = content.replace(old_register, new_register)

with open(path, "w") as f:
    f.write(content)
