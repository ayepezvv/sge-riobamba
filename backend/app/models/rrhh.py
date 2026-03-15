"""
Módulo: rrhh — Arquitectura V3 (Super Modelo + Motor de Cálculo)
Esquema: rrhh
Fuente de verdad: .agent/skills/sge-rrhh-nomina/resources/02_ddl_esquema_rrhh_v3.sql
                  + campos enriquecidos de Fase 1 (codigo_sercop, firma, etc.)
Fase 1 scope: estructura organizacional + directorio de personal.
"""
from sqlalchemy import (
    Column, BigInteger, Integer, String, Boolean, ForeignKey,
    Date, DateTime, Numeric, Text, UniqueConstraint
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base


# ---------------------------------------------------------------------------
# MOTOR DE CÁLCULOS
# ---------------------------------------------------------------------------

class ParametroCalculo(Base):
    """Almacena valores globales por año: SBU, % IESS, etc."""
    __tablename__ = "parametro_calculo"
    __table_args__ = (
        UniqueConstraint("anio_vigencia", "codigo_parametro", name="uq_parametro_anio_codigo_rrhh"),
        {"schema": "rrhh"},
    )

    id_parametro = Column(BigInteger, primary_key=True, autoincrement=True)
    anio_vigencia = Column(Integer, nullable=False)
    codigo_parametro = Column(String(50), nullable=False)
    descripcion = Column(String(150), nullable=True)
    valor_numerico = Column(Numeric(15, 6), nullable=True)
    valor_texto = Column(String(255), nullable=True)
    estado = Column(String(20), default="ACTIVO")


class ImpuestoRentaEscala(Base):
    """Tabla progresiva del SRI por año vigente."""
    __tablename__ = "impuesto_renta_escala"
    __table_args__ = {"schema": "rrhh"}

    id_escala = Column(BigInteger, primary_key=True, autoincrement=True)
    anio_vigencia = Column(Integer, nullable=False)
    fraccion_basica = Column(Numeric(12, 2), nullable=False)
    exceso_hasta = Column(Numeric(12, 2), nullable=True)
    impuesto_fraccion_basica = Column(Numeric(12, 2), nullable=False)
    porcentaje_fraccion_excedente = Column(Numeric(5, 2), nullable=False)


# ---------------------------------------------------------------------------
# ESTRUCTURA ORGANIZACIONAL
# ---------------------------------------------------------------------------

class AreaOrganizacional(Base):
    """Organigrama dinámico con recursividad (Dirección > Departamento > Unidad)."""
    __tablename__ = "area_organizacional"
    __table_args__ = {"schema": "rrhh"}

    id_area = Column(BigInteger, primary_key=True, autoincrement=True)
    id_area_padre = Column(BigInteger, ForeignKey("rrhh.area_organizacional.id_area"), nullable=True)
    tipo_area = Column(String(50), nullable=False)  # DIRECCION, DEPARTAMENTO, UNIDAD
    nombre = Column(String(150), nullable=False)
    estado = Column(String(20), default="ACTIVO")

    padre = relationship("AreaOrganizacional", remote_side=[id_area], backref="hijos")
    empleados_historial = relationship("HistorialLaboral", back_populates="area")


class EscalaSalarial(Base):
    """Catálogo legal de salarios (SP1, SP2, CT1, etc.)."""
    __tablename__ = "escala_salarial"
    __table_args__ = {"schema": "rrhh"}

    id_escala = Column(BigInteger, primary_key=True, autoincrement=True)
    grado = Column(String(20), nullable=False)
    salario_base = Column(Numeric(10, 2), nullable=False)
    regimen_laboral = Column(String(50), nullable=False)

    cargos = relationship("Cargo", back_populates="escala")


class Cargo(Base):
    """Catálogo de puestos institucionales vinculado a escala salarial."""
    __tablename__ = "cargo"
    __table_args__ = {"schema": "rrhh"}

    id_cargo = Column(BigInteger, primary_key=True, autoincrement=True)
    nombre_cargo = Column(String(150), nullable=False)
    id_escala_salarial = Column(BigInteger, ForeignKey("rrhh.escala_salarial.id_escala"), nullable=True)
    partida_presupuestaria = Column(String(100), nullable=True)
    estado = Column(String(20), default="ACTIVO")

    escala = relationship("EscalaSalarial", back_populates="cargos")
    empleados_historial = relationship("HistorialLaboral", back_populates="cargo")


# ---------------------------------------------------------------------------
# SUPER MODELO EMPLEADO (V3 + Campos Enriquecidos)
# ---------------------------------------------------------------------------

class Empleado(Base):
    """
    Tabla central del directorio de personal — Súper Modelo V3.
    Combina estructura base V3 + campos robustos de Fase 1:
      - codigo_sercop, archivo_firma_electronica, foto_perfil
      - regimen_legal, tipo_contrato_actual (string enums al estilo DDL V3)
      - auditoría: creado_por_id, actualizado_por_id → configuracion.usuarios
    Soft Delete: estado_empleado = 'DESVINCULADO' + eliminado_en.
    """
    __tablename__ = "empleado"
    __table_args__ = {"schema": "rrhh"}

    id_empleado = Column(BigInteger, primary_key=True, autoincrement=True)

    # Identificación
    tipo_identificacion = Column(String(20), default="CEDULA")
    identificacion = Column(String(20), unique=True, nullable=False, index=True)

    # Datos personales
    nombres = Column(String(100), nullable=False)
    apellidos = Column(String(100), nullable=False)
    fecha_nacimiento = Column(Date, nullable=False)
    genero = Column(String(20), nullable=True)  # MASCULINO, FEMENINO, OTRO

    # Datos laborales y previsionales (V3 base)
    porcentaje_discapacidad = Column(Numeric(5, 2), default=0)
    aplica_iess = Column(Boolean, default=True)
    acumula_fondos_reserva = Column(Boolean, default=True)
    acumula_decimos = Column(Boolean, default=False)

    # --- Campos enriquecidos (Fase 1 robusta) ---
    regimen_legal = Column(String(50), nullable=True)         # LOEP, CODIGO_TRABAJO
    tipo_contrato_actual = Column(String(50), nullable=True)  # NOMBRAMIENTO, INDEFINIDO, ...
    codigo_sercop = Column(String(100), nullable=True)
    archivo_firma_electronica = Column(String, nullable=True)

    # Datos de contacto
    telefono_celular = Column(String(20), nullable=True)
    correo_personal = Column(String(100), nullable=True)
    direccion_domicilio = Column(String(255), nullable=True)
    foto_perfil = Column(String, nullable=True)

    # Vinculación al sistema de usuarios (nullable)
    usuario_id = Column(
        BigInteger,
        ForeignKey("configuracion.usuarios.id", ondelete="SET NULL"),
        nullable=True, unique=True
    )

    # Estado y soft delete
    estado_empleado = Column(String(50), default="ACTIVO")
    eliminado_en = Column(DateTime(timezone=True), nullable=True)

    # Auditoría (FK a configuracion.usuarios)
    creado_por_id = Column(
        BigInteger,
        ForeignKey("configuracion.usuarios.id", ondelete="SET NULL"),
        nullable=True
    )
    actualizado_por_id = Column(
        BigInteger,
        ForeignKey("configuracion.usuarios.id", ondelete="SET NULL"),
        nullable=True
    )
    creado_en = Column(DateTime(timezone=True), server_default=func.now())
    actualizado_en = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # -----------------------------------------------------------------------
    # RELACIONES — foreign_keys explícitos para evitar ambigüedad (3 FKs → usuarios)
    # -----------------------------------------------------------------------
    usuario = relationship("User", foreign_keys=[usuario_id], backref="rrhh_empleado")
    creado_por = relationship("User", foreign_keys=[creado_por_id])
    actualizado_por = relationship("User", foreign_keys=[actualizado_por_id])
    cargas = relationship("EmpleadoCargaFamiliar", back_populates="empleado",
                          cascade="all, delete-orphan")
    historial = relationship("HistorialLaboral", back_populates="empleado",
                             cascade="all, delete-orphan",
                             order_by="HistorialLaboral.fecha_inicio.desc()")


# ---------------------------------------------------------------------------
# TABLAS SATÉLITE
# ---------------------------------------------------------------------------

class EmpleadoCargaFamiliar(Base):
    """Cargas familiares. Fundamental para cálculo de Renta y Utilidades."""
    __tablename__ = "empleado_carga_familiar"
    __table_args__ = {"schema": "rrhh"}

    id_carga = Column(BigInteger, primary_key=True, autoincrement=True)
    id_empleado = Column(BigInteger, ForeignKey("rrhh.empleado.id_empleado", ondelete="CASCADE"),
                         nullable=False)
    identificacion = Column(String(20), nullable=True)
    nombres_completos = Column(String(200), nullable=False)
    parentesco = Column(String(50), nullable=False)  # HIJO, CONYUGE, DISCAPACITADO
    fecha_nacimiento = Column(Date, nullable=False)
    aplica_deduccion_ir = Column(Boolean, default=True)
    estado = Column(String(20), default="ACTIVO")

    empleado = relationship("Empleado", back_populates="cargas")


class HistorialLaboral(Base):
    """
    Registro cronológico de posiciones del empleado (Effective Dating).
    Nunca se hace UPDATE de cargo/salario: se cierra el registro con fecha_fin
    y se inserta uno nuevo con fecha_inicio.
    """
    __tablename__ = "historial_laboral"
    __table_args__ = {"schema": "rrhh"}

    id_historial = Column(BigInteger, primary_key=True, autoincrement=True)
    id_empleado = Column(BigInteger, ForeignKey("rrhh.empleado.id_empleado", ondelete="CASCADE"),
                         nullable=False)
    id_area = Column(BigInteger, ForeignKey("rrhh.area_organizacional.id_area"), nullable=False)
    id_cargo = Column(BigInteger, ForeignKey("rrhh.cargo.id_cargo"), nullable=False)
    tipo_contrato = Column(String(50), nullable=False)
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=True)  # NULL = registro vigente
    salario_acordado = Column(Numeric(10, 2), nullable=False)

    empleado = relationship("Empleado", back_populates="historial")
    area = relationship("AreaOrganizacional", back_populates="empleados_historial")
    cargo = relationship("Cargo", back_populates="empleados_historial")


# ---------------------------------------------------------------------------
# MOTOR DE RUBROS (estructura — lógica de cálculo en Fase 2)
# ---------------------------------------------------------------------------

class RubroNomina(Base):
    """Catálogo de ingresos/descuentos con fórmulas dinámicas."""
    __tablename__ = "rubro_nomina"
    __table_args__ = {"schema": "rrhh"}

    id_rubro = Column(BigInteger, primary_key=True, autoincrement=True)
    codigo_rubro = Column(String(20), unique=True, nullable=False)
    nombre = Column(String(100), nullable=False)
    naturaleza = Column(String(20), nullable=False)  # INGRESO, DESCUENTO, PROVISION
    tipo_valor = Column(String(20), nullable=False)   # FIJO, PORCENTAJE, FORMULA
    formula_calculo = Column(Text, nullable=True)
    orden_ejecucion = Column(Integer, nullable=False)
    es_imponible = Column(Boolean, default=True)
    estado = Column(String(20), default="ACTIVO")
