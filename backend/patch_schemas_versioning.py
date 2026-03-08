import re
path = "/home/ayepez/.openclaw/workspace/sge/backend/app/schemas/contratacion.py"
with open(path, "r") as f:
    content = f.read()

new_fields = """    ruta_archivo_docx: str
    tipo_proceso_id: Optional[int] = None
    anio: Optional[int] = 2026
    version: Optional[int] = 1
    is_activa: Optional[bool] = True"""

content = content.replace('    ruta_archivo_docx: str\n    tipo_proceso_id: Optional[int] = None', new_fields)

with open(path, "w") as f:
    f.write(content)
