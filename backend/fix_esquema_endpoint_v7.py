path = "app/api/routes/contratacion.py"
with open(path, "r") as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if "return doc_gen" in line:
        new_lines.append("""    # 4. Devolver el archivo fisico descargable
    from fastapi.responses import FileResponse
    return FileResponse(
        path=out_path,
        filename=f"documento_generado_{doc_gen.id}.docx",
        media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    )\n""")
    elif "@router.post(\"/documento\", response_model=DocumentoGeneradoResponse)" in line:
        new_lines.append('@router.post("/documento")\n')
    else:
        new_lines.append(line)

with open(path, "w") as f:
    f.writelines(new_lines)
