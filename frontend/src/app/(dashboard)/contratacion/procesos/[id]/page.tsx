'use client';

import { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { DataGrid, GridColDef } from '@mui/x-data-grid';
import { Box, Button, Dialog, DialogTitle, DialogContent, DialogActions, TextField, Snackbar, Alert, Typography, Grid, IconButton, Tooltip, FormControl, InputLabel, Select, MenuItem, Chip, CircularProgress, Card, CardContent } from '@mui/material';
import EditIcon from '@mui/icons-material/Edit';
import DownloadIcon from '@mui/icons-material/Download';
import CloseIcon from '@mui/icons-material/Close';
import AddIcon from '@mui/icons-material/Add';
import MainCard from 'ui-component/cards/MainCard';
import { obtenerProceso, listarPlantillas, obtenerEsquemaPlantilla, obtenerDatosDocumento, crearDocumento, regenerarDocumento, descargarDocumento } from 'api/contratacion';

export default function ProcesoDetailPage() {
  const params = useParams();
  const router = useRouter();
  const procesoId = params.id;
  
  const [proceso, setProceso] = useState<any>(null);
  const [plantillas, setPlantillas] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  
  // Dialog Generate / Regenerate
  const [openDoc, setOpenDoc] = useState(false);
  const [editingDocId, setEditingDocId] = useState<number | null>(null);
  
  // Dynamic Form State based on backend Schema
  const [selectedPlantillaId, setSelectedPlantillaId] = useState<string>('');
  const [esquemaVariables, setEsquemaVariables] = useState<any[]>([]);
  const [loadingEsquema, setLoadingEsquema] = useState(false);
  const [dinamicData, setDinamicData] = useState<any>({});
  const [miPerfil, setMiPerfil] = useState<any>(null);

  const renderContexto = (contextoStr: string, variableNombre: string) => {
    if (!contextoStr) return null;
    const parts = contextoStr.split(`[ ${variableNombre} ]`);
    if (parts.length === 1) return <Typography variant="caption" color="textSecondary">{contextoStr}</Typography>;
    return (
      <Typography variant="caption" color="textSecondary" component="span" sx={{ display: 'block', mt: 0.5, lineHeight: 1.2 }}>
        {parts[0]}
        <Typography component="span" fontWeight="bold" color="primary.main" sx={{ bgcolor: 'primary.light', px: 0.5, borderRadius: 1 }}>
          {variableNombre}
        </Typography>
        {parts[1]}
      </Typography>
    );
  };

  const [toast, setToast] = useState({ open: false, message: '', severity: 'success' });

  // UX Modal Table State
  const [openRowModal, setOpenRowModal] = useState(false);
  const [activeTableVar, setActiveTableVar] = useState<string>('');
  const [tempRowItem, setTempRowItem] = useState<any>({});

  const fetchData = async () => {
    setLoading(true);
    try {
      const proc = await obtenerProceso(Number(procesoId));
      setProceso(proc);

      const rawPlantillas = await listarPlantillas({ tipo_proceso_id: proc.tipo_proceso_id, is_activa: true });
      setPlantillas(rawPlantillas);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { if (procesoId) fetchData(); }, [procesoId]);

  // Cuando el usuario elige una plantilla, pedimos al backend que la abra y lea sus variables
  useEffect(() => {
    if (selectedPlantillaId && !editingDocId) {
      const fetchEsquema = async () => {
        setLoadingEsquema(true);
        try {
          const res = await obtenerEsquemaPlantilla(Number(selectedPlantillaId));
          setEsquemaVariables(res.variables || []);
          
          // Persistencia de memoria: Si el expediente ya tiene datos guardados, usarlos. Si no, pre-poblar.
          if (proceso?.datos_formulario && Object.keys(proceso.datos_formulario).length > 0) {
            setDinamicData(proceso.datos_formulario);
          } else {
            const initialData: any = {};
            res.variables.forEach((v: any) => {
              const k = v.nombre.toLowerCase();
              if (v.nombre === 'nombre_proyecto' || v.nombre === 'objeto_contratacion') {
                initialData[v.nombre] = proceso?.nombre_proyecto || '';
              } else if (v.nombre === 'codigo_proceso') {
                initialData[v.nombre] = proceso?.codigo_proceso || '';
              } else if (k.includes('fecha')) {
                initialData[v.nombre] = new Date().toLocaleDateString('es-EC');
              } else if (miPerfil) {
                // Diccionario de Mapeo Inteligente (Autocompletado)
                if (k.includes('persona_elabora')) initialData[v.nombre] = `${miPerfil.nombres} ${miPerfil.apellidos}`;
                else if (k.includes('cargo_elabora')) initialData[v.nombre] = miPerfil.cargo || '';
                else if (k.includes('unidad_requirente')) initialData[v.nombre] = miPerfil.unidad?.nombre || '';
                else if (k.includes('cedula_elabora')) initialData[v.nombre] = miPerfil.cedula || '';
                else if (k.includes('certificacion_elabora') || k.includes('codigo_sercop')) initialData[v.nombre] = miPerfil.codigo_certificacion_sercop || '';
                else initialData[v.nombre] = '';
              } else {
                initialData[v.nombre] = '';
              }
            });
            setDinamicData(initialData);
          }

        } catch (e) {
          setToast({ open: true, message: 'Error extrayendo variables del .docx', severity: 'error' });
          setEsquemaVariables([]);
        } finally {
          setLoadingEsquema(false);
        }
      };
      fetchEsquema();
    }
  }, [selectedPlantillaId, editingDocId, proceso, miPerfil]);

  const handleOpenNewDoc = () => {
    setEditingDocId(null);
    setSelectedPlantillaId('');
    setEsquemaVariables([]);
    setDinamicData({});
    setOpenDoc(true);
  };

  const handleOpenEditDoc = async (doc: any) => {
    try {
      setEditingDocId(doc.id);
      setSelectedPlantillaId(doc.plantilla_id);
      
      // 1. Pedir el esquema de la plantilla (aunque sea historica)
      const resEsquema = await obtenerEsquemaPlantilla(doc.plantilla_id);
      setEsquemaVariables(resEsquema.variables || []);

      const datos = await obtenerDatosDocumento(doc.id);
      setDinamicData(datos);
      
      setOpenDoc(true);
    } catch (error) {
      setToast({ open: true, message: 'Error al recuperar datos del documento o su esquema', severity: 'error' });
    }
  };

  const handleDynamicChange = (nombreVar: string, valor: any) => {
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
    
    const tableSchema = esquemaVariables.find((e: any) => e.nombre === varName);
    const currentList = Array.isArray(dinamicData[varName]) ? dinamicData[varName] : [];
    
    let template: any = {};
    const cols = tableSchema?.columnas || tableSchema?.sub_atributos;
    if (cols && cols.length > 0) {
      cols.forEach((attr: string) => { 
        const lower = attr.toLowerCase();
        if (lower.includes('disponibilidad') || lower.includes('aplica') || lower.includes('estado')) {
            template[attr] = 'SÍ'; // Default state to prevent nulls
        } else {
            template[attr] = ''; 
        }
      });
    } else if (currentList.length > 0) {
      template = { ...currentList[0] };
      for (let k in template) {
        const lower = k.toLowerCase();
        template[k] = (lower.includes('disponibilidad') || lower.includes('aplica') || lower.includes('estado')) ? 'SÍ' : '';
      }
    } else {
      template = { nombre_atributo: "" };
    }
    
    setTempRowItem(template);
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
    setDinamicData((prev: any) => ({
      ...prev,
      [activeTableVar]: [...(prev[activeTableVar] || []), tempRowItem]
    }));
    setTempRowItem({});
    setOpenRowModal(false);
  };

  const handleRemoveRow = (varName: string, rowIndex: number) => {
    const currentList = [...(dinamicData[varName] || [])];
    currentList.splice(rowIndex, 1);
    handleDynamicChange(varName, currentList);
  };

  const handleDocSubmit = async () => {
    try {
      if (editingDocId) {
        const response = await regenerarDocumento(editingDocId, dinamicData);
        
        if (response.data instanceof Blob || response.headers['content-type']?.includes('wordprocessingml') || response.headers['content-type']?.includes('octet-stream')) {
          const url = window.URL.createObjectURL(new Blob([response.data]));
          const link = document.createElement('a');
          link.href = url;
          // El backend envia el filename en Content-Disposition si esta disponible
                    let fileName = `Proceso_${procesoId}_Generado.docx`;
          const disposition = response.headers['content-disposition'];
          if (disposition && disposition.includes('filename=')) {
              fileName = disposition.split('filename=')[1].replace(/['"]/g, '').split(';')[0];
          }
          link.setAttribute('download', fileName);
          document.body.appendChild(link);
          link.click();
          link.parentNode?.removeChild(link);
          window.URL.revokeObjectURL(url);
          setToast({ open: true, message: 'Documento procesado exitosamente', severity: 'success' });
        } else {
          setToast({ open: true, message: 'El servidor no devolvió un archivo válido.', severity: 'error' });
        }
      } else {
        const response = await crearDocumento({
          proceso_contratacion_id: parseInt(procesoId as string),
          plantilla_id: parseInt(selectedPlantillaId),
          datos: dinamicData
        });
        
        if (response.data instanceof Blob || response.headers['content-type']?.includes('wordprocessingml') || response.headers['content-type']?.includes('octet-stream')) {
          const url = window.URL.createObjectURL(new Blob([response.data]));
          const link = document.createElement('a');
          link.href = url;
          // El backend envia el filename en Content-Disposition si esta disponible
                    let fileName = `Proceso_${procesoId}_Generado.docx`;
          const disposition = response.headers['content-disposition'];
          if (disposition && disposition.includes('filename=')) {
              fileName = disposition.split('filename=')[1].replace(/['"]/g, '').split(';')[0];
          }
          link.setAttribute('download', fileName);
          document.body.appendChild(link);
          link.click();
          link.parentNode?.removeChild(link);
          window.URL.revokeObjectURL(url);
          setToast({ open: true, message: 'Documento procesado exitosamente', severity: 'success' });
        } else {
          setToast({ open: true, message: 'El servidor no devolvió un archivo válido.', severity: 'error' });
        }
      }
      setOpenDoc(false);
      fetchData(); // Refresh list
    } catch (error: any) {
      // Axios con blob devuelve el error como FileReader
      if (error.response && error.response.data instanceof Blob) {
          const reader = new FileReader();
          reader.onload = () => {
              try {
                  const errorData = JSON.parse(reader.result as string);
                  setToast({ open: true, message: errorData.detail || 'Error al generar', severity: 'error' });
              } catch (e) {
                  setToast({ open: true, message: 'Error de validación en la generación', severity: 'error' });
              }
          };
          reader.readAsText(error.response.data);
      } else {
          setToast({ open: true, message: error.response?.data?.detail || 'Error al generar', severity: 'error' });
      }
    }
  };

  const handleDownload = async (docId: number, version: number) => {
    try {
      const response = await descargarDocumento(docId);
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `Documento_v${version}.docx`);
      document.body.appendChild(link);
      link.click();
      link.parentNode?.removeChild(link);
      window.URL.revokeObjectURL(url);
    } catch (error) {
      setToast({ open: true, message: 'Error al descargar el archivo', severity: 'error' });
    }
  };

  const columns: GridColDef[] = [
    { field: 'id', headerName: 'ID', width: 70 },
    { 
      field: 'plantilla_id', 
      headerName: 'Plantilla', 
      flex: 1,
      renderCell: (params) => {
        // Here we might need a general catalog of all templates (even inactive) to map names, but for now we fallback to ID
        const p = plantillas.find((pl: any) => pl.id === params.value);
        return p ? p.nombre : `Plantilla Historica #${params.value}`;
      }
    },
    { 
      field: 'version', 
      headerName: 'Versión', 
      width: 100,
      renderCell: (params) => <Chip label={`v${params.value}`} color="primary" size="small" />
    },
    { field: 'fecha_generacion', headerName: 'Última Generación', width: 200, valueGetter: (params) => params.value ? new Date(params.value).toLocaleString('es-EC') : 'Sin fecha' },
    {
      field: 'acciones', headerName: 'Acciones', width: 150, sortable: false,
      renderCell: (params) => (
        <Box sx={{ display: 'flex', gap: 1 }}>
          <Tooltip title="Corregir y Regenerar (Docx)">
            <IconButton color="warning" onClick={() => handleOpenEditDoc(params.row)}>
              <EditIcon />
            </IconButton>
          </Tooltip>
          <Tooltip title="Descargar Final">
            <IconButton color="success" onClick={() => handleDownload(params.row.id, params.row.version)}>
              <DownloadIcon />
            </IconButton>
          </Tooltip>
        </Box>
      )
    }
  ];

  if (!proceso) return <Typography>Cargando expediente...</Typography>;

  return (
    <MainCard 
      title={`Expediente: ${proceso.codigo_proceso} - ${proceso.nombre_proyecto}`}
      secondary={<Button variant="contained" color="secondary" startIcon={<AddIcon />} onClick={handleOpenNewDoc}>Generar Documento</Button>}
    >
      <Box sx={{ height: 400, width: '100%', mt: 2 }}>
        <DataGrid rows={proceso.documentos || []} columns={columns} loading={loading} disableRowSelectionOnClick />
      </Box>

      {/* Modal de Generación / Edición con Extracción Dinámica */}
      <Dialog open={openDoc} onClose={() => setOpenDoc(false)} maxWidth="md" fullWidth>
        <DialogTitle>{editingDocId ? 'Corregir y Regenerar Documento' : 'Asistente de Generación Dinámica'}</DialogTitle>
        <DialogContent dividers>
          <Box component="form" sx={{ display: 'flex', flexDirection: 'column', gap: 3, mt: 1 }}>
            
            <FormControl fullWidth disabled={!!editingDocId}>
              <InputLabel>Seleccione el Formato (Plantilla Vigente)</InputLabel>
              <Select 
                value={selectedPlantillaId} 
                label="Seleccione el Formato (Plantilla Vigente)" 
                onChange={(e) => setSelectedPlantillaId(e.target.value as string)}
              >
                {plantillas.map((p: any) => (
                  <MenuItem key={p.id} value={p.id}>{p.nombre} (v{p.version})</MenuItem>
                ))}
              </Select>
            </FormControl>
            
            {loadingEsquema && (
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                <CircularProgress size={20} />
                <Typography variant="body2" color="textSecondary">El Motor SGE está leyendo el archivo DOCX y extrayendo las variables...</Typography>
              </Box>
            )}

            {!loadingEsquema && esquemaVariables.length > 0 && (
              <Box sx={{ bgcolor: 'grey.50', p: 2, borderRadius: 2, border: '1px solid', borderColor: 'divider' }}>
                <Typography variant="subtitle1" color="primary" sx={{ mb: 2 }}>Formulario Autogenerado desde el DOCX</Typography>
                <Grid container spacing={2}>
                  {esquemaVariables.map((v: any, index: number) => (
                    <Grid size={{ xs: 12, sm: v.tipo === 'texto' && v.nombre.includes('fecha') ? 6 : 12 }} key={index}>
                      {v.tipo === 'texto' && (
                        <TextField 
                          label={v.nombre.replace(/_/g, ' ').toUpperCase()} 
                          value={dinamicData[v.nombre] || ''} 
                          onChange={(e) => handleDynamicChange(v.nombre, e.target.value)} 
                          fullWidth 
                          helperText={renderContexto(v.contexto, v.nombre)}
                          multiline={!v.nombre.includes('fecha') && !v.nombre.includes('codigo')}
                          rows={v.nombre.includes('descripcion') || v.nombre.includes('objeto') ? 3 : 1}
                        />
                      )}
                      
                      {v.tipo === 'imagen' && (
                        <Box sx={{ border: '1px dashed grey', p: 2, borderRadius: 1 }}>
                           <Typography variant="body2" color="primary" sx={{mb: 1}}>📸 Subir Imagen para: {v.nombre}</Typography>
                           <input type="file" accept="image/*" onChange={(e) => handleImageUpload(v.nombre, e)} />
                           {renderContexto(v.contexto, v.nombre)}
                           {dinamicData[v.nombre] && <img src={dinamicData[v.nombre]} alt="preview" style={{maxHeight: 100, marginTop: 8}} />}
                        </Box>
                      )}
                      
                      {v.tipo === 'tabla_dinamica' && (
                        <Box sx={{ border: '1px solid', borderColor: 'divider', p: 2, borderRadius: 1, bgcolor: 'background.paper' }}>
                          <Typography variant="subtitle2" color="primary">{v.nombre} (Grilla Dinámica)</Typography>
                          {renderContexto(v.contexto, v.nombre)}
                          
                                                    <Box sx={{ mb: 2 }}>
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
                        </Box>
                      )}
                    </Grid>
                  ))}
                </Grid>
              </Box>
            )}

            {!loadingEsquema && selectedPlantillaId && esquemaVariables.length === 0 && (
              <Alert severity="warning">Esta plantilla no tiene variables {'{{ campos }}'} configuradas en su archivo DOCX.</Alert>
            )}

          </Box>
        </DialogContent>
        <DialogActions sx={{ p: 2 }}>
          <Button onClick={() => setOpenDoc(false)} color="error">Cancelar</Button>
          <Button 
            onClick={handleDocSubmit} 
            variant="contained" 
            color="primary"
            disabled={!selectedPlantillaId || loadingEsquema}
          >
            {editingDocId ? 'Reemplazar y Descargar vN+1' : 'Generar y Descargar DOCX'}
          </Button>
        </DialogActions>
      </Dialog>

      
      {/* Modal UX para Tablas Dinámicas */}
      <Dialog open={openRowModal} onClose={handleCloseRowModal} maxWidth="sm" fullWidth>
        <DialogTitle>Añadir Registro a {activeTableVar}</DialogTitle>
        <DialogContent dividers>
          <Box component="form" sx={{ display: 'flex', flexDirection: 'column', gap: 2.5, mt: 1 }}>
                          {(() => {
                const tableSchema = esquemaVariables.find((e: any) => e.nombre === activeTableVar);
                const columnsToRender = (tableSchema && (tableSchema.columnas || tableSchema.sub_atributos)) 
                  ? (tableSchema.columnas || tableSchema.sub_atributos)
                  : Object.keys(tempRowItem);

                return columnsToRender.map((colKey: string) => {
                  const lowerKey = colKey.toLowerCase();
                  
                  // REGLA A: Selectores Booleanos
                  if (lowerKey.includes('disponibilidad') || lowerKey.includes('aplica') || lowerKey.includes('estado')) {
                    return (
                      <FormControl fullWidth key={colKey} size="small" sx={{ mb: 2 }}>
                        <InputLabel>{colKey.replace(/_/g, ' ').toUpperCase()}</InputLabel>
                        <Select
                          value={tempRowItem[colKey] || 'SÍ'}
                          label={colKey.replace(/_/g, ' ').toUpperCase()}
                          onChange={(e) => handleTempRowPropChange(colKey, e.target.value)}
                        >
                          <MenuItem value="SÍ">SÍ</MenuItem>
                          <MenuItem value="NO">NO</MenuItem>
                        </Select>
                      </FormControl>
                    );
                  }
                  
                  // REGLA B: Imágenes Base64
                  if (lowerKey.includes('img_')) {
                    return (
                      <Box key={colKey} sx={{ mb: 2 }}>
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
                  
                  // REGLA C: Campos de texto normales
                  return (
                    <TextField 
                      key={colKey} 
                      label={colKey.replace(/_/g, ' ').toUpperCase()} 
                      fullWidth 
                      sx={{ mb: 2 }}
                      size="small"
                      value={tempRowItem[colKey] || ''} 
                      onChange={(e) => handleTempRowPropChange(colKey, e.target.value)} 
                    />
                  );
                });
             })()}
             <Button size="small" variant="text" onClick={handleAddPropToTempRow}>+ Añadir Nueva Columna/Atributo</Button>
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseRowModal} color="error" variant="text">Cancelar</Button>
          <Button onClick={handleSaveRow} variant="contained" color="primary">Guardar Registro</Button>
        </DialogActions>
      </Dialog>

      <Snackbar open={toast.open} autoHideDuration={4000} onClose={() => setToast({...toast, open: false})} anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}>
        <Alert severity={toast.severity as any} variant="filled">{toast.message}</Alert>
      </Snackbar>
    </MainCard>
  );
}
