import re

path = "app/api/routes/administrativo.py"
with open(path, "r") as f:
    content = f.read()

# Since app.main.py does: app.include_router(administrativo.router, prefix="/api/administrativo")
# and the router itself has: router = APIRouter(prefix="/administrativo")
# The resulting path is /api/administrativo/administrativo/direcciones
# We need to fix the router prefix to be empty.
content = content.replace('router = APIRouter(prefix="/administrativo", tags=["Administrativo"])', 'router = APIRouter(tags=["Administrativo"])')

with open(path, "w") as f:
    f.write(content)
