import re
path = "/home/ayepez/.openclaw/workspace/sge/backend/app/models/contratacion.py"
with open(path, "r") as f:
    content = f.read()

content = content.replace("from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text", "from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Boolean")

with open(path, "w") as f:
    f.write(content)
