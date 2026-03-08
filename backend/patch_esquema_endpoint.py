import re

path = "app/api/routes/contratacion.py"
with open(path, "r") as f:
    content = f.read()

new_endpoint = """
@router.get("/plantillas/{id}/esquema")
def get_plantilla_esquema(id: int, db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_user)):
    plantilla = db.query(PlantillaDocumento).filter(PlantillaDocumento.id == id).first()
    if not plantilla:
        raise HTTPException(404, "Plantilla no encontrada")
        
    if not os.path.exists(plantilla.ruta_archivo_docx):
        raise HTTPException(400, "El archivo fisico no existe")
        
    try:
        doc = DocxTemplate(plantilla.ruta_archivo_docx)
        # Extraer variables simples usando la libreria subyacente jinja2
        undeclared_variables = doc.get_undeclared_template_variables()
        
        # Un analizador muy basico:
        esquema = []
        for var in undeclared_variables:
            if var.startswith("img_"):
                esquema.append({"nombre": var, "tipo": "imagen"})
            elif var.startswith("tbl_"):
                esquema.append({"nombre": var, "tipo": "tabla_dinamica"})
            else:
                esquema.append({"nombre": var, "tipo": "texto"})
                
        return {"variables": esquema}
    except Exception as e:
        raise HTTPException(500, f"Error analizando plantilla: {str(e)}")
"""

if "def get_plantilla_esquema" not in content:
    content = content.replace("# ----- DOCUMENTOS GENERADOS -----", new_endpoint + "\n# ----- DOCUMENTOS GENERADOS -----")

with open(path, "w") as f:
    f.write(content)
