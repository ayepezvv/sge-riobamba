import json

file_path = "src/utils/locales/en.json"
with open(file_path, "r") as f:
    data = json.load(f)

data["admin"] = "Administración"
data["user-management"] = "Gestión de Usuarios"

with open(file_path, "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
