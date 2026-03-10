from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum, UniqueConstraint, Float
from sqlalchemy.orm import relationship
from app.db.base_class import Base
import enum


class NivelEducacion(enum.Enum):
    TECNICO = "TECNICO"
    TECNOLOGICO = "TECNOLOGICO"
    TERCER_NIVEL = "TERCER_NIVEL"
    CUARTO_NIVEL = "CUARTO_NIVEL"
    PHD = "PHD"

class TipoRegimenLegal(enum.Enum):
    LOEP = "LOEP"
    CODIGO_TRABAJO = "CODIGO_TRABAJO"

class TipoContrato(enum.Enum):
    NOMBRAMIENTO = "NOMBRAMIENTO"
    INDEFINIDO = "INDEFINIDO"
    CONTRATADO_LOEP = "CONTRATADO_LOEP"
    CONTRATADO_CT = "CONTRATADO_CT"
    REQUERIDO_PROYECTO = "REQUERIDO_PROYECTO"

class Puesto(Base):
    __tablename__ = "puestos"
    __table_args__ = {"schema": "administracion"}

    id = Column(Integer, primary_key=True, index=True)
    denominacion = Column(String(150), nullable=False)
    escala_ocupacional = Column(String(100), nullable=True)
    remuneracion_mensual = Column(Float, nullable=False)
    partida_presupuestaria = Column(String(100), nullable=False)
    es_activo = Column(Boolean, default=True)

    personal = relationship("Personal", back_populates="puesto")

class Direccion(Base):
    __tablename__ = "direcciones"
    __table_args__ = {"schema": "administracion"}

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(150), unique=True, nullable=False)
    descripcion = Column(String(255), nullable=True)
    es_activo = Column(Boolean, default=True)

    unidades = relationship("Unidad", back_populates="direccion", cascade="all, delete-orphan")

class Unidad(Base):
    __tablename__ = "unidades"
    __table_args__ = {"schema": "administracion"}

    id = Column(Integer, primary_key=True, index=True)
    direccion_id = Column(Integer, ForeignKey("administracion.direcciones.id", ondelete="CASCADE"), nullable=False)
    nombre = Column(String(150), nullable=False)
    descripcion = Column(String(255), nullable=True)
    es_activo = Column(Boolean, default=True)

    direccion = relationship("Direccion", back_populates="unidades")
    personal = relationship("Personal", back_populates="unidad")

class Personal(Base):
    __tablename__ = "personal"
    __table_args__ = {"schema": "administracion"}

    id = Column(Integer, primary_key=True, index=True)
    unidad_id = Column(Integer, ForeignKey("administracion.unidades.id", ondelete="RESTRICT"), nullable=False)
    usuario_id = Column(Integer, ForeignKey("configuracion.usuarios.id", ondelete="SET NULL"), nullable=True, unique=True)
    puesto_id = Column(Integer, ForeignKey("administracion.puestos.id", ondelete="RESTRICT"), nullable=True)
    
    cedula = Column(String(20), unique=True, nullable=False, index=True)
    nombres = Column(String(100), nullable=False)
    apellidos = Column(String(100), nullable=False)
    cargo = Column(String(150), nullable=False)
    
    regimen_legal = Column(Enum(TipoRegimenLegal, name="tipo_regimen_legal"), nullable=False)
    tipo_contrato = Column(Enum(TipoContrato, name="tipo_contrato"), nullable=False)
    codigo_certificacion_sercop = Column(String(100), nullable=True)
    foto_perfil = Column(String, nullable=True)
    direccion_domicilio = Column(String(255), nullable=True)
    telefono_celular = Column(String(20), nullable=True)
    correo_personal = Column(String(100), nullable=True)
    archivo_firma_electronica = Column(String, nullable=True)
    
    es_activo = Column(Boolean, default=True)

    unidad = relationship("Unidad", back_populates="personal")
    usuario = relationship("User", backref="personal_link")
    titulos = relationship("TituloProfesional", back_populates="personal", cascade="all, delete-orphan")
    puesto = relationship("Puesto", back_populates="personal")

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

