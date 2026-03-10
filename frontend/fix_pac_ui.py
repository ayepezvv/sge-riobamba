import re

path = "src/app/(dashboard)/contratacion/pac/page.tsx"
with open(path, "r") as f:
    content = f.read()

# Add Imports
content = content.replace("import { IconTrash } from '@tabler/icons-react';", "import { IconTrash, IconUpload, IconExchange } from '@tabler/icons-react';")

# Add States for Reforma and CSV Modals
states = """
  const [openReforma, setOpenReforma] = useState(false);
  const [openCsv, setOpenCsv] = useState(false);
  const [selectedPacForReforma, setSelectedPacForReforma] = useState<number | null>(null);
"""
content = content.replace("const [selectedPacId, setSelectedPacId] = useState<number | null>(null);", "const [selectedPacId, setSelectedPacId] = useState<number | null>(null);" + states)

# Add Modals HTML
modals_html = """
      {/* Modal Importar CSV */}
      <Dialog open={openCsv} onClose={() => setOpenCsv(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Importar PAC (CSV / Excel)</DialogTitle>
        <DialogContent dividers>
          <Typography variant="body2" gutterBottom>
            Sube el archivo oficial del portal SERCOP o formato interno para cargar masivamente las líneas presupuestarias.
          </Typography>
          <Button variant="outlined" component="label" fullWidth startIcon={<IconUpload />} sx={{ mt: 2, height: 100, borderStyle: 'dashed' }}>
            Seleccionar archivo .csv / .xlsx
            <input hidden type="file" accept=".csv, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/vnd.ms-excel" />
          </Button>
        </DialogContent>
        <DialogActions sx={{ p: 2 }}>
          <Button onClick={() => setOpenCsv(false)}>Cancelar</Button>
          <Button variant="contained" color="success">Procesar Archivo</Button>
        </DialogActions>
      </Dialog>

      {/* Modal Reforma Complexa (N:M) */}
      <Dialog open={openReforma} onClose={() => setOpenReforma(false)} maxWidth="lg" fullWidth scroll="paper">
        <DialogTitle>Aplicar Reforma al PAC</DialogTitle>
        <DialogContent dividers>
            <Grid container spacing={2}>
                <Grid item xs={12}>
                    <TextField fullWidth label="Resolución / Justificación de la Reforma" multiline rows={2} />
                </Grid>
                <Grid item xs={12} sm={6}>
                    <Card variant="outlined" sx={{ bgcolor: 'error.light', opacity: 0.9 }}>
                        <CardHeader title="Ítems Origen (Ceden Fondos)" titleTypographyProps={{ variant: 'subtitle1', color: 'error.dark' }} />
                        <CardContent>
                            <Typography variant="body2" color="textSecondary" sx={{ mb: 2 }}>Selecciona los ítems que serán reducidos o eliminados.</Typography>
                            <Button fullWidth variant="outlined" color="error">+ Añadir Ítem a reducir</Button>
                        </CardContent>
                    </Card>
                </Grid>
                <Grid item xs={12} sm={6}>
                    <Card variant="outlined" sx={{ bgcolor: 'success.light', opacity: 0.9 }}>
                        <CardHeader title="Ítems Destino (Reciben Fondos)" titleTypographyProps={{ variant: 'subtitle1', color: 'success.dark' }} />
                        <CardContent>
                            <Typography variant="body2" color="textSecondary" sx={{ mb: 2 }}>Crea los nuevos ítems presupuestarios (o incrementa existentes).</Typography>
                            <Button fullWidth variant="outlined" color="success">+ Crear Nuevo Ítem (Destino)</Button>
                        </CardContent>
                    </Card>
                </Grid>
            </Grid>
        </DialogContent>
        <DialogActions sx={{ p: 2 }}>
          <Button onClick={() => setOpenReforma(false)}>Cancelar</Button>
          <Button variant="contained" startIcon={<IconExchange />}>Ejecutar Reforma Transaccional</Button>
        </DialogActions>
      </Dialog>
"""
content = content.replace("</Box>", modals_html + "\n    </Box>")

# Update Action Button in DataGrid
buttons_search = """<Button variant="contained" onClick={() => handleOpen()}>+ Crear PAC / Reforma</Button>"""
buttons_replace = """<Box display="flex" gap={1}>
          <Button variant="outlined" color="success" startIcon={<IconUpload />} onClick={() => setOpenCsv(true)}>Importar PAC</Button>
          <Button variant="contained" onClick={() => handleOpen()}>+ Crear PAC Anual</Button>
        </Box>"""
content = content.replace(buttons_search, buttons_replace)

# Detail panel actions
detail_search = """<Typography variant="subtitle2" gutterBottom>Líneas del PAC ({params.row.anio})</Typography>"""
detail_replace = """<Box display="flex" justifyContent="space-between" alignItems="center" mb={1}>
                        <Typography variant="subtitle2">Líneas del PAC ({params.row.anio})</Typography>
                        <Button size="small" color="secondary" variant="contained" startIcon={<IconExchange size={16}/>} onClick={() => { setSelectedPacForReforma(params.row.id); setOpenReforma(true); }}>Aplicar Reforma</Button>
                    </Box>"""
content = content.replace(detail_search, detail_replace)

# Status column for Items
item_columns_search = "columns={[\n                            { field: 'partida_presupuestaria'"
item_columns_replace = "columns={[\n                            { field: 'status', headerName: 'Estado', width: 110, renderCell: (p) => <Typography variant=\"caption\" sx={{ fontWeight: 'bold', color: p.value === 'ACTIVO' ? 'success.main' : 'error.main' }}>{p.value?.replace('_POR_REFORMA', '')}</Typography> },\n                            { field: 'partida_presupuestaria'"
content = content.replace(item_columns_search, item_columns_replace)

with open(path, "w") as f:
    f.write(content)
