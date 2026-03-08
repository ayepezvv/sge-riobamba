import re

path = "/home/ayepez/.openclaw/workspace/sge/frontend/src/app/(dashboard)/contratacion/procesos/[id]/page.tsx"
with open(path, "r") as f:
    content = f.read()

# Make sure CloseIcon is imported
if "CloseIcon" not in content:
    content = content.replace("import AddIcon", "import CloseIcon from '@mui/icons-material/Close';\nimport AddIcon")

# Also Card and others if missing
if "Card" not in content:
    content = content.replace("Typography, Grid", "Typography, Grid, Card, CardContent")

# Add the new handlers inside the component before return
handlers = """  const handleDynamicChange = (nombreVar: string, valor: any) => {
    setDinamicData({ ...dinamicData, [nombreVar]: valor });
  };"""

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

  const handleAddRow = (varName: string) => {
    const currentList = Array.isArray(dinamicData[varName]) ? dinamicData[varName] : [];
    handleDynamicChange(varName, [...currentList, { propiedad1: "", propiedad2: "" }]);
  };

  const handleRowPropChange = (varName: string, rowIndex: number, key: string, val: string) => {
    const currentList = [...(dinamicData[varName] || [])];
    currentList[rowIndex] = { ...currentList[rowIndex], [key]: val };
    handleDynamicChange(varName, currentList);
  };

  const handleAddPropToRow = (varName: string, rowIndex: number) => {
    const newProp = prompt("Nombre exacto de la variable en el DOCX (Ej. descripcion):", "nueva_columna");
    if (newProp) {
        const currentList = [...(dinamicData[varName] || [])];
        currentList[rowIndex] = { ...currentList[rowIndex], [newProp]: "" };
        handleDynamicChange(varName, currentList);
    }
  };

  const handleRemoveRow = (varName: string, rowIndex: number) => {
    const currentList = [...(dinamicData[varName] || [])];
    currentList.splice(rowIndex, 1);
    handleDynamicChange(varName, currentList);
  };"""

content = content.replace(handlers, advanced_handlers)

# Replace the render logic for the dynamic variables
old_render = """{v.tipo === 'texto' && (
                        <TextField 
                          label={v.nombre.replace(/_/g, ' ').toUpperCase()} 
                          value={dinamicData[v.nombre] || ''} 
                          onChange={(e) => handleDynamicChange(v.nombre, e.target.value)} 
                          fullWidth 
                          multiline={!v.nombre.includes('fecha') && !v.nombre.includes('codigo')}
                          rows={v.nombre.includes('descripcion') || v.nombre.includes('objeto') ? 3 : 1}
                        />
                      )}
                      {v.tipo === 'imagen' && (
                        <Box sx={{ border: '1px dashed grey', p: 2, textAlign: 'center', borderRadius: 1 }}>
                           <Typography variant="body2">📸 Subir Imagen para: {v.nombre}</Typography>
                           <Button size="small" variant="outlined" sx={{ mt: 1 }}>Seleccionar Archivo</Button>
                        </Box>
                      )}
                      {v.tipo === 'tabla_dinamica' && (
                        <Alert severity="info">El motor detectó una tabla dinámica ({v.nombre}). Su integración requerirá un módulo avanzado de presupuesto.</Alert>
                      )}"""

new_render = """{v.tipo === 'texto' && (
                        <TextField 
                          label={v.nombre.replace(/_/g, ' ').toUpperCase()} 
                          value={dinamicData[v.nombre] || ''} 
                          onChange={(e) => handleDynamicChange(v.nombre, e.target.value)} 
                          fullWidth 
                          helperText={v.contexto}
                          multiline={!v.nombre.includes('fecha') && !v.nombre.includes('codigo')}
                          rows={v.nombre.includes('descripcion') || v.nombre.includes('objeto') ? 3 : 1}
                        />
                      )}
                      
                      {v.tipo === 'imagen' && (
                        <Box sx={{ border: '1px dashed grey', p: 2, borderRadius: 1 }}>
                           <Typography variant="body2" color="primary" sx={{mb: 1}}>📸 Subir Imagen para: {v.nombre}</Typography>
                           <input type="file" accept="image/*" onChange={(e) => handleImageUpload(v.nombre, e)} />
                           <Typography variant="caption" color="textSecondary" display="block" sx={{mt: 1}}>{v.contexto}</Typography>
                           {dinamicData[v.nombre] && <img src={dinamicData[v.nombre]} alt="preview" style={{maxHeight: 100, marginTop: 8}} />}
                        </Box>
                      )}
                      
                      {v.tipo === 'tabla_dinamica' && (
                        <Box sx={{ border: '1px solid', borderColor: 'divider', p: 2, borderRadius: 1, bgcolor: 'background.paper' }}>
                          <Typography variant="subtitle2" color="primary">{v.nombre} (Grilla Dinámica)</Typography>
                          <Typography variant="caption" color="textSecondary" display="block" sx={{mb: 2}}>{v.contexto}</Typography>
                          
                          {(Array.isArray(dinamicData[v.nombre]) ? dinamicData[v.nombre] : []).map((row: any, rIndex: number) => (
                             <Card key={rIndex} sx={{ mb: 2, border: '1px solid', borderColor: 'divider', boxShadow: 'none' }}>
                                 <CardContent sx={{ p: '12px !important', bgcolor: 'grey.50' }}>
                                   <Box sx={{display:'flex', justifyContent:'space-between', mb: 1, alignItems: 'center'}}>
                                      <Typography variant="caption" fontWeight="bold">Registro {rIndex + 1}</Typography>
                                      <IconButton size="small" color="error" onClick={() => handleRemoveRow(v.nombre, rIndex)}><CloseIcon fontSize="small"/></IconButton>
                                   </Box>
                                   <Grid container spacing={1}>
                                      {Object.keys(row).map(key => (
                                         <Grid item xs={12} sm={6} key={key}>
                                            <TextField label={key} size="small" value={row[key]} onChange={(e) => handleRowPropChange(v.nombre, rIndex, key, e.target.value)} fullWidth />
                                         </Grid>
                                      ))}
                                      <Grid item xs={12}>
                                         <Button size="small" variant="text" onClick={() => handleAddPropToRow(v.nombre, rIndex)}>+ Añadir Atributo</Button>
                                      </Grid>
                                   </Grid>
                                 </CardContent>
                             </Card>
                          ))}
                          <Button variant="outlined" size="small" onClick={() => handleAddRow(v.nombre)}>+ Agregar Registro</Button>
                        </Box>
                      )}"""

content = content.replace(old_render, new_render)

with open(path, "w") as f:
    f.write(content)
