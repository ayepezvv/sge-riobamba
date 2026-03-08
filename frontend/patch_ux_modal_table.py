import re

path = "/home/ayepez/.openclaw/workspace/sge/frontend/src/app/(dashboard)/contratacion/procesos/[id]/page.tsx"
with open(path, "r") as f:
    content = f.read()

# 1. State logic
new_state = """  const [toast, setToast] = useState({ open: false, message: '', severity: 'success' });

  // UX Modal Table State
  const [openRowModal, setOpenRowModal] = useState(false);
  const [activeTableVar, setActiveTableVar] = useState<string>('');
  const [tempRowItem, setTempRowItem] = useState<any>({});"""

content = content.replace("  const [toast, setToast] = useState({ open: false, message: '', severity: 'success' });", new_state)

# 2. Table modal handlers
advanced_handlers = """  const handleDynamicChange = (nombreVar: string, valor: any) => {
    setDinamicData((prev: any) => ({ ...prev, [nombreVar]: valor }));
  };

  const handleImageUpload = (varName: string, e: any) => {
    const file = e.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onloadend = () => {
            handleDynamicChange(varName, reader.result);
        };
        reader.readAsDataURL(file);
    }
  };

  const handleOpenRowModal = (varName: string) => {
    setActiveTableVar(varName);
    // Initialize with a default structure if the array is empty to guide the user, or let them add properties
    const currentList = Array.isArray(dinamicData[varName]) ? dinamicData[varName] : [];
    if (currentList.length > 0) {
      // Inherit schema from previous row
      const template = { ...currentList[0] };
      for (let k in template) template[k] = '';
      setTempRowItem(template);
    } else {
      setTempRowItem({ propiedad_1: "" }); // Empty slate
    }
    setOpenRowModal(true);
  };

  const handleCloseRowModal = () => {
    setOpenRowModal(false);
    setTempRowItem({});
    setActiveTableVar('');
  };

  const handleTempRowPropChange = (key: string, val: any) => {
    setTempRowItem((prev: any) => ({ ...prev, [key]: val }));
  };

  const handleTempRowImageUpload = (key: string, e: any) => {
    const file = e.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onloadend = () => {
            handleTempRowPropChange(key, reader.result as string);
        };
        reader.readAsDataURL(file);
    }
  };

  const handleAddPropToTempRow = () => {
    const newProp = prompt("Nombre exacto de la variable en el DOCX (Ej. descripcion, img_captura):", "nueva_columna");
    if (newProp && newProp.trim() !== '') {
        handleTempRowPropChange(newProp.trim(), '');
    }
  };

  const handleSaveRow = () => {
    const currentList = Array.isArray(dinamicData[activeTableVar]) ? [...dinamicData[activeTableVar]] : [];
    currentList.push(tempRowItem);
    handleDynamicChange(activeTableVar, currentList);
    handleCloseRowModal();
  };

  const handleRemoveRow = (varName: string, rowIndex: number) => {
    const currentList = [...(dinamicData[varName] || [])];
    currentList.splice(rowIndex, 1);
    handleDynamicChange(varName, currentList);
  };"""

# I need to wipe out the old handlers and inject the new ones
# Replacing the chunk starting at handleDynamicChange
content = re.sub(r'  const handleDynamicChange = \(nombreVar: string, valor: any\) => \{.*?(?=  const handleDocSubmit)', advanced_handlers + "\n\n", content, flags=re.DOTALL)

# 3. Replace the Inline Grid render with the Summary + Add Button approach
old_render = re.search(r'\{\(Array\.isArray\(dinamicData\[v\.nombre\]\)\s*\?\s*dinamicData\[v\.nombre\]\s*:\s*\[\]\)\.map.*?\+\s*Agregar\s*Registro\s*</Button>\s*</Box>', content, re.DOTALL)

new_render = """                          <Box sx={{ mb: 2 }}>
                            {(Array.isArray(dinamicData[v.nombre]) ? dinamicData[v.nombre] : []).map((row: any, rIndex: number) => (
                               <Card key={rIndex} sx={{ mb: 1, border: '1px solid', borderColor: 'divider', boxShadow: 'none' }}>
                                   <CardContent sx={{ p: '12px !important', bgcolor: 'grey.50', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                                     <Box>
                                        <Typography variant="caption" fontWeight="bold" color="primary" display="block" sx={{mb: 0.5}}>Registro {rIndex + 1}</Typography>
                                        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                                          {Object.keys(row).map(k => (
                                            <Chip key={k} label={`${k}: ${k.includes('img_') ? (row[k] ? 'Imagen' : 'N/A') : row[k] || 'N/A'}`} size="small" variant="outlined" />
                                          ))}
                                        </Box>
                                     </Box>
                                     <IconButton size="small" color="error" onClick={() => handleRemoveRow(v.nombre, rIndex)}><CloseIcon fontSize="small"/></IconButton>
                                   </CardContent>
                               </Card>
                            ))}
                          </Box>
                          <Button variant="outlined" size="small" startIcon={<AddIcon />} onClick={() => handleOpenRowModal(v.nombre)}>
                            Agregar Registro a {v.nombre}
                          </Button>
                        </Box>"""

if old_render:
    content = content.replace(old_render.group(0), new_render)

# 4. Inject the new Dialog before the existing Snackbar
new_dialog = """
      {/* Modal UX para Tablas Dinámicas */}
      <Dialog open={openRowModal} onClose={handleCloseRowModal} maxWidth="sm" fullWidth>
        <DialogTitle>Añadir Registro a {activeTableVar}</DialogTitle>
        <DialogContent dividers>
          <Box component="form" sx={{ display: 'flex', flexDirection: 'column', gap: 2.5, mt: 1 }}>
             {Object.keys(tempRowItem).map((colKey) => {
                // REGLA A: Selector SÍ/NO
                if (colKey.toLowerCase().includes('disponibilidad') || colKey.toLowerCase().includes('aplica') || colKey.toLowerCase().includes('estado')) {
                  return (
                    <FormControl fullWidth key={colKey} size="small">
                      <InputLabel>{colKey.replace(/_/g, ' ').toUpperCase()}</InputLabel>
                      <Select
                        value={tempRowItem[colKey] || 'NO'}
                        label={colKey.replace(/_/g, ' ').toUpperCase()}
                        onChange={(e) => handleTempRowPropChange(colKey, e.target.value)}
                      >
                        <MenuItem value="SÍ">SÍ</MenuItem>
                        <MenuItem value="NO">NO</MenuItem>
                      </Select>
                    </FormControl>
                  );
                }
                
                // REGLA B: Subida de Imagen
                if (colKey.toLowerCase().includes('img_')) {
                  return (
                    <Box key={colKey}>
                      <Button variant={tempRowItem[colKey] ? "contained" : "outlined"} color={tempRowItem[colKey] ? "success" : "primary"} component="label" fullWidth size="small">
                        {tempRowItem[colKey] ? `✅ Imagen Cargada (${colKey})` : `📸 Subir Imagen (${colKey})`}
                        <input 
                          type="file" 
                          hidden 
                          accept="image/*" 
                          onChange={(e) => handleTempRowImageUpload(colKey, e)} 
                        />
                      </Button>
                      {tempRowItem[colKey] && <img src={tempRowItem[colKey]} alt="preview" style={{maxHeight: 60, marginTop: 4, display: 'block', margin: '4px auto'}} />}
                    </Box>
                  );
                }
                
                // REGLA C: Texto por defecto
                return (
                  <TextField 
                    key={colKey} 
                    label={colKey.replace(/_/g, ' ').toUpperCase()} 
                    fullWidth 
                    size="small"
                    value={tempRowItem[colKey] || ''} 
                    onChange={(e) => handleTempRowPropChange(colKey, e.target.value)} 
                  />
                );
             })}
             <Button size="small" variant="text" onClick={handleAddPropToTempRow}>+ Añadir Nueva Columna/Atributo</Button>
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseRowModal} color="error" variant="text">Cancelar</Button>
          <Button onClick={handleSaveRow} variant="contained" color="primary">Guardar Registro</Button>
        </DialogActions>
      </Dialog>
"""

content = content.replace("<Snackbar open={toast.open}", new_dialog + "\n      <Snackbar open={toast.open}")

with open(path, "w") as f:
    f.write(content)
