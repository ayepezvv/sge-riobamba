import re

path = "/home/ayepez/.openclaw/workspace/sge/backend/app/api/routes/contratacion.py"
with open(path, "r") as f:
    content = f.read()

# Fix backend POST /documento
old_return_post = """    # 4. Devolver el archivo fisico descargable
    from fastapi.responses import FileResponse
    return FileResponse(
        path=out_path,
        filename=f"Proceso_{req.proceso_contratacion_id}.docx",
        media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    )"""

new_return_post = """    # 4. Devolver el archivo fisico descargable
    from fastapi.responses import FileResponse
    return FileResponse(
        path=out_path,
        filename=f"Proceso_{req.proceso_contratacion_id}.docx",
        media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        headers={"Content-Disposition": f"attachment; filename=Proceso_{req.proceso_contratacion_id}.docx"}
    )"""

content = content.replace(old_return_post, new_return_post)

# Fix backend PUT /documento/{id}/regenerar
old_return_put = """    # 4. Devolver el archivo fisico descargable
    from fastapi.responses import FileResponse
    return FileResponse(
        path=out_path,
        filename=f"documento_generado_{doc_gen.id}.docx",
        media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    )"""

new_return_put = """    # 4. Devolver el archivo fisico descargable
    from fastapi.responses import FileResponse
    return FileResponse(
        path=out_path,
        filename=f"Proceso_Regenerado_v{new_version}.docx",
        media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        headers={"Content-Disposition": f"attachment; filename=Proceso_Regenerado_v{new_version}.docx"}
    )"""

content = content.replace(old_return_put, new_return_put)

with open(path, "w") as f:
    f.write(content)
