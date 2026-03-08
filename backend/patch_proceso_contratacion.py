import re

path = "app/models/contratacion.py"
with open(path, "r") as f:
    content = f.read()

new_fields = """    usuario_id = Column(Integer, ForeignKey("administracion.users.id", ondelete="RESTRICT"))
    tipo_proceso_id = Column(Integer, ForeignKey("contratacion.tipo_proceso.id", ondelete="RESTRICT"), nullable=True)"""

content = content.replace('    usuario_id = Column(Integer, ForeignKey("administracion.users.id", ondelete="RESTRICT"))', new_fields)

with open(path, "w") as f:
    f.write(content)

# Tambien actulizamos el schema pydantic
path_schema = "app/schemas/contratacion.py"
with open(path_schema, "r") as f:
    schema_content = f.read()

new_schema = """class ProcesoContratacionBase(BaseModel):
    codigo_proceso: str
    nombre_proyecto: str
    descripcion: Optional[str] = None
    tipo_proceso_id: Optional[int] = None"""

schema_content = schema_content.replace("""class ProcesoContratacionBase(BaseModel):
    codigo_proceso: str
    nombre_proyecto: str
    descripcion: Optional[str] = None""", new_schema)

with open(path_schema, "w") as f:
    f.write(schema_content)
