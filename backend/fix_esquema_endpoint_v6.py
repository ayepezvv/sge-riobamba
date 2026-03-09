import re
path = "app/api/routes/contratacion.py"
with open(path, "r") as f:
    content = f.read()

# Replace the POST to return the FileResponse directly
old_post = """@router.post("/documento")
def generar_documento(req: GenerarDocumentoRequest, db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_user)):
    # 1. Obtener plantilla
    plantilla = db.query(PlantillaDocumento).filter(PlantillaDocumento.id == req.plantilla_id).first()
    if not plantilla:
        raise HTTPException(404, "Plantilla no encontrada")
    
    if not os.path.exists(plantilla.ruta_archivo_docx):
        raise HTTPException(400, "Archivo físico de plantilla no existe")

    # 2. Generar DOCX
    doc = DocxTemplate(plantilla.ruta_archivo_docx)
    doc.render(get_render_data(doc, req.datos))
    
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
    return doc_gen"""

new_post = """@router.post("/documento")
def generar_documento(req: GenerarDocumentoRequest, db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_user)):
    # 1. Obtener plantilla
    plantilla = db.query(PlantillaDocumento).filter(PlantillaDocumento.id == req.plantilla_id).first()
    if not plantilla:
        raise HTTPException(404, "Plantilla no encontrada")
    
    if not os.path.exists(plantilla.ruta_archivo_docx):
        raise HTTPException(400, "Archivo fisico de plantilla no existe")

    # 2. Generar DOCX
    from docxtpl import DocxTemplate
    doc = DocxTemplate(plantilla.ruta_archivo_docx)
    
    # Render with base64 decoded images recursively
    doc.render(get_render_data(doc, req.datos))
    
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
    return FileResponse(
        path=out_path,
        filename=f"documento_generado_{doc_gen.id}.docx",
        media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    )"""

content = re.sub(r'@router.post\("/documento"\).*?return doc_gen', new_post, content, flags=re.DOTALL)

with open(path, "w") as f:
    f.write(content)
