import os
path = "app/main.py"
with open(path, "r") as f:
    content = f.read()

content = content.replace("territorio, ciudadanos", "territorio, ciudadanos, comercial")

routers = """app.include_router(ciudadanos.router, prefix="/api/ciudadanos", tags=["ciudadanos"])
app.include_router(comercial.router, prefix="/api/comercial", tags=["comercial"])"""

content = content.replace('app.include_router(ciudadanos.router, prefix="/api/ciudadanos", tags=["ciudadanos"])', routers)

with open(path, "w") as f:
    f.write(content)
