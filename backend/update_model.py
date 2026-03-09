path = "app/models/administrativo.py"
with open(path, "r") as f:
    content = f.read()

content = content.replace("    codigo_certificacion_sercop = Column(String(100), nullable=True)", "    codigo_certificacion_sercop = Column(String(100), nullable=True)\n    foto_perfil = Column(String, nullable=True)")
with open(path, "w") as f:
    f.write(content)
