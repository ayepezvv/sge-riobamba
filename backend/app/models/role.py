from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base

# Tabla intermedia Muchos a Muchos (Role <-> Permission)
role_permission = Table(
    "role_permission",
    Base.metadata,
    Column("role_id", Integer, ForeignKey("administracion.roles.id", ondelete="CASCADE"), primary_key=True),
    Column("permission_id", Integer, ForeignKey("administracion.permissions.id", ondelete="CASCADE"), primary_key=True),
    schema="administracion"
)

class Role(Base):
    __tablename__ = "roles"
    __table_args__ = {"schema": "administracion"}

    id = Column(Integer, primary_key=True, index=True)
    nombre_rol = Column(String(50), unique=True, index=True, nullable=False)
    descripcion = Column(String(255))

    # Relación M:M con Permisos
    permissions = relationship("Permission", secondary=role_permission, backref="roles")
    # Relación 1:M con Usuarios
    users = relationship("User", back_populates="role")
