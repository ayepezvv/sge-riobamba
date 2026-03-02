path = "src/menu-items/index.tsx"
with open(path, "r") as f:
    content = f.read()

content = content.replace("import dashboard from './dashboard';", "import admin from './admin';\nimport dashboard from './dashboard';")
content = content.replace("items: [dashboard,", "items: [admin, dashboard,")

with open(path, "w") as f:
    f.write(content)
