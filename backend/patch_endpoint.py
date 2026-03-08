import re

path = "app/api/routes/contratacion.py"
with open(path, "r") as f:
    content = f.read()

# Replace any lingering "is_activo" with "is_activa" specifically in the upload_plantilla route
content = content.replace("is_activo=True).first()", "is_activa=True).first()")
content = content.replace("old_tpl.is_activo = False", "old_tpl.is_activa = False")
content = content.replace("is_activo=True,", "is_activa=True,")

with open(path, "w") as f:
    f.write(content)
