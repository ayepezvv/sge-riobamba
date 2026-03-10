import re

path_models = "app/models/administrativo.py"
with open(path_models, "r") as f:
    content = f.read()

# Add Float to imports if missing
if "Float" not in content:
    content = content.replace("from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum, UniqueConstraint", "from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum, UniqueConstraint, Float")

# Add Puesto model
puesto_model = """class Puesto(Base):
    __tablename__ = "puestos"
    __table_args__ = {"schema": "administracion"}

    id = Column(Integer, primary_key=True, index=True)
    denominacion = Column(String(150), nullable=False)
    escala_ocupacional = Column(String(100), nullable=True)
    remuneracion_mensual = Column(Float, nullable=False)
    partida_presupuestaria = Column(String(100), nullable=False)
    es_activo = Column(Boolean, default=True)

    personal = relationship("Personal", back_populates="puesto")

class Direccion(Base):"""

content = content.replace("class Direccion(Base):", puesto_model)

# Modify Personal model
old_personal_cols = """    id = Column(Integer, primary_key=True, index=True)
    unidad_id = Column(Integer, ForeignKey("administracion.unidades.id", ondelete="RESTRICT"), nullable=False)
    usuario_id = Column(Integer, ForeignKey("administracion.users.id", ondelete="SET NULL"), nullable=True, unique=True)"""

new_personal_cols = """    id = Column(Integer, primary_key=True, index=True)
    unidad_id = Column(Integer, ForeignKey("administracion.unidades.id", ondelete="RESTRICT"), nullable=False)
    usuario_id = Column(Integer, ForeignKey("administracion.users.id", ondelete="SET NULL"), nullable=True, unique=True)
    puesto_id = Column(Integer, ForeignKey("administracion.puestos.id", ondelete="RESTRICT"), nullable=True)"""
content = content.replace(old_personal_cols, new_personal_cols)

# Add relation to Personal
old_personal_rel = """    titulos = relationship("TituloProfesional", back_populates="personal", cascade="all, delete-orphan")"""
new_personal_rel = """    titulos = relationship("TituloProfesional", back_populates="personal", cascade="all, delete-orphan")
    puesto = relationship("Puesto", back_populates="personal")"""
content = content.replace(old_personal_rel, new_personal_rel)

with open(path_models, "w") as f:
    f.write(content)

path_init = "app/models/__init__.py"
with open(path_init, "r") as f:
    content_init = f.read()

if "Puesto" not in content_init:
    content_init = content_init.replace("TituloProfesional", "TituloProfesional, Puesto")
    with open(path_init, "w") as f:
        f.write(content_init)
