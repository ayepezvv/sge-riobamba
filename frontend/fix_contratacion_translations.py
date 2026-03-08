import json

file_path = "src/utils/locales/en.json"
with open(file_path, "r") as f:
    data = json.load(f)

data["contratacion"] = "Contratación Pública"
data["mis-procesos"] = "Mis Procesos / Expedientes"

with open(file_path, "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
