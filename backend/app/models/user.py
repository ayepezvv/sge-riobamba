from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class User(Base):
    __tablename__ = "usuarios"
    __table_args__ = {"schema": "configuracion"}

    id = Column(Integer, primary_key=True, index=True)
    cedula = Column(String(20), unique=True, index=True, nullable=False)
    nombres = Column(String(100), nullable=False)
    apellidos = Column(String(100), nullable=False)
    correo = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)

    # Relación M:1 con Roles
    role_id = Column(Integer, ForeignKey("configuracion.roles.id", ondelete="SET NULL"), nullable=True)
    role = relationship("Role", back_populates="users")
