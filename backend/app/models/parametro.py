from sqlalchemy import Column, Integer, String
from app.db.base_class import Base
from app.models.mixins import AuditMixin

class ParametroSistema(AuditMixin, Base):
    __tablename__ = "parametros_sistema"
    __table_args__ = {"schema": "core"}

    id = Column(Integer, primary_key=True, index=True)
    clave = Column(String(100), unique=True, index=True, nullable=False)
    valor = Column(String(255), nullable=False)
    tipo_dato = Column(String(50), nullable=False) # 'int', 'float', 'boolean', 'string', 'json'
    descripcion = Column(String(255), nullable=True)

