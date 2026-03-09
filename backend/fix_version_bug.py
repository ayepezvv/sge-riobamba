import re

path = "app/api/routes/contratacion.py"
with open(path, "r") as f:
    content = f.read()

old_return = """    return FileResponse(
        path=out_path,
        filename=f"Proceso_Regenerado_v{new_version}.docx",
        media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        headers={"Content-Disposition": f"attachment; filename=Proceso_Regenerado_v{new_version}.docx"}
    )"""

new_return = """    return FileResponse(
        path=out_path,
        filename=f"Proceso_Generado_v1.docx",
        media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        headers={"Content-Disposition": f"attachment; filename=Proceso_Generado_v1.docx"}
    )"""

content = content.replace(old_return, new_return, 1)

with open(path, "w") as f:
    f.write(content)
