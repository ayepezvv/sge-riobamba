import re
path = "app/schemas/contratacion.py"
with open(path, "r") as f:
    content = f.read()

# We need the ItemPacResponse to also include the parent pac data so the frontend can display the year/reforma.
new_schemas = """
class PacAnualSimpleResponse(BaseModel):
    id: int
    anio: int
    version_reforma: int
    
    class Config:
        from_attributes = True

class ItemPacResponse(ItemPacBase):
    id: int
    pac_anual_id: int
    status: Optional[StatusItemPac] = StatusItemPac.ACTIVO
    pac: Optional[PacAnualSimpleResponse] = None

    class Config:
        from_attributes = True
"""
content = re.sub(r'class ItemPacResponse.*?from_attributes = True', new_schemas, content, flags=re.DOTALL)

with open(path, "w") as f:
    f.write(content)
