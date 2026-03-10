import re

path = "app/api/routes/contratacion.py"
with open(path, "r") as f:
    content = f.read()

content = content.replace("from sqlalchemy.orm import Session", "from sqlalchemy.orm import Session, joinedload")

with open(path, "w") as f:
    f.write(content)
