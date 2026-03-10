import re

path = "app/schemas/contratacion.py"
with open(path, "r") as f:
    content = f.read()

# I used "from app.models.contratacion import ... StatusItemPac" but the import is at the top of the file, wait,
# Schema files should ideally define the Enum or import it properly.
# Let's just import it at the top of the schema file.
content = "from app.models.contratacion import StatusItemPac\n" + content

with open(path, "w") as f:
    f.write(content)
