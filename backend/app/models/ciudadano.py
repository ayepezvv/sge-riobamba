from sqlalchemy import Column, Integer, String, Boolean, Float, Date, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from app.models.mixins import AuditMixin

class Ciudadano(AuditMixin, Base):
    __tablename__ = "ciudadanos"

    id = Column(Integer, primary_key=True, index=True)
    tipo_persona = Column(String(20), nullable=False) # 'Natural', 'Juridica'
    identificacion = Column(String(20), unique=True, index=True, nullable=False)
    
    # Nombres/Apellidos para Natural, Razon Social para Juridica
    nombres = Column(String(100), nullable=True)
    apellidos = Column(String(100), nullable=True)
    razon_social = Column(String(200), nullable=True)

    # Contacto
    correo_principal = Column(String(150), nullable=True)
    telefono_fijo = Column(String(20), nullable=True)
    celular = Column(String(20), nullable=True)
    preferencia_contacto = Column(String(50), nullable=True) # WhatsApp, Messenger, SMS, Correo
    redes_sociales = Column(JSONB, nullable=True) # Para multiples perfiles/correos extras

    # Especificos Persona Natural
    fecha_nacimiento = Column(Date, nullable=True)
    nacionalidad = Column(String(50), nullable=True)
    genero = Column(String(20), nullable=True)
    estado_civil = Column(String(50), nullable=True)

    # Beneficios de Ley
    tiene_discapacidad = Column(Boolean, default=False)
    porcentaje_discapacidad = Column(Float, default=0.0)
    aplica_tercera_edad = Column(Boolean, default=False) # Se validara via backend usando fecha_nacimiento

    # Especificos Persona Juridica
    tipo_empresa = Column(String(50), nullable=True) # Publica, Privada
    naturaleza_juridica = Column(String(50), nullable=True) # Personal, Sociedad

    # Relaciones
    referencias = relationship("ReferenciaCiudadano", back_populates="ciudadano", cascade="all, delete-orphan")


class ReferenciaCiudadano(AuditMixin, Base):
    __tablename__ = "referencias_ciudadanos"

    id = Column(Integer, primary_key=True, index=True)
    ciudadano_id = Column(Integer, ForeignKey("ciudadanos.id", ondelete="CASCADE"), nullable=False)
    tipo_referencia = Column(String(50), nullable=False) # Conyuge, Representante Legal, Referencia Familiar, Referencia Personal
    nombres = Column(String(100), nullable=False)
    apellidos = Column(String(100), nullable=False)
    identificacion = Column(String(20), nullable=True)
    telefono = Column(String(20), nullable=True)
    correo = Column(String(150), nullable=True)

    ciudadano = relationship("Ciudadano", back_populates="referencias")
