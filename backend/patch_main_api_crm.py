import os
path = "app/main.py"
with open(path, "r") as f:
    content = f.read()

content = content.replace("from app.api.routes import auth, users, roles, permissions, parametros, territorio", "from app.api.routes import auth, users, roles, permissions, parametros, territorio, ciudadanos")

routers = """app.include_router(territorio.router, prefix="/api/territorio", tags=["territorio"])
app.include_router(ciudadanos.router, prefix="/api/ciudadanos", tags=["ciudadanos"])"""

content = content.replace('app.include_router(territorio.router, prefix="/api/territorio", tags=["territorio"])', routers)

with open(path, "w") as f:
    f.write(content)
