import os
path = "app/main.py"
with open(path, "r") as f:
    content = f.read()

content = content.replace("from app.api.routes import auth, users, roles", "from app.api.routes import auth, users, roles, permissions")
content = content.replace("app.include_router(roles.router, prefix=\"/api/roles\", tags=[\"roles\"])", "app.include_router(roles.router, prefix=\"/api/roles\", tags=[\"roles\"])\napp.include_router(permissions.router, prefix=\"/api/permissions\", tags=[\"permissions\"])")

with open(path, "w") as f:
    f.write(content)
