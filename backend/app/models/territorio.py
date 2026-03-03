from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
from app.db.base_class import Base
from app.models.mixins import AuditMixin

class Red(AuditMixin, Base):
    __tablename__ = "redes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), unique=True, nullable=False)
    codigo = Column(String(50), unique=True, index=True, nullable=False)

    # Relaciones
    sectores = relationship("Sector", back_populates="red", cascade="all, delete-orphan")

class Sector(AuditMixin, Base):
    __tablename__ = "sectores"

    id = Column(Integer, primary_key=True, index=True)
    red_id = Column(Integer, ForeignKey("redes.id", ondelete="CASCADE"), nullable=False)
    nombre = Column(String(100), nullable=False)
    codigo_sector = Column(String(50), unique=True, index=True, nullable=False)

    # Relaciones
    red = relationship("Red", back_populates="sectores")
    rutas = relationship("Ruta", back_populates="sector", cascade="all, delete-orphan")

class Ruta(AuditMixin, Base):
    __tablename__ = "rutas"

    id = Column(Integer, primary_key=True, index=True)
    sector_id = Column(Integer, ForeignKey("sectores.id", ondelete="CASCADE"), nullable=False)
    nombre = Column(String(100), nullable=False)
    codigo_ruta = Column(String(50), unique=True, index=True, nullable=False)

    # Relaciones
    sector = relationship("Sector", back_populates="rutas")

class Barrio(AuditMixin, Base):
    __tablename__ = "barrios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(150), nullable=False, index=True)
    # Geometría EPSG:4326 (WGS84 estándar) o 32717 (UTM 17S - Ecuador), usaremos 4326 para mapas web por defecto
    geometria = Column(Geometry(geometry_type='MULTIPOLYGON', srid=4326), nullable=True)

class Calle(AuditMixin, Base):
    __tablename__ = "calles"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(200), nullable=False, index=True)
    tipo = Column(String(50), nullable=False) # ej: Principal, Secundaria, Pasaje
    geometria = Column(Geometry(geometry_type='MULTILINESTRING', srid=4326), nullable=True)

