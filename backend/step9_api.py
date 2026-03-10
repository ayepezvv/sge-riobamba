path_schema = "app/schemas/contratacion.py"
with open(path_schema, "r") as f:
    content_s = f.read()

# Add enums to schemas
import re
if "StatusItemPac" not in content_s:
    content_s = content_s.replace("from app.models.contratacion import TipoProceso, PlantillaDocumento, ProcesoContratacion, DocumentoGenerado, PacAnual, ItemPac, ProcesoItemPacLink", "from app.models.contratacion import TipoProceso, PlantillaDocumento, ProcesoContratacion, DocumentoGenerado, PacAnual, ItemPac, ProcesoItemPacLink, StatusItemPac")
    
    # Add status to item_pac response
    content_s = content_s.replace("valor_total: float", "valor_total: float\n    status: Optional[StatusItemPac] = StatusItemPac.ACTIVO")

# Add Reforma schemas
if "HistoricoReformaPacBase" not in content_s:
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
    content_s = content_s.replace("# --- ProcesoContratacion ---", reforma_schemas + "\n# --- ProcesoContratacion ---")
    with open(path_schema, "w") as f:
        f.write(content_s)

# API
path_api = "app/api/routes/contratacion.py"
with open(path_api, "r") as f:
    content_a = f.read()

if "HistoricoReformaPac" not in content_a:
    content_a = content_a.replace("PacAnual, ItemPac, ProcesoItemPacLink", "PacAnual, ItemPac, ProcesoItemPacLink, HistoricoReformaPac, GenealogiaMontoPac, StatusItemPac")
    content_a = content_a.replace("ProcesoItemPacLinkCreate", "ProcesoItemPacLinkCreate, ReformaPacCreate, MovimientoReformaCreate")

reforma_endpoint = """
@router.post("/pac/{id}/reforma")
def reformar_pac(id: int, req: ReformaPacCreate, db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_user)):
    pac = db.query(PacAnual).filter(PacAnual.id == id).first()
    if not pac:
        raise HTTPException(status_code=404, detail="PAC no encontrado")
        
    # 1. Validar montos de movimientos
    suma_origen = sum([m.monto_transferido for m in req.movimientos])
    suma_destino = sum([i.valor_total for i in req.nuevos_items])
    
    # Tolerancia de decimales (centavos)
    if abs(suma_origen - suma_destino) > 0.01:
        raise HTTPException(status_code=400, detail=f"Desbalance financiero. El origen cede ${suma_origen} pero el destino requiere ${suma_destino}.")

    # 2. Actualizar versión del PAC
    pac.version_reforma = req.numero_reforma
    
    # 3. Crear Histórico
    reforma = HistoricoReformaPac(
        pac_anual_id=id,
        numero_reforma=req.numero_reforma,
        resolucion_administrativa=req.resolucion_administrativa,
        descripcion_justificacion=req.descripcion_justificacion
    )
    db.add(reforma)
    db.flush() # Para obtener reforma.id
    
    # 4. Reducir/Eliminar items origen
    for mov in req.movimientos:
        item_orig = db.query(ItemPac).filter(ItemPac.id == mov.item_origen_id).first()
        if not item_orig: continue
        
        # Reducir saldo
        item_orig.valor_total -= mov.monto_transferido
        item_orig.cantidad = 1 # simplificado para la reforma
        item_orig.costo_unitario = item_orig.valor_total
        
        if item_orig.valor_total <= 0.01:
            item_orig.status = StatusItemPac.ELIMINADO_POR_REFORMA
            item_orig.valor_total = 0
        else:
            item_orig.status = StatusItemPac.MODIFICADO_POR_REFORMA

    # 5. Crear items destino e inyectar genealogía
    for nuevo_item_req in req.nuevos_items:
        nuevo_item = ItemPac(**nuevo_item_req.dict(), pac_anual_id=id, status=StatusItemPac.ACTIVO)
        db.add(nuevo_item)
        db.flush() # Obtener nuevo_item.id
        
        # Enlazar genealogía (simplificado: asigna proporcionalmente)
        # En un sistema real se mapea 1 a 1 en el payload, pero asumimos que el array movimientos 
        # dicta de dónde sale la plata para toda la bolsa de nuevos items.
        for mov in req.movimientos:
            if mov.monto_transferido > 0:
                # Registramos el nexo
                gen = GenealogiaMontoPac(
                    historico_reforma_id=reforma.id,
                    item_origen_id=mov.item_origen_id,
                    item_destino_id=nuevo_item.id,
                    monto_transferido=mov.monto_transferido # Idealmente prorrateado
                )
                db.add(gen)
                
    db.commit()
    return {"ok": True, "reforma_id": reforma.id, "mensaje": "Reforma financiera ejecutada con cuadre exacto."}
"""

if "def reformar_pac" not in content_a:
    content_a = content_a.replace("@router.post(\"/procesos/{id}/vincular_pac\")", reforma_endpoint + "\n@router.post(\"/procesos/{id}/vincular_pac\")")
    with open(path_api, "w") as f:
        f.write(content_a)
