import re
path = "/home/ayepez/.openclaw/workspace/sge/backend/app/api/routes/contratacion.py"
with open(path, "r") as f:
    content = f.read()

imports = """import os
import time
import shutil
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form"""

content = content.replace("import os\nimport time\nfrom docxtpl import DocxTemplate", imports + "\nfrom docxtpl import DocxTemplate")

upload_endpoint = """
@router.get("/tipos", response_model=List[TipoProcesoResponse])
def get_tipos(db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_user)):
    return db.query(TipoProceso).all()

@router.post("/plantillas/upload", response_model=PlantillaDocumentoResponse)
def upload_plantilla(
    nombre: str = Form(...),
    tipo_proceso_id: int = Form(...),
    anio: int = Form(2026),
    file: UploadFile = File(...),
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    if not file.filename.endswith('.docx'):
        raise HTTPException(400, "El archivo debe ser .docx")
        
    old_tpl = db.query(PlantillaDocumento).filter_by(nombre=nombre, tipo_proceso_id=tipo_proceso_id, is_activa=True).first()
    new_version = 1
    
    if old_tpl:
        old_tpl.is_activa = False
        new_version = old_tpl.version + 1
        db.add(old_tpl)
        
    os.makedirs("templates/contratacion", exist_ok=True)
    safe_name = nombre.replace(' ', '_')
    file_path = f"templates/contratacion/{tipo_proceso_id}_{safe_name}_v{new_version}_{int(time.time())}.docx"
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    new_tpl = PlantillaDocumento(
        nombre=nombre, 
        ruta_archivo_docx=file_path, 
        tipo_proceso_id=tipo_proceso_id, 
        anio=anio, 
        version=new_version, 
        is_activa=True,
        creado_por_id=current_user.id
    )
    db.add(new_tpl)
    db.commit()
    db.refresh(new_tpl)
    return new_tpl
"""

content = content.replace("# ----- PLANTILLAS -----", "# ----- PLANTILLAS -----\n" + upload_endpoint)

with open(path, "w") as f:
    f.write(content)
