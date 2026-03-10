import re

path_models = "app/models/contratacion.py"
with open(path_models, "r") as f:
    content = f.read()

new_models = """from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, JSON, Text, Float
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from app.models.mixins import AuditMixin

class PacAnual(AuditMixin, Base):
    __tablename__ = "pac_anual"
    __table_args__ = {"schema": "contratacion"}

    id = Column(Integer, primary_key=True, index=True)
    anio = Column(Integer, nullable=False)
    version_reforma = Column(Integer, default=0, nullable=False)
    descripcion = Column(String(255), nullable=True)
    es_activo = Column(Boolean, default=True)

    items = relationship("ItemPac", back_populates="pac", cascade="all, delete-orphan")

class ItemPac(AuditMixin, Base):
    __tablename__ = "item_pac"
    __table_args__ = {"schema": "contratacion"}

    id = Column(Integer, primary_key=True, index=True)
    pac_anual_id = Column(Integer, ForeignKey("contratacion.pac_anual.id", ondelete="CASCADE"), nullable=False)
    partida_presupuestaria = Column(String(100), nullable=False)
    cpc = Column(String(50), nullable=True)
    tipo_compra = Column(String(100), nullable=True)
    procedimiento = Column(String(100), nullable=True)
    descripcion = Column(Text, nullable=False)
    cantidad = Column(Float, nullable=False, default=1.0)
    costo_unitario = Column(Float, nullable=False, default=0.0)
    valor_total = Column(Float, nullable=False, default=0.0)

    pac = relationship("PacAnual", back_populates="items")
    procesos_links = relationship("ProcesoItemPacLink", back_populates="item_pac")

class ProcesoItemPacLink(Base):
    __tablename__ = "proceso_item_pac_link"
    __table_args__ = {"schema": "contratacion"}

    id = Column(Integer, primary_key=True, index=True)
    proceso_id = Column(Integer, ForeignKey("contratacion.proceso_contratacion.id", ondelete="CASCADE"), nullable=False)
    item_pac_id = Column(Integer, ForeignKey("contratacion.item_pac.id", ondelete="CASCADE"), nullable=False)
    monto_comprometido = Column(Float, nullable=False, default=0.0)

    proceso = relationship("ProcesoContratacion", back_populates="items_pac_links")
    item_pac = relationship("ItemPac", back_populates="procesos_links")

"""

content = content.replace("from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, JSON\nfrom sqlalchemy.orm import relationship\nfrom app.db.base_class import Base\nfrom app.models.mixins import AuditMixin\n", new_models)

# Update ProcesoContratacion
content = content.replace('documentos = relationship("DocumentoGenerado", back_populates="proceso")', 'documentos = relationship("DocumentoGenerado", back_populates="proceso")\n    items_pac_links = relationship("ProcesoItemPacLink", back_populates="proceso", cascade="all, delete-orphan")')

with open(path_models, "w") as f:
    f.write(content)

path_init = "app/models/__init__.py"
with open(path_init, "r") as f:
    content_init = f.read()

if "PacAnual" not in content_init:
    content_init = content_init.replace("ProcesoContratacion, DocumentoGenerado", "ProcesoContratacion, DocumentoGenerado, PacAnual, ItemPac, ProcesoItemPacLink")
    with open(path_init, "w") as f:
        f.write(content_init)
