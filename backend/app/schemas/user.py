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

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True
