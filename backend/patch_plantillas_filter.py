import re

path = "/home/ayepez/.openclaw/workspace/sge/backend/app/api/routes/contratacion.py"
with open(path, "r") as f:
    content = f.read()

# We need to filter plantillas by the process type
# Let's add a parameter to the get_plantillas endpoint
old_get_plantillas = """@router.get("/plantillas", response_model=List[PlantillaDocumentoResponse])
def get_plantillas(db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_user)):
    return db.query(PlantillaDocumento).all()"""

new_get_plantillas = """from typing import Optional
from fastapi import Query

@router.get("/plantillas", response_model=List[PlantillaDocumentoResponse])
def get_plantillas(
    tipo_proceso_id: Optional[int] = Query(None),
    is_activa: Optional[bool] = Query(None),
    db: Session = Depends(deps.get_db), 
    current_user: User = Depends(deps.get_current_user)
):
    query = db.query(PlantillaDocumento)
    if tipo_proceso_id is not None:
        query = query.filter(PlantillaDocumento.tipo_proceso_id == tipo_proceso_id)
    if is_activa is not None:
        query = query.filter(PlantillaDocumento.is_activa == is_activa)
    return query.all()"""

content = content.replace(old_get_plantillas, new_get_plantillas)

with open(path, "w") as f:
    f.write(content)
