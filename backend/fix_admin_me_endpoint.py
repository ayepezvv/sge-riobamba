import re

path = "app/api/routes/administrativo.py"
with open(path, "r") as f:
    content = f.read()

endpoint = """
@router.get("/personal/me", response_model=PersonalResponse)
def obtener_mi_perfil(db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_user)):
    db_obj = db.query(Personal).options(
        joinedload(Personal.unidad).joinedload(Unidad.direccion),
        joinedload(Personal.titulos)
    ).filter(Personal.usuario_id == current_user.id).first()
    
    if not db_obj:
        raise HTTPException(status_code=404, detail="Perfil de personal no encontrado para este usuario")
    return db_obj

@router.get("/personal", response_model=List[PersonalResponse])
"""

content = content.replace('@router.get("/personal", response_model=List[PersonalResponse])', endpoint)

# Note: previous script used deps.get_current_active_user but the patched one is deps.get_current_user
content = content.replace('deps.get_current_active_user', 'deps.get_current_user')

with open(path, "w") as f:
    f.write(content)
