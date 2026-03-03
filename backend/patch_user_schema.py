import re

path = "app/schemas/user.py"
with open(path, "r") as f:
    content = f.read()

update_schema = """class UserUpdate(BaseModel):
    cedula: Optional[str] = None
    nombres: Optional[str] = None
    apellidos: Optional[str] = None
    correo: Optional[EmailStr] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    role_id: Optional[int] = None

class UserResponse"""

content = content.replace("class UserResponse", update_schema)

with open(path, "w") as f:
    f.write(content)
