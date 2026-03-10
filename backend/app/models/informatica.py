from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class SegmentoRed(Base):
    __tablename__ = "segmento_red"
    __table_args__ = {'schema': 'informatica'}

    id = Column(String, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    red_cidr = Column(String, nullable=False)
    descripcion = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)

    direcciones = relationship("DireccionIpAsignada", back_populates="segmento", cascade="all, delete-orphan")

class DireccionIpAsignada(Base):
    __tablename__ = "direccion_ip_asignada"
    __table_args__ = {'schema': 'informatica'}

    id = Column(String, primary_key=True, index=True)
    segmento_id = Column(String, ForeignKey("informatica.segmento_red.id"), nullable=False)
    direccion_ip = Column(String, nullable=False, unique=True)
    mac_address = Column(String, nullable=True)
    nombre_equipo = Column(String, nullable=True)
    dominio = Column(String, nullable=True)
    ubicacion_geografica = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)

    segmento = relationship("SegmentoRed", back_populates="direcciones")
