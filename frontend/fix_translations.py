import json
import os

# 1. Revert dashboard.tsx
dashboard_path = "/home/ayepez/.openclaw/workspace/sge/frontend/src/menu-items/dashboard.tsx"
with open(dashboard_path, "r") as f:
    content = f.read()

content = content.replace("title: 'Panel de Control',", "title: 'dashboard',")

with open(dashboard_path, "w") as f:
    f.write(content)

# 2. Update en.json (and others just in case)
locale_dir = "/home/ayepez/.openclaw/workspace/sge/frontend/src/utils/locales/"
for file_name in os.listdir(locale_dir):
    if file_name.endswith(".json"):
        file_path = os.path.join(locale_dir, file_name)
        with open(file_path, "r") as f:
            try:
                data = json.load(f)
                # Ensure the dashboard key maps to our Spanish title
                data["dashboard"] = "Panel de Control"
                # Optional: translate a few more important ones
                if "default" in data:
                    data["default"] = "Principal"
                if "analytics" in data:
                    data["analytics"] = "Métricas"
                if "users" in data:
                    data["users"] = "Usuarios"
                if "widget" in data:
                    data["widget"] = "Componentes"
                if "application" in data:
                    data["application"] = "Aplicación"
            except Exception as e:
                print(f"Error reading {file_name}: {e}")
                continue
                
        with open(file_path, "w") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

print("Translations fixed and files updated.")
