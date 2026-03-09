path = "app/models/__init__.py"
with open(path, "r") as f:
    content = f.read()

content = content.replace("TipoRegimenLegal, TipoContrato", "TipoRegimenLegal, TipoContrato, NivelEducacion, TituloProfesional")
with open(path, "w") as f:
    f.write(content)
