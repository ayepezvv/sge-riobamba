from sqlalchemy import Column, String, Boolean, ForeignKey, Integer, BigInteger
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
    # FK actualizada: apunta al nuevo esquema rrhh V3
    # La columna se renombra de personal_id → empleado_id para claridad
    empleado_id = Column(
        BigInteger,
        ForeignKey("rrhh.empleado.id_empleado", ondelete="SET NULL"),
        nullable=True
    )
    activo_id = Column(Integer, ForeignKey("bodega.activos_fijos.id"), nullable=True)
    is_active = Column(Boolean, default=True)

    segmento = relationship("SegmentoRed", back_populates="direcciones")
    # Relación explícita al nuevo modelo Empleado del esquema rrhh
    empleado = relationship("Empleado", foreign_keys=[empleado_id])
    activo = relationship("ActivoFijo")
