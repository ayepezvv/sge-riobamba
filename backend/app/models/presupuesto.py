"""
Módulo: presupuesto — Gestión Presupuestaria SGE
Esquema: presupuesto
Basado en: OpenERP budget_ext + SIGEF Ecuador
Versión: 1.0 — YXP-10

Ciclo presupuestario ecuatoriano:
  PartidaPresupuestaria → AsignacionPresupuestaria → CertificadoPresupuestario → Compromiso → Devengado → Pago
"""
from sqlalchemy import (
    Column, BigInteger, Integer, String, Boolean, Numeric, Text,
    ForeignKey, Date, DateTime, UniqueConstraint, CheckConstraint, Index
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base


# ---------------------------------------------------------------------------
# CATÁLOGO: PARTIDAS PRESUPUESTARIAS (SIGEF Ecuador)
# ---------------------------------------------------------------------------

class PartidaPresupuestaria(Base):
    """
    Catálogo oficial de partidas presupuestarias según clasificador SIGEF.
    Estructura jerárquica: Grupo > Subgrupo > Item > Subitem.
    Ejemplo: 5.1.01.05.001 — Remuneraciones Unificadas
    """
    __tablename__ = "partidas_presupuestarias"
    __table_args__ = (
        UniqueConstraint("codigo", name="uq_partida_codigo"),
        {"schema": "presupuesto"},
    )

    id_partida = Column(BigInteger, primary_key=True, autoincrement=True)
    codigo = Column(String(30), nullable=False, index=True)         # ej: 5.1.01.05.001
    nombre = Column(String(255), nullable=False)
    descripcion = Column(Text, nullable=True)
    tipo = Column(String(20), nullable=False)                        # INGRESO, GASTO
    nivel = Column(Integer, nullable=False)                          # 1-5 niveles SIGEF
    es_hoja = Column(Boolean, default=True)                          # solo hojas permiten movimientos
    id_partida_padre = Column(
        BigInteger,
        ForeignKey("presupuesto.partidas_presupuestarias.id_partida"),
        nullable=True
    )
    estado = Column(String(20), default="ACTIVO")                   # ACTIVO, INACTIVO
    creado_en = Column(DateTime(timezone=True), server_default=func.now())

    padre = relationship("PartidaPresupuestaria", remote_side=[id_partida], backref="hijos")
    asignaciones = relationship("AsignacionPresupuestaria", back_populates="partida")


# ---------------------------------------------------------------------------
# PRESUPUESTO ANUAL
# ---------------------------------------------------------------------------

class PresupuestoAnual(Base):
    """
    Presupuesto institucional aprobado por ejercicio fiscal.
    Un solo presupuesto APROBADO por año (SIGEF no permite duplicados).
    """
    __tablename__ = "presupuestos_anuales"
    __table_args__ = (
        UniqueConstraint("anio_fiscal", "estado", name="uq_presupuesto_anio_aprobado"),
        {"schema": "presupuesto"},
    )

    id_presupuesto = Column(BigInteger, primary_key=True, autoincrement=True)
    anio_fiscal = Column(Integer, nullable=False, index=True)
    denominacion = Column(String(255), nullable=False)
    monto_inicial = Column(Numeric(18, 2), nullable=False, default=0)
    monto_codificado = Column(Numeric(18, 2), nullable=False, default=0)  # tras reformas
    estado = Column(String(20), default="BORRADOR")     # BORRADOR, APROBADO, LIQUIDADO, CERRADO
    fecha_aprobacion = Column(Date, nullable=True)
    resolucion_aprobacion = Column(String(100), nullable=True)
    observaciones = Column(Text, nullable=True)
    creado_en = Column(DateTime(timezone=True), server_default=func.now())
    actualizado_en = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    asignaciones = relationship("AsignacionPresupuestaria", back_populates="presupuesto")


# ---------------------------------------------------------------------------
# ASIGNACIÓN PRESUPUESTARIA (Partida × Presupuesto Anual)
# ---------------------------------------------------------------------------

class AsignacionPresupuestaria(Base):
    """
    Asignación de monto a una partida presupuestaria dentro de un ejercicio.
    Incluye control de reformas: cada modificación genera una nueva línea
    de reforma manteniendo el historial de cambios.
    """
    __tablename__ = "asignaciones_presupuestarias"
    __table_args__ = (
        UniqueConstraint("id_presupuesto", "id_partida", name="uq_asignacion_presupuesto_partida"),
        {"schema": "presupuesto"},
    )

    id_asignacion = Column(BigInteger, primary_key=True, autoincrement=True)
    id_presupuesto = Column(
        BigInteger,
        ForeignKey("presupuesto.presupuestos_anuales.id_presupuesto", ondelete="RESTRICT"),
        nullable=False
    )
    id_partida = Column(
        BigInteger,
        ForeignKey("presupuesto.partidas_presupuestarias.id_partida", ondelete="RESTRICT"),
        nullable=False
    )
    monto_inicial = Column(Numeric(18, 2), nullable=False, default=0)
    monto_codificado = Column(Numeric(18, 2), nullable=False, default=0)  # = inicial ± reformas
    monto_comprometido = Column(Numeric(18, 2), nullable=False, default=0)
    monto_devengado = Column(Numeric(18, 2), nullable=False, default=0)
    monto_pagado = Column(Numeric(18, 2), nullable=False, default=0)
    estado = Column(String(20), default="ACTIVO")
    creado_en = Column(DateTime(timezone=True), server_default=func.now())

    presupuesto = relationship("PresupuestoAnual", back_populates="asignaciones")
    partida = relationship("PartidaPresupuestaria", back_populates="asignaciones")
    certificados = relationship("CertificadoPresupuestario", back_populates="asignacion")
    reformas = relationship("ReformaPresupuestaria", back_populates="asignacion")


# ---------------------------------------------------------------------------
# REFORMA PRESUPUESTARIA
# ---------------------------------------------------------------------------

class ReformaPresupuestaria(Base):
    """
    Registro de modificaciones al presupuesto (traspasos, suplementos, reducciones).
    RN-PRES-01: Toda reforma debe estar respaldada por resolución.
    """
    __tablename__ = "reformas_presupuestarias"
    __table_args__ = {"schema": "presupuesto"}

    id_reforma = Column(BigInteger, primary_key=True, autoincrement=True)
    id_asignacion = Column(
        BigInteger,
        ForeignKey("presupuesto.asignaciones_presupuestarias.id_asignacion"),
        nullable=False
    )
    tipo_reforma = Column(String(30), nullable=False)   # TRASPASO, SUPLEMENTO, REDUCCION
    monto = Column(Numeric(18, 2), nullable=False)      # positivo = aumento, negativo = reducción
    numero_resolucion = Column(String(100), nullable=False)
    fecha_resolucion = Column(Date, nullable=False)
    motivo = Column(Text, nullable=True)
    estado = Column(String(20), default="APROBADO")
    creado_en = Column(DateTime(timezone=True), server_default=func.now())

    asignacion = relationship("AsignacionPresupuestaria", back_populates="reformas")


# ---------------------------------------------------------------------------
# CERTIFICADO PRESUPUESTARIO
# ---------------------------------------------------------------------------

class CertificadoPresupuestario(Base):
    """
    Certificación de disponibilidad presupuestaria previa a todo gasto.
    RN-03: Ningún compromiso puede crearse sin certificado aprobado.
    Basado en OpenERP: budget_certificate (30.898 registros históricos).
    """
    __tablename__ = "certificados_presupuestarios"
    __table_args__ = (
        UniqueConstraint("numero_certificado", name="uq_certificado_numero"),
        {"schema": "presupuesto"},
    )

    id_certificado = Column(BigInteger, primary_key=True, autoincrement=True)
    numero_certificado = Column(String(50), nullable=False, index=True)  # ej: CERT-2025-00001
    id_asignacion = Column(
        BigInteger,
        ForeignKey("presupuesto.asignaciones_presupuestarias.id_asignacion"),
        nullable=False
    )
    monto_certificado = Column(Numeric(18, 2), nullable=False)
    concepto = Column(Text, nullable=False)
    fecha_solicitud = Column(Date, nullable=False)
    fecha_certificacion = Column(Date, nullable=True)
    fecha_vencimiento = Column(Date, nullable=True)
    estado = Column(String(20), default="SOLICITADO")
    # SOLICITADO → APROBADO → COMPROMETIDO → DEVENGADO → LIQUIDADO | ANULADO
    motivo_anulacion = Column(Text, nullable=True)
    # Referencia al proceso que originó el certificado
    referencia_tipo = Column(String(50), nullable=True)   # CONTRATACION, NOMINA, SERVICIO_BASICO
    referencia_id = Column(BigInteger, nullable=True)
    # FK opcional a proceso de contratación
    id_proceso_contratacion = Column(
        BigInteger,
        ForeignKey("contratacion.proceso_contratacion.id", ondelete="SET NULL"),
        nullable=True
    )
    creado_en = Column(DateTime(timezone=True), server_default=func.now())
    actualizado_en = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    asignacion = relationship("AsignacionPresupuestaria", back_populates="certificados")
    compromisos = relationship("Compromiso", back_populates="certificado")


# ---------------------------------------------------------------------------
# COMPROMISO PRESUPUESTARIO
# ---------------------------------------------------------------------------

class Compromiso(Base):
    """
    Compromiso formal de gasto — etapa posterior al certificado.
    Vincula el presupuesto con una obligación concreta (contrato, orden de compra).
    RN-PRES-02: Un compromiso no puede superar el monto del certificado.
    """
    __tablename__ = "compromisos"
    __table_args__ = {"schema": "presupuesto"}

    id_compromiso = Column(BigInteger, primary_key=True, autoincrement=True)
    id_certificado = Column(
        BigInteger,
        ForeignKey("presupuesto.certificados_presupuestarios.id_certificado"),
        nullable=False
    )
    numero_compromiso = Column(String(50), nullable=False, index=True)
    monto_comprometido = Column(Numeric(18, 2), nullable=False)
    concepto = Column(Text, nullable=False)
    fecha_compromiso = Column(Date, nullable=False)
    estado = Column(String(20), default="ACTIVO")         # ACTIVO, DEVENGADO, ANULADO
    motivo_anulacion = Column(Text, nullable=True)
    creado_en = Column(DateTime(timezone=True), server_default=func.now())

    certificado = relationship("CertificadoPresupuestario", back_populates="compromisos")
    devengados = relationship("Devengado", back_populates="compromiso")


# ---------------------------------------------------------------------------
# DEVENGADO PRESUPUESTARIO
# ---------------------------------------------------------------------------

class Devengado(Base):
    """
    Reconocimiento del gasto devengado — etapa final del ciclo presupuestario.
    Se registra cuando la obligación es exigible (bien recibido, servicio prestado).
    RN-PRES-03: El devengado genera automáticamente un asiento contable.
    FK a contabilidad.asientos_contables para trazabilidad completa.
    """
    __tablename__ = "devengados"
    __table_args__ = {"schema": "presupuesto"}

    id_devengado = Column(BigInteger, primary_key=True, autoincrement=True)
    id_compromiso = Column(
        BigInteger,
        ForeignKey("presupuesto.compromisos.id_compromiso"),
        nullable=False
    )
    numero_devengado = Column(String(50), nullable=False, index=True)
    monto_devengado = Column(Numeric(18, 2), nullable=False)
    concepto = Column(Text, nullable=False)
    fecha_devengado = Column(Date, nullable=False)
    estado = Column(String(20), default="REGISTRADO")    # REGISTRADO, PAGADO, ANULADO
    # FK a contabilidad para asiento automático (RN-PRES-03)
    id_asiento_contable = Column(
        BigInteger,
        ForeignKey("contabilidad.asientos_contables.id", ondelete="SET NULL"),
        nullable=True
    )
    # FK a factura proveedor (financiero)
    id_factura = Column(
        BigInteger,
        ForeignKey("financiero.facturas.id", ondelete="SET NULL"),
        nullable=True
    )
    motivo_anulacion = Column(Text, nullable=True)
    creado_en = Column(DateTime(timezone=True), server_default=func.now())

    compromiso = relationship("Compromiso", back_populates="devengados")
