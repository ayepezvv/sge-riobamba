from pydantic import BaseModel, Field
from typing import Optional, List
from app.models.administrativo import TipoRegimenLegal, TipoContrato, NivelEducacion


# --- Puesto ---
class PuestoBase(BaseModel):
    denominacion: str = Field(..., max_length=150)
    escala_ocupacional: Optional[str] = Field(None, max_length=100)
    remuneracion_mensual: float
    partida_presupuestaria: str = Field(..., max_length=100)
    es_activo: bool = True

class PuestoCreate(PuestoBase):
    pass

class PuestoUpdate(BaseModel):
    denominacion: Optional[str] = Field(None, max_length=150)
    escala_ocupacional: Optional[str] = Field(None, max_length=100)
    remuneracion_mensual: Optional[float] = None
    partida_presupuestaria: Optional[str] = Field(None, max_length=100)
    es_activo: Optional[bool] = None

class PuestoResponse(PuestoBase):
    id: int

    class Config:
        from_attributes = True

# --- Direccion ---
class DireccionBase(BaseModel):
    nombre: str = Field(..., max_length=150)
    descripcion: Optional[str] = Field(None, max_length=255)
    es_activo: bool = True

class DireccionCreate(DireccionBase):
    pass

class DireccionUpdate(BaseModel):
    nombre: Optional[str] = Field(None, max_length=150)
    descripcion: Optional[str] = Field(None, max_length=255)
    es_activo: Optional[bool] = None

class DireccionResponse(DireccionBase):
    id: int

    class Config:
        from_attributes = True

# --- Unidad ---
class UnidadBase(BaseModel):
    direccion_id: int
    nombre: str = Field(..., max_length=150)
    descripcion: Optional[str] = Field(None, max_length=255)
    es_activo: bool = True

class UnidadCreate(UnidadBase):
    pass

class UnidadUpdate(BaseModel):
    direccion_id: Optional[int] = None
    nombre: Optional[str] = Field(None, max_length=150)
    descripcion: Optional[str] = Field(None, max_length=255)
    es_activo: Optional[bool] = None

class UnidadResponse(UnidadBase):
    id: int
    direccion: Optional[DireccionResponse] = None

    class Config:
        from_attributes = True


# --- TituloProfesional ---
class TituloProfesionalBase(BaseModel):
    nivel: NivelEducacion
    nombre_titulo: str = Field(..., max_length=200)
    institucion: str = Field(..., max_length=200)
    registro_senescyt: Optional[str] = Field(None, max_length=100)

class TituloProfesionalCreate(TituloProfesionalBase):
    personal_id: int

class TituloProfesionalResponse(TituloProfesionalBase):
    id: int
    personal_id: int

    class Config:
        from_attributes = True

# --- Personal ---
class PersonalBase(BaseModel):
    unidad_id: int
    usuario_id: Optional[int] = None
    puesto_id: Optional[int] = None
    cedula: str = Field(..., max_length=20)
    nombres: str = Field(..., max_length=100)
    apellidos: str = Field(..., max_length=100)
    cargo: str = Field(..., max_length=150)
    regimen_legal: TipoRegimenLegal
    tipo_contrato: TipoContrato
    codigo_certificacion_sercop: Optional[str] = Field(None, max_length=100)
    foto_perfil: Optional[str] = None
    direccion_domicilio: Optional[str] = Field(None, max_length=255)
    telefono_celular: Optional[str] = Field(None, max_length=20)
    correo_personal: Optional[str] = Field(None, max_length=100)
    archivo_firma_electronica: Optional[str] = None
    es_activo: bool = True

class PersonalCreate(PersonalBase):
    pass

class PersonalUpdate(BaseModel):
    unidad_id: Optional[int] = None
    usuario_id: Optional[int] = None
    puesto_id: Optional[int] = None
    cedula: Optional[str] = Field(None, max_length=20)
    nombres: Optional[str] = Field(None, max_length=100)
    apellidos: Optional[str] = Field(None, max_length=100)
    cargo: Optional[str] = Field(None, max_length=150)
    regimen_legal: Optional[TipoRegimenLegal] = None
    tipo_contrato: Optional[TipoContrato] = None
    codigo_certificacion_sercop: Optional[str] = Field(None, max_length=100)
    foto_perfil: Optional[str] = None
    direccion_domicilio: Optional[str] = Field(None, max_length=255)
    telefono_celular: Optional[str] = Field(None, max_length=20)
    correo_personal: Optional[str] = Field(None, max_length=100)
    archivo_firma_electronica: Optional[str] = None
    es_activo: Optional[bool] = None

class PersonalResponse(PersonalBase):
    id: int
    unidad: Optional[UnidadResponse] = None
    puesto: Optional[PuestoResponse] = None
    titulos: List[TituloProfesionalResponse] = []

    class Config:
        from_attributes = True
