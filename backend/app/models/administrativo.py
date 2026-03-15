"""
Módulo: administracion
Scope: Estructura organizacional base (Direcciones, Unidades, Puestos).
NOTA: Empleado, EscalaSalarial y EmpleadoCargaFamiliar fueron migrados
      al esquema 'rrhh' (app/models/rrhh.py) en la Fase V3.
      NO duplicar esas clases aquí.
"""
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from app.models.mixins import AuditMixin


# ---------------------------------------------------------------------------
# ESTRUCTURA ORGANIZACIONAL
# ---------------------------------------------------------------------------
class Direccion(Base, AuditMixin):
    """Unidades de primer nivel: Dirección de RRHH, Dirección TI, etc."""
    __tablename__ = "direcciones"
    __table_args__ = {"schema": "administracion"}

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(150), unique=True, nullable=False)
    descripcion = Column(String(255), nullable=True)
    es_activo = Column(Boolean, default=True)

    unidades = relationship("Unidad", back_populates="direccion", cascade="all, delete-orphan")


class Unidad(Base, AuditMixin):
    """Sub-unidades dentro de una Dirección."""
    __tablename__ = "unidades"
    __table_args__ = {"schema": "administracion"}

    id = Column(Integer, primary_key=True, index=True)
    direccion_id = Column(Integer, ForeignKey("administracion.direcciones.id", ondelete="CASCADE"), nullable=False)
    nombre = Column(String(150), nullable=False)
    descripcion = Column(String(255), nullable=True)
    es_activo = Column(Boolean, default=True)

    direccion = relationship("Direccion", back_populates="unidades")
    # NOTA: Empleado migrado a rrhh.py — relación desvinculada del esquema administracion


class Puesto(Base, AuditMixin):
    """Catálogo de puestos institucionales con partida presupuestaria."""
    __tablename__ = "puestos"
    __table_args__ = {"schema": "administracion"}

    id = Column(Integer, primary_key=True, index=True)
    denominacion = Column(String(150), nullable=False)
    partida_presupuestaria = Column(String(100), nullable=False)
    es_activo = Column(Boolean, default=True)

    # NOTA: Empleado migrado a rrhh.py — relación inversa desvinculada del esquema administracion


# ---------------------------------------------------------------------------
# TABLAS SATÉLITE LEGACY (se mantienen para compatibilidad de FK históricas)
# ---------------------------------------------------------------------------
# NOTA: TituloProfesional ya no tiene relación hacia 'Empleado' de administracion
# porque esa clase fue eliminada. Si la tabla física sigue existiendo en la BD,
# las FKs físicas apuntan a administracion.empleados. Esta clase se conserva
# solo como reflejo ORM de esa tabla física legacy.
class TituloProfesional(Base, AuditMixin):
    """Títulos académicos registrados en SENESCYT (tabla legacy)."""
    __tablename__ = "titulos_profesionales"
    __table_args__ = {"schema": "administracion"}

    id = Column(Integer, primary_key=True, index=True)
    empleado_id = Column(Integer, nullable=False)  # FK física a administracion.empleados (legacy)
    nombre_titulo = Column(String(200), nullable=False)
    institucion = Column(String(200), nullable=False)
    registro_senescyt = Column(String(100), nullable=True)
