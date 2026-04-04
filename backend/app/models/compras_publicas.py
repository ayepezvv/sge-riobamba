"""
Módulo: Compras Públicas
Esquema PostgreSQL: compras_publicas

Entidades principales:
- CarpetaAnual: Agrupación de procesos por dirección/unidad y año fiscal
- ProcesoCompra: Proceso de contratación pública (vinculado al PAC)
- SeguimientoProceso: Estado actual y avance de cada proceso
- PlazoProceso: Control de plazos por etapa (cumplimiento LOSNCP)
- ChecklistDocumental: Control de documentos requeridos por proceso
"""

import enum
from sqlalchemy import (
    Column, Integer, String, Text, Numeric, Date, DateTime,
    Boolean, ForeignKey, CheckConstraint, UniqueConstraint, Index
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base


# ---------------------------------------------------------------------------
# Enumeraciones
# ---------------------------------------------------------------------------

class EstadoProcesoEnum(str, enum.Enum):
    ACTIVO = "ACTIVO"
    ANULADO = "ANULADO"
    FINALIZADO = "FINALIZADO"


class EtapaProcesoEnum(str, enum.Enum):
    PREPARATORIA = "PREPARATORIA"
    PRECONTRACTUAL = "PRECONTRACTUAL"
    CONTRACTUAL = "CONTRACTUAL"
    EJECUCION = "EJECUCION"
    LIQUIDACION = "LIQUIDACION"


class EstadoDocumentoEnum(str, enum.Enum):
    PENDIENTE = "PENDIENTE"
    PRESENTADO = "PRESENTADO"
    APROBADO = "APROBADO"
    RECHAZADO = "RECHAZADO"


class TipoAreaEnum(str, enum.Enum):
    DIRECCION = "DIRECCION"
    UNIDAD = "UNIDAD"


# ---------------------------------------------------------------------------
# CarpetaAnual — Agrupación por área y año fiscal
# ---------------------------------------------------------------------------

class CarpetaAnual(Base):
    __tablename__ = "carpeta_anual"
    __table_args__ = (
        UniqueConstraint("anio", "nombre_area", name="uq_carpeta_anual_anio_area"),
        {"schema": "compras_publicas"},
    )

    id = Column(Integer, primary_key=True, index=True)
    anio = Column(Integer, nullable=False, index=True)
    nombre_area = Column(String(200), nullable=False)
    tipo_area = Column(
        String(20),
        CheckConstraint("tipo_area IN ('DIRECCION', 'UNIDAD')", name="ck_tipo_area"),
        nullable=False,
        default="UNIDAD",
    )
    descripcion = Column(Text, nullable=True)
    activa = Column(Boolean, nullable=False, default=True)
    creada_en = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    actualizada_en = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    creada_por_id = Column(
        Integer,
        ForeignKey("configuracion.usuarios.id", ondelete="SET NULL"),
        nullable=True,
    )

    procesos = relationship("ProcesoCompra", back_populates="carpeta_anual", cascade="all, delete-orphan")


# ---------------------------------------------------------------------------
# ProcesoCompra — Proceso de contratación pública
# ---------------------------------------------------------------------------

class ProcesoCompra(Base):
    __tablename__ = "proceso_compra"
    __table_args__ = (
        CheckConstraint(
            "estado IN ('ACTIVO', 'ANULADO', 'FINALIZADO')",
            name="ck_proceso_estado",
        ),
        {"schema": "compras_publicas"},
    )

    id = Column(Integer, primary_key=True, index=True)
    carpeta_anual_id = Column(
        Integer,
        ForeignKey("compras_publicas.carpeta_anual.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    # Referencia al PAC en el módulo contratacion (opcional)
    pac_item_id = Column(
        Integer,
        ForeignKey("contratacion.item_pac.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    codigo_sercop = Column(String(50), nullable=True)
    nombre_proceso = Column(String(500), nullable=False)
    objeto_contratacion = Column(Text, nullable=True)
    tipo_contratacion = Column(String(100), nullable=False)
    procedimiento = Column(String(100), nullable=True)
    partida_presupuestaria = Column(String(50), nullable=True)

    presupuesto_referencial = Column(Numeric(15, 2), nullable=False, default=0)
    monto_adjudicado = Column(Numeric(15, 2), nullable=True)
    proveedor = Column(String(300), nullable=True)
    numero_contrato = Column(String(100), nullable=True)

    fecha_inicio_proceso = Column(Date, nullable=True)
    fecha_fin_planificada = Column(Date, nullable=True)
    fecha_adjudicacion = Column(Date, nullable=True)
    fecha_firma_contrato = Column(Date, nullable=True)

    estado = Column(String(20), nullable=False, default="ACTIVO", index=True)
    etapa_actual = Column(String(50), nullable=True, default="PREPARATORIA")

    administrador_contrato = Column(String(200), nullable=True)
    fiscalizador = Column(String(200), nullable=True)
    observaciones = Column(Text, nullable=True)

    creado_en = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    actualizado_en = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    creado_por_id = Column(
        Integer,
        ForeignKey("configuracion.usuarios.id", ondelete="SET NULL"),
        nullable=True,
    )

    carpeta_anual = relationship("CarpetaAnual", back_populates="procesos")
    seguimiento = relationship(
        "SeguimientoProceso",
        back_populates="proceso",
        uselist=False,
        cascade="all, delete-orphan",
    )
    plazos = relationship("PlazoProceso", back_populates="proceso", cascade="all, delete-orphan")
    documentos = relationship(
        "ChecklistDocumental", back_populates="proceso", cascade="all, delete-orphan"
    )


# ---------------------------------------------------------------------------
# SeguimientoProceso — Avance físico y financiero
# ---------------------------------------------------------------------------

class SeguimientoProceso(Base):
    __tablename__ = "seguimiento_proceso"
    __table_args__ = (
        UniqueConstraint("proceso_id", name="uq_seguimiento_proceso"),
        {"schema": "compras_publicas"},
    )

    id = Column(Integer, primary_key=True, index=True)
    proceso_id = Column(
        Integer,
        ForeignKey("compras_publicas.proceso_compra.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    avance_fisico_pct = Column(Numeric(5, 2), nullable=False, default=0)
    avance_financiero_pct = Column(Numeric(5, 2), nullable=False, default=0)
    valor_ejecutado = Column(Numeric(15, 2), nullable=False, default=0)
    valor_pendiente = Column(Numeric(15, 2), nullable=False, default=0)

    dias_retraso = Column(Integer, nullable=False, default=0)
    motivo_retraso = Column(Text, nullable=True)
    accion_correctiva = Column(Text, nullable=True)

    ultima_actualizacion = Column(Date, nullable=True)
    observaciones = Column(Text, nullable=True)

    actualizado_en = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    actualizado_por_id = Column(
        Integer,
        ForeignKey("configuracion.usuarios.id", ondelete="SET NULL"),
        nullable=True,
    )

    proceso = relationship("ProcesoCompra", back_populates="seguimiento")


# ---------------------------------------------------------------------------
# PlazoProceso — Control de plazos por etapa (LOSNCP)
# ---------------------------------------------------------------------------

class PlazoProceso(Base):
    __tablename__ = "plazo_proceso"
    __table_args__ = (
        CheckConstraint(
            "etapa IN ('PREPARATORIA','PRECONTRACTUAL','CONTRACTUAL','EJECUCION','LIQUIDACION')",
            name="ck_plazo_etapa",
        ),
        Index("idx_plazo_proceso_id", "proceso_id"),
        {"schema": "compras_publicas"},
    )

    id = Column(Integer, primary_key=True, index=True)
    proceso_id = Column(
        Integer,
        ForeignKey("compras_publicas.proceso_compra.id", ondelete="CASCADE"),
        nullable=False,
    )
    etapa = Column(String(50), nullable=False)
    descripcion_actividad = Column(String(300), nullable=True)

    fecha_planificada = Column(Date, nullable=True)
    fecha_real = Column(Date, nullable=True)
    plazo_legal_dias = Column(Integer, nullable=True)
    plazo_planificado_dias = Column(Integer, nullable=True)
    dias_atraso = Column(Integer, nullable=False, default=0)

    cumplido = Column(Boolean, nullable=False, default=False)
    observaciones = Column(Text, nullable=True)

    creado_en = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    actualizado_en = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    proceso = relationship("ProcesoCompra", back_populates="plazos")


# ---------------------------------------------------------------------------
# ChecklistDocumental — Control documental por proceso
# ---------------------------------------------------------------------------

class ChecklistDocumental(Base):
    __tablename__ = "checklist_documental"
    __table_args__ = (
        CheckConstraint(
            "estado IN ('PENDIENTE','PRESENTADO','APROBADO','RECHAZADO')",
            name="ck_checklist_estado",
        ),
        {"schema": "compras_publicas"},
    )

    id = Column(Integer, primary_key=True, index=True)
    proceso_id = Column(
        Integer,
        ForeignKey("compras_publicas.proceso_compra.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    nombre_documento = Column(String(300), nullable=False)
    tipo_documento = Column(String(100), nullable=True)
    etapa = Column(String(50), nullable=True)
    obligatorio = Column(Boolean, nullable=False, default=True)
    estado = Column(String(20), nullable=False, default="PENDIENTE")
    fecha_presentacion = Column(Date, nullable=True)
    observaciones = Column(Text, nullable=True)

    creado_en = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    actualizado_en = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    proceso = relationship("ProcesoCompra", back_populates="documentos")
