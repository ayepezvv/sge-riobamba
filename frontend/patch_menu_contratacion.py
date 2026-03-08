import re

path = "src/menu-items/index.tsx"
with open(path, "r") as f:
    content = f.read()

content = content.replace("import catastro from './catastro';", "import catastro from './catastro';\nimport contratacion from './contratacion';")
content = content.replace("items: [admin, catastro, gis]", "items: [admin, contratacion, catastro, gis]")

with open(path, "w") as f:
    f.write(content)
