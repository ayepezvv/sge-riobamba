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

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True
