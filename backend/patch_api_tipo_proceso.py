import re

path = "/home/ayepez/.openclaw/workspace/sge/backend/app/api/routes/contratacion.py"
with open(path, "r") as f:
    content = f.read()

new_routes = """
@router.post("/tipos", response_model=TipoProcesoResponse)
def create_tipo(item_in: TipoProcesoCreate, db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_user)):
    db_item = TipoProceso(**item_in.model_dump(), creado_por_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.put("/tipos/{id}", response_model=TipoProcesoResponse)
def update_tipo(id: int, item_in: TipoProcesoUpdate, db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_user)):
    db_item = db.query(TipoProceso).filter(TipoProceso.id == id).first()
    if not db_item:
        raise HTTPException(404, "Tipo de proceso no encontrado")
        
    update_data = item_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_item, field, value)
        
    db_item.actualizado_por_id = current_user.id
    db.commit()
    db.refresh(db_item)
    return db_item
"""

content = content.replace("from app.schemas.contratacion import (", "from app.schemas.contratacion import (\n    TipoProcesoCreate, TipoProcesoUpdate,")
content = content.replace("def get_tipos(db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_user)):\n    return db.query(TipoProceso).all()", "def get_tipos(db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_user)):\n    return db.query(TipoProceso).all()\n" + new_routes)

with open(path, "w") as f:
    f.write(content)
