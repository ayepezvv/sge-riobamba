import re

path = "app/api/routes/contratacion.py"
with open(path, "r") as f:
    content = f.read()

# I notice the decorator was accidentally stripped in a previous regex!
if '@router.post("/documento")' not in content:
    content = content.replace("def generar_documento(", '@router.post("/documento")\ndef generar_documento(')

# While we are here, let's also check if regenerar lost its decorator
if '@router.put("/documento/{id}/regenerar")' not in content and "def regenerar_documento" in content:
    content = content.replace("def regenerar_documento(", '@router.put("/documento/{id}/regenerar")\ndef regenerar_documento(')

with open(path, "w") as f:
    f.write(content)
