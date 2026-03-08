import re

path = "app/api/routes/contratacion.py"
with open(path, "r") as f:
    content = f.read()

new_func = """@router.get("/plantillas/{id}/esquema")
def get_plantilla_esquema(id: int, db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_user)):
    plantilla = db.query(PlantillaDocumento).filter(PlantillaDocumento.id == id).first()
    if not plantilla:
        raise HTTPException(404, "Plantilla no encontrada")
        
    if not os.path.exists(plantilla.ruta_archivo_docx):
        raise HTTPException(400, "El archivo fisico no existe")
        
    from jinja2.exceptions import TemplateSyntaxError
    from docxtpl import DocxTemplate
    try:
        doc = DocxTemplate(plantilla.ruta_archivo_docx)
        # Usamos el entorno nativo de docxtpl que soporta {% p y {% tr
        variables_detectadas = doc.get_undeclared_template_variables()
        
        esquema = []
        for var in variables_detectadas:
            if var.startswith("img_"):
                esquema.append({"nombre": var, "tipo": "imagen"})
            elif var.startswith("tbl_") or var.startswith("lista_"):
                esquema.append({"nombre": var, "tipo": "tabla_dinamica"})
            else:
                esquema.append({"nombre": var, "tipo": "texto"})
                
        return {"variables": esquema}
    except TemplateSyntaxError as e:
        raise HTTPException(status_code=422, detail=f"Error de sintaxis en la plantilla (Jinja2): Linea {e.lineno}, Mensaje: {e.message}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error procesando documento: {str(e)}")"""

content = re.sub(r'@router.get\("/plantillas/\{id\}/esquema"\).*?raise HTTPException\(500, f"Error analizando plantilla con jinja2: \{str\(e\)\}"\)', new_func, content, flags=re.DOTALL)

with open(path, "w") as f:
    f.write(content)
