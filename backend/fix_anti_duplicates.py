path = "app/api/routes/contratacion.py"
with open(path, "r") as f:
    content = f.read()

import re

# We need to inject the logic to prevent duplicates based on existing items.
anti_duplicate_logic = """
    # Lógica Anti-Duplicados
    items_existentes = db.query(ItemPac).filter(ItemPac.pac_anual_id == id).all()
    set_existentes = set()
    for ie in items_existentes:
        key = (str(ie.partida_presupuestaria).strip(), str(ie.cpc).strip(), str(ie.descripcion).strip()[:100])
        set_existentes.add(key)

    items_to_insert = []
    ignorados = 0
"""

content = content.replace("    items_to_insert = []", anti_duplicate_logic)

duplicate_check = """            partida = str(row['partida_presupuestaria']) if row['partida_presupuestaria'] else "N/A"
            if partida == "N/A" or partida.strip() == "" or partida == "None": continue # Skip empty lines
            
            cpc_val = str(row['cpc']) if 'cpc' in df.columns and row['cpc'] else ""
            desc_val = str(row['descripcion']) if row['descripcion'] else "Sin descripcion"
            
            # Verificación en Set
            row_key = (partida.strip(), cpc_val.strip(), desc_val.strip()[:100])
            if row_key in set_existentes:
                ignorados += 1
                continue
                
            item = ItemPac(
                pac_anual_id=id,
                partida_presupuestaria=partida,
                cpc=cpc_val if cpc_val else None,
                tipo_compra=str(row['tipo_compra']) if 'tipo_compra' in df.columns and row['tipo_compra'] else "Bien/Servicio",
                procedimiento=str(row['procedimiento']) if 'procedimiento' in df.columns and row['procedimiento'] else None,
                descripcion=desc_val,"""

content = re.sub(r'            partida = str\(row\[\'partida_presupuestaria\'\]\).*?descripcion=str\(row\[\'descripcion\'\]\) if row\[\'descripcion\'\] else "Sin descripcion",', duplicate_check, content, flags=re.DOTALL)

return_search = """return {"ok": True, "filas_procesadas": len(items_to_insert)}"""
return_replace = """return {"ok": True, "filas_procesadas": len(items_to_insert), "ignoradas_por_duplicado": ignorados}"""
content = content.replace(return_search, return_replace)

# Missing GET /pac/{id}/items endpoint? Let's add it just in case frontend needs it to fetch cleanly
get_items_endpoint = """
@router.get("/pac/{id}/items", response_model=List[ItemPacResponse])
def listar_items_pac(id: int, db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_user)):
    items = db.query(ItemPac).filter(ItemPac.pac_anual_id == id).all()
    return items
"""

if "@router.get(\"/pac/{id}/items\"" not in content:
    content = content.replace("@router.post(\"/pac/{id}/items\",", get_items_endpoint + "\n@router.post(\"/pac/{id}/items\",")

with open(path, "w") as f:
    f.write(content)
