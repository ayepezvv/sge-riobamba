import os
path = "app/main.py"
with open(path, "r") as f:
    content = f.read()

content = content.replace("from app.api.routes import auth, users, roles, permissions, parametros, territorio, ciudadanos, comercial", "from app.api.routes import auth, users, roles, permissions, parametros, territorio, ciudadanos, comercial, contratacion")

routers = """app.include_router(comercial.router, prefix="/api/comercial", tags=["comercial"])
app.include_router(contratacion.router, prefix="/api/contratacion", tags=["contratacion"])"""

content = content.replace('app.include_router(comercial.router, prefix="/api/comercial", tags=["comercial"])', routers)

with open(path, "w") as f:
    f.write(content)
