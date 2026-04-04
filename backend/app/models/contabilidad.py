"""
Módulo: contabilidad
Esquema PostgreSQL: contabilidad
Reglas de negocio aplicadas:
  RN-01: Plan de cuentas SIGEF Ecuador (hasta 10 niveles jerárquicos)
  RN-02: Vinculación cuenta ↔ partida presupuestaria
  RN-10: Cierre contable con validación de asientos cuadrados
  RN-11: Estado ANULADO como estado permanente (no eliminación física)
"""
import enum
from sqlalchemy import (
    Column, Integer, BigInteger, String, Boolean, Date,
    DateTime, Numeric, Text, ForeignKey, CheckConstraint, UniqueConstraint
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base
from app.models.mixins import AuditMixin


# ---------------------------------------------------------------------------
# Enumeraciones
# ---------------------------------------------------------------------------

class NaturalezaCuenta(str, enum.Enum):
    DEUDORA = "DEUDORA"
    ACREEDORA = "ACREEDORA"


class EstadoCuenta(str, enum.Enum):
    ACTIVA = "ACTIVA"
    INACTIVA = "INACTIVA"


class TipoDiario(str, enum.Enum):
    GENERAL = "GENERAL"
    VENTAS = "VENTAS"
    COMPRAS = "COMPRAS"
    BANCO = "BANCO"
    CAJA = "CAJA"
    APERTURA = "APERTURA"
    CIERRE = "CIERRE"
    AJUSTE = "AJUSTE"


class EstadoPeriodo(str, enum.Enum):
    ABIERTO = "ABIERTO"
    CERRADO = "CERRADO"
    BLOQUEADO = "BLOQUEADO"


class EstadoAsiento(str, enum.Enum):
    BORRADOR = "BORRADOR"
    PUBLICADO = "PUBLICADO"
    ANULADO = "ANULADO"


# ---------------------------------------------------------------------------
# TipoCuenta — Clasificación de cuentas del plan SIGEF
# ---------------------------------------------------------------------------

class TipoCuenta(AuditMixin, Base):
    __tablename__ = "tipos_cuenta"
    __table_args__ = (
        UniqueConstraint("codigo", name="uq_tipos_cuenta_codigo"),
        {"schema": "contabilidad"},
    )

    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String(10), nullable=False)
    nombre = Column(String(100), nullable=False)
    naturaleza = Column(
        String(10),
        nullable=False,
        comment="DEUDORA (activo/gasto) o ACREEDORA (pasivo/patrimonio/ingreso)"
    )
    descripcion = Column(String(255), nullable=True)

    cuentas = relationship("CuentaContable", back_populates="tipo_cuenta")


# ---------------------------------------------------------------------------
# CuentaContable — Plan de Cuentas SIGEF (hasta 10 niveles)
# ---------------------------------------------------------------------------

class CuentaContable(AuditMixin, Base):
    __tablename__ = "cuentas_contables"
    __table_args__ = (
        UniqueConstraint("codigo", name="uq_cuentas_contables_codigo"),
        CheckConstraint("nivel BETWEEN 1 AND 10", name="chk_nivel_cuenta"),
        {"schema": "contabilidad"},
    )

    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String(50), nullable=False, index=True,
                    comment="Código jerárquico SIGEF, ej: 1.1.1.01.01.001")
    nombre = Column(String(200), nullable=False)
    descripcion = Column(Text, nullable=True)

    tipo_cuenta_id = Column(
        Integer,
        ForeignKey("contabilidad.tipos_cuenta.id", ondelete="RESTRICT"),
        nullable=False
    )
    cuenta_padre_id = Column(
        Integer,
        ForeignKey("contabilidad.cuentas_contables.id", ondelete="RESTRICT"),
        nullable=True,
        comment="NULL para cuentas raíz (nivel 1)"
    )

    nivel = Column(Integer, nullable=False, comment="Nivel jerárquico 1-10")
    es_hoja = Column(Boolean, nullable=False, default=True,
                     comment="True = cuenta de detalle que acepta movimientos")
    permite_movimientos = Column(Boolean, nullable=False, default=True,
                                  comment="Solo True en cuentas hoja")
    partida_presupuestaria = Column(String(100), nullable=True,
                                    comment="RN-02: vínculo con partida presupuestaria SIGEF")
    estado = Column(String(10), nullable=False, default=EstadoCuenta.ACTIVA,
                    comment="ACTIVA | INACTIVA")

    # Relaciones
    tipo_cuenta = relationship("TipoCuenta", back_populates="cuentas")
    cuenta_padre = relationship("CuentaContable", remote_side="CuentaContable.id",
                                 back_populates="subcuentas")
    subcuentas = relationship("CuentaContable", back_populates="cuenta_padre")
    lineas_asiento = relationship("LineaAsiento", back_populates="cuenta")


# ---------------------------------------------------------------------------
# Diario — Libro diario contable
# ---------------------------------------------------------------------------

class Diario(AuditMixin, Base):
    __tablename__ = "diarios"
    __table_args__ = (
        UniqueConstraint("codigo", name="uq_diarios_codigo"),
        {"schema": "contabilidad"},
    )

    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String(20), nullable=False)
    nombre = Column(String(100), nullable=False)
    tipo = Column(String(20), nullable=False, default=TipoDiario.GENERAL,
                  comment="GENERAL|VENTAS|COMPRAS|BANCO|CAJA|APERTURA|CIERRE|AJUSTE")
    cuenta_default_id = Column(
        Integer,
        ForeignKey("contabilidad.cuentas_contables.id", ondelete="SET NULL"),
        nullable=True,
        comment="Cuenta contraparte por defecto para este diario"
    )
    es_activo = Column(Boolean, nullable=False, default=True)

    cuenta_default = relationship("CuentaContable", foreign_keys=[cuenta_default_id])
    asientos = relationship("AsientoContable", back_populates="diario")


# ---------------------------------------------------------------------------
# PeriodoContable — Control de periodos abiertos/cerrados
# ---------------------------------------------------------------------------

class PeriodoContable(AuditMixin, Base):
    __tablename__ = "periodos_contables"
    __table_args__ = (
        UniqueConstraint("anio", "mes", name="uq_periodos_anio_mes"),
        CheckConstraint("mes BETWEEN 1 AND 12", name="chk_mes_periodo"),
        {"schema": "contabilidad"},
    )

    id = Column(Integer, primary_key=True, index=True)
    anio = Column(Integer, nullable=False)
    mes = Column(Integer, nullable=False)
    nombre = Column(String(50), nullable=False, comment="Ej: Enero 2026")
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=False)
    estado = Column(String(10), nullable=False, default=EstadoPeriodo.ABIERTO,
                    comment="ABIERTO | CERRADO | BLOQUEADO")

    asientos = relationship("AsientoContable", back_populates="periodo")


# ---------------------------------------------------------------------------
# AsientoContable — Asiento (cabecera del Journal Entry)
# ---------------------------------------------------------------------------

class AsientoContable(AuditMixin, Base):
    __tablename__ = "asientos_contables"
    __table_args__ = (
        UniqueConstraint("numero", name="uq_asientos_numero"),
        {"schema": "contabilidad"},
    )

    id = Column(Integer, primary_key=True, index=True)
    numero = Column(String(30), nullable=False, index=True,
                    comment="Número secuencial generado al publicar: DIARIO/PERIODO/SEQ")
    diario_id = Column(
        Integer,
        ForeignKey("contabilidad.diarios.id", ondelete="RESTRICT"),
        nullable=False
    )
    periodo_id = Column(
        Integer,
        ForeignKey("contabilidad.periodos_contables.id", ondelete="RESTRICT"),
        nullable=False
    )
    fecha = Column(Date, nullable=False)
    referencia = Column(String(100), nullable=True,
                        comment="Número de documento origen (factura, cheque, etc.)")
    concepto = Column(Text, nullable=False, comment="Descripción del asiento")
    estado = Column(String(10), nullable=False, default=EstadoAsiento.BORRADOR,
                    comment="BORRADOR | PUBLICADO | ANULADO (RN-11)")

    # Totales denormalizados para reportes rápidos (se actualizan al publicar)
    total_debe = Column(Numeric(18, 2), nullable=False, default=0,
                        comment="Suma de todos los débitos de las líneas")
    total_haber = Column(Numeric(18, 2), nullable=False, default=0,
                         comment="Suma de todos los créditos de las líneas")

    usuario_id = Column(
        Integer,
        ForeignKey("configuracion.usuarios.id", ondelete="SET NULL"),
        nullable=True
    )
    fecha_publicacion = Column(DateTime(timezone=True), nullable=True)
    motivo_anulacion = Column(Text, nullable=True, comment="RN-11: razón del estado ANULADO")

    # Relaciones
    diario = relationship("Diario", back_populates="asientos")
    periodo = relationship("PeriodoContable", back_populates="asientos")
    lineas = relationship("LineaAsiento", back_populates="asiento",
                          cascade="all, delete-orphan",
                          order_by="LineaAsiento.orden")


# ---------------------------------------------------------------------------
# LineaAsiento — Línea de asiento (Journal Entry Line)
# ---------------------------------------------------------------------------

class LineaAsiento(AuditMixin, Base):
    __tablename__ = "lineas_asiento"
    __table_args__ = (
        CheckConstraint(
            "(debe >= 0 AND haber >= 0) AND NOT (debe > 0 AND haber > 0)",
            name="chk_linea_debe_o_haber"
        ),
        {"schema": "contabilidad"},
    )

    id = Column(Integer, primary_key=True, index=True)
    asiento_id = Column(
        Integer,
        ForeignKey("contabilidad.asientos_contables.id", ondelete="CASCADE"),
        nullable=False
    )
    cuenta_id = Column(
        Integer,
        ForeignKey("contabilidad.cuentas_contables.id", ondelete="RESTRICT"),
        nullable=False
    )
    descripcion = Column(String(255), nullable=True)
    debe = Column(Numeric(18, 2), nullable=False, default=0,
                  comment="Valor débito (solo uno de debe/haber puede ser > 0)")
    haber = Column(Numeric(18, 2), nullable=False, default=0,
                   comment="Valor crédito (solo uno de debe/haber puede ser > 0)")
    orden = Column(Integer, nullable=False, default=1)

    # Relaciones
    asiento = relationship("AsientoContable", back_populates="lineas")
    cuenta = relationship("CuentaContable", back_populates="lineas_asiento")


# ---------------------------------------------------------------------------
# ParametroContable — Parámetros de configuración para asientos automáticos
# (YXP-21: auto-asientos)
# ---------------------------------------------------------------------------

class ParametroContable(AuditMixin, Base):
    """
    Tabla de parámetros clave→cuenta/diario para generación automática de asientos.

    Claves predefinidas:
      CUENTA_CXC            — Cuenta por cobrar (AR) por defecto
      CUENTA_CXP            — Cuenta por pagar (AP) por defecto
      CUENTA_IVA_COBRADO    — IVA en ventas (haber al aprobar factura cliente)
      CUENTA_IVA_PAGADO     — IVA en compras (debe al aprobar factura proveedor)
      CUENTA_CAJA_RECAUDACION — Caja de recaudación diaria
      CUENTA_BCE_CUT        — Cuenta Única del Tesoro BCE
      DIARIO_VENTAS         — Diario para facturas de venta
      DIARIO_COMPRAS        — Diario para facturas de compra
      DIARIO_BANCO          — Diario para pagos/cobros bancarios
      DIARIO_CAJA           — Diario para operaciones de caja
      DIARIO_PRESUPUESTO    — Diario para asientos de ejecución presupuestaria
    """
    __tablename__ = "parametros_contables"
    __table_args__ = (
        UniqueConstraint("clave", name="uq_parametros_contables_clave"),
        {"schema": "contabilidad"},
    )

    id = Column(Integer, primary_key=True, index=True)
    clave = Column(String(50), nullable=False, index=True,
                   comment="Identificador único del parámetro, ej: CUENTA_CXC")
    descripcion = Column(String(255), nullable=True)

    # Un parámetro puede apuntar a una cuenta o a un diario (solo uno a la vez)
    cuenta_id = Column(
        Integer,
        ForeignKey("contabilidad.cuentas_contables.id", ondelete="RESTRICT"),
        nullable=True,
        comment="Cuenta contable asociada (NULL si es parámetro de diario)"
    )
    diario_id = Column(
        Integer,
        ForeignKey("contabilidad.diarios.id", ondelete="RESTRICT"),
        nullable=True,
        comment="Diario asociado (NULL si es parámetro de cuenta)"
    )

    # Relaciones
    cuenta = relationship("CuentaContable", foreign_keys=[cuenta_id])
    diario = relationship("Diario", foreign_keys=[diario_id])
