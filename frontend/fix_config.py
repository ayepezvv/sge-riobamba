import re

path = "src/config.ts"
with open(path, "r") as f:
    content = f.read()

content = content.replace("i18n: 'en',", "i18n: 'es',")

with open(path, "w") as f:
    f.write(content)
