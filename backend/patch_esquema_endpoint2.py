import re

path = "app/api/routes/contratacion.py"
with open(path, "r") as f:
    content = f.read()

# Make a safer replace logic targeting the whole function content
new_func = """@router.get("/plantillas/{id}/esquema")
def get_plantilla_esquema(id: int, db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_user)):
    plantilla = db.query(PlantillaDocumento).filter(PlantillaDocumento.id == id).first()
    if not plantilla:
        raise HTTPException(404, "Plantilla no encontrada")
        
    if not os.path.exists(plantilla.ruta_archivo_docx):
        raise HTTPException(400, "El archivo fisico no existe")
        
    import jinja2
    from docxtpl import DocxTemplate
    try:
        doc = DocxTemplate(plantilla.ruta_archivo_docx)
        env = jinja2.Environment()
        variables_detectadas = doc.get_undeclared_template_variables(env)
        
        esquema = []
        for var in variables_detectadas:
            if var.startswith("img_"):
                esquema.append({"nombre": var, "tipo": "imagen"})
            elif var.startswith("tbl_") or var.startswith("lista_"):
                esquema.append({"nombre": var, "tipo": "tabla_dinamica"})
            else:
                esquema.append({"nombre": var, "tipo": "texto"})
                
        return {"variables": esquema}
    except Exception as e:
        raise HTTPException(500, f"Error analizando plantilla con jinja2: {str(e)}")"""

content = re.sub(r'@router.get\("/plantillas/\{id\}/esquema"\).*?raise HTTPException\(500, f"Error analizando plantilla: \{str\(e\)\}"\)', new_func, content, flags=re.DOTALL)

with open(path, "w") as f:
    f.write(content)
