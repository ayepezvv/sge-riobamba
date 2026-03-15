from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Enum, Date
from sqlalchemy.orm import relationship
import enum
from app.db.base_class import Base

class EstadoFisico(enum.Enum):
    BUENO = "BUENO"
    REGULAR = "REGULAR"
    MALO = "MALO"
    DE_BAJA = "DE_BAJA"

class CategoriaBien(Base):
    __tablename__ = "categorias"
    __table_args__ = {"schema": "bodega"}

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), unique=True, nullable=False)
    descripcion = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)

    activos = relationship("ActivoFijo", back_populates="categoria")

class ActivoFijo(Base):
    __tablename__ = "activos_fijos"
    __table_args__ = {"schema": "bodega"}

    id = Column(Integer, primary_key=True, index=True)
    codigo_inventario = Column(String(50), unique=True, index=True, nullable=False)
    nombre = Column(String(150), nullable=False)
    descripcion = Column(String(255), nullable=True)
    marca = Column(String(100), nullable=True)
    modelo = Column(String(100), nullable=True)
    numero_serie = Column(String(100), nullable=True)
    
    costo_inicial = Column(Float, nullable=True)
    valor_depreciado = Column(Float, nullable=True)
    fecha_compra = Column(Date, nullable=True)
    factura_referencia = Column(String(100), nullable=True)
    
    estado_fisico = Column(Enum(EstadoFisico, name="estado_fisico"), default=EstadoFisico.BUENO)
    categoria_id = Column(Integer, ForeignKey("bodega.categorias.id"), nullable=False)
    is_active = Column(Boolean, default=True)

    categoria = relationship("CategoriaBien", back_populates="activos")
