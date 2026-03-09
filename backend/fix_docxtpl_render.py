import re

path = "app/api/routes/contratacion.py"
with open(path, "r") as f:
    content = f.read()

# Make absolutely sure we use the correct rendering method and import
new_post = """    # 2. Generar DOCX
    from docxtpl import DocxTemplate
    doc = DocxTemplate(plantilla.ruta_archivo_docx)
    
    # Process base64
    datos_limpios = get_render_data(doc, req.datos)
    
    # Render explicitly without any env argument
    doc.render(datos_limpios)"""
    
content = re.sub(r'# 2\. Generar DOCX.*?doc\.render\(get_render_data\(doc, req\.datos\)\)', new_post, content, flags=re.DOTALL)

# Do the same for regenerar
new_put = """    # Render new docx
    from docxtpl import DocxTemplate
    docx_tpl = DocxTemplate(plantilla.ruta_archivo_docx)
    datos_limpios = get_render_data(docx_tpl, req.datos)
    
    docx_tpl.render(datos_limpios)"""
    
content = re.sub(r'# Render new docx.*?docx_tpl\.render\(get_render_data\(docx_tpl, req\.datos\)\)', new_put, content, flags=re.DOTALL)

with open(path, "w") as f:
    f.write(content)
