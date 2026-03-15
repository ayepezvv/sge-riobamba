from pydantic import BaseModel, Field, field_validator
import ipaddress
from typing import Optional

# SegmentoRed Schemas
class SegmentoRedBase(BaseModel):
    id: Optional[str] = None
    nombre: str = Field(..., description="Nombre del segmento ej: VLAN 10")
    red_cidr: str = Field(..., description="Bloque CIDR ej: 192.168.1.0/24")
    descripcion: Optional[str] = None
    is_active: bool = True

    @field_validator('red_cidr')
    def validate_cidr(cls, v):
        try:
            ipaddress.IPv4Network(v, strict=False)
        except ValueError:
            raise ValueError(f"'{v}' no es un CIDR IPv4 válido")
        return v

class SegmentoRedCreate(SegmentoRedBase):
    pass

class SegmentoRedUpdate(BaseModel):
    nombre: Optional[str] = None
    red_cidr: Optional[str] = None
    descripcion: Optional[str] = None
    is_active: Optional[bool] = None

    @field_validator('red_cidr')
    def validate_cidr(cls, v):
        if v is not None:
            try:
                ipaddress.IPv4Network(v, strict=False)
            except ValueError:
                raise ValueError(f"'{v}' no es un CIDR IPv4 válido")
        return v

class SegmentoRed(SegmentoRedBase):
    class Config:
        from_attributes = True

# DireccionIpAsignada Schemas
class DireccionIpAsignadaBase(BaseModel):
    id: Optional[str] = None
    segmento_id: str
    direccion_ip: str
    mac_address: Optional[str] = None
    nombre_equipo: Optional[str] = None
    dominio: Optional[str] = None
    ubicacion_geografica: Optional[str] = None
    personal_id: Optional[int] = None
    activo_id: Optional[int] = None
    is_active: bool = True

    @field_validator('direccion_ip')
    def validate_ip(cls, v):
        try:
            ipaddress.IPv4Address(v)
        except ValueError:
            raise ValueError(f"'{v}' no es una dirección IPv4 válida")
        return v

class DireccionIpAsignadaCreate(DireccionIpAsignadaBase):
    pass

class DireccionIpAsignadaUpdate(BaseModel):
    segmento_id: Optional[str] = None
    direccion_ip: Optional[str] = None
    mac_address: Optional[str] = None
    nombre_equipo: Optional[str] = None
    dominio: Optional[str] = None
    ubicacion_geografica: Optional[str] = None
    personal_id: Optional[int] = None
    activo_id: Optional[int] = None
    is_active: Optional[bool] = None

    @field_validator('direccion_ip')
    def validate_ip(cls, v):
        if v is not None:
            try:
                ipaddress.IPv4Address(v)
            except ValueError:
                raise ValueError(f"'{v}' no es una dirección IPv4 válida")
        return v

class EmpleadoMinimo(BaseModel):
    id: int
    nombres: str
    apellidos: str
    # En el nuevo modelo Empleado, el cargo se obtiene de Puesto.denominacion, 
    # pero para compatibilidad mantendremos el esquema o lo ajustaremos.
    # El modelo Empleado ya no tiene el campo string 'cargo'.
    # Usaremos una representación básica.

    class Config:
        from_attributes = True

class ActivoMinimo(BaseModel):
    id: int
    codigo_inventario: str
    marca: Optional[str] = None
    modelo: Optional[str] = None
    numero_serie: Optional[str] = None

    class Config:
        from_attributes = True

class DireccionIpAsignada(DireccionIpAsignadaBase):
    empleado: Optional[EmpleadoMinimo] = None
    activo: Optional[ActivoMinimo] = None
    class Config:
        from_attributes = True
