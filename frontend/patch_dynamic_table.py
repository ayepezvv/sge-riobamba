import re

path = "/home/ayepez/.openclaw/workspace/sge/frontend/src/app/(dashboard)/contratacion/procesos/[id]/page.tsx"
with open(path, "r") as f:
    content = f.read()

# Add the image handler for table rows
new_handler = """
  const handleRowImageUpload = (varName: string, rowIndex: number, key: string, e: any) => {
    const file = e.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onloadend = () => {
            handleRowPropChange(varName, rowIndex, key, reader.result as string);
        };
        reader.readAsDataURL(file);
    }
  };
"""

content = content.replace("  const handleRowPropChange =", new_handler + "\n  const handleRowPropChange =")

# Replace the inner map for table fields
old_grid_map = """                                   <Grid container spacing={1}>
                                      {Object.keys(row).map(key => (
                                         <Grid item xs={12} sm={6} key={key}>
                                            <TextField label={key} size="small" value={row[key]} onChange={(e) => handleRowPropChange(v.nombre, rIndex, key, e.target.value)} fullWidth />
                                         </Grid>
                                      ))}
                                      <Grid item xs={12}>
                                         <Button size="small" variant="text" onClick={() => handleAddPropToRow(v.nombre, rIndex)}>+ Añadir Atributo</Button>
                                      </Grid>
                                   </Grid>"""

new_grid_map = """                                   <Grid container spacing={2} alignItems="center">
                                      {Object.keys(row).map(key => {
                                        const isImage = key.toLowerCase().includes('img_');
                                        const isSelect = ['disponibilidad', 'aplica', 'estado'].some(word => key.toLowerCase().includes(word));
                                        
                                        return (
                                         <Grid item xs={12} sm={isImage ? 4 : isSelect ? 3 : 5} key={key}>
                                            {isImage ? (
                                              <Box sx={{ border: '1px dashed grey', p: 1, borderRadius: 1, textAlign: 'center', height: '100%', display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
                                                <Typography variant="caption" display="block" sx={{mb: 0.5}}>📸 {key}</Typography>
                                                <Button variant="outlined" size="small" component="label" sx={{ textTransform: 'none' }}>
                                                  Subir Imagen
                                                  <input type="file" accept="image/*" hidden onChange={(e) => handleRowImageUpload(v.nombre, rIndex, key, e)} />
                                                </Button>
                                                {row[key] && <img src={row[key]} alt="preview" style={{maxHeight: 40, marginTop: 4, alignSelf: 'center'}} />}
                                              </Box>
                                            ) : isSelect ? (
                                              <FormControl fullWidth size="small">
                                                <InputLabel>{key.replace(/_/g, ' ').toUpperCase()}</InputLabel>
                                                <Select
                                                  value={row[key] || 'NO'}
                                                  label={key.replace(/_/g, ' ').toUpperCase()}
                                                  onChange={(e) => handleRowPropChange(v.nombre, rIndex, key, e.target.value)}
                                                >
                                                  <MenuItem value="SI">SÍ</MenuItem>
                                                  <MenuItem value="NO">NO</MenuItem>
                                                </Select>
                                              </FormControl>
                                            ) : (
                                              <TextField 
                                                label={key.replace(/_/g, ' ').toUpperCase()} 
                                                size="small" 
                                                value={row[key]} 
                                                onChange={(e) => handleRowPropChange(v.nombre, rIndex, key, e.target.value)} 
                                                fullWidth 
                                              />
                                            )}
                                         </Grid>
                                        );
                                      })}
                                      <Grid item xs={12}>
                                         <Button size="small" variant="text" onClick={() => handleAddPropToRow(v.nombre, rIndex)}>+ Añadir Atributo</Button>
                                      </Grid>
                                   </Grid>"""

content = content.replace(old_grid_map, new_grid_map)

with open(path, "w") as f:
    f.write(content)
