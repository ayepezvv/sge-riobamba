path = "app/schemas/contratacion.py"
with open(path, "r") as f:
    content = f.read()

# Make sure schemas are fully injected
pac_s = """
class ItemPacBase(BaseModel):
    partida_presupuestaria: str
    cpc: Optional[str] = None
    tipo_compra: Optional[str] = None
    procedimiento: Optional[str] = None
    descripcion: str
    cantidad: float
    costo_unitario: float
    valor_total: float

class ItemPacCreate(ItemPacBase):
    pass

class ItemPacResponse(ItemPacBase):
    id: int
    pac_anual_id: int

    class Config:
        from_attributes = True

class PacAnualBase(BaseModel):
    anio: int
    version_reforma: int
    descripcion: Optional[str] = None
    es_activo: bool = True

class PacAnualCreate(PacAnualBase):
    pass

class PacAnualResponse(PacAnualBase):
    id: int
    items: List[ItemPacResponse] = []

    class Config:
        from_attributes = True

class ProcesoItemPacLinkCreate(BaseModel):
    item_pac_id: int
    monto_comprometido: float
"""
if "PacAnualCreate" not in content:
    content += pac_s
with open(path, "w") as f:
    f.write(content)
