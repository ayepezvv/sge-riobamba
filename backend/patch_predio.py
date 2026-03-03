import re

path = "/home/ayepez/.openclaw/workspace/sge/backend/app/models/comercial.py"
with open(path, "r") as f:
    content = f.read()

new_fields = """    numero_casa = Column(String(50), nullable=True)
    foto_fachada = Column(String(255), nullable=True)
    croquis = Column(String(255), nullable=True)"""

content = content.replace("    numero_casa = Column(String(50), nullable=True)", new_fields)

with open(path, "w") as f:
    f.write(content)
