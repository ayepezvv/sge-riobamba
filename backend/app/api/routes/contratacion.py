from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import os
import time
from docxtpl import DocxTemplate

from app.api import deps
from app.models.user import User
from app.models.contratacion import TipoProceso, PlantillaDocumento, ProcesoContratacion, DocumentoGenerado
from app.schemas.contratacion import (
    TipoProcesoResponse, PlantillaDocumentoResponse, 
    ProcesoContratacionCreate, ProcesoContratacionResponse,
    GenerarDocumentoRequest, RegenerarDocumentoRequest, DocumentoGeneradoResponse
)

router = APIRouter()

# ----- PROCESOS DE CONTRATACIÓN -----
@router.get("/procesos", response_model=List[ProcesoContratacionResponse])
def get_procesos(db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_user)):
    return db.query(ProcesoContratacion).all()

@router.post("/procesos", response_model=ProcesoContratacionResponse)
def create_proceso(item_in: ProcesoContratacionCreate, db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_user)):
    db_item = ProcesoContratacion(**item_in.model_dump(), usuario_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/procesos/{id}", response_model=ProcesoContratacionResponse)
def get_proceso(id: int, db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_user)):
    db_item = db.query(ProcesoContratacion).filter(ProcesoContratacion.id == id).first()
    if not db_item:
        raise HTTPException(404, "Proceso no encontrado")
    return db_item

# ----- PLANTILLAS -----
@router.get("/plantillas", response_model=List[PlantillaDocumentoResponse])
def get_plantillas(db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_user)):
    return db.query(PlantillaDocumento).all()

# ----- DOCUMENTOS GENERADOS -----
@router.post("/documento", response_model=DocumentoGeneradoResponse)
def generar_documento(req: GenerarDocumentoRequest, db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_user)):
    # 1. Obtener plantilla
    plantilla = db.query(PlantillaDocumento).filter(PlantillaDocumento.id == req.plantilla_id).first()
    if not plantilla:
        raise HTTPException(404, "Plantilla no encontrada")
    
    if not os.path.exists(plantilla.ruta_archivo_docx):
        raise HTTPException(400, "Archivo físico de plantilla no existe")

    # 2. Generar DOCX
    doc = DocxTemplate(plantilla.ruta_archivo_docx)
    doc.render(req.datos)
    
    os.makedirs("generated", exist_ok=True)
    out_path = f"generated/doc_proc_{req.proceso_contratacion_id}_tpl_{req.plantilla_id}_v1_{int(time.time())}.docx"
    doc.save(out_path)

    # 3. Guardar en DB
    doc_gen = DocumentoGenerado(
        proceso_contratacion_id=req.proceso_contratacion_id,
        plantilla_id=req.plantilla_id,
        version=1,
        datos_json=req.datos,
        ruta_archivo_generado=out_path
    )
    db.add(doc_gen)
    db.commit()
    db.refresh(doc_gen)
    return doc_gen

@router.get("/documento/{id}/datos")
def get_datos_documento(id: int, db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_user)):
    doc = db.query(DocumentoGenerado).filter(DocumentoGenerado.id == id).first()
    if not doc:
        raise HTTPException(404, "Documento no encontrado")
    return doc.datos_json

@router.put("/documento/{id}/regenerar", response_model=DocumentoGeneradoResponse)
def regenerar_documento(id: int, req: RegenerarDocumentoRequest, db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_user)):
    doc = db.query(DocumentoGenerado).filter(DocumentoGenerado.id == id).first()
    if not doc:
        raise HTTPException(404, "Documento no encontrado")
        
    plantilla = db.query(PlantillaDocumento).filter(PlantillaDocumento.id == doc.plantilla_id).first()
    
    # Render new docx
    docx_tpl = DocxTemplate(plantilla.ruta_archivo_docx)
    docx_tpl.render(req.datos)
    
    new_version = doc.version + 1
    out_path = f"generated/doc_proc_{doc.proceso_contratacion_id}_tpl_{doc.plantilla_id}_v{new_version}_{int(time.time())}.docx"
    docx_tpl.save(out_path)
    
    # Update DB
    doc.datos_json = req.datos
    doc.version = new_version
    doc.ruta_archivo_generado = out_path
    
    db.commit()
    db.refresh(doc)
    return doc
