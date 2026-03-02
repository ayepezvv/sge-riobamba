from sqlalchemy import Column, Integer, String
from app.db.base_class import Base

class Permission(Base):
    __tablename__ = "permissions"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre_permiso = Column(String(100), unique=True, index=True, nullable=False)
