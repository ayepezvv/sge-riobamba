import os
import glob

# 7. Refactor Auth/User API endpoints that may use literal queries or need schema context
# Basically, replacing User queries usually uses the ORM so it adapts automatically, but we might have raw SQL or error messages.
# Let's search the routes for any explicit "administracion" references just in case.

routes_dir = "app/api/routes"
for filepath in glob.glob(os.path.join(routes_dir, "*.py")):
    with open(filepath, "r") as f:
        content = f.read()
    
    if 'administracion.users' in content:
        content = content.replace('administracion.users', 'configuracion.usuarios')
        with open(filepath, "w") as f:
            f.write(content)

