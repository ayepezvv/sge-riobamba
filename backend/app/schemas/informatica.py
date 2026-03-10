from pydantic import BaseModel, Field, field_validator
import ipaddress
from typing import Optional

# SegmentoRed Schemas
class SegmentoRedBase(BaseModel):
    id: str
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
    id: str
    segmento_id: str
    direccion_ip: str
    mac_address: Optional[str] = None
    nombre_equipo: Optional[str] = None
    dominio: Optional[str] = None
    ubicacion_geografica: Optional[str] = None
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
    is_active: Optional[bool] = None

    @field_validator('direccion_ip')
    def validate_ip(cls, v):
        if v is not None:
            try:
                ipaddress.IPv4Address(v)
            except ValueError:
                raise ValueError(f"'{v}' no es una dirección IPv4 válida")
        return v

class DireccionIpAsignada(DireccionIpAsignadaBase):
    class Config:
        from_attributes = True
