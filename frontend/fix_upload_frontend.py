import re

path = "src/app/(dashboard)/contratacion/pac/page.tsx"
with open(path, "r") as f:
    content = f.read()

# Update handleCsvUpload state and logic
state_add = """  const [uploadFile, setUploadFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);"""
content = content.replace("const [selectedPacForReforma, setSelectedPacForReforma] = useState<number | null>(null);", "const [selectedPacForReforma, setSelectedPacForReforma] = useState<number | null>(null);\n" + state_add)

# Replace the modal opening logic so it knows WHICH pac we are importing to
button_csv_search = "onClick={() => setOpenCsv(true)}"
button_csv_replace = "onClick={() => { setSelectedPacId(params.row.id); setOpenCsv(true); }}"
content = content.replace(button_csv_search, button_csv_replace)

# Also there's a button Importar PAC that is at the top right, but it needs a pac ID to import to.
# Let's fix that. The generic import button should probably not be at the top right if we don't have a PAC selected.
# I'll remove the top-right import button and keep the one inside the actions per PAC row.
content = content.replace("""<Button variant="outlined" color="success" startIcon={<IconUpload />} onClick={() => setOpenCsv(true)}>Importar PAC</Button>""", "")

# But let's add an Import button inside the renderCell actions for the PAC
action_search = """<Button size="small" variant="contained" onClick={() => handleOpenItem(params.row.id)}>+ Ítem</Button>"""
action_replace = """<Button size="small" color="secondary" variant="contained" onClick={() => { setSelectedPacId(params.row.id); setOpenCsv(true); }}><IconUpload size={16}/></Button>
            <Button size="small" variant="contained" onClick={() => handleOpenItem(params.row.id)}>+ Ítem</Button>"""
content = content.replace(action_search, action_replace)

# Add logic for file selection and sending
upload_logic = """
  const handleFileChange = (e: any) => {
    if (e.target.files && e.target.files.length > 0) {
        setUploadFile(e.target.files[0]);
    }
  };

  const handleProcessCsv = async () => {
    if (!uploadFile || !selectedPacId) return;
    setUploading(true);
    const formData = new FormData();
    formData.append('file', uploadFile);

    try {
      const res = await fetch(`http://192.168.1.15:8000/api/contratacion/pac/${selectedPacId}/importar`, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${window.localStorage.getItem('serviceToken')}` },
        body: formData
      });
      
      if (res.ok) {
        const result = await res.json();
        setToast({ open: true, message: `Importación exitosa. Se procesaron ${result.filas_procesadas} líneas.`, severity: 'success' });
        setOpenCsv(false);
        setUploadFile(null);
        fetchPac();
      } else {
        const error = await res.json();
        setToast({ open: true, message: error.detail || 'Error al procesar el archivo', severity: 'error' });
      }
    } catch (e) {
      setToast({ open: true, message: 'Error de red al subir el archivo', severity: 'error' });
    } finally {
      setUploading(false);
    }
  };
"""
content = content.replace("const handleSaveItem = async () => {", upload_logic + "\n  const handleSaveItem = async () => {")

# Update CSV Modal JSX
csv_jsx_search = """<input hidden type="file" accept=".csv, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/vnd.ms-excel" />
          </Button>
        </DialogContent>
        <DialogActions sx={{ p: 2 }}>
          <Button onClick={() => setOpenCsv(false)}>Cancelar</Button>
          <Button variant="contained" color="success">Procesar Archivo</Button>"""

csv_jsx_replace = """<input hidden type="file" accept=".csv, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/vnd.ms-excel" onChange={handleFileChange} />
          </Button>
          {uploadFile && <Typography variant="caption" sx={{ mt: 1, color: 'success.main', display: 'block' }}>Archivo seleccionado: {uploadFile.name}</Typography>}
        </DialogContent>
        <DialogActions sx={{ p: 2 }}>
          <Button onClick={() => setOpenCsv(false)} disabled={uploading}>Cancelar</Button>
          <Button variant="contained" color="success" onClick={handleProcessCsv} disabled={!uploadFile || uploading}>
            {uploading ? 'Procesando...' : 'Procesar Archivo'}
          </Button>"""
content = content.replace(csv_jsx_search, csv_jsx_replace)

with open(path, "w") as f:
    f.write(content)
