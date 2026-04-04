"""
Módulo: financiero
Esquema PostgreSQL: financiero
Reglas de negocio aplicadas:
  RN-F01: CXP usa budget_certificate + account_voucher + SPI (no invoice estándar OpenERP)
  RN-F02: Sistema de recaudación con cierre único por día (UNIQUE date)
  RN-F03: Doble asiento: recaudación + traslado BCE
  RN-F04: Estado ANULADO permanente (no eliminación física)
  RN-F05: Integración automática con Contabilidad (asiento generado al publicar)
"""
import enum
from sqlalchemy import (
    Column, Integer, String, Boolean, Date,
    DateTime, Numeric, Text, ForeignKey, CheckConstraint, UniqueConstraint
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base
from app.models.mixins import AuditMixin


# ---------------------------------------------------------------------------
# Enumeraciones
# ---------------------------------------------------------------------------

class TipoDocumentoFinanciero(str, enum.Enum):
    FACTURA = "FACTURA"
    NOTA_CREDITO = "NOTA_CREDITO"
    NOTA_DEBITO = "NOTA_DEBITO"
    LIQUIDACION = "LIQUIDACION"
    PROFORMA = "PROFORMA"
    CERTIFICADO_PRESUPUESTARIO = "CERTIFICADO_PRESUPUESTARIO"


class TipoFactura(str, enum.Enum):
    CLIENTE = "CLIENTE"   # Cuentas por Cobrar (AR)
    PROVEEDOR = "PROVEEDOR"  # Cuentas por Pagar (AP)


class EstadoFactura(str, enum.Enum):
    BORRADOR = "BORRADOR"
    APROBADA = "APROBADA"
    PAGADA = "PAGADA"
    PARCIAL = "PARCIAL"
    ANULADA = "ANULADA"


class TipoImpuesto(str, enum.Enum):
    IVA_15 = "IVA_15"
    IVA_12 = "IVA_12"
    IVA_5 = "IVA_5"
    IVA_0 = "IVA_0"
    EXENTO = "EXENTO"
    ICE = "ICE"


class TipoPago(str, enum.Enum):
    EFECTIVO = "EFECTIVO"
    CHEQUE = "CHEQUE"
    TRANSFERENCIA = "TRANSFERENCIA"
    SPI = "SPI"
    BCE = "BCE"
    NOTA_CREDITO = "NOTA_CREDITO"


class EstadoPago(str, enum.Enum):
    BORRADOR = "BORRADOR"
    CONFIRMADO = "CONFIRMADO"
    ANULADO = "ANULADO"


# ---------------------------------------------------------------------------
# TipoDocumentoConfig — Configuración de tipos de documento
# ---------------------------------------------------------------------------

class TipoDocumentoConfig(AuditMixin, Base):
    __tablename__ = "tipos_documento"
    __table_args__ = (
        UniqueConstraint("codigo", name="uq_tipos_documento_codigo"),
        {"schema": "financiero"},
    )

    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String(10), nullable=False)
    nombre = Column(String(100), nullable=False)
    tipo = Column(String(30), nullable=False,
                  comment="FACTURA|NOTA_CREDITO|NOTA_DEBITO|LIQUIDACION|PROFORMA|CERTIFICADO_PRESUPUESTARIO")
    secuencia_prefijo = Column(String(10), nullable=True, comment="Prefijo para numeración, ej: FAC-")
    secuencia_siguiente = Column(Integer, nullable=False, default=1)
    es_activo = Column(Boolean, nullable=False, default=True)

    facturas = relationship("Factura", back_populates="tipo_documento")


# ---------------------------------------------------------------------------
# Factura — Cabecera de factura (AR/AP)
# ---------------------------------------------------------------------------

class Factura(AuditMixin, Base):
    __tablename__ = "facturas"
    __table_args__ = (
        UniqueConstraint("numero", name="uq_facturas_numero"),
        {"schema": "financiero"},
    )

    id = Column(Integer, primary_key=True, index=True)
    numero = Column(String(50), nullable=False, index=True,
                    comment="Número secuencial generado al aprobar")
    tipo_documento_id = Column(
        Integer,
        ForeignKey("financiero.tipos_documento.id", ondelete="RESTRICT"),
        nullable=False
    )
    tipo = Column(String(15), nullable=False,
                  comment="CLIENTE (AR) | PROVEEDOR (AP)")
    estado = Column(String(10), nullable=False, default=EstadoFactura.BORRADOR,
                    comment="BORRADOR|APROBADA|PAGADA|PARCIAL|ANULADA (RN-F04)")

    # Tercero (ciudadano o proveedor del sistema)
    tercero_id = Column(Integer, nullable=True,
                         comment="ID del ciudadano o proveedor según tipo")
    nombre_tercero = Column(String(200), nullable=False,
                             comment="Nombre guardado al momento de emisión")
    identificacion_tercero = Column(String(20), nullable=False,
                                     comment="RUC/CI del tercero")

    fecha_emision = Column(Date, nullable=False)
    fecha_vencimiento = Column(Date, nullable=True)

    # Totales calculados
    subtotal = Column(Numeric(18, 2), nullable=False, default=0)
    descuento = Column(Numeric(18, 2), nullable=False, default=0)
    base_imponible = Column(Numeric(18, 2), nullable=False, default=0)
    total_iva = Column(Numeric(18, 2), nullable=False, default=0)
    total = Column(Numeric(18, 2), nullable=False, default=0)
    saldo_pendiente = Column(Numeric(18, 2), nullable=False, default=0,
                              comment="total - pagos aplicados")

    # Referencia a documento electrónico SRI (clave de acceso)
    clave_acceso_sri = Column(String(49), nullable=True,
                               comment="Clave de acceso del comprobante electrónico SRI")
    numero_autorizacion_sri = Column(String(49), nullable=True)

    # Integración contable (RN-F05)
    asiento_contable_id = Column(
        Integer,
        ForeignKey("contabilidad.asientos_contables.id", ondelete="SET NULL"),
        nullable=True,
        comment="RN-F05: asiento contable generado automáticamente al aprobar"
    )

    observaciones = Column(Text, nullable=True)
    motivo_anulacion = Column(Text, nullable=True, comment="RN-F04: motivo del estado ANULADA")

    # Relaciones
    tipo_documento = relationship("TipoDocumentoConfig", back_populates="facturas")
    lineas = relationship("LineaFactura", back_populates="factura",
                          cascade="all, delete-orphan",
                          order_by="LineaFactura.orden")
    pagos_aplicados = relationship("LineaPago", back_populates="factura")


# ---------------------------------------------------------------------------
# LineaFactura — Línea de detalle de factura
# ---------------------------------------------------------------------------

class LineaFactura(AuditMixin, Base):
    __tablename__ = "lineas_factura"
    __table_args__ = (
        CheckConstraint("cantidad > 0", name="chk_linea_factura_cantidad_positiva"),
        CheckConstraint("precio_unitario >= 0", name="chk_linea_factura_precio_no_negativo"),
        {"schema": "financiero"},
    )

    id = Column(Integer, primary_key=True, index=True)
    factura_id = Column(
        Integer,
        ForeignKey("financiero.facturas.id", ondelete="CASCADE"),
        nullable=False
    )
    orden = Column(Integer, nullable=False, default=1)
    descripcion = Column(String(500), nullable=False)

    # Cuenta contable de la línea
    cuenta_contable_id = Column(
        Integer,
        ForeignKey("contabilidad.cuentas_contables.id", ondelete="RESTRICT"),
        nullable=True,
        comment="Cuenta para el asiento automático"
    )

    cantidad = Column(Numeric(18, 4), nullable=False, default=1)
    precio_unitario = Column(Numeric(18, 4), nullable=False, default=0)
    descuento_linea = Column(Numeric(18, 2), nullable=False, default=0)
    tipo_impuesto = Column(String(10), nullable=False, default=TipoImpuesto.IVA_15,
                            comment="IVA_15|IVA_12|IVA_5|IVA_0|EXENTO|ICE")
    porcentaje_impuesto = Column(Numeric(5, 2), nullable=False, default=15,
                                  comment="Porcentaje del impuesto: 15, 12, 5, 0")
    subtotal_linea = Column(Numeric(18, 2), nullable=False, default=0,
                             comment="cantidad * precio_unitario - descuento_linea")
    valor_impuesto = Column(Numeric(18, 2), nullable=False, default=0,
                             comment="subtotal_linea * porcentaje_impuesto / 100")
    total_linea = Column(Numeric(18, 2), nullable=False, default=0,
                          comment="subtotal_linea + valor_impuesto")

    # Relaciones
    factura = relationship("Factura", back_populates="lineas")


# ---------------------------------------------------------------------------
# Pago — Cabecera de pago (AR/AP)
# ---------------------------------------------------------------------------

class Pago(AuditMixin, Base):
    __tablename__ = "pagos"
    __table_args__ = (
        UniqueConstraint("numero", name="uq_pagos_numero"),
        {"schema": "financiero"},
    )

    id = Column(Integer, primary_key=True, index=True)
    numero = Column(String(50), nullable=False, index=True)
    tipo = Column(String(15), nullable=False,
                  comment="CLIENTE (cobro AR) | PROVEEDOR (pago AP)")
    estado = Column(String(15), nullable=False, default=EstadoPago.BORRADOR,
                    comment="BORRADOR|CONFIRMADO|ANULADO (RN-F04)")

    # Tercero
    tercero_id = Column(Integer, nullable=True)
    nombre_tercero = Column(String(200), nullable=False)
    identificacion_tercero = Column(String(20), nullable=False)

    fecha_pago = Column(Date, nullable=False)
    tipo_pago = Column(String(20), nullable=False, default=TipoPago.TRANSFERENCIA,
                       comment="EFECTIVO|CHEQUE|TRANSFERENCIA|SPI|BCE|NOTA_CREDITO")

    # Cuenta bancaria usada en el pago
    cuenta_bancaria_id = Column(
        Integer,
        ForeignKey("tesoreria.cuentas_bancarias.id", ondelete="SET NULL"),
        nullable=True
    )

    monto_total = Column(Numeric(18, 2), nullable=False, default=0)
    referencia_bancaria = Column(String(100), nullable=True,
                                  comment="Número de transacción SPI/BCE/cheque")

    # Integración contable (RN-F05)
    asiento_contable_id = Column(
        Integer,
        ForeignKey("contabilidad.asientos_contables.id", ondelete="SET NULL"),
        nullable=True,
        comment="RN-F05: asiento contable generado automáticamente al confirmar"
    )
    # RN-F03: asiento de traslado BCE (cuando aplica)
    asiento_traslado_id = Column(
        Integer,
        ForeignKey("contabilidad.asientos_contables.id", ondelete="SET NULL"),
        nullable=True,
        comment="RN-F03: asiento de traslado BCE (recaudación → CUT)"
    )

    observaciones = Column(Text, nullable=True)
    motivo_anulacion = Column(Text, nullable=True, comment="RN-F04")

    # Relaciones
    lineas = relationship("LineaPago", back_populates="pago",
                          cascade="all, delete-orphan")


# ---------------------------------------------------------------------------
# LineaPago — Aplicación de pago a una factura
# ---------------------------------------------------------------------------

class LineaPago(AuditMixin, Base):
    __tablename__ = "lineas_pago"
    __table_args__ = (
        CheckConstraint("monto_aplicado > 0", name="chk_linea_pago_monto_positivo"),
        {"schema": "financiero"},
    )

    id = Column(Integer, primary_key=True, index=True)
    pago_id = Column(
        Integer,
        ForeignKey("financiero.pagos.id", ondelete="CASCADE"),
        nullable=False
    )
    factura_id = Column(
        Integer,
        ForeignKey("financiero.facturas.id", ondelete="RESTRICT"),
        nullable=False
    )
    monto_aplicado = Column(Numeric(18, 2), nullable=False,
                             comment="Monto de este pago aplicado a esta factura")

    # Relaciones
    pago = relationship("Pago", back_populates="lineas")
    factura = relationship("Factura", back_populates="pagos_aplicados")


# ---------------------------------------------------------------------------
# CierreRecaudacion — Cierre diario de recaudación (RN-F02)
# ---------------------------------------------------------------------------

class CierreRecaudacion(AuditMixin, Base):
    __tablename__ = "cierres_recaudacion"
    __table_args__ = (
        UniqueConstraint("fecha", name="uq_cierre_recaudacion_fecha",
                         comment="RN-F02: cierre único por día"),
        {"schema": "financiero"},
    )

    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(Date, nullable=False, unique=True,
                   comment="RN-F02: UNIQUE — un solo cierre por día")
    total_recaudado = Column(Numeric(18, 2), nullable=False, default=0)
    numero_transacciones = Column(Integer, nullable=False, default=0)

    # RN-F03: doble asiento
    asiento_recaudacion_id = Column(
        Integer,
        ForeignKey("contabilidad.asientos_contables.id", ondelete="SET NULL"),
        nullable=True,
        comment="RN-F03: asiento de recaudación del día"
    )
    asiento_traslado_bce_id = Column(
        Integer,
        ForeignKey("contabilidad.asientos_contables.id", ondelete="SET NULL"),
        nullable=True,
        comment="RN-F03: asiento de traslado a BCE"
    )

    observaciones = Column(Text, nullable=True)
