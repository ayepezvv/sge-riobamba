from sqlalchemy import (
    Column, BigInteger, Integer, String, Numeric, DateTime,
    SmallInteger, Text, ForeignKey, Date, Boolean
)
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class CuentaContableInventario(Base):
    """Plan de cuentas de inventario (cuentas 131.xx y 132.xx del sector público)."""
    __tablename__ = "cuenta_contable"
    __table_args__ = {"schema": "inventario"}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    codigo_cuenta = Column(String(35), nullable=False, unique=True, index=True)
    nombre_cuenta = Column(String(60), nullable=False)
    tipo_movimiento = Column(SmallInteger, nullable=False, comment="1=solo movimiento, 2=nivel padre")
    nivel = Column(SmallInteger, nullable=False, comment="3=titulo, 6=grupo, 9=cuenta movible")
    cuenta_gasto = Column(String(35), nullable=True, comment="Cuenta de gasto relacionada 634.xx")

    articulos = relationship("ArticuloInventario", back_populates="cuenta_contable")


class Destino(Base):
    """Áreas o departamentos receptores de materiales de bodega."""
    __tablename__ = "destino"
    __table_args__ = {"schema": "inventario"}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    id_origen_mysql = Column(BigInteger, nullable=True, index=True, comment="INTDES en MySQL origen")
    nombre = Column(String(100), nullable=False)
    activo = Column(Boolean, default=True, nullable=False)

    movimientos = relationship("Movimiento", back_populates="destino")


class Encargado(Base):
    """Personal custodio o responsable de los movimientos de bodega."""
    __tablename__ = "encargado"
    __table_args__ = {"schema": "inventario"}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    id_origen_mysql = Column(BigInteger, nullable=True, index=True, comment="INTENC en MySQL origen")
    nombre = Column(String(100), nullable=False)
    cedula = Column(String(10), nullable=True)
    activo = Column(Boolean, default=True, nullable=False)

    movimientos = relationship("Movimiento", back_populates="encargado")


class Proveedor(Base):
    """Proveedores de bienes de inventario."""
    __tablename__ = "proveedor"
    __table_args__ = {"schema": "inventario"}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    id_origen_mysql = Column(BigInteger, nullable=True, index=True, comment="INTPRO en MySQL origen")
    nombre = Column(String(100), nullable=False)
    ruc_cedula = Column(String(13), nullable=True, index=True)
    direccion = Column(String(100), nullable=True)
    telefono = Column(String(15), nullable=True)
    contacto = Column(String(100), nullable=True)
    activo = Column(Boolean, default=True, nullable=False)

    movimientos = relationship("Movimiento", back_populates="proveedor")


class UnidadGestion(Base):
    """Estructura funcional / unidades de gestión de la EP-EMAPAR."""
    __tablename__ = "unidad_gestion"
    __table_args__ = {"schema": "inventario"}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    id_origen_mysql = Column(BigInteger, nullable=True, index=True, comment="INTEST en MySQL origen")
    codigo = Column(String(10), nullable=False, unique=True)
    nombre = Column(String(100), nullable=False)
    puede_mover = Column(Boolean, default=True, nullable=False, comment="1=puede generar movimientos")


class ArticuloInventario(Base):
    """Catálogo maestro de artículos/insumos del almacén."""
    __tablename__ = "articulo"
    __table_args__ = {"schema": "inventario"}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    id_origen_mysql = Column(BigInteger, nullable=True, index=True, comment="intart en MySQL origen")
    codigo_articulo = Column(String(8), nullable=False, unique=True, index=True,
                             comment="Código único alfanumérico de 8 chars: 3 letras + 4 dígitos")
    nombre = Column(String(100), nullable=False)
    descripcion_extendida = Column(String(254), nullable=True)
    codigo_cuenta = Column(String(35), ForeignKey("inventario.cuenta_contable.codigo_cuenta"),
                           nullable=False)
    unidad_medida = Column(String(10), nullable=True)
    existencia_inicial = Column(Numeric(18, 2), nullable=True)
    costo_inicial = Column(Numeric(18, 4), nullable=True)
    existencia_actual = Column(Numeric(18, 4), nullable=True)
    costo_actual = Column(Numeric(18, 4), nullable=False, default=0)
    valor_total = Column(Numeric(18, 4), nullable=True)
    stock_minimo = Column(Numeric(18, 2), nullable=True)
    stock_maximo = Column(Numeric(18, 2), nullable=True)
    codigo_barras = Column(String(45), nullable=True)
    anno_fiscal = Column(Integer, nullable=False, comment="Año fiscal de origen (2021-2025)")
    activo = Column(Boolean, default=True, nullable=False)
    usuario_crea = Column(String(50), nullable=True)
    creado_en = Column(DateTime, nullable=True)
    usuario_modifica = Column(String(50), nullable=True)
    modificado_en = Column(DateTime, nullable=True)

    cuenta_contable = relationship("CuentaContableInventario", back_populates="articulos")
    movimiento_detalles = relationship("MovimientoDetalle", back_populates="articulo")


class Movimiento(Base):
    """Cabecera de transacciones de inventario (entradas y salidas)."""
    __tablename__ = "movimiento"
    __table_args__ = {"schema": "inventario"}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    id_origen_mysql = Column(BigInteger, nullable=True, index=True, comment="INTMOV en MySQL origen")
    numero_movimiento = Column(Integer, nullable=False)
    fecha = Column(DateTime, nullable=False, index=True)
    tipo_movimiento = Column(String(10), nullable=False,
                             comment="ENTRADA o SALIDA")
    subtipo = Column(String(1), nullable=True, comment="R=Reversal, NULL=normal")
    costo_total = Column(Numeric(18, 4), nullable=True)
    numero_factura = Column(String(20), nullable=True)
    fecha_factura = Column(DateTime, nullable=True)
    comprobante_egreso = Column(String(20), nullable=True)
    observacion = Column(String(254), nullable=True)
    numero_entrada_ref = Column(BigInteger, nullable=True,
                                comment="Referencia al movimiento original en reversales")
    aprobado = Column(SmallInteger, nullable=True, default=0)
    anexo = Column(String(20), nullable=True)
    anno_fiscal = Column(Integer, nullable=False, comment="Año fiscal de origen (2021-2025)")
    id_proveedor = Column(BigInteger, ForeignKey("inventario.proveedor.id"), nullable=True)
    id_destino = Column(BigInteger, ForeignKey("inventario.destino.id"), nullable=True)
    id_encargado = Column(BigInteger, ForeignKey("inventario.encargado.id"), nullable=True)
    usuario_crea = Column(String(50), nullable=True)
    creado_en = Column(DateTime, nullable=True)

    proveedor = relationship("Proveedor", back_populates="movimientos")
    destino = relationship("Destino", back_populates="movimientos")
    encargado = relationship("Encargado", back_populates="movimientos")
    detalles = relationship("MovimientoDetalle", back_populates="movimiento")


class MovimientoDetalle(Base):
    """Líneas de movimiento / kardex: detalle de cada artículo por movimiento."""
    __tablename__ = "movimiento_detalle"
    __table_args__ = {"schema": "inventario"}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    id_origen_mysql = Column(BigInteger, nullable=True, index=True, comment="intartm en MySQL origen")
    id_movimiento = Column(BigInteger, ForeignKey("inventario.movimiento.id"),
                           nullable=False, index=True)
    id_articulo = Column(BigInteger, ForeignKey("inventario.articulo.id"),
                         nullable=False, index=True)
    fecha = Column(DateTime, nullable=False)
    tipo_movimiento = Column(String(10), nullable=False)
    cantidad = Column(Numeric(18, 2), nullable=False)
    costo_unitario = Column(Numeric(18, 4), nullable=False)
    total_linea = Column(Numeric(18, 4), nullable=True)
    costo_promedio = Column(Numeric(18, 4), nullable=True,
                            comment="Costo promedio ponderado resultante")
    anno_fiscal = Column(Integer, nullable=False)
    usuario_crea = Column(String(50), nullable=True)
    creado_en = Column(DateTime, nullable=True)

    movimiento = relationship("Movimiento", back_populates="detalles")
    articulo = relationship("ArticuloInventario", back_populates="movimiento_detalles")
