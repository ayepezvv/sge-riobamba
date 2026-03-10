path_schema = "app/schemas/contratacion.py"
with open(path_schema, "r") as f:
    content_s = f.read()

pac_schemas = """
# --- PAC ---
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

# --- ProcesoContratacion ---
"""
content_s = content_s.replace("# --- ProcesoContratacion ---", pac_schemas)

with open(path_schema, "w") as f:
    f.write(content_s)

path_api = "app/api/routes/contratacion.py"
with open(path_api, "r") as f:
    content_a = f.read()

# Add imports
content_a = content_a.replace("ProcesoContratacion, DocumentoGenerado", "ProcesoContratacion, DocumentoGenerado, PacAnual, ItemPac, ProcesoItemPacLink")
content_a = content_a.replace("RegenerarDocumentoRequest", "RegenerarDocumentoRequest, PacAnualCreate, PacAnualResponse, ItemPacCreate, ItemPacResponse, ProcesoItemPacLinkCreate")

pac_endpoints = """
# --- PAC Endpoints ---
@router.post("/pac", response_model=PacAnualResponse, status_code=status.HTTP_201_CREATED)
def crear_pac(req: PacAnualCreate, db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_user)):
    db_obj = PacAnual(**req.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

@router.get("/pac", response_model=List[PacAnualResponse])
def listar_pac(db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_user)):
    return db.query(PacAnual).options(joinedload(PacAnual.items)).all()

@router.post("/pac/{id}/items", response_model=ItemPacResponse, status_code=status.HTTP_201_CREATED)
def agregar_item_pac(id: int, req: ItemPacCreate, db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_user)):
    db_obj = ItemPac(**req.dict(), pac_anual_id=id)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

@router.post("/procesos/{id}/vincular_pac")
def vincular_pac_proceso(id: int, req_links: List[ProcesoItemPacLinkCreate], db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_user)):
    proceso = db.query(ProcesoContratacion).filter(ProcesoContratacion.id == id).first()
    if not proceso:
        raise HTTPException(status_code=404, detail="Proceso no encontrado")
    
    # Clean existing links
    db.query(ProcesoItemPacLink).filter(ProcesoItemPacLink.proceso_id == id).delete()
    
    for link in req_links:
        db_link = ProcesoItemPacLink(
            proceso_id=id,
            item_pac_id=link.item_pac_id,
            monto_comprometido=link.monto_comprometido
        )
        db.add(db_link)
    db.commit()
    return {"ok": True}

"""
content_a += pac_endpoints

with open(path_api, "w") as f:
    f.write(content_a)
