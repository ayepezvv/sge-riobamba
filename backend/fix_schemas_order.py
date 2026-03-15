path = "app/schemas/contratacion.py"
with open(path, "r") as f:
    content = f.read()

import re

# 1. We need to cut the ProcesoItemPacLinkCreate block from the bottom
block_search = r'class ProcesoItemPacLinkCreate\(BaseModel\):\n    item_pac_id: int\n    monto_comprometido: float\n'
content = re.sub(block_search, '', content)

# 2. Re-insert it at the top, right before ProcesoContratacionCreate
new_block = """
class ProcesoItemPacLinkBase(BaseModel):
    item_pac_id: int
    monto_comprometido: float

class ProcesoItemPacLinkCreate(ProcesoItemPacLinkBase):
    pass

class ProcesoItemPacLinkResponse(ProcesoItemPacLinkBase):
    id: int
    proceso_id: int

    class Config:
        from_attributes = True

"""
content = content.replace("class ProcesoContratacionCreate(ProcesoContratacionBase):", new_block + "class ProcesoContratacionCreate(ProcesoContratacionBase):")

with open(path, "w") as f:
    f.write(content)
