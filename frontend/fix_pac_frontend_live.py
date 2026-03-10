import re

path = "src/app/(dashboard)/contratacion/pac/page.tsx"
with open(path, "r") as f:
    content = f.read()

# Add detailItems state to fetch dynamically
state_search = "const [selectedPacData, setSelectedPacData] = useState<any>(null);"
state_replace = "const [selectedPacData, setSelectedPacData] = useState<any>(null);\n  const [detailItems, setDetailItems] = useState<any[]>([]);"
content = content.replace(state_search, state_replace)

# Create fetch function for items
fetch_items_func = """
  const fetchPacItems = async (pacId: number) => {
    try {
      const res = await fetch(`http://192.168.1.15:8000/api/contratacion/pac/${pacId}/items`, { 
        headers: { 'Authorization': `Bearer ${window.localStorage.getItem('serviceToken')}` } 
      });
      if (res.ok) {
        setDetailItems(await res.json());
      }
    } catch (e) { console.error(e); }
  };
"""
content = content.replace("const handleOpen = (item = null) => {", fetch_items_func + "\n  const handleOpen = (item = null) => {")

# Call fetchItems when opening detail modal
open_detail_search = "onClick={() => { setSelectedPacId(params.row.id); setSelectedPacData(params.row); setOpenDetail(true); }}"
open_detail_replace = "onClick={() => { setSelectedPacId(params.row.id); setSelectedPacData(params.row); fetchPacItems(params.row.id); setOpenDetail(true); }}"
content = content.replace(open_detail_search, open_detail_replace)

# Call fetchItems after successful upload
upload_success_search = """setToast({ open: true, message: `Importación exitosa. Se procesaron ${result.filas_procesadas} líneas.`, severity: 'success' });
        setOpenCsv(false);
        setUploadFile(null);
        fetchPac();"""
upload_success_replace = """setToast({ open: true, message: `Importación: ${result.filas_procesadas} filas nuevas. Ignoradas por duplicado: ${result.ignoradas_por_duplicado}`, severity: 'success' });
        setOpenCsv(false);
        setUploadFile(null);
        fetchPac();
        if (selectedPacId) fetchPacItems(selectedPacId);"""
content = content.replace(upload_success_search, upload_success_replace)

# Call fetchItems after manual item added
manual_item_search = """// Optimistic update for detail modal
        const newItem = await res.json();
        if (selectedPacData) {
            setSelectedPacData({...selectedPacData, items: [...(selectedPacData.items || []), newItem]});
        }"""
manual_item_replace = """if (selectedPacId) fetchPacItems(selectedPacId);"""
content = content.replace(manual_item_search, manual_item_replace)

# Update Modal JSX to use detailItems and show Total
modal_jsx_search = """<Box display="flex" gap={1}>
                <Button size="small" variant="outlined" color="success" startIcon={<IconUpload size={18}/>} onClick={() => setOpenCsv(true)}>Importar CSV/Excel</Button>
                <Button size="small" variant="contained" color="primary" onClick={() => handleOpenItem(selectedPacData?.id)}>+ Ítem Manual</Button>
                <Button size="small" variant="contained" color="error" startIcon={<IconExchange size={18}/>} onClick={() => { setSelectedPacForReforma(selectedPacData?.id); setOpenReforma(true); }}>Reforma (Traspaso)</Button>
            </Box>
        </DialogTitle>
        <DialogContent dividers sx={{ p: 0, height: 500 }}>
            <DataGrid 
                rows={selectedPacData?.items || []} """

total_logic = """
            <Box display="flex" flexDirection="column" alignItems="flex-end">
                <Box display="flex" gap={1} mb={1}>
                    <Button size="small" variant="outlined" color="success" startIcon={<IconUpload size={18}/>} onClick={() => setOpenCsv(true)}>Importar</Button>
                    <Button size="small" variant="contained" color="primary" onClick={() => handleOpenItem(selectedPacData?.id)}>+ Ítem Manual</Button>
                    <Button size="small" variant="contained" color="error" startIcon={<IconExchange size={18}/>} onClick={() => { setSelectedPacForReforma(selectedPacData?.id); setOpenReforma(true); }}>Reforma M:M</Button>
                </Box>
                <Alert severity="info" sx={{ py: 0, px: 2, fontWeight: 'bold' }}>
                  Total Presupuesto: ${detailItems.reduce((acc, row) => acc + Number(row.valor_total || 0), 0).toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2})}
                </Alert>
            </Box>
        </DialogTitle>
        <DialogContent dividers sx={{ p: 0, height: 500 }}>
            <DataGrid 
                rows={detailItems} """

content = content.replace(modal_jsx_search, total_logic)

with open(path, "w") as f:
    f.write(content)

