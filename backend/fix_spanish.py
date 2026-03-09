path = "app/models/administrativo.py"
with open(path, "r") as f:
    content = f.read()

content = content.replace("is_active =", "es_activo =")
with open(path, "w") as f:
    f.write(content)
