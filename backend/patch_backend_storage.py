import re

path = "/home/ayepez/.openclaw/workspace/sge/backend/app/api/routes/contratacion.py"
with open(path, "r") as f:
    content = f.read()

# Replace the save and response logic in POST /documento
old_logic = """
    # Render with base64 decoded images recursively
    datos_limpios = get_render_data(doc, req.datos)
    doc.render(datos_limpios)
    
    os.makedirs("generated", exist_ok=True)
    out_path = f"generated/doc_proc_{req.proceso_contratacion_id}_tpl_{req.plantilla_id}_v1_{int(time.time())}.docx"
    doc.save(out_path)

    # 3. Guardar en DB el doc generado
    doc_gen = DocumentoGenerado(
        proceso_contratacion_id=req.proceso_contratacion_id,
        plantilla_id=req.plantilla_id,
        version=1,
        datos_json=req.datos,
        ruta_archivo_generado=out_path
    )
    db.add(doc_gen)
    
    # 3.1. Persistencia de Datos JSONB en el Proceso
    proceso = db.query(ProcesoContratacion).filter(ProcesoContratacion.id == req.proceso_contratacion_id).first()
    if proceso:
        proceso.datos_formulario = req.datos
        db.add(proceso)

    db.commit()
    db.refresh(doc_gen)
    
    # 4. Devolver el archivo fisico descargable
    from fastapi.responses import FileResponse
    return FileResponse(
        path=out_path,
        filename=f"documento_generado_{doc_gen.id}.docx",
        media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    )"""

new_logic = """
    # Render with base64 decoded images recursively
    datos_limpios = get_render_data(doc, req.datos)
    doc.render(datos_limpios)
    
    import uuid
    directorio_salida = os.path.join(os.getcwd(), "documentos_generados")
    os.makedirs(directorio_salida, exist_ok=True)
    out_path = os.path.join(directorio_salida, f"Documento_{req.proceso_contratacion_id}_{uuid.uuid4().hex[:6]}.docx")
    doc.save(out_path)

    # 3. Guardar en DB el doc generado
    doc_gen = DocumentoGenerado(
        proceso_contratacion_id=req.proceso_contratacion_id,
        plantilla_id=req.plantilla_id,
        version=1,
        datos_json=req.datos,
        ruta_archivo_generado=out_path
    )
    db.add(doc_gen)
    
    # 3.1. Persistencia de Datos JSONB en el Proceso
    proceso = db.query(ProcesoContratacion).filter(ProcesoContratacion.id == req.proceso_contratacion_id).first()
    if proceso:
        proceso.datos_formulario = req.datos
        db.add(proceso)

    db.commit()
    db.refresh(doc_gen)
    
    # 4. Devolver el archivo fisico descargable
    from fastapi.responses import FileResponse
    return FileResponse(
        path=out_path,
        filename=f"Proceso_{req.proceso_contratacion_id}.docx",
        media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    )"""

content = content.replace(old_logic, new_logic)

with open(path, "w") as f:
    f.write(content)
