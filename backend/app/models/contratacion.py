import enum
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Boolean, Float, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base
from app.models.mixins import AuditMixin


class StatusItemPac(enum.Enum):
    ACTIVO = "ACTIVO"
    ELIMINADO_POR_REFORMA = "ELIMINADO_POR_REFORMA"
    MODIFICADO_POR_REFORMA = "MODIFICADO_POR_REFORMA"

class PacAnual(AuditMixin, Base):
    __tablename__ = "pac_anual"
    __table_args__ = {"schema": "contratacion"}

    id = Column(Integer, primary_key=True, index=True)
    anio = Column(Integer, nullable=False)
    version_reforma = Column(Integer, default=0, nullable=False)
    descripcion = Column(String(255), nullable=True)
    es_activo = Column(Boolean, default=True)

    items = relationship("ItemPac", back_populates="pac", cascade="all, delete-orphan")

class ItemPac(AuditMixin, Base):
    __tablename__ = "item_pac"
    __table_args__ = {"schema": "contratacion"}

    id = Column(Integer, primary_key=True, index=True)
    pac_anual_id = Column(Integer, ForeignKey("contratacion.pac_anual.id", ondelete="CASCADE"), nullable=False)
    partida_presupuestaria = Column(String(100), nullable=False)
    cpc = Column(String(50), nullable=True)
    tipo_compra = Column(String(100), nullable=True)
    procedimiento = Column(String(100), nullable=True)
    descripcion = Column(Text, nullable=False)
    cantidad = Column(Float, nullable=False, default=1.0)
    costo_unitario = Column(Float, nullable=False, default=0.0)
    valor_total = Column(Float, nullable=False, default=0.0)
    status = Column(SQLEnum(StatusItemPac, name="status_item_pac"), default=StatusItemPac.ACTIVO, nullable=False)

    pac = relationship("PacAnual", back_populates="items")
    procesos_links = relationship("ProcesoItemPacLink", back_populates="item_pac")


class HistoricoReformaPac(AuditMixin, Base):
    __tablename__ = "historico_reforma_pac"
    __table_args__ = {"schema": "contratacion"}

    id = Column(Integer, primary_key=True, index=True)
    pac_anual_id = Column(Integer, ForeignKey("contratacion.pac_anual.id", ondelete="CASCADE"), nullable=False)
    numero_reforma = Column(Integer, nullable=False)
    fecha_reforma = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    resolucion_administrativa = Column(String(255), nullable=True)
    descripcion_justificacion = Column(Text, nullable=False)

    pac = relationship("PacAnual", backref="reformas")
    movimientos = relationship("GenealogiaMontoPac", back_populates="reforma", cascade="all, delete-orphan")

class GenealogiaMontoPac(Base):
    __tablename__ = "genealogia_monto_pac"
    __table_args__ = {"schema": "contratacion"}

    id = Column(Integer, primary_key=True, index=True)
    historico_reforma_id = Column(Integer, ForeignKey("contratacion.historico_reforma_pac.id", ondelete="CASCADE"), nullable=False)
    item_origen_id = Column(Integer, ForeignKey("contratacion.item_pac.id", ondelete="RESTRICT"), nullable=True)
    item_destino_id = Column(Integer, ForeignKey("contratacion.item_pac.id", ondelete="RESTRICT"), nullable=True)
    monto_transferido = Column(Float, nullable=False)

    reforma = relationship("HistoricoReformaPac", back_populates="movimientos")
    item_origen = relationship("ItemPac", foreign_keys=[item_origen_id])
    item_destino = relationship("ItemPac", foreign_keys=[item_destino_id])

class ProcesoItemPacLink(Base):
    __tablename__ = "proceso_item_pac_link"
    __table_args__ = {"schema": "contratacion"}

    id = Column(Integer, primary_key=True, index=True)
    proceso_id = Column(Integer, ForeignKey("contratacion.proceso_contratacion.id", ondelete="CASCADE"), nullable=False)
    item_pac_id = Column(Integer, ForeignKey("contratacion.item_pac.id", ondelete="CASCADE"), nullable=False)
    monto_comprometido = Column(Float, nullable=False, default=0.0)

    proceso = relationship("ProcesoContratacion", back_populates="items_pac_links")
    item_pac = relationship("ItemPac", back_populates="procesos_links")


class TipoProceso(AuditMixin, Base):
    __tablename__ = "tipo_proceso"
    __table_args__ = {"schema": "contratacion"}
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    categoria = Column(String(50), nullable=False, server_default="Bienes y Servicios")
    condicion_monto = Column(String(255), nullable=True)
    is_activo = Column(Boolean, default=True, server_default="true", nullable=False)

class PlantillaDocumento(AuditMixin, Base):
    __tablename__ = "plantilla_documento"
    __table_args__ = {"schema": "contratacion"}
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    ruta_archivo_docx = Column(String(255), nullable=False)
    tipo_proceso_id = Column(Integer, ForeignKey("contratacion.tipo_proceso.id"))
    anio = Column(Integer, server_default="2026", nullable=False)
    version = Column(Integer, server_default="1", nullable=False)
    is_activa = Column(Boolean, default=True, server_default="true", nullable=False)

class ProcesoContratacion(AuditMixin, Base):
    __tablename__ = "proceso_contratacion"
    __table_args__ = {"schema": "contratacion"}
    id = Column(Integer, primary_key=True, index=True)
    codigo_proceso = Column(String(50), unique=True, index=True, nullable=False)
    nombre_proyecto = Column(String(255), nullable=False)
    descripcion = Column(Text, nullable=True)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    usuario_id = Column(Integer, ForeignKey("configuracion.usuarios.id", ondelete="RESTRICT"))
    tipo_proceso_id = Column(Integer, ForeignKey("contratacion.tipo_proceso.id", ondelete="RESTRICT"), nullable=True)
    datos_formulario = Column(JSONB, nullable=True)
    
    documentos = relationship("DocumentoGenerado", back_populates="proceso", cascade="all, delete-orphan")
    items_pac_links = relationship("ProcesoItemPacLink", back_populates="proceso", cascade="all, delete-orphan")

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
