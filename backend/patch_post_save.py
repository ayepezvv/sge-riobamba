import re

path = "/home/ayepez/.openclaw/workspace/sge/backend/app/api/routes/contratacion.py"
with open(path, "r") as f:
    content = f.read()

save_logic = """
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
"""

content = re.sub(r'# Render with base64 decoded images recursively.*?db\.refresh\(doc_gen\)', save_logic, content, flags=re.DOTALL)

with open(path, "w") as f:
    f.write(content)
