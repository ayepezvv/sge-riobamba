import re
path = "app/api/routes/ciudadanos.py"
with open(path, "r") as f:
    content = f.read()

new_logic = """
@router.patch("/{ciudadano_id}/status", response_model=CiudadanoResponse)
def toggle_ciudadano_status(
    ciudadano_id: int, 
    db: Session = Depends(deps.get_db), 
    current_user: User = Depends(deps.get_current_user)
):
    db_item = db.query(Ciudadano).filter(Ciudadano.id == ciudadano_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Ciudadano no encontrado")
    
    db_item.is_active = not db_item.is_active
    db.commit()
    db.refresh(db_item)
    return db_item
"""

content = re.sub(r'@router.patch\("/\{ciudadano_id\}/status".*?pass(?: #.*?)?\n', new_logic, content, flags=re.DOTALL)

with open(path, "w") as f:
    f.write(content)
