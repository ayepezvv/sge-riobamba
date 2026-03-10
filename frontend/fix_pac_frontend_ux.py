import re

path = "src/app/(dashboard)/contratacion/pac/page.tsx"
with open(path, "r") as f:
    content = f.read()

# 1. Add "Ver Detalles" icon and refactor actions
# Also let's manage the modal states better
content = content.replace("import { IconTrash, IconUpload, IconExchange } from '@tabler/icons-react';", "import { IconTrash, IconUpload, IconExchange, IconEye, IconEdit } from '@tabler/icons-react';")

# Add state for Detail Modal
content = content.replace("const [openItem, setOpenItem] = useState(false);", "const [openItem, setOpenItem] = useState(false);\n  const [openDetail, setOpenDetail] = useState(false);\n  const [selectedPacData, setSelectedPacData] = useState<any>(null);")

# Refactor columns to have View Details instead of all actions inline
action_search = """<Button size="small" color="secondary" variant="contained" onClick={() => { setSelectedPacId(params.row.id); setOpenCsv(true); }}><IconUpload size={16}/></Button>
            <Button size="small" variant="contained" onClick={() => handleOpenItem(params.row.id)}>+ Ítem</Button>"""

action_replace = """<Button size="small" variant="outlined" onClick={() => handleOpen(params.row)}><IconEdit size={16}/></Button>
            <Button size="small" variant="contained" color="secondary" onClick={() => { setSelectedPacId(params.row.id); setSelectedPacData(params.row); setOpenDetail(true); }}>Ver / Gestionar Ítems</Button>"""

content = content.replace(action_search, action_replace)

# Modify handleSaveItem to refresh selected data
save_item_replace = """      if (res.ok) {
        setToast({ open: true, message: 'Ítem agregado al PAC', severity: 'success' });
        setOpenItem(false);
        fetchPac();
        // Optimistic update for detail modal
        const newItem = await res.json();
        if (selectedPacData) {
            setSelectedPacData({...selectedPacData, items: [...(selectedPacData.items || []), newItem]});
        }
      } else {"""
content = re.sub(r'      if \(res.ok\) \{\n        setToast\(\{ open: true, message: \'Ítem agregado al PAC\', severity: \'success\' \}\);\n        setOpenItem\(false\);\n        fetchPac\(\);\n      \} else \{', save_item_replace, content)

# Remove the detail panel from master grid to use a clean Modal
# getDetailPanelContent={(params) => (...)} getDetailPanelHeight={() => 'auto'}
content = re.sub(r'getDetailPanelContent=\{.*?getDetailPanelHeight=\{\(\) => \'auto\'\}', '', content, flags=re.DOTALL)

# Add the robust Detail Modal JSX
detail_modal = """
      {/* Modal Detalles del PAC (Gestión de Ítems) */}
      <Dialog open={openDetail} onClose={() => setOpenDetail(false)} maxWidth="xl" fullWidth scroll="paper">
        <DialogTitle sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <Typography variant="h5">PAC {selectedPacData?.anio} {selectedPacData?.version_reforma === 0 ? '(Inicial)' : `(Reforma ${selectedPacData?.version_reforma})`}</Typography>
            <Box display="flex" gap={1}>
                <Button size="small" variant="outlined" color="success" startIcon={<IconUpload size={18}/>} onClick={() => setOpenCsv(true)}>Importar CSV/Excel</Button>
                <Button size="small" variant="contained" color="primary" onClick={() => handleOpenItem(selectedPacData?.id)}>+ Ítem Manual</Button>
                <Button size="small" variant="contained" color="error" startIcon={<IconExchange size={18}/>} onClick={() => { setSelectedPacForReforma(selectedPacData?.id); setOpenReforma(true); }}>Reforma (Traspaso)</Button>
            </Box>
        </DialogTitle>
        <DialogContent dividers sx={{ p: 0, height: 500 }}>
            <DataGrid 
                rows={selectedPacData?.items || []} 
                columns={[
                    { field: 'status', headerName: 'Estado', width: 110, renderCell: (p) => <Typography variant="caption" sx={{ fontWeight: 'bold', color: p.value === 'ACTIVO' ? 'success.main' : 'error.main' }}>{p.value?.replace('_POR_REFORMA', '')}</Typography> },
                    { field: 'partida_presupuestaria', headerName: 'Partida', width: 130 },
                    { field: 'cpc', headerName: 'CPC', width: 100 },
                    { field: 'descripcion', headerName: 'Descripción', flex: 1 },
                    { field: 'cantidad', headerName: 'Cant.', width: 80 },
                    { field: 'costo_unitario', headerName: 'V. Unit.', width: 100, renderCell: (p) => `$${p.value?.toFixed(2)}` },
                    { field: 'valor_total', headerName: 'V. Total', width: 110, renderCell: (p) => `$${p.value?.toFixed(2)}` }
                ]}
                rowHeight={40}
                disableRowSelectionOnClick
            />
        </DialogContent>
        <DialogActions>
            <Button onClick={() => setOpenDetail(false)}>Cerrar</Button>
        </DialogActions>
      </Dialog>
"""

content = content.replace("{/* Modal PAC */}", detail_modal + "\n      {/* Modal PAC */}")

with open(path, "w") as f:
    f.write(content)

