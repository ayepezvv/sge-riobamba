import re

path = "/home/ayepez/.openclaw/workspace/sge/backend/app/models/contratacion.py"
with open(path, "r") as f:
    content = f.read()

new_fields = """    nombre = Column(String(100), nullable=False)
    categoria = Column(String(50), nullable=False, server_default="Bienes y Servicios")
    condicion_monto = Column(String(255), nullable=True)
    is_activo = Column(Boolean, default=True, server_default="true", nullable=False)"""

content = content.replace('    nombre = Column(String(100), nullable=False)', new_fields)

with open(path, "w") as f:
    f.write(content)
