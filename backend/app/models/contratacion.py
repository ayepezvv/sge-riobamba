from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base
from app.models.mixins import AuditMixin

class TipoProceso(AuditMixin, Base):
    __tablename__ = "tipo_proceso"
    __table_args__ = {"schema": "contratacion"}
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)

class PlantillaDocumento(AuditMixin, Base):
    __tablename__ = "plantilla_documento"
    __table_args__ = {"schema": "contratacion"}
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    ruta_archivo_docx = Column(String(255), nullable=False)
    tipo_proceso_id = Column(Integer, ForeignKey("contratacion.tipo_proceso.id"))

class ProcesoContratacion(AuditMixin, Base):
    __tablename__ = "proceso_contratacion"
    __table_args__ = {"schema": "contratacion"}
    id = Column(Integer, primary_key=True, index=True)
    codigo_proceso = Column(String(50), unique=True, index=True, nullable=False)
    nombre_proyecto = Column(String(255), nullable=False)
    descripcion = Column(Text, nullable=True)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    usuario_id = Column(Integer, ForeignKey("administracion.users.id", ondelete="RESTRICT"))
    
    documentos = relationship("DocumentoGenerado", back_populates="proceso", cascade="all, delete-orphan")

class DocumentoGenerado(AuditMixin, Base):
    __tablename__ = "documento_generado"
    __table_args__ = {"schema": "contratacion"}
    id = Column(Integer, primary_key=True, index=True)
    proceso_contratacion_id = Column(Integer, ForeignKey("contratacion.proceso_contratacion.id", ondelete="CASCADE"))
    plantilla_id = Column(Integer, ForeignKey("contratacion.plantilla_documento.id", ondelete="RESTRICT"))
    version = Column(Integer, default=1, nullable=False)
    datos_json = Column(JSONB, nullable=False)
    ruta_archivo_generado = Column(String(255), nullable=False)
    fecha_generacion = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    proceso = relationship("ProcesoContratacion", back_populates="documentos")
    plantilla = relationship("PlantillaDocumento")
