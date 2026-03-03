from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from app.db.base_class import Base

class AuditMixin:
    """
    Mixin para proveer a todos los modelos de trazabilidad de datos universales
    """
    creado_en = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    actualizado_en = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Usaremos ondelete="SET NULL" para no perder la trazabilidad si el usuario es eliminado
    creado_por_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    actualizado_por_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

class AuditLog(Base):
    """
    Tabla genérica para auditoría profunda de cambios críticos
    """
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    tabla_afectada = Column(String(100), nullable=False, index=True)
    registro_id = Column(Integer, nullable=False, index=True)
    accion = Column(String(50), nullable=False) # INSERT, UPDATE, DELETE
    valores_viejos = Column(Text, nullable=True) # JSON serializado
    valores_nuevos = Column(Text, nullable=True) # JSON serializado
    
    # Metadatos del evento
    fecha_evento = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    usuario_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
