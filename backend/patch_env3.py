import os

env_path = "alembic/env.py"
with open(env_path, "r") as f:
    content = f.read()

import re
# Find the include_object function and replace it
new_func = """def include_object(object, name, type_, reflected, compare_to):
    if type_ == "table":
        return name in ["users", "roles", "permissions", "role_permission"]
    return True"""

# Simple replacement
content = re.sub(r"def include_object.*?return True", new_func, content, flags=re.DOTALL)

with open(env_path, "w") as f:
    f.write(content)
