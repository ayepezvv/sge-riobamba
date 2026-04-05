"""
Módulo: tesoreria
Esquema PostgreSQL: tesoreria
Reglas de negocio aplicadas:
  RN-T01: Conciliación bancaria completamente custom con marcado por línea de asiento
  RN-T02: 23 tipos de transacción bancaria (IESS, SRI, BCE, SPI, etc.)
  RN-T03: Extractos bancarios ligados a cuenta bancaria institucional
  RN-T04: Estado CERRADO de conciliación es definitivo (no se reabre)
  RN-T05: Movimientos de caja con doble asiento (recaudación + traslado BCE)
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

class TipoTransaccion(str, enum.Enum):
    IESS = "IESS"
    SRI = "SRI"
    BCE = "BCE"
    SPI = "SPI"
    TRANSFERENCIA = "TRANSFERENCIA"
    CHEQUE = "CHEQUE"
    DEPOSITO = "DEPOSITO"
    DEBITO = "DEBITO"
    CREDITO = "CREDITO"
    NOTA_DEBITO = "NOTA_DEBITO"
    NOTA_CREDITO = "NOTA_CREDITO"
    RETENCION = "RETENCION"
    OTRO = "OTRO"


class EstadoExtracto(str, enum.Enum):
    BORRADOR = "BORRADOR"
    CONFIRMADO = "CONFIRMADO"
    CERRADO = "CERRADO"


class EstadoConciliacion(str, enum.Enum):
    ABIERTO = "ABIERTO"
    CERRADO = "CERRADO"


class TipoCuenta(str, enum.Enum):
    CORRIENTE = "CORRIENTE"
    AHORROS = "AHORROS"
    RECAUDACION = "RECAUDACION"
    PAGOS = "PAGOS"


class EstadoCaja(str, enum.Enum):
    ABIERTA = "ABIERTA"
    CERRADA = "CERRADA"


class TipoMovimientoCaja(str, enum.Enum):
    INGRESO = "INGRESO"
    EGRESO = "EGRESO"
    APERTURA = "APERTURA"
    CIERRE = "CIERRE"


# ---------------------------------------------------------------------------
# EntidadBancaria — Bancos e instituciones financieras
# ---------------------------------------------------------------------------

class EntidadBancaria(AuditMixin, Base):
    __tablename__ = "entidades_bancarias"
    __table_args__ = (
        UniqueConstraint("codigo", name="uq_entidades_bancarias_codigo"),
        {"schema": "tesoreria"},
    )

    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String(20), nullable=False)
    nombre = Column(String(150), nullable=False)
    sigla = Column(String(20), nullable=True)
    es_activa = Column(Boolean, nullable=False, default=True)

    cuentas_bancarias = relationship("CuentaBancaria", back_populates="entidad_bancaria")


# ---------------------------------------------------------------------------
# CuentaBancaria — Cuenta bancaria institucional
# ---------------------------------------------------------------------------

class CuentaBancaria(AuditMixin, Base):
    __tablename__ = "cuentas_bancarias"
    __table_args__ = (
        UniqueConstraint("numero_cuenta", name="uq_cuentas_bancarias_numero"),
        {"schema": "tesoreria"},
    )

    id = Column(Integer, primary_key=True, index=True)
    entidad_bancaria_id = Column(
        Integer,
        ForeignKey("tesoreria.entidades_bancarias.id", ondelete="RESTRICT"),
        nullable=False
    )
    numero_cuenta = Column(String(50), nullable=False, index=True)
    nombre = Column(String(200), nullable=False, comment="Nombre descriptivo de la cuenta")
    tipo = Column(String(20), nullable=False, default=TipoCuenta.CORRIENTE,
                  comment="CORRIENTE|AHORROS|RECAUDACION|PAGOS")
    moneda = Column(String(3), nullable=False, default="USD")
    # Vinculación con plan de cuentas contable
    cuenta_contable_id = Column(
        Integer,
        ForeignKey("contabilidad.cuentas_contables.id", ondelete="SET NULL"),
        nullable=True,
        comment="Cuenta contable asociada para asientos automáticos"
    )
    saldo_inicial = Column(Numeric(18, 2), nullable=False, default=0)
    es_activa = Column(Boolean, nullable=False, default=True)

    # Relaciones
    entidad_bancaria = relationship("EntidadBancaria", back_populates="cuentas_bancarias")
    extractos = relationship("ExtractoBancario", back_populates="cuenta_bancaria")
    conciliaciones = relationship("ConciliacionBancaria", back_populates="cuenta_bancaria")


# ---------------------------------------------------------------------------
# ExtractoBancario — Estado de cuenta bancario (cabecera)
# ---------------------------------------------------------------------------

class ExtractoBancario(AuditMixin, Base):
    __tablename__ = "extractos_bancarios"
    __table_args__ = (
        UniqueConstraint("cuenta_bancaria_id", "fecha_inicio", "fecha_fin",
                         name="uq_extracto_cuenta_periodo"),
        {"schema": "tesoreria"},
    )

    id = Column(Integer, primary_key=True, index=True)
    cuenta_bancaria_id = Column(
        Integer,
        ForeignKey("tesoreria.cuentas_bancarias.id", ondelete="RESTRICT"),
        nullable=False
    )
    referencia = Column(String(100), nullable=True, comment="Número de extracto del banco")
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=False)
    saldo_inicial = Column(Numeric(18, 2), nullable=False, default=0)
    saldo_final = Column(Numeric(18, 2), nullable=False, default=0)
    estado = Column(String(15), nullable=False, default=EstadoExtracto.BORRADOR,
                    comment="BORRADOR | CONFIRMADO | CERRADO")

    # Relaciones
    cuenta_bancaria = relationship("CuentaBancaria", back_populates="extractos")
    lineas = relationship("LineaExtracto", back_populates="extracto",
                          cascade="all, delete-orphan",
                          order_by="LineaExtracto.fecha")
    conciliaciones = relationship("ConciliacionBancaria", back_populates="extracto")


# ---------------------------------------------------------------------------
# LineaExtracto — Línea de extracto bancario
# ---------------------------------------------------------------------------

class LineaExtracto(AuditMixin, Base):
    __tablename__ = "lineas_extracto"
    __table_args__ = (
        {"schema": "tesoreria"},
    )

    id = Column(Integer, primary_key=True, index=True)
    extracto_id = Column(
        Integer,
        ForeignKey("tesoreria.extractos_bancarios.id", ondelete="CASCADE"),
        nullable=False
    )
    fecha = Column(Date, nullable=False)
    tipo_transaccion = Column(String(20), nullable=False, default=TipoTransaccion.OTRO,
                               comment="IESS|SRI|BCE|SPI|TRANSFERENCIA|CHEQUE|...")
    referencia = Column(String(100), nullable=True, comment="Número de transacción del banco")
    descripcion = Column(String(500), nullable=True)
    valor = Column(Numeric(18, 2), nullable=False,
                   comment="Positivo = crédito (ingreso), negativo = débito (salida)")
    esta_conciliada = Column(Boolean, nullable=False, default=False,
                              comment="RN-T01: marcado por el proceso de conciliación")

    # Relaciones
    extracto = relationship("ExtractoBancario", back_populates="lineas")
    marca_conciliacion = relationship("MarcaConciliacion", back_populates="linea_extracto",
                                       uselist=False)


# ---------------------------------------------------------------------------
# ConciliacionBancaria — Proceso de conciliación (RN-T01)
# ---------------------------------------------------------------------------

class ConciliacionBancaria(AuditMixin, Base):
    __tablename__ = "conciliaciones_bancarias"
    __table_args__ = (
        {"schema": "tesoreria"},
    )

    id = Column(Integer, primary_key=True, index=True)
    cuenta_bancaria_id = Column(
        Integer,
        ForeignKey("tesoreria.cuentas_bancarias.id", ondelete="RESTRICT"),
        nullable=False
    )
    extracto_id = Column(
        Integer,
        ForeignKey("tesoreria.extractos_bancarios.id", ondelete="RESTRICT"),
        nullable=True
    )
    nombre = Column(String(100), nullable=False, comment="Nombre descriptivo del proceso")
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=False)
    saldo_libro = Column(Numeric(18, 2), nullable=False, default=0,
                          comment="Saldo según libros contables")
    saldo_banco = Column(Numeric(18, 2), nullable=False, default=0,
                          comment="Saldo según extracto bancario")
    diferencia = Column(Numeric(18, 2), nullable=False, default=0,
                         comment="saldo_banco - saldo_libro")
    estado = Column(String(10), nullable=False, default=EstadoConciliacion.ABIERTO,
                    comment="ABIERTO | CERRADO (RN-T04: CERRADO es definitivo)")
    observaciones = Column(Text, nullable=True)

    # Relaciones
    cuenta_bancaria = relationship("CuentaBancaria", back_populates="conciliaciones")
    extracto = relationship("ExtractoBancario", back_populates="conciliaciones")
    marcas = relationship("MarcaConciliacion", back_populates="conciliacion",
                          cascade="all, delete-orphan")


# ---------------------------------------------------------------------------
# MarcaConciliacion — Marcado de líneas ya conciliadas (RN-T01)
# ---------------------------------------------------------------------------

class MarcaConciliacion(AuditMixin, Base):
    __tablename__ = "marcas_conciliacion"
    __table_args__ = (
        UniqueConstraint("linea_extracto_id", name="uq_marca_linea_extracto"),
        {"schema": "tesoreria"},
    )

    id = Column(Integer, primary_key=True, index=True)
    conciliacion_id = Column(
        Integer,
        ForeignKey("tesoreria.conciliaciones_bancarias.id", ondelete="CASCADE"),
        nullable=False
    )
    linea_extracto_id = Column(
        Integer,
        ForeignKey("tesoreria.lineas_extracto.id", ondelete="CASCADE"),
        nullable=False
    )
    # Referencia al asiento contable correspondiente (cross-schema FK)
    asiento_contable_id = Column(
        Integer,
        ForeignKey("contabilidad.asientos_contables.id", ondelete="SET NULL"),
        nullable=True,
        comment="Asiento contable que originó esta transacción"
    )
    valor_conciliado = Column(Numeric(18, 2), nullable=False)
    observacion = Column(String(255), nullable=True)

    # Relaciones
    conciliacion = relationship("ConciliacionBancaria", back_populates="marcas")
    linea_extracto = relationship("LineaExtracto", back_populates="marca_conciliacion")


# ---------------------------------------------------------------------------
# CajaChica — Caja chica / Fondo rotativo
# ---------------------------------------------------------------------------

class CajaChica(AuditMixin, Base):
    __tablename__ = "cajas_chicas"
    __table_args__ = (
        UniqueConstraint("codigo", name="uq_cajas_chicas_codigo"),
        {"schema": "tesoreria"},
    )

    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String(20), nullable=False)
    nombre = Column(String(150), nullable=False)
    monto_fijo = Column(Numeric(18, 2), nullable=False, default=0,
                         comment="Monto asignado del fondo fijo")
    monto_disponible = Column(Numeric(18, 2), nullable=False, default=0,
                               comment="Saldo actual disponible")
    # Vinculación con plan de cuentas contable
    cuenta_contable_id = Column(
        Integer,
        ForeignKey("contabilidad.cuentas_contables.id", ondelete="SET NULL"),
        nullable=True
    )
    responsable_id = Column(
        Integer,
        ForeignKey("configuracion.usuarios.id", ondelete="SET NULL"),
        nullable=True
    )
    estado = Column(String(10), nullable=False, default=EstadoCaja.CERRADA,
                    comment="ABIERTA | CERRADA")

    movimientos = relationship("MovimientoCaja", back_populates="caja")


# ---------------------------------------------------------------------------
# MovimientoCaja — Movimiento de caja chica
# ---------------------------------------------------------------------------

class MovimientoCaja(AuditMixin, Base):
    __tablename__ = "movimientos_caja"
    __table_args__ = (
        CheckConstraint("monto > 0", name="chk_movimiento_monto_positivo"),
        {"schema": "tesoreria"},
    )

    id = Column(Integer, primary_key=True, index=True)
    caja_id = Column(
        Integer,
        ForeignKey("tesoreria.cajas_chicas.id", ondelete="RESTRICT"),
        nullable=False
    )
    fecha = Column(Date, nullable=False)
    tipo = Column(String(15), nullable=False,
                  comment="INGRESO|EGRESO|APERTURA|CIERRE")
    concepto = Column(String(500), nullable=False)
    monto = Column(Numeric(18, 2), nullable=False)
    numero_comprobante = Column(String(50), nullable=True)
    beneficiario = Column(String(200), nullable=True)
    # Referencia al asiento contable generado (RN-T05)
    asiento_contable_id = Column(
        Integer,
        ForeignKey("contabilidad.asientos_contables.id", ondelete="SET NULL"),
        nullable=True,
        comment="RN-T05: asiento contable generado automáticamente"
    )

    caja = relationship("CajaChica", back_populates="movimientos")


# ---------------------------------------------------------------------------
# Enumeraciones SPI
# ---------------------------------------------------------------------------

class EstadoArchivoSpi(str, enum.Enum):
    BORRADOR = "BORRADOR"
    GENERADO = "GENERADO"
    ENVIADO = "ENVIADO"
    CONFIRMADO = "CONFIRMADO"
    RECHAZADO = "RECHAZADO"


class TipoPagoSpi(str, enum.Enum):
    NOMINA = "NOMINA"
    PROVEEDOR = "PROVEEDOR"
    IMPUESTO = "IMPUESTO"
    OTRO = "OTRO"


class EstadoLineaSpi(str, enum.Enum):
    PENDIENTE = "PENDIENTE"
    PROCESADO = "PROCESADO"
    RECHAZADO = "RECHAZADO"


class OrigenLineaSpi(str, enum.Enum):
    NOMINA = "NOMINA"
    CXP = "CXP"
    OTRO = "OTRO"


# ---------------------------------------------------------------------------
# ArchivoSpi — Cabecera de cada lote SPI enviado al BCE
# ---------------------------------------------------------------------------

class ArchivoSpi(AuditMixin, Base):
    __tablename__ = "archivo_spi"
    __table_args__ = (
        UniqueConstraint("numero_lote", name="uq_archivo_spi_numero_lote"),
        {"schema": "tesoreria"},
    )

    id_archivo_spi = Column(BigInteger, primary_key=True, autoincrement=True)
    numero_lote = Column(String(30), nullable=False, index=True)
    fecha_envio = Column(Date, nullable=True)
    estado = Column(String(20), nullable=False, default=EstadoArchivoSpi.BORRADOR,
                    comment="BORRADOR|GENERADO|ENVIADO|CONFIRMADO|RECHAZADO")
    monto_total = Column(Numeric(18, 2), nullable=False, default=0)
    id_cuenta_bancaria = Column(
        Integer,
        ForeignKey("tesoreria.cuentas_bancarias.id", ondelete="RESTRICT"),
        nullable=False,
        comment="Cuenta bancaria origen del pago"
    )
    tipo_pago = Column(String(20), nullable=False,
                       comment="NOMINA|PROVEEDOR|IMPUESTO|OTRO")
    ruta_archivo = Column(String(500), nullable=True,
                          comment="Ruta en el servidor del TXT generado")
    nombre_archivo = Column(String(200), nullable=True)
    creado_en = Column(DateTime(timezone=True), server_default=func.now())

    cuenta_bancaria = relationship("CuentaBancaria")
    lineas = relationship("LineaSpi", back_populates="archivo_spi",
                          cascade="all, delete-orphan",
                          order_by="LineaSpi.id_linea_spi")


# ---------------------------------------------------------------------------
# LineaSpi — Cada fila del archivo SPI
# ---------------------------------------------------------------------------

class LineaSpi(AuditMixin, Base):
    __tablename__ = "linea_spi"
    __table_args__ = (
        {"schema": "tesoreria"},
    )

    id_linea_spi = Column(BigInteger, primary_key=True, autoincrement=True)
    id_archivo_spi = Column(
        BigInteger,
        ForeignKey("tesoreria.archivo_spi.id_archivo_spi", ondelete="CASCADE"),
        nullable=False
    )
    ruc_beneficiario = Column(String(20), nullable=False)
    nombre_beneficiario = Column(String(200), nullable=False)
    banco_destino = Column(String(100), nullable=False)
    cuenta_destino = Column(String(30), nullable=False)
    tipo_cuenta = Column(String(20), nullable=False, default="CORRIENTE",
                         comment="CORRIENTE|AHORROS")
    valor = Column(Numeric(12, 2), nullable=False)
    referencia = Column(String(50), nullable=True)
    descripcion = Column(String(200), nullable=True)
    estado = Column(String(20), nullable=False, default=EstadoLineaSpi.PENDIENTE,
                    comment="PENDIENTE|PROCESADO|RECHAZADO")
    origen_tipo = Column(String(10), nullable=False, default=OrigenLineaSpi.OTRO,
                         comment="NOMINA|CXP|OTRO")
    origen_id = Column(BigInteger, nullable=True,
                       comment="ID del objeto origen (id_linea_rol, id factura, etc.)")

    archivo_spi = relationship("ArchivoSpi", back_populates="lineas")
