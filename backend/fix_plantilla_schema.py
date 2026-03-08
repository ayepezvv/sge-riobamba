import re

path = "app/schemas/contratacion.py"
with open(path, "r") as f:
    content = f.read()

# Make sure we clean up the Pydantic schema that might be asking for `categoria` and `condicion_monto`
old_base = """class PlantillaDocumentoBase(BaseModel):
    nombre: str
    ruta_archivo_docx: str
    tipo_proceso_id: Optional[int] = None
    anio: Optional[int] = 2026
    version: Optional[int] = 1
    is_activa: Optional[bool] = True"""

if old_base not in content:
    match = re.search(r'class PlantillaDocumentoBase\(BaseModel\):.*?is_activa: Optional\[bool\] = True', content, re.DOTALL)
    if match:
        content = content.replace(match.group(0), old_base)

with open(path, "w") as f:
    f.write(content)
