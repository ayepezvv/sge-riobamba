path = "app/api/routes/contratacion.py"
with open(path, "r") as f:
    content = f.read()

# Make sure we import what we need
if "from fastapi import APIRouter" in content:
    endpoint = """
@router.get("/pac/items/all", response_model=List[ItemPacResponse])
def explorar_todos_items(db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_user)):
    # Trae todos los items sin importar a que PAC pertenecen, usando join para traer data del padre
    return db.query(ItemPac).options(joinedload(ItemPac.pac)).all()
"""
    # Insert it near the other PAC endpoints
    content = content.replace("@router.post(\"/pac/{id}/items\",", endpoint + "\n@router.post(\"/pac/{id}/items\",")
    
with open(path, "w") as f:
    f.write(content)
