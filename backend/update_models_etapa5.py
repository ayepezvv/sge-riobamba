import re

path = "app/models/administrativo.py"
with open(path, "r") as f:
    content = f.read()

# Add NivelEducacion Enum
enum_block = """
class NivelEducacion(enum.Enum):
    TECNICO = "TECNICO"
    TECNOLOGICO = "TECNOLOGICO"
    TERCER_NIVEL = "TERCER_NIVEL"
    CUARTO_NIVEL = "CUARTO_NIVEL"
    PHD = "PHD"

class TipoRegimenLegal(enum.Enum):"""
content = content.replace("class TipoRegimenLegal(enum.Enum):", enum_block)

# Add TituloProfesional Model
model_block = """    unidad = relationship("Unidad", back_populates="personal")
    usuario = relationship("User", backref="personal_link")
    titulos = relationship("TituloProfesional", back_populates="personal", cascade="all, delete-orphan")

class TituloProfesional(Base):
    __tablename__ = "titulos_profesionales"
    __table_args__ = {"schema": "administracion"}

    id = Column(Integer, primary_key=True, index=True)
    personal_id = Column(Integer, ForeignKey("administracion.personal.id", ondelete="CASCADE"), nullable=False)
    nivel = Column(Enum(NivelEducacion, name="nivel_educacion"), nullable=False)
    nombre_titulo = Column(String(200), nullable=False)
    institucion = Column(String(200), nullable=False)
    registro_senescyt = Column(String(100), nullable=True)

    personal = relationship("Personal", back_populates="titulos")
"""
content = content.replace('    unidad = relationship("Unidad", back_populates="personal")\n    usuario = relationship("User", backref="personal_link")', model_block)

# Add new columns to Personal
new_columns = """    codigo_certificacion_sercop = Column(String(100), nullable=True)
    foto_perfil = Column(String, nullable=True)
    direccion_domicilio = Column(String(255), nullable=True)
    telefono_celular = Column(String(20), nullable=True)
    correo_personal = Column(String(100), nullable=True)
    archivo_firma_electronica = Column(String, nullable=True)"""
content = content.replace('    codigo_certificacion_sercop = Column(String(100), nullable=True)\n    foto_perfil = Column(String, nullable=True)', new_columns)

with open(path, "w") as f:
    f.write(content)
