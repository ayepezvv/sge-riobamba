import re

path = "/home/ayepez/.openclaw/workspace/sge/frontend/src/app/(dashboard)/contratacion/procesos/[id]/page.tsx"
with open(path, "r") as f:
    content = f.read()

# I will replace the entire logic for handling rows inside the tabla_dinamica renderer 
# to absolutely match the prompt requirements and ensure no ghost updates.

old_table_render = re.search(r'\{\(Array\.isArray\(dinamicData\[v\.nombre\]\)\s*\?\s*dinamicData\[v\.nombre\]\s*:\s*\[\]\)\.map.*?\+\s*Agregar\s*Registro\s*</Button>\s*</Box>', content, re.DOTALL)

new_table_render = """{(Array.isArray(dinamicData[v.nombre]) ? dinamicData[v.nombre] : []).map((row: any, rIndex: number) => (
                             <Card key={rIndex} sx={{ mb: 2, border: '1px solid', borderColor: 'divider', boxShadow: 'none' }}>
                                 <CardContent sx={{ p: '12px !important', bgcolor: 'grey.50' }}>
                                   <Box sx={{display:'flex', justifyContent:'space-between', mb: 2, alignItems: 'center'}}>
                                      <Typography variant="caption" fontWeight="bold" color="primary">Registro {rIndex + 1}</Typography>
                                      <IconButton size="small" color="error" onClick={() => handleRemoveRow(v.nombre, rIndex)}><CloseIcon fontSize="small"/></IconButton>
                                   </Box>
                                   
                                   {Object.keys(row).map((colKey) => {
                                      // REGLA A: Selector SÍ/NO
                                      if (colKey.toLowerCase().includes('disponibilidad') || colKey.toLowerCase().includes('aplica') || colKey.toLowerCase().includes('estado')) {
                                        return (
                                          <FormControl fullWidth sx={{ mb: 2 }} key={colKey} size="small">
                                            <InputLabel>{colKey.replace(/_/g, ' ').toUpperCase()}</InputLabel>
                                            <Select
                                              value={row[colKey] || 'NO'}
                                              label={colKey.replace(/_/g, ' ').toUpperCase()}
                                              onChange={(e) => handleRowPropChange(v.nombre, rIndex, colKey, e.target.value)}
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
                                          <Box key={colKey} sx={{ mb: 2 }}>
                                            <Button variant={row[colKey] ? "contained" : "outlined"} color={row[colKey] ? "success" : "primary"} component="label" fullWidth size="small">
                                              {row[colKey] ? `✅ Imagen Cargada (Clic para cambiar ${colKey})` : `📸 Subir Imagen (${colKey})`}
                                              <input 
                                                type="file" 
                                                hidden 
                                                accept="image/*" 
                                                onChange={(e) => handleRowImageUpload(v.nombre, rIndex, colKey, e)} 
                                              />
                                            </Button>
                                            {row[colKey] && <img src={row[colKey]} alt="preview" style={{maxHeight: 60, marginTop: 4, display: 'block', margin: '4px auto'}} />}
                                          </Box>
                                        );
                                      }
                                      
                                      // REGLA C: Texto por defecto
                                      return (
                                        <TextField 
                                          key={colKey} 
                                          label={colKey.replace(/_/g, ' ').toUpperCase()} 
                                          fullWidth 
                                          sx={{ mb: 2 }} 
                                          size="small"
                                          value={row[colKey] || ''} 
                                          onChange={(e) => handleRowPropChange(v.nombre, rIndex, colKey, e.target.value)} 
                                        />
                                      );
                                   })}
                                   
                                   <Button size="small" variant="text" onClick={() => handleAddPropToRow(v.nombre, rIndex)}>+ Añadir Nueva Columna/Atributo</Button>
                                 </CardContent>
                             </Card>
                          ))}
                          <Button variant="outlined" size="small" onClick={() => handleAddRow(v.nombre)}>+ Agregar Registro</Button>
                        </Box>"""

if old_table_render:
    content = content.replace(old_table_render.group(0), new_table_render)
else:
    print("Could not find the target string to replace.")

with open(path, "w") as f:
    f.write(content)
