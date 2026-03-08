import re
path = "app/models/contratacion.py"
with open(path, "r") as f:
    content = f.read()

# Fix PlantillaDocumento AGAIN. For some reason my previous python scripts didn't write to it.
old_plantilla = """class PlantillaDocumento(AuditMixin, Base):
    __tablename__ = "plantilla_documento"
    __table_args__ = {"schema": "contratacion"}
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    categoria = Column(String(50), nullable=False, server_default="Bienes y Servicios")
    condicion_monto = Column(String(255), nullable=True)
    is_activo = Column(Boolean, default=True, server_default="true", nullable=False)
    ruta_archivo_docx = Column(String(255), nullable=False)
    tipo_proceso_id = Column(Integer, ForeignKey("contratacion.tipo_proceso.id"))"""

new_plantilla = """class PlantillaDocumento(AuditMixin, Base):
    __tablename__ = "plantilla_documento"
    __table_args__ = {"schema": "contratacion"}
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    ruta_archivo_docx = Column(String(255), nullable=False)
    tipo_proceso_id = Column(Integer, ForeignKey("contratacion.tipo_proceso.id"))
    anio = Column(Integer, server_default="2026", nullable=False)
    version = Column(Integer, server_default="1", nullable=False)
    is_activa = Column(Boolean, default=True, server_default="true", nullable=False)"""

content = content.replace(old_plantilla, new_plantilla)

with open(path, "w") as f:
    f.write(content)
