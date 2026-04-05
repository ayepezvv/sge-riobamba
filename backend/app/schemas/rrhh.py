"""
Schemas Pydantic — Módulo RRHH V3 (Súper Modelo)
Esquema: rrhh
"""
from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Optional, List
from datetime import date, datetime
from decimal import Decimal


# ---------------------------------------------------------------------------
# ÁREA ORGANIZACIONAL
# ---------------------------------------------------------------------------
class AreaOrganizacionalBase(BaseModel):
    id_area_padre: Optional[int] = None
    tipo_area: str = Field(..., max_length=50)
    nombre: str = Field(..., max_length=150)
    estado: str = "ACTIVO"

class AreaOrganizacionalCreate(AreaOrganizacionalBase):
    pass

class AreaOrganizacionalUpdate(BaseModel):
    id_area_padre: Optional[int] = None
    tipo_area: Optional[str] = None
    nombre: Optional[str] = None
    estado: Optional[str] = None

class AreaOrganizacionalResponse(AreaOrganizacionalBase):
    id_area: int
    model_config = ConfigDict(from_attributes=True)


# ---------------------------------------------------------------------------
# ESCALA SALARIAL
# ---------------------------------------------------------------------------
class EscalaSalarialBase(BaseModel):
    grado: str = Field(..., max_length=20)
    salario_base: Decimal = Field(..., gt=0)
    regimen_laboral: str = Field(..., max_length=50)

class EscalaSalarialCreate(EscalaSalarialBase):
    pass

class EscalaSalarialResponse(EscalaSalarialBase):
    id_escala: int
    model_config = ConfigDict(from_attributes=True)


# ---------------------------------------------------------------------------
# CARGO
# ---------------------------------------------------------------------------
class CargoBase(BaseModel):
    nombre_cargo: str = Field(..., max_length=150)
    id_escala_salarial: Optional[int] = None
    partida_presupuestaria: Optional[str] = Field(None, max_length=100)
    estado: str = "ACTIVO"

class CargoCreate(CargoBase):
    pass

class CargoUpdate(BaseModel):
    nombre_cargo: Optional[str] = None
    id_escala_salarial: Optional[int] = None
    partida_presupuestaria: Optional[str] = None
    estado: Optional[str] = None

class CargoResponse(CargoBase):
    id_cargo: int
    escala: Optional[EscalaSalarialResponse] = None
    model_config = ConfigDict(from_attributes=True)


# ---------------------------------------------------------------------------
# HISTORIAL LABORAL
# ---------------------------------------------------------------------------
class HistorialLaboralBase(BaseModel):
    id_area: int
    id_cargo: int
    tipo_contrato: str = Field(..., max_length=50)
    fecha_inicio: date
    fecha_fin: Optional[date] = None
    salario_acordado: Decimal = Field(..., gt=0)

class HistorialLaboralCreate(HistorialLaboralBase):
    id_empleado: int

class HistorialLaboralResponse(HistorialLaboralBase):
    id_historial: int
    id_empleado: int
    area: Optional[AreaOrganizacionalResponse] = None
    cargo: Optional[CargoResponse] = None
    model_config = ConfigDict(from_attributes=True)


# ---------------------------------------------------------------------------
# CARGA FAMILIAR
# ---------------------------------------------------------------------------
class CargaFamiliarBase(BaseModel):
    identificacion: Optional[str] = Field(None, max_length=20)
    nombres_completos: str = Field(..., max_length=200)
    parentesco: str = Field(..., max_length=50)
    fecha_nacimiento: date
    aplica_deduccion_ir: bool = True
    estado: str = "ACTIVO"

class CargaFamiliarCreate(CargaFamiliarBase):
    id_empleado: int

class CargaFamiliarResponse(CargaFamiliarBase):
    id_carga: int
    id_empleado: int
    model_config = ConfigDict(from_attributes=True)


# ---------------------------------------------------------------------------
# EMPLEADO — Súper Modelo V3
# ---------------------------------------------------------------------------
class EmpleadoBase(BaseModel):
    # Identificación
    tipo_identificacion: str = "CEDULA"
    identificacion: str = Field(..., max_length=20)
    # Datos personales
    nombres: str = Field(..., max_length=100)
    apellidos: str = Field(..., max_length=100)
    fecha_nacimiento: date
    genero: Optional[str] = Field(None, max_length=20)       # MASCULINO, FEMENINO, OTRO
    # Previsional V3
    porcentaje_discapacidad: Decimal = Decimal("0.00")
    aplica_iess: bool = True
    acumula_fondos_reserva: bool = True
    acumula_decimos: bool = False
    # Campos enriquecidos
    regimen_legal: Optional[str] = Field(None, max_length=50)             # LOEP, CODIGO_TRABAJO
    tipo_contrato_actual: Optional[str] = Field(None, max_length=50)      # NOMBRAMIENTO, ...
    codigo_sercop: Optional[str] = Field(None, max_length=100)
    archivo_firma_electronica: Optional[str] = None
    # Contacto
    telefono_celular: Optional[str] = Field(None, max_length=20)
    correo_personal: Optional[str] = Field(None, max_length=100)
    direccion_domicilio: Optional[str] = Field(None, max_length=255)
    foto_perfil: Optional[str] = None
    # Vinculación sistema
    usuario_id: Optional[int] = None
    # Estado
    estado_empleado: str = "ACTIVO"

class EmpleadoCreate(EmpleadoBase):
    pass

class EmpleadoUpdate(BaseModel):
    tipo_identificacion: Optional[str] = None
    identificacion: Optional[str] = None
    nombres: Optional[str] = None
    apellidos: Optional[str] = None
    fecha_nacimiento: Optional[date] = None
    genero: Optional[str] = None
    porcentaje_discapacidad: Optional[Decimal] = None
    aplica_iess: Optional[bool] = None
    acumula_fondos_reserva: Optional[bool] = None
    acumula_decimos: Optional[bool] = None
    regimen_legal: Optional[str] = None
    tipo_contrato_actual: Optional[str] = None
    codigo_sercop: Optional[str] = None
    archivo_firma_electronica: Optional[str] = None
    telefono_celular: Optional[str] = None
    correo_personal: Optional[str] = None
    direccion_domicilio: Optional[str] = None
    foto_perfil: Optional[str] = None
    usuario_id: Optional[int] = None
    estado_empleado: Optional[str] = None

class EmpleadoResponse(EmpleadoBase):
    id_empleado: int
    creado_en: Optional[datetime] = None
    actualizado_en: Optional[datetime] = None
    cargas: List[CargaFamiliarResponse] = []
    historial: List[HistorialLaboralResponse] = []
    model_config = ConfigDict(from_attributes=True)

# =========================================================================
# CONTRATOS
# =========================================================================
class ContratoBase(BaseModel):
    id_empleado: int
    id_escala_salarial: Optional[int] = None
    id_cargo: int
    tipo_contrato: str
    fecha_inicio: date
    fecha_fin: Optional[date] = None
    sueldo_pactado: Decimal
    estado_contrato: Optional[str] = "ACTIVO"
    observaciones: Optional[str] = None

class ContratoCreate(ContratoBase):
    pass

class ContratoUpdate(BaseModel):
    fecha_fin: Optional[date] = None
    estado_contrato: Optional[str] = None
    observaciones: Optional[str] = None

class ContratoResponse(ContratoBase):
    id_contrato: int
    empleado: Optional[EmpleadoResponse] = None
    cargo: Optional[CargoResponse] = None
    escala: Optional[EscalaSalarialResponse] = None
    model_config = ConfigDict(from_attributes=True)

# =========================================================================
# PARAMETROS NOMINA
# =========================================================================
class ParametroCalculoBase(BaseModel):
    anio_vigencia: int
    codigo_parametro: str
    descripcion: Optional[str] = None
    valor_numerico: Optional[Decimal] = None
    valor_texto: Optional[str] = None
    estado: Optional[str] = "ACTIVO"

class ParametroCalculoCreate(ParametroCalculoBase):
    pass

class ParametroCalculoResponse(ParametroCalculoBase):
    id_parametro: int
    model_config = ConfigDict(from_attributes=True)


# ---------------------------------------------------------------------------
# RUBRO NÓMINA
# ---------------------------------------------------------------------------
class RubroNominaBase(BaseModel):
    codigo_rubro: str = Field(..., max_length=20)
    nombre: str = Field(..., max_length=100)
    naturaleza: str = Field(..., description="INGRESO|DESCUENTO|PROVISION")
    tipo_valor: str = Field(..., description="FIJO|PORCENTAJE|FORMULA")
    formula_calculo: Optional[str] = None
    orden_ejecucion: int
    es_imponible: bool = True
    estado: str = "ACTIVO"

class RubroNominaCreate(RubroNominaBase):
    pass

class RubroNominaResponse(RubroNominaBase):
    id_rubro: int
    model_config = ConfigDict(from_attributes=True)


# ---------------------------------------------------------------------------
# ROL DE PAGOS
# ---------------------------------------------------------------------------
class RolPagoCreate(BaseModel):
    periodo_anio: int = Field(..., ge=2020, le=2099)
    periodo_mes: int = Field(..., ge=1, le=12)
    tipo_rol: str = Field("MENSUAL", description="MENSUAL|DECIMO_TERCERO|DECIMO_CUARTO|FONDOS_RESERVA|LIQUIDACION")
    observaciones: Optional[str] = None

class RolPagoResponse(BaseModel):
    id_rol_pago: int
    periodo_anio: int
    periodo_mes: int
    tipo_rol: str
    estado: str
    fecha_generacion: Optional[date]
    fecha_aprobacion: Optional[date]
    observaciones: Optional[str]
    creado_en: Optional[datetime]
    model_config = ConfigDict(from_attributes=True)


# ---------------------------------------------------------------------------
# LÍNEA ROL DE PAGOS
# ---------------------------------------------------------------------------
class DetalleLineaRolResponse(BaseModel):
    id_detalle: int
    id_rubro: int
    codigo_rubro: str
    nombre_rubro: str
    naturaleza: str
    valor_calculado: Decimal
    descripcion_calculo: Optional[str]
    model_config = ConfigDict(from_attributes=True)


class LineaRolPagoUpdate(BaseModel):
    banco_destino: Optional[str] = None
    cuenta_bancaria: Optional[str] = None
    tipo_cuenta: Optional[str] = None

class LineaRolPagoResponse(BaseModel):
    id_linea: int
    id_rol_pago: int
    id_empleado: int
    sueldo_base: Decimal
    dias_trabajados: int
    total_ingresos: Decimal
    total_descuentos: Decimal
    total_provisiones: Decimal
    liquido_a_recibir: Decimal
    banco_destino: Optional[str]
    cuenta_bancaria: Optional[str]
    tipo_cuenta: Optional[str]
    estado: str
    detalles: List[DetalleLineaRolResponse] = []
    model_config = ConfigDict(from_attributes=True)


class RolPagoDetalleResponse(RolPagoResponse):
    lineas: List[LineaRolPagoResponse] = []
