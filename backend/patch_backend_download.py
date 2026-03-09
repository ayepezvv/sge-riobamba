import re

path = "app/api/routes/contratacion.py"
with open(path, "r") as f:
    content = f.read()

new_endpoint = """
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
"""

content = content.replace('@router.put("/documento/{id}/regenerar")', new_endpoint + '\n@router.put("/documento/{id}/regenerar")')

with open(path, "w") as f:
    f.write(content)
