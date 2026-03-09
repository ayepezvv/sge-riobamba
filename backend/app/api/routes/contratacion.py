from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import os
import time
import shutil
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse
from docxtpl import DocxTemplate

from app.api import deps
from app.models.user import User
from app.models.contratacion import TipoProceso, PlantillaDocumento, ProcesoContratacion, DocumentoGenerado
from app.schemas.contratacion import (
    TipoProcesoCreate, TipoProcesoUpdate,
    TipoProcesoResponse, PlantillaDocumentoResponse, 
    ProcesoContratacionCreate, ProcesoContratacionResponse,
    GenerarDocumentoRequest, RegenerarDocumentoRequest, DocumentoGeneradoResponse
)

router = APIRouter()

def get_render_data(doc, req_datos):
    from docxtpl import InlineImage
    from docx.shared import Mm
    import base64
    import io

    def procesar_valor(val):
        # Si es un string base64 de imagen
        if isinstance(val, str) and val.startswith("data:image"):
            try:
                header, encoded = val.split(",", 1)
                image_data = base64.b64decode(encoded)
                image_stream = io.BytesIO(image_data)
                return InlineImage(doc, image_stream, width=Mm(50))
            except Exception:
                return val
        # Si es una lista (para tablas dinamicas), aplicar recursividad
        elif isinstance(val, list):
            nueva_lista = []
            for item in val:
                if isinstance(item, dict):
                    nueva_lista.append(procesar_valor(item))
                else:
                    nueva_lista.append(item)
            return nueva_lista
        # Si es un diccionario
        elif isinstance(val, dict):
            nuevo_dict = {}
            for k, v in val.items():
                nuevo_dict[k] = procesar_valor(v)
            return nuevo_dict
        
        # Cualquier otra cosa se queda igual
        return val

    return procesar_valor(req_datos)


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

@router.get("/tipos", response_model=List[TipoProcesoResponse])
def get_tipos(db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_user)):
    return db.query(TipoProceso).all()

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

from typing import Optional
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
    return query.all()


@router.get("/plantillas/{id}/esquema")
def get_plantilla_esquema(id: int, db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_user)):
    plantilla = db.query(PlantillaDocumento).filter(PlantillaDocumento.id == id).first()
    if not plantilla:
        raise HTTPException(404, "Plantilla no encontrada")
        
    if not os.path.exists(plantilla.ruta_archivo_docx):
        raise HTTPException(400, "El archivo fisico no existe")
        
    import docx
    import re
    try:
        doc_docx = docx.Document(plantilla.ruta_archivo_docx)
        texto_completo = ""
        
        for p in doc_docx.paragraphs:
            texto_completo += p.text + "\n"
        for table in doc_docx.tables:
            for row in table.rows:
                for cell in row.cells:
                    texto_completo += cell.text + "\n"
        # Extraer texto de encabezados y pies de pagina en todas sus variantes
        for section in doc_docx.sections:
            elementos_hf = [
                section.header, section.first_page_header, section.even_page_header,
                section.footer, section.first_page_footer, section.even_page_footer
            ]
            for hf in elementos_hf:
                if hf:
                    for p in hf.paragraphs:
                        texto_completo += p.text + "\n"
                    for table in hf.tables:
                        for row in table.rows:
                            for cell in row.cells:
                                texto_completo += cell.text + "\n"

        
        # 1. Buscar todos los bucles y sus iteradores
        patron_bucle = r'{%\s*(?:tr\s+|p\s+)?for\s+(\w+)\s+in\s+(\w+)\s*%}'
        bucles_encontrados = re.findall(patron_bucle, texto_completo)
        mapa_iteradores = {iterador: nombre_lista for iterador, nombre_lista in bucles_encontrados}
        
        # 2. Buscar todas las variables con finditer para preservar el orden y sacar contexto
        patron_vars = r'\{\{\s*([\w.]+)\s*\}\}'
        matches = list(re.finditer(patron_vars, texto_completo))
        
        esquema_dict = {} # Preserva orden de insercion en Python 3.7+
        tablas_dict = {} # Preserva sub_atributos ordenados
        
        for match in matches:
            var_raw = match.group(1)
            
            # Omitir variables internas de jinja2 (ej: loop.index)
            if 'loop' in var_raw.lower():
                continue
                
            # Extraer contexto (40 chars)
            start_pos = max(0, match.start() - 40)
            end_pos = min(len(texto_completo), match.end() + 40)
            contexto = "..." + texto_completo[start_pos:match.start()].replace('\n', ' ').strip() + f" [ {var_raw} ] " + texto_completo[match.end():end_pos].replace('\n', ' ').strip() + "..."
            
            # Si tiene punto, pertenece a un iterador de tabla
            if '.' in var_raw:
                partes = var_raw.split('.', 1)
                iterador = partes[0]
                atributo = partes[1]
                
                if iterador in mapa_iteradores:
                    nombre_lista = mapa_iteradores[iterador]
                    if nombre_lista not in tablas_dict:
                        tablas_dict[nombre_lista] = {}
                    if atributo not in tablas_dict[nombre_lista]:
                        tablas_dict[nombre_lista][atributo] = contexto
                else:
                    if var_raw not in esquema_dict:
                        esquema_dict[var_raw] = {"tipo": "texto", "contexto": contexto}
            else:
                if var_raw not in esquema_dict:
                    if var_raw.startswith("img_"):
                        esquema_dict[var_raw] = {"tipo": "imagen", "contexto": contexto}
                    else:
                        esquema_dict[var_raw] = {"tipo": "texto", "contexto": contexto}
                
        # 4. Construir esquema JSON final
        esquema_final = []
        for nombre_var, datos in esquema_dict.items():
            esquema_final.append({
                "nombre": nombre_var,
                "tipo": datos["tipo"],
                "contexto": datos["contexto"]
            })
                
        for nombre_lista, atributos_dict in tablas_dict.items():
            # El frontend frontend usaba sub_atributos, pero lo unificaremos como columnas
            esquema_final.append({
                "nombre": nombre_lista,
                "tipo": "tabla_dinamica",
                "columnas": list(atributos_dict.keys()),
                "contexto": f"Matriz dinamica ({len(atributos_dict)} columnas)"
            })
            
        return {"variables": esquema_final}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analizando documento: {str(e)}")

# ----- DOCUMENTOS GENERADOS -----
@router.post("/documento")
def generar_documento(req: GenerarDocumentoRequest, db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_user)):
    # 1. Obtener plantilla
    plantilla = db.query(PlantillaDocumento).filter(PlantillaDocumento.id == req.plantilla_id).first()
    if not plantilla:
        raise HTTPException(404, "Plantilla no encontrada")
    
    if not os.path.exists(plantilla.ruta_archivo_docx):
        raise HTTPException(400, "Archivo físico de plantilla no existe")

        # 2. Generar DOCX
    from docxtpl import DocxTemplate
    doc = DocxTemplate(plantilla.ruta_archivo_docx)
    
    # Process base64
    datos_limpios = get_render_data(doc, req.datos)
    
    # Render explicitly without any env argument
    doc.render(datos_limpios)
    
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
    # 4. Devolver el archivo fisico descargable
    from fastapi.responses import FileResponse
    return FileResponse(
        path=out_path,
        filename=f"Proceso_Generado_v1.docx",
        media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        headers={"Content-Disposition": f"attachment; filename=Proceso_Generado_v1.docx"}
    )

@router.get("/documento/{id}/datos")
def get_datos_documento(id: int, db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_user)):
    doc = db.query(DocumentoGenerado).filter(DocumentoGenerado.id == id).first()
    if not doc:
        raise HTTPException(404, "Documento no encontrado")
    return doc.datos_json


@router.get("/documento/{id}/descargar")
def descargar_documento(id: int, db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_user)):
    doc = db.query(DocumentoGenerado).filter(DocumentoGenerado.id == id).first()
    if not doc or not os.path.exists(doc.ruta_archivo_generado):
        raise HTTPException(404, "Documento fisico no encontrado")
        
    from fastapi.responses import FileResponse
    return FileResponse(
        path=doc.ruta_archivo_generado,
        filename=f"Documento_v{doc.version}.docx",
        media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    )

@router.put("/documento/{id}/regenerar")
def regenerar_documento(id: int, req: RegenerarDocumentoRequest, db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_user)):
    doc = db.query(DocumentoGenerado).filter(DocumentoGenerado.id == id).first()
    if not doc:
        raise HTTPException(404, "Documento no encontrado")
        
    plantilla = db.query(PlantillaDocumento).filter(PlantillaDocumento.id == doc.plantilla_id).first()
    
        # Render new docx
    from docxtpl import DocxTemplate
    docx_tpl = DocxTemplate(plantilla.ruta_archivo_docx)
    datos_limpios = get_render_data(docx_tpl, req.datos)
    
    docx_tpl.render(datos_limpios)
    
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
