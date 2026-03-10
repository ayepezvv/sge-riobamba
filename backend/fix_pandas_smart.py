path = "app/api/routes/contratacion.py"
with open(path, "r") as f:
    content = f.read()

import re

old_block_search = r'    try:\n        if ext == "csv":\n            # Pandas is smart enough.*?    for index, row in df\.iterrows\(\):'

new_block = """    try:
        if ext == "csv":
            try:
                df = pd.read_csv(io.BytesIO(contents), encoding='utf-8')
            except UnicodeDecodeError:
                # Failsafe para archivos generados por Excel/Windows antiguos
                df = pd.read_csv(io.BytesIO(contents), encoding='latin1')
        else:
            df = pd.read_excel(io.BytesIO(contents))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"No se pudo leer el archivo: {str(e)}")

    # 1. Limpiar los nombres de columnas originales del archivo (quitar espacios sobrantes)
    df.columns = df.columns.str.strip()
    
    # 2. Mapeo Inteligente (Diccionario Traductor)
    mapeo_columnas = {
        'Partida Pres.': 'partida_presupuestaria',
        'CPC': 'cpc',
        'Tipo de Compra': 'tipo_compra',
        'Procedimiento': 'procedimiento',
        'Descripción': 'descripcion',
        'Cant.': 'cantidad',
        'Costo U.': 'costo_unitario',
        'V. Total': 'valor_total'
    }
    
    # Aplicar traduccion
    df = df.rename(columns=mapeo_columnas)
    
    # 3. Verificacion de Columnas Obligatorias
    columnas_requeridas = ['partida_presupuestaria', 'descripcion']
    columnas_faltantes = [col for col in columnas_requeridas if col not in df.columns]
    
    if columnas_faltantes:
        raise HTTPException(
            status_code=400, 
            detail=f"El archivo no tiene el formato correcto del SERCOP. Faltan las columnas mapeadas: {', '.join(columnas_faltantes)}"
        )

    # 4. Prevenir que SQLAlchemy explote por los NaNs nativos de Pandas
    df = df.replace({np.nan: None})

    def clean_money(val):
        if val is None: return 0.0
        if isinstance(val, (int, float)): return float(val)
        val_str = str(val).replace('$', '').replace(',', '').strip()
        try: return float(val_str)
        except: return 0.0

    items_to_insert = []
    
    for index, row in df.iterrows():"""

content = re.sub(old_block_search, new_block, content, flags=re.DOTALL)

old_row_logic = r'            partida = str\(row\[col_partida\]\).*?status=StatusItemPac\.ACTIVO\n            \)'

new_row_logic = """            partida = str(row['partida_presupuestaria']) if row['partida_presupuestaria'] else "N/A"
            if partida == "N/A" or partida.strip() == "" or partida == "None": continue # Skip empty lines
            
            item = ItemPac(
                pac_anual_id=id,
                partida_presupuestaria=partida,
                cpc=str(row['cpc']) if 'cpc' in df.columns and row['cpc'] else None,
                tipo_compra=str(row['tipo_compra']) if 'tipo_compra' in df.columns and row['tipo_compra'] else "Bien/Servicio",
                procedimiento=str(row['procedimiento']) if 'procedimiento' in df.columns and row['procedimiento'] else None,
                descripcion=str(row['descripcion']) if row['descripcion'] else "Sin descripcion",
                cantidad=clean_money(row['cantidad']) if 'cantidad' in df.columns else 1.0,
                costo_unitario=clean_money(row['costo_unitario']) if 'costo_unitario' in df.columns else 0.0,
                valor_total=clean_money(row['valor_total']) if 'valor_total' in df.columns else 0.0,
                status=StatusItemPac.ACTIVO
            )"""

content = re.sub(old_row_logic, new_row_logic, content, flags=re.DOTALL)

with open(path, "w") as f:
    f.write(content)
