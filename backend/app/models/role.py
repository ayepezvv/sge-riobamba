from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base

# Tabla intermedia Muchos a Muchos (Role <-> Permission)
role_permission = Table(
    "rol_permiso",
    Base.metadata,
    Column("role_id", Integer, ForeignKey("configuracion.roles.id", ondelete="CASCADE"), primary_key=True),
    Column("permission_id", Integer, ForeignKey("configuracion.permisos.id", ondelete="CASCADE"), primary_key=True),
    schema="configuracion"
)

class Role(Base):
    __tablename__ = "roles"
    __table_args__ = {"schema": "configuracion"}

    id = Column(Integer, primary_key=True, index=True)
    nombre_rol = Column(String(50), unique=True, index=True, nullable=False)
    descripcion = Column(String(255))

    # Relación M:M con Permisos
    permissions = relationship("Permission", secondary=role_permission, backref="roles")
    # Relación 1:M con Usuarios
    users = relationship("User", back_populates="role")
