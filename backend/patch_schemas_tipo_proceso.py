import re

path = "/home/ayepez/.openclaw/workspace/sge/backend/app/schemas/contratacion.py"
with open(path, "r") as f:
    content = f.read()

new_base = """class TipoProcesoBase(BaseModel):
    nombre: str
    categoria: str
    condicion_monto: Optional[str] = None
    is_activo: Optional[bool] = True

class TipoProcesoCreate(TipoProcesoBase):
    pass

class TipoProcesoUpdate(BaseModel):
    nombre: Optional[str] = None
    categoria: Optional[str] = None
    condicion_monto: Optional[str] = None
    is_activo: Optional[bool] = None"""

content = content.replace('class TipoProcesoBase(BaseModel):\n    nombre: str', new_base)

with open(path, "w") as f:
    f.write(content)
