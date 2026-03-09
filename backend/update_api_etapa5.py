import re

path = "app/api/routes/administrativo.py"
with open(path, "r") as f:
    content = f.read()

# Models import
old_import = "from app.models.administrativo import Direccion, Unidad, Personal"
new_import = "from app.models.administrativo import Direccion, Unidad, Personal, TituloProfesional"
content = content.replace(old_import, new_import)

# Schemas import
old_schemas = "PersonalCreate, PersonalUpdate, PersonalResponse\n)"
new_schemas = "PersonalCreate, PersonalUpdate, PersonalResponse,\n    TituloProfesionalCreate, TituloProfesionalResponse\n)"
content = content.replace(old_schemas, new_schemas)

# Update GET /personal to joinload titulos
old_get_personal = "return db.query(Personal).options(joinedload(Personal.unidad).joinedload(Unidad.direccion)).all()"
new_get_personal = "return db.query(Personal).options(joinedload(Personal.unidad).joinedload(Unidad.direccion), joinedload(Personal.titulos)).all()"
content = content.replace(old_get_personal, new_get_personal)

# Append new endpoints
new_endpoints = """
# --- Titulos Profesionales ---
@router.post("/personal/{id}/titulos", response_model=TituloProfesionalResponse, status_code=status.HTTP_201_CREATED)
def agregar_titulo(id: int, req: TituloProfesionalCreate, db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_user)):
    personal = db.query(Personal).filter(Personal.id == id).first()
    if not personal:
        raise HTTPException(status_code=404, detail="Personal no encontrado")
    
    db_obj = TituloProfesional(**req.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

@router.delete("/personal/titulos/{id}")
def eliminar_titulo(id: int, db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_user)):
    db_obj = db.query(TituloProfesional).filter(TituloProfesional.id == id).first()
    if not db_obj:
        raise HTTPException(status_code=404, detail="Titulo no encontrado")
    db.delete(db_obj)
    db.commit()
    return {"ok": True}
"""
content += new_endpoints

with open(path, "w") as f:
    f.write(content)
