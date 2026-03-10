import re

path_models = "app/models/contratacion.py"
with open(path_models, "r") as f:
    content = f.read()

# Make sure Enum is imported
if "from enum import Enum" not in content:
    content = "import enum\n" + content

# Enums
enums = """
class StatusItemPac(enum.Enum):
    ACTIVO = "ACTIVO"
    ELIMINADO_POR_REFORMA = "ELIMINADO_POR_REFORMA"
    MODIFICADO_POR_REFORMA = "MODIFICADO_POR_REFORMA"

class PacAnual(AuditMixin, Base):"""

content = content.replace("class PacAnual(AuditMixin, Base):", enums)

# Mod ItemPac
item_pac_search = """    valor_total = Column(Float, nullable=False, default=0.0)

    pac = relationship("PacAnual", back_populates="items")"""
item_pac_replace = """    valor_total = Column(Float, nullable=False, default=0.0)
    status = Column(enum.Enum(StatusItemPac, name="status_item_pac"), default=StatusItemPac.ACTIVO, nullable=False)

    pac = relationship("PacAnual", back_populates="items")"""
content = content.replace(item_pac_search, item_pac_replace)

# Historico & Genealogia
historico_models = """
class HistoricoReformaPac(AuditMixin, Base):
    __tablename__ = "historico_reforma_pac"
    __table_args__ = {"schema": "contratacion"}

    id = Column(Integer, primary_key=True, index=True)
    pac_anual_id = Column(Integer, ForeignKey("contratacion.pac_anual.id", ondelete="CASCADE"), nullable=False)
    numero_reforma = Column(Integer, nullable=False)
    fecha_reforma = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    resolucion_administrativa = Column(String(255), nullable=True)
    descripcion_justificacion = Column(Text, nullable=False)

    pac = relationship("PacAnual", backref="reformas")
    movimientos = relationship("GenealogiaMontoPac", back_populates="reforma", cascade="all, delete-orphan")

class GenealogiaMontoPac(Base):
    __tablename__ = "genealogia_monto_pac"
    __table_args__ = {"schema": "contratacion"}

    id = Column(Integer, primary_key=True, index=True)
    historico_reforma_id = Column(Integer, ForeignKey("contratacion.historico_reforma_pac.id", ondelete="CASCADE"), nullable=False)
    item_origen_id = Column(Integer, ForeignKey("contratacion.item_pac.id", ondelete="RESTRICT"), nullable=True)
    item_destino_id = Column(Integer, ForeignKey("contratacion.item_pac.id", ondelete="RESTRICT"), nullable=True)
    monto_transferido = Column(Float, nullable=False)

    reforma = relationship("HistoricoReformaPac", back_populates="movimientos")
    item_origen = relationship("ItemPac", foreign_keys=[item_origen_id])
    item_destino = relationship("ItemPac", foreign_keys=[item_destino_id])

class ProcesoItemPacLink(Base):"""
content = content.replace("class ProcesoItemPacLink(Base):", historico_models)

with open(path_models, "w") as f:
    f.write(content)

path_init = "app/models/__init__.py"
with open(path_init, "r") as f:
    content_init = f.read()

content_init = content_init.replace("PacAnual, ItemPac, ProcesoItemPacLink", "PacAnual, ItemPac, ProcesoItemPacLink, HistoricoReformaPac, GenealogiaMontoPac, StatusItemPac")
with open(path_init, "w") as f:
    f.write(content_init)
