path = "app/schemas/contratacion.py"
with open(path, "r") as f:
    content = f.read()

reforma_schemas = """
# --- Reforma PAC ---
class MovimientoReformaCreate(BaseModel):
    item_origen_id: int
    item_destino_id: int
    monto_transferido: float

class ReformaPacCreate(BaseModel):
    numero_reforma: int
    resolucion_administrativa: Optional[str] = None
    descripcion_justificacion: str
    movimientos: List[MovimientoReformaCreate]
    nuevos_items: List[ItemPacCreate]

"""
content += reforma_schemas

with open(path, "w") as f:
    f.write(content)
