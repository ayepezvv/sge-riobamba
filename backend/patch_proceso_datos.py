import re

path = "app/models/contratacion.py"
with open(path, "r") as f:
    content = f.read()

new_fields = """    usuario_id = Column(Integer, ForeignKey("administracion.users.id", ondelete="RESTRICT"))
    tipo_proceso_id = Column(Integer, ForeignKey("contratacion.tipo_proceso.id", ondelete="RESTRICT"), nullable=True)
    datos_formulario = Column(JSONB, nullable=True)"""

content = content.replace('    usuario_id = Column(Integer, ForeignKey("administracion.users.id", ondelete="RESTRICT"))\n    tipo_proceso_id = Column(Integer, ForeignKey("contratacion.tipo_proceso.id", ondelete="RESTRICT"), nullable=True)', new_fields)

with open(path, "w") as f:
    f.write(content)

path_schema = "app/schemas/contratacion.py"
with open(path_schema, "r") as f:
    content_schema = f.read()

new_schema = """class ProcesoContratacionBase(BaseModel):
    codigo_proceso: str
    nombre_proyecto: str
    descripcion: Optional[str] = None
    tipo_proceso_id: Optional[int] = None
    datos_formulario: Optional[Dict[str, Any]] = None"""

content_schema = content_schema.replace("""class ProcesoContratacionBase(BaseModel):
    codigo_proceso: str
    nombre_proyecto: str
    descripcion: Optional[str] = None
    tipo_proceso_id: Optional[int] = None""", new_schema)

with open(path_schema, "w") as f:
    f.write(content_schema)
