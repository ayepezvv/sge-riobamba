import re

path = "app/schemas/administrativo.py"
with open(path, "r") as f:
    content = f.read()

# Add Enum
enum_import = "from app.models.administrativo import TipoRegimenLegal, TipoContrato, NivelEducacion\n"
content = content.replace("from app.models.administrativo import TipoRegimenLegal, TipoContrato\n", enum_import)

# Titulos Schemas
titulos_schemas = """
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

# --- Personal ---"""
content = content.replace("# --- Personal ---", titulos_schemas)

# Update PersonalBase
old_personal_base = """    codigo_certificacion_sercop: Optional[str] = Field(None, max_length=100)
    foto_perfil: Optional[str] = None
    es_activo: bool = True"""
new_personal_base = """    codigo_certificacion_sercop: Optional[str] = Field(None, max_length=100)
    foto_perfil: Optional[str] = None
    direccion_domicilio: Optional[str] = Field(None, max_length=255)
    telefono_celular: Optional[str] = Field(None, max_length=20)
    correo_personal: Optional[str] = Field(None, max_length=100)
    archivo_firma_electronica: Optional[str] = None
    es_activo: bool = True"""
content = content.replace(old_personal_base, new_personal_base)

# Update PersonalUpdate
old_personal_update = """    codigo_certificacion_sercop: Optional[str] = Field(None, max_length=100)
    foto_perfil: Optional[str] = None
    es_activo: Optional[bool] = None"""
new_personal_update = """    codigo_certificacion_sercop: Optional[str] = Field(None, max_length=100)
    foto_perfil: Optional[str] = None
    direccion_domicilio: Optional[str] = Field(None, max_length=255)
    telefono_celular: Optional[str] = Field(None, max_length=20)
    correo_personal: Optional[str] = Field(None, max_length=100)
    archivo_firma_electronica: Optional[str] = None
    es_activo: Optional[bool] = None"""
content = content.replace(old_personal_update, new_personal_update)

# Update PersonalResponse
old_personal_resp = """class PersonalResponse(PersonalBase):
    id: int
    unidad: Optional[UnidadResponse] = None

    class Config:"""
new_personal_resp = """class PersonalResponse(PersonalBase):
    id: int
    unidad: Optional[UnidadResponse] = None
    titulos: List[TituloProfesionalResponse] = []

    class Config:"""
content = content.replace(old_personal_resp, new_personal_resp)

with open(path, "w") as f:
    f.write(content)
