'use client';
import { useEffect, useState } from 'react';
import { API_BASE_URL } from 'config/api';
import {
  Box,
  Button,
  Card,
  CardContent,
  CardHeader,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  Grid,
  TextField,
  MenuItem,
  Select,
  FormControl,
  InputLabel,
  Snackbar,
  Alert,
  Typography,
  Divider,
  IconButton
} from '@mui/material';
import { DataGrid, GridColDef, GridToolbar } from '@mui/x-data-grid';
import { IconTrash, IconUpload, IconExchange, IconEye, IconEdit } from '@tabler/icons-react';

export default function PacPage() {
  const [data, setData] = useState([]);
  const [open, setOpen] = useState(false);
  const [openItem, setOpenItem] = useState(false);
  const [openDetail, setOpenDetail] = useState(false);
  const [selectedPacData, setSelectedPacData] = useState<any>(null);
  const [detailItems, setDetailItems] = useState<any[]>([]);
  const [toast, setToast] = useState({ open: false, message: '', severity: 'success' });
  const [formData, setFormData] = useState<any>({
    anio: new Date().getFullYear(), version_reforma: 0, descripcion: '', es_activo: true
  });
  const [itemForm, setItemForm] = useState<any>({
    partida_presupuestaria: '', cpc: '', tipo_compra: '', procedimiento: '', descripcion: '', cantidad: 1, costo_unitario: 0, valor_total: 0
  });
  const [editingId, setEditingId] = useState<number | null>(null);
  const [selectedPacId, setSelectedPacId] = useState<number | null>(null);
  const [openReforma, setOpenReforma] = useState(false);
  const [openCsv, setOpenCsv] = useState(false);
  const [selectedPacForReforma, setSelectedPacForReforma] = useState<number | null>(null);
  const [uploadFile, setUploadFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);


  const fetchPac = async () => {
    try {
      const res = await fetch(`${API_BASE_URL}/api/contratacion/pac`, { headers: { 'Authorization': `Bearer ${window.localStorage.getItem('serviceToken')}` } });
      if (res.ok) setData(await res.json());
    } catch (e) { console.error(e); }
  };

  useEffect(() => { fetchPac(); }, []);

  
  const fetchPacItems = async (pacId: number) => {
    try {
      const res = await fetch(`${API_BASE_URL}/api/contratacion/pac/${pacId}/items`, {
        headers: { 'Authorization': `Bearer ${window.localStorage.getItem('serviceToken')}` }
      });
      if (res.ok) {
        setDetailItems(await res.json());
      }
    } catch (e) { console.error(e); }
  };

  const handleOpen = (item = null) => {
    if (item) {
      setEditingId(item.id);
      setFormData(item);
    } else {
      setEditingId(null);
      setFormData({ anio: new Date().getFullYear(), version_reforma: 0, descripcion: '', es_activo: true });
    }
    setOpen(true);
  };

  const handleSavePac = async () => {
    const url = editingId ? `${API_BASE_URL}/api/contratacion/pac/${editingId}` : `${API_BASE_URL}/api/contratacion/pac`;
    const method = editingId ? 'PUT' : 'POST';
    try {
      const res = await fetch(url, {
        method,
        headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${window.localStorage.getItem('serviceToken')}` },
        body: JSON.stringify(formData)
      });
      if (res.ok) {
        setToast({ open: true, message: 'PAC guardado exitosamente', severity: 'success' });
        setOpen(false);
        fetchPac();
      } else {
        setToast({ open: true, message: 'Error al guardar el PAC', severity: 'error' });
      }
    } catch (e) {
      setToast({ open: true, message: 'Error de red', severity: 'error' });
    }
  };

  const handleOpenItem = (pacId: number) => {
    setSelectedPacId(pacId);
    setItemForm({ partida_presupuestaria: '', cpc: '', tipo_compra: '', procedimiento: '', descripcion: '', cantidad: 1, costo_unitario: 0, valor_total: 0 });
    setOpenItem(true);
  };

  
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
      const res = await fetch(`${API_BASE_URL}/api/contratacion/pac/${selectedPacId}/importar`, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${window.localStorage.getItem('serviceToken')}` },
        body: formData
      });
      
      if (res.ok) {
        const result = await res.json();
        setToast({ open: true, message: `Importación: ${result.filas_procesadas} filas nuevas. Ignoradas por duplicado: ${result.ignoradas_por_duplicado}`, severity: 'success' });
        setOpenCsv(false);
        setUploadFile(null);
        fetchPac();
        if (selectedPacId) fetchPacItems(selectedPacId);
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

  const handleSaveItem = async () => {
    if (!selectedPacId) return;
    // Calculate total
    const itemData = { ...itemForm, valor_total: itemForm.cantidad * itemForm.costo_unitario };
    try {
      const res = await fetch(`${API_BASE_URL}/api/contratacion/pac/${selectedPacId}/items`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${window.localStorage.getItem('serviceToken')}` },
        body: JSON.stringify(itemData)
      });
      if (res.ok) {
        setToast({ open: true, message: 'Ítem agregado al PAC', severity: 'success' });
        setOpenItem(false);
        fetchPac();
        if (selectedPacId) fetchPacItems(selectedPacId);
      } else {
        setToast({ open: true, message: 'Error al agregar ítem', severity: 'error' });
      }
    } catch (e) {
      setToast({ open: true, message: 'Error de red', severity: 'error' });
    }
  };

  const pacColumns: GridColDef[] = [
    { field: 'anio', headerName: 'Año', width: 90 },
    { field: 'version_reforma', headerName: 'Reforma', width: 100, renderCell: (p) => p.value === 0 ? 'Inicial' : `Reforma ${p.value}` },
    { field: 'descripcion', headerName: 'Descripción', flex: 1 },
    { field: 'es_activo', headerName: 'Estado', width: 100, renderCell: (p) => p.value ? 'Activo' : 'Inactivo' },
    { field: 'items', headerName: 'Líneas', width: 90, renderCell: (p) => p.value?.length || 0 },
    {
      field: 'acciones', headerName: 'Acciones', width: 250,
      renderCell: (params) => (
        <Box display="flex" gap={1}>
            <Button size="small" variant="outlined" onClick={() => handleOpen(params.row)}><IconEdit size={16}/></Button>
            <Button size="small" variant="contained" color="secondary" onClick={() => { setSelectedPacId(params.row.id); setSelectedPacData(params.row); fetchPacItems(params.row.id); setOpenDetail(true); }}>Ver / Gestionar Ítems</Button>
        
      {/* Modal Importar CSV */}
      <Dialog open={openCsv} onClose={() => setOpenCsv(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Importar PAC (CSV / Excel)</DialogTitle>
        <DialogContent dividers>
          <Typography variant="body2" gutterBottom>
            Sube el archivo oficial del portal SERCOP o formato interno para cargar masivamente las líneas presupuestarias.
          </Typography>
          <Button variant="outlined" component="label" fullWidth startIcon={<IconUpload />} sx={{ mt: 2, height: 100, borderStyle: 'dashed' }}>
            Seleccionar archivo .csv / .xlsx
            <input hidden type="file" accept=".csv, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/vnd.ms-excel" onChange={handleFileChange} />
          </Button>
          {uploadFile && <Typography variant="caption" sx={{ mt: 1, color: 'success.main', display: 'block' }}>Archivo seleccionado: {uploadFile.name}</Typography>}
        </DialogContent>
        <DialogActions sx={{ p: 2 }}>
          <Button onClick={() => setOpenCsv(false)} disabled={uploading}>Cancelar</Button>
          <Button variant="contained" color="success" onClick={handleProcessCsv} disabled={!uploadFile || uploading}>
            {uploading ? 'Procesando...' : 'Procesar Archivo'}
          </Button>
        </DialogActions>
      </Dialog>

      {/* Modal Reforma Complexa (N:M) */}
      <Dialog open={openReforma} onClose={() => setOpenReforma(false)} maxWidth="lg" fullWidth scroll="paper">
        <DialogTitle>Aplicar Reforma al PAC</DialogTitle>
        <DialogContent dividers>
            <Grid container spacing={2}>
                <Grid size={12}>
                    <TextField fullWidth label="Resolución / Justificación de la Reforma" multiline rows={2} />
                </Grid>
                <Grid size={{ xs: 12, sm: 6 }}>
                    <Card variant="outlined" sx={{ bgcolor: 'error.light', opacity: 0.9 }}>
                        <CardHeader title="Ítems Origen (Ceden Fondos)" titleTypographyProps={{ variant: 'subtitle1', color: 'error.dark' }} />
                        <CardContent>
                            <Typography variant="body2" color="textSecondary" sx={{ mb: 2 }}>Selecciona los ítems que serán reducidos o eliminados.</Typography>
                            <Button fullWidth variant="outlined" color="error">+ Añadir Ítem a reducir</Button>
                        </CardContent>
                    </Card>
                </Grid>
                <Grid size={{ xs: 12, sm: 6 }}>
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

    </Box>
      )
    }
  ];

  return (
    <Box>
      <Card>
        <CardHeader title="Plan Anual de Contratación (PAC)" action={<Box display="flex" gap={1}>
          <Button variant="outlined" color="success" startIcon={<IconUpload />} onClick={() => { setSelectedPacId(params.row.id); setOpenCsv(true); }}>Importar PAC</Button>
          <Button variant="contained" onClick={() => handleOpen()}>+ Crear PAC Anual</Button>
        </Box>} />
        <CardContent>
          <DataGrid rows={data} columns={pacColumns} autoHeight 
            
          />
        </CardContent>
      </Card>

      
      {/* Modal Detalles del PAC (Gestión de Ítems) */}
      <Dialog open={openDetail} onClose={() => setOpenDetail(false)} maxWidth="xl" fullWidth scroll="paper">
        <DialogTitle sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <Typography variant="h5">PAC {selectedPacData?.anio} {selectedPacData?.version_reforma === 0 ? '(Inicial)' : `(Reforma ${selectedPacData?.version_reforma})`}</Typography>
            
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
                rows={detailItems} 
                slots={{ toolbar: GridToolbar }}
                slotProps={{ toolbar: { showQuickFilter: true } }}
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

      {/* Modal PAC */}
      <Dialog open={open} onClose={() => setOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>{editingId ? 'Editar' : 'Nuevo'} PAC / Reforma</DialogTitle>
        <DialogContent dividers>
          <Grid container spacing={2}>
            <Grid size={{ xs: 12, sm: 6 }}>
              <TextField fullWidth type="number" label="Año Fiscal" value={formData.anio} onChange={(e) => setFormData({ ...formData, anio: parseInt(e.target.value) })} />
            </Grid>
            <Grid size={{ xs: 12, sm: 6 }}>
              <TextField fullWidth type="number" label="Versión Reforma (0 = Inicial)" value={formData.version_reforma} onChange={(e) => setFormData({ ...formData, version_reforma: parseInt(e.target.value) })} />
            </Grid>
            <Grid size={12}>
              <TextField fullWidth label="Descripción de la Resolución / PAC" value={formData.descripcion} onChange={(e) => setFormData({ ...formData, descripcion: e.target.value })} />
            </Grid>
            <Grid size={12}>
              <FormControl fullWidth>
                <InputLabel>Estado</InputLabel>
                <Select value={formData.es_activo} label="Estado" onChange={(e) => setFormData({ ...formData, es_activo: e.target.value })}>
                  <MenuItem value={true}>Activo</MenuItem>
                  <MenuItem value={false}>Inactivo (Histórico)</MenuItem>
                </Select>
              </FormControl>
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions sx={{ p: 2 }}>
          <Button onClick={() => setOpen(false)}>Cancelar</Button>
          <Button variant="contained" onClick={handleSavePac}>Guardar</Button>
        </DialogActions>
      </Dialog>

      {/* Modal Item PAC */}
      <Dialog open={openItem} onClose={() => setOpenItem(false)} maxWidth="md" fullWidth>
        <DialogTitle>Agregar Línea al PAC</DialogTitle>
        <DialogContent dividers>
          <Grid container spacing={2}>
            <Grid size={{ xs: 12, sm: 6 }}>
              <TextField fullWidth label="Partida Presupuestaria" value={itemForm.partida_presupuestaria} onChange={(e) => setItemForm({ ...itemForm, partida_presupuestaria: e.target.value })} />
            </Grid>
            <Grid size={{ xs: 12, sm: 6 }}>
              <TextField fullWidth label="Código CPC" value={itemForm.cpc} onChange={(e) => setItemForm({ ...itemForm, cpc: e.target.value })} />
            </Grid>
            <Grid size={{ xs: 12, sm: 6 }}>
              <FormControl fullWidth>
                <InputLabel>Tipo de Compra</InputLabel>
                <Select value={itemForm.tipo_compra} label="Tipo de Compra" onChange={(e) => setItemForm({ ...itemForm, tipo_compra: e.target.value })}>
                  <MenuItem value="Bien">Bien</MenuItem>
                  <MenuItem value="Servicio">Servicio</MenuItem>
                  <MenuItem value="Obra">Obra</MenuItem>
                  <MenuItem value="Consultoría">Consultoría</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid size={{ xs: 12, sm: 6 }}>
              <TextField fullWidth label="Procedimiento Sugerido" value={itemForm.procedimiento} onChange={(e) => setItemForm({ ...itemForm, procedimiento: e.target.value })} />
            </Grid>
            <Grid size={12}>
              <TextField fullWidth multiline rows={2} label="Descripción de la Contratación" value={itemForm.descripcion} onChange={(e) => setItemForm({ ...itemForm, descripcion: e.target.value })} />
            </Grid>
            <Grid size={{ xs: 12, sm: 4 }}>
              <TextField fullWidth type="number" label="Cantidad" value={itemForm.cantidad} onChange={(e) => setItemForm({ ...itemForm, cantidad: parseFloat(e.target.value) })} />
            </Grid>
            <Grid size={{ xs: 12, sm: 4 }}>
              <TextField fullWidth type="number" label="Costo Unitario ($)" value={itemForm.costo_unitario} onChange={(e) => setItemForm({ ...itemForm, costo_unitario: parseFloat(e.target.value) })} />
            </Grid>
            <Grid size={{ xs: 12, sm: 4 }}>
              <TextField fullWidth disabled label="Valor Total Estimado ($)" value={`$${(itemForm.cantidad * itemForm.costo_unitario).toFixed(2)}`} />
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions sx={{ p: 2 }}>
          <Button onClick={() => setOpenItem(false)}>Cancelar</Button>
          <Button variant="contained" onClick={handleSaveItem}>Agregar Línea</Button>
        </DialogActions>
      </Dialog>

      <Snackbar open={toast.open} autoHideDuration={4000} onClose={() => setToast({...toast, open: false})}>
        <Alert severity={toast.severity as any}>{toast.message}</Alert>
      </Snackbar>
    
      {/* Modal Importar CSV */}
      <Dialog open={openCsv} onClose={() => setOpenCsv(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Importar PAC (CSV / Excel)</DialogTitle>
        <DialogContent dividers>
          <Typography variant="body2" gutterBottom>
            Sube el archivo oficial del portal SERCOP o formato interno para cargar masivamente las líneas presupuestarias.
          </Typography>
          <Button variant="outlined" component="label" fullWidth startIcon={<IconUpload />} sx={{ mt: 2, height: 100, borderStyle: 'dashed' }}>
            Seleccionar archivo .csv / .xlsx
            <input hidden type="file" accept=".csv, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/vnd.ms-excel" onChange={handleFileChange} />
          </Button>
          {uploadFile && <Typography variant="caption" sx={{ mt: 1, color: 'success.main', display: 'block' }}>Archivo seleccionado: {uploadFile.name}</Typography>}
        </DialogContent>
        <DialogActions sx={{ p: 2 }}>
          <Button onClick={() => setOpenCsv(false)} disabled={uploading}>Cancelar</Button>
          <Button variant="contained" color="success" onClick={handleProcessCsv} disabled={!uploadFile || uploading}>
            {uploading ? 'Procesando...' : 'Procesar Archivo'}
          </Button>
        </DialogActions>
      </Dialog>

      {/* Modal Reforma Complexa (N:M) */}
      <Dialog open={openReforma} onClose={() => setOpenReforma(false)} maxWidth="lg" fullWidth scroll="paper">
        <DialogTitle>Aplicar Reforma al PAC</DialogTitle>
        <DialogContent dividers>
            <Grid container spacing={2}>
                <Grid size={12}>
                    <TextField fullWidth label="Resolución / Justificación de la Reforma" multiline rows={2} />
                </Grid>
                <Grid size={{ xs: 12, sm: 6 }}>
                    <Card variant="outlined" sx={{ bgcolor: 'error.light', opacity: 0.9 }}>
                        <CardHeader title="Ítems Origen (Ceden Fondos)" titleTypographyProps={{ variant: 'subtitle1', color: 'error.dark' }} />
                        <CardContent>
                            <Typography variant="body2" color="textSecondary" sx={{ mb: 2 }}>Selecciona los ítems que serán reducidos o eliminados.</Typography>
                            <Button fullWidth variant="outlined" color="error">+ Añadir Ítem a reducir</Button>
                        </CardContent>
                    </Card>
                </Grid>
                <Grid size={{ xs: 12, sm: 6 }}>
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

    </Box>
  );
}
