path_api = "app/api/routes/contratacion.py"
with open(path_api, "r") as f:
    content = f.read()

imports = """from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
import pandas as pd
import io"""

if "UploadFile" not in content:
    content = content.replace("from fastapi import APIRouter, Depends, HTTPException, status", imports)

upload_logic = """
# --- PAC Carga Masiva ---
@router.post("/pac/{id}/importar")
async def importar_pac(id: int, file: UploadFile = File(...), db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_user)):
    pac = db.query(PacAnual).filter(PacAnual.id == id).first()
    if not pac:
        raise HTTPException(status_code=404, detail="PAC no encontrado")
        
    ext = file.filename.split(".")[-1].lower()
    if ext not in ["csv", "xls", "xlsx"]:
        raise HTTPException(status_code=400, detail="Formato no soportado. Usa CSV o Excel.")
        
    contents = await file.read()
    
    try:
        if ext == "csv":
            # Pandas is smart enough to handle most encodings but let's assume utf-8
            df = pd.read_csv(io.BytesIO(contents))
        else:
            df = pd.read_excel(io.BytesIO(contents))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"No se pudo leer el archivo: {str(e)}")

    # Clean headers (lower and strip)
    df.columns = df.columns.str.lower().str.strip()
    
    # Mapeo dinamico (acepta variaciones del nombre de la columna SERCOP)
    def find_col(possible_names):
        for name in possible_names:
            for col in df.columns:
                if name in col: return col
        return None

    col_partida = find_col(["partida", "presupuestaria"])
    col_cpc = find_col(["cpc"])
    col_tipo = find_col(["tipo", "compra"])
    col_proc = find_col(["procedimiento"])
    col_desc = find_col(["descrip"])
    col_cant = find_col(["cant"])
    col_costo = find_col(["costo", "unitario"])
    col_total = find_col(["total", "v. total"])

    if not col_partida or not col_desc:
        raise HTTPException(status_code=400, detail="El archivo no contiene las columnas minimas requeridas (Partida y Descripcion).")

    def clean_money(val):
        if pd.isna(val): return 0.0
        if isinstance(val, (int, float)): return float(val)
        val_str = str(val).replace('$', '').replace(',', '').strip()
        try: return float(val_str)
        except: return 0.0

    items_to_insert = []
    
    for index, row in df.iterrows():
        try:
            partida = str(row[col_partida]) if not pd.isna(row[col_partida]) else "N/A"
            if partida == "N/A" or partida.strip() == "": continue # Skip empty lines
            
            item = ItemPac(
                pac_anual_id=id,
                partida_presupuestaria=partida,
                cpc=str(row[col_cpc]) if col_cpc and not pd.isna(row[col_cpc]) else None,
                tipo_compra=str(row[col_tipo]) if col_tipo and not pd.isna(row[col_tipo]) else "Bien/Servicio",
                procedimiento=str(row[col_proc]) if col_proc and not pd.isna(row[col_proc]) else None,
                descripcion=str(row[col_desc]) if not pd.isna(row[col_desc]) else "Sin descripcion",
                cantidad=clean_money(row[col_cant]) if col_cant else 1.0,
                costo_unitario=clean_money(row[col_costo]) if col_costo else 0.0,
                valor_total=clean_money(row[col_total]) if col_total else 0.0,
                status=StatusItemPac.ACTIVO
            )
            items_to_insert.append(item)
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=400, detail=f"Error en la fila Excel {index + 2}: {str(e)}")
            
    try:
        db.add_all(items_to_insert)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error transaccional al guardar en la base de datos.")
        
    return {"ok": True, "filas_procesadas": len(items_to_insert)}

@router.post("/pac/{id}/reforma")
"""

if "@router.post(\"/pac/{id}/importar\")" not in content:
    content = content.replace("@router.post(\"/pac/{id}/reforma\")", upload_logic)
    with open(path_api, "w") as f:
        f.write(content)
