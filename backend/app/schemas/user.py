from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    cedula: str
    nombres: str
    apellidos: str
    correo: EmailStr
    is_active: Optional[bool] = True
    role_id: Optional[int] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    cedula: Optional[str] = None
    nombres: Optional[str] = None
    apellidos: Optional[str] = None
    correo: Optional[EmailStr] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    role_id: Optional[int] = None

class RoleBasico(BaseModel):
    id: int
    nombre_rol: str

    class Config:
        from_attributes = True


class UserResponse(UserBase):
    id: int
    role: Optional[RoleBasico] = None

    class Config:
        from_attributes = True
