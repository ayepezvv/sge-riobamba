import re

# SCHEMAS
path_schemas = "app/schemas/administrativo.py"
with open(path_schemas, "r") as f:
    content_schemas = f.read()

puesto_schemas = """
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

# --- Direccion ---"""

content_schemas = content_schemas.replace("# --- Direccion ---", puesto_schemas)

# Update PersonalBase
old_pb = """    unidad_id: int
    usuario_id: Optional[int] = None"""
new_pb = """    unidad_id: int
    usuario_id: Optional[int] = None
    puesto_id: Optional[int] = None"""
content_schemas = content_schemas.replace(old_pb, new_pb)

# Update PersonalUpdate
old_pu = """    unidad_id: Optional[int] = None
    usuario_id: Optional[int] = None"""
new_pu = """    unidad_id: Optional[int] = None
    usuario_id: Optional[int] = None
    puesto_id: Optional[int] = None"""
content_schemas = content_schemas.replace(old_pu, new_pu)

# Update PersonalResponse
old_pr = """class PersonalResponse(PersonalBase):
    id: int
    unidad: Optional[UnidadResponse] = None"""
new_pr = """class PersonalResponse(PersonalBase):
    id: int
    unidad: Optional[UnidadResponse] = None
    puesto: Optional[PuestoResponse] = None"""
content_schemas = content_schemas.replace(old_pr, new_pr)

with open(path_schemas, "w") as f:
    f.write(content_schemas)

# API ROUTES
path_api = "app/api/routes/administrativo.py"
with open(path_api, "r") as f:
    content_api = f.read()

# Models
content_api = content_api.replace("Unidad, Personal, TituloProfesional", "Unidad, Personal, TituloProfesional, Puesto")

# Schemas
old_imp = """    TituloProfesionalCreate, TituloProfesionalResponse
)"""
new_imp = """    TituloProfesionalCreate, TituloProfesionalResponse,
    PuestoCreate, PuestoUpdate, PuestoResponse
)"""
content_api = content_api.replace(old_imp, new_imp)

puesto_endpoints = """
# --- Puestos ---
@router.post("/puestos", response_model=PuestoResponse, status_code=status.HTTP_201_CREATED)
def crear_puesto(req: PuestoCreate, db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_user)):
    db_obj = Puesto(**req.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

@router.get("/puestos", response_model=List[PuestoResponse])
def listar_puestos(db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_user)):
    return db.query(Puesto).all()

@router.put("/puestos/{id}", response_model=PuestoResponse)
def actualizar_puesto(id: int, req: PuestoUpdate, db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_user)):
    db_obj = db.query(Puesto).filter(Puesto.id == id).first()
    if not db_obj:
        raise HTTPException(status_code=404, detail="Puesto no encontrado")
    for field, value in req.dict(exclude_unset=True).items():
        setattr(db_obj, field, value)
    db.commit()
    db.refresh(db_obj)
    return db_obj

@router.delete("/puestos/{id}")
def eliminar_puesto(id: int, db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_user)):
    db_obj = db.query(Puesto).filter(Puesto.id == id).first()
    if not db_obj:
        raise HTTPException(status_code=404, detail="Puesto no encontrado")
    db.delete(db_obj)
    db.commit()
    return {"ok": True}

# --- Direcciones ---"""
content_api = content_api.replace("# --- Direcciones ---", puesto_endpoints)

# Update Personal joins
content_api = content_api.replace("joinedload(Personal.unidad).joinedload(Unidad.direccion),", "joinedload(Personal.unidad).joinedload(Unidad.direccion), joinedload(Personal.puesto),")

with open(path_api, "w") as f:
    f.write(content_api)

