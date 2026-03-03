import re
path = "app/schemas/ciudadano.py"
with open(path, "r") as f:
    content = f.read()

# Add is_active
content = content.replace("aplica_tercera_edad: Optional[bool] = False", "aplica_tercera_edad: Optional[bool] = False\n    is_active: Optional[bool] = True")

with open(path, "w") as f:
    f.write(content)
