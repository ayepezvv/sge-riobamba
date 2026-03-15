import re

path_schemas = "app/schemas/contratacion.py"
with open(path_schemas, "r") as f:
    content_s = f.read()

# Update ProcesoContratacionCreate to include links
if "items_pac: Optional[List[ProcesoItemPacLinkCreate]] = []" not in content_s:
    old_pcc = """class ProcesoContratacionCreate(ProcesoContratacionBase):
    pass"""
    new_pcc = """class ProcesoContratacionCreate(ProcesoContratacionBase):
    items_pac: Optional[List[ProcesoItemPacLinkCreate]] = []"""
    content_s = content_s.replace(old_pcc, new_pcc)

    # And add to Update as well just in case
    old_pcu = """class ProcesoContratacionUpdate(ProcesoContratacionBase):
    pass"""
    new_pcu = """class ProcesoContratacionUpdate(ProcesoContratacionBase):
    items_pac: Optional[List[ProcesoItemPacLinkCreate]] = []"""
    content_s = content_s.replace(old_pcu, new_pcu)
    
    with open(path_schemas, "w") as f:
        f.write(content_s)

path_api = "app/api/routes/contratacion.py"
with open(path_api, "r") as f:
    content_a = f.read()

# Update create_proceso to handle items_pac array
old_create = """@router.post("/procesos", response_model=ProcesoContratacionResponse)
def create_proceso(item_in: ProcesoContratacionCreate, db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_user)):
    db_item = ProcesoContratacion(**item_in.model_dump(), usuario_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item"""

new_create = """@router.post("/procesos", response_model=ProcesoContratacionResponse)
def create_proceso(item_in: ProcesoContratacionCreate, db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_user)):
    data = item_in.model_dump()
    items_pac = data.pop("items_pac", [])
    
    db_item = ProcesoContratacion(**data, usuario_id=current_user.id)
    db.add(db_item)
    db.flush() # get id
    
    for link in items_pac:
        db_link = ProcesoItemPacLink(
            proceso_id=db_item.id,
            item_pac_id=link['item_pac_id'],
            monto_comprometido=link['monto_comprometido']
        )
        db.add(db_link)
        
    db.commit()
    db.refresh(db_item)
    return db_item"""

content_a = content_a.replace(old_create, new_create)

# Also update put_proceso to handle it if we want
old_put = """@router.put("/procesos/{id}", response_model=ProcesoContratacionResponse)
def update_proceso(id: int, item_in: ProcesoContratacionUpdate, db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_user)):
    db_item = db.query(ProcesoContratacion).filter(ProcesoContratacion.id == id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Proceso no encontrado")
        
    update_data = item_in.model_dump(exclude_unset=True)
    for field in update_data:
        setattr(db_item, field, update_data[field])
        
    db.commit()
    db.refresh(db_item)
    return db_item"""

new_put = """@router.put("/procesos/{id}", response_model=ProcesoContratacionResponse)
def update_proceso(id: int, item_in: ProcesoContratacionUpdate, db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_user)):
    db_item = db.query(ProcesoContratacion).filter(ProcesoContratacion.id == id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Proceso no encontrado")
        
    update_data = item_in.model_dump(exclude_unset=True)
    items_pac = update_data.pop("items_pac", None)
    
    for field in update_data:
        setattr(db_item, field, update_data[field])
        
    if items_pac is not None:
        db.query(ProcesoItemPacLink).filter(ProcesoItemPacLink.proceso_id == id).delete()
        for link in items_pac:
            db_link = ProcesoItemPacLink(
                proceso_id=id,
                item_pac_id=link['item_pac_id'],
                monto_comprometido=link['monto_comprometido']
            )
            db.add(db_link)
            
    db.commit()
    db.refresh(db_item)
    return db_item"""

content_a = content_a.replace(old_put, new_put)

with open(path_api, "w") as f:
    f.write(content_a)
