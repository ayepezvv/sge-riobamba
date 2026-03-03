from pydantic import BaseModel, EmailStr, field_validator, Field
from typing import Optional, Dict, Any, List
from datetime import date

# Funcion utilitaria para validacion Modulo 10 Ecuador (Cedula)
def validar_cedula_ecuador(cedula: str) -> bool:
    if len(cedula) != 10 or not cedula.isdigit():
        return False
    provincia = int(cedula[0:2])
    if provincia < 1 or provincia > 24:
        return False
    tercer_digito = int(cedula[2])
    if tercer_digito >= 6:
        return False # Solo personas naturales en este caso
    
    coeficientes = [2, 1, 2, 1, 2, 1, 2, 1, 2]
    suma = 0
    for i in range(9):
        valor = int(cedula[i]) * coeficientes[i]
        suma += valor if valor < 10 else valor - 9
    
    digito_verificador = (10 - (suma % 10)) % 10
    return digito_verificador == int(cedula[9])

class ReferenciaBase(BaseModel):
    tipo_referencia: str
    nombres: str
    apellidos: str
    identificacion: Optional[str] = None
    telefono: Optional[str] = None
    correo: Optional[EmailStr] = None

class ReferenciaCreate(ReferenciaBase):
    pass

class ReferenciaResponse(ReferenciaBase):
    id: int
    ciudadano_id: int
    class Config:
        from_attributes = True

class CiudadanoBase(BaseModel):
    tipo_persona: str = Field(..., description="'Natural' o 'Juridica'")
    identificacion: str
    nombres: Optional[str] = None
    apellidos: Optional[str] = None
    razon_social: Optional[str] = None
    correo_principal: Optional[EmailStr] = None
    telefono_fijo: Optional[str] = None
    celular: Optional[str] = None
    preferencia_contacto: Optional[str] = None
    redes_sociales: Optional[Dict[str, Any]] = None
    
    fecha_nacimiento: Optional[date] = None
    nacionalidad: Optional[str] = None
    genero: Optional[str] = None
    estado_civil: Optional[str] = None
    tiene_discapacidad: Optional[bool] = False
    porcentaje_discapacidad: Optional[float] = 0.0
    aplica_tercera_edad: Optional[bool] = False
    is_active: Optional[bool] = True
    
    tipo_empresa: Optional[str] = None
    naturaleza_juridica: Optional[str] = None

    @field_validator('identificacion')
    @classmethod
    def validar_identificacion(cls, v, info):
        # info.data contiene los valores previos validados (en Pydantic v2)
        tipo = info.data.get('tipo_persona')
        if tipo == 'Natural':
            if not validar_cedula_ecuador(v):
                raise ValueError('La cedula ecuatoriana no es valida (Falla en Modulo 10)')
        # Nota: Futura implementacion para RUC de empresas
        return v

class CiudadanoCreate(CiudadanoBase):
    referencias: Optional[List[ReferenciaCreate]] = []

class CiudadanoResponse(CiudadanoBase):
    id: int
    referencias: List[ReferenciaResponse] = []
    
    class Config:
        from_attributes = True
