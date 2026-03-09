path = "app/api/routes/contratacion.py"
with open(path, "r") as f:
    content = f.read()

# Fix the double decorator on regenerar
content = content.replace('@router.put("/documento/{id}/regenerar", response_model=DocumentoGeneradoResponse)\n@router.put("/documento/{id}/regenerar")', '@router.put("/documento/{id}/regenerar")')

with open(path, "w") as f:
    f.write(content)
