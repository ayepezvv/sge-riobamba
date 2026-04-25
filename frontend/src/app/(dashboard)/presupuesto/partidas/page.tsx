'use client';

import React, { useCallback, useEffect, useState } from 'react';
import {
  Alert, Box, Button, Chip, CircularProgress, Dialog, DialogActions,
  DialogContent, DialogTitle, FormControl, Grid, InputLabel, MenuItem,
  Select, TextField, Typography
} from '@mui/material';
import { DataGrid, GridColDef, GridToolbar, GridActionsCellItem } from '@mui/x-data-grid';
import { IconPlus, IconEdit } from '@tabler/icons-react';

import MainCard from 'ui-component/cards/MainCard';
import { listarPartidas, crearPartida, actualizarPartida } from 'api/presupuesto';
import { PartidaPresupuestaria, PartidaPresupuestariaCrear, TipoPartida } from 'types/presupuesto';

const NIVELES = [1, 2, 3, 4, 5];
const TIPOS: TipoPartida[] = ['INGRESO', 'GASTO'];

const PartidasPage = () => {
  const [partidas, setPartidas] = useState<PartidaPresupuestaria[]>([]);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filtroTipo, setFiltroTipo] = useState<string>('');

  const [abrirFormulario, setAbrirFormulario] = useState(false);
  const [partidaEditar, setPartidaEditar] = useState<PartidaPresupuestaria | null>(null);
  const [formulario, setFormulario] = useState<PartidaPresupuestariaCrear>({
    codigo: '', nombre: '', tipo: 'GASTO', nivel: 1, es_hoja: true,
  });
  const [guardando, setGuardando] = useState(false);
  const [errorForm, setErrorForm] = useState<string | null>(null);

  const cargarPartidas = useCallback(async () => {
    setCargando(true);
    setError(null);
    try {
      const res = await listarPartidas(filtroTipo ? { tipo: filtroTipo } : {});
      setPartidas(res);
    } catch (err: any) {
      setError(err?.detail || err?.message || 'Error al cargar partidas');
    } finally {
      setCargando(false);
    }
  }, [filtroTipo]);

  useEffect(() => { cargarPartidas(); }, [cargarPartidas]);

  const abrirNueva = () => {
    setPartidaEditar(null);
    setFormulario({ codigo: '', nombre: '', tipo: 'GASTO', nivel: 1, es_hoja: true });
    setErrorForm(null);
    setAbrirFormulario(true);
  };

  const abrirEdicion = (partida: PartidaPresupuestaria) => {
    setPartidaEditar(partida);
    setFormulario({
      codigo: partida.codigo,
      nombre: partida.nombre,
      descripcion: partida.descripcion,
      tipo: partida.tipo,
      nivel: partida.nivel,
      es_hoja: partida.es_hoja,
      id_partida_padre: partida.id_partida_padre,
      estado: partida.estado,
    });
    setErrorForm(null);
    setAbrirFormulario(true);
  };

  const handleGuardar = async () => {
    if (!formulario.codigo || !formulario.nombre) {
      setErrorForm('Código y nombre son obligatorios.');
      return;
    }
    setGuardando(true);
    setErrorForm(null);
    try {
      if (partidaEditar) {
        await actualizarPartida(partidaEditar.id_partida, {
          nombre: formulario.nombre,
          descripcion: formulario.descripcion,
          es_hoja: formulario.es_hoja,
          estado: formulario.estado,
        });
      } else {
        await crearPartida(formulario);
      }
      setAbrirFormulario(false);
      cargarPartidas();
    } catch (err: any) {
      setErrorForm(err?.response?.data?.detail || err?.message || 'Error al guardar');
    } finally {
      setGuardando(false);
    }
  };

  const columnas: GridColDef[] = [
    { field: 'codigo', headerName: 'Código SIGEF', width: 160 },
    { field: 'nombre', headerName: 'Nombre', flex: 1 },
    {
      field: 'tipo', headerName: 'Tipo', width: 110,
      renderCell: ({ value }) => (
        <Chip label={value} size="small" color={value === 'INGRESO' ? 'success' : 'warning'} />
      ),
    },
    { field: 'nivel', headerName: 'Nivel', width: 80, type: 'number' },
    {
      field: 'es_hoja', headerName: 'Hoja', width: 80,
      renderCell: ({ value }) => <Chip label={value ? 'Sí' : 'No'} size="small" color={value ? 'primary' : 'default'} />,
    },
    {
      field: 'estado', headerName: 'Estado', width: 100,
      renderCell: ({ value }) => <Chip label={value} size="small" color={value === 'ACTIVO' ? 'success' : 'error'} />,
    },
    {
      field: 'acciones', type: 'actions', headerName: 'Acciones', width: 90,
      getActions: ({ row }) => [
        <GridActionsCellItem key="editar" icon={<IconEdit size={18} />} label="Editar"
          onClick={() => abrirEdicion(row as PartidaPresupuestaria)} />,
      ],
    },
  ];

  return (
    <MainCard title="Partidas Presupuestarias">
      <Box sx={{ mb: 2, display: 'flex', gap: 2, alignItems: 'center', flexWrap: 'wrap' }}>
        <FormControl size="small" sx={{ minWidth: 160 }}>
          <InputLabel>Tipo</InputLabel>
          <Select value={filtroTipo} label="Tipo" onChange={e => setFiltroTipo(e.target.value)}>
            <MenuItem value="">Todos</MenuItem>
            {TIPOS.map(t => <MenuItem key={t} value={t}>{t}</MenuItem>)}
          </Select>
        </FormControl>
        <Button variant="contained" startIcon={<IconPlus />} onClick={abrirNueva}>
          Nueva Partida
        </Button>
      </Box>

      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

      {cargando ? (
        <Box display="flex" justifyContent="center" p={4}><CircularProgress /></Box>
      ) : (
        <DataGrid
          rows={partidas}
          columns={columnas}
          getRowId={r => r.id_partida}
          slots={{ toolbar: GridToolbar }}
          slotProps={{ toolbar: { showQuickFilter: true } }}
          autoHeight
          density="compact"
          initialState={{ pagination: { paginationModel: { pageSize: 25 } } }}
          pageSizeOptions={[25, 50, 100]}
        />
      )}

      <Dialog open={abrirFormulario} onClose={() => setAbrirFormulario(false)} maxWidth="sm" fullWidth>
        <DialogTitle>{partidaEditar ? 'Editar Partida' : 'Nueva Partida Presupuestaria'}</DialogTitle>
        <DialogContent>
          <Grid container spacing={2} sx={{ mt: 0.5 }}>
            <Grid size={6}>
              <TextField
                fullWidth label="Código SIGEF" value={formulario.codigo}
                onChange={e => setFormulario(f => ({ ...f, codigo: e.target.value }))}
                disabled={!!partidaEditar} required size="small"
              />
            </Grid>
            <Grid size={6}>
              <FormControl fullWidth size="small" disabled={!!partidaEditar}>
                <InputLabel>Tipo</InputLabel>
                <Select value={formulario.tipo} label="Tipo"
                  onChange={e => setFormulario(f => ({ ...f, tipo: e.target.value as TipoPartida }))}>
                  {TIPOS.map(t => <MenuItem key={t} value={t}>{t}</MenuItem>)}
                </Select>
              </FormControl>
            </Grid>
            <Grid size={12}>
              <TextField
                fullWidth label="Nombre" value={formulario.nombre}
                onChange={e => setFormulario(f => ({ ...f, nombre: e.target.value }))}
                required size="small"
              />
            </Grid>
            <Grid size={12}>
              <TextField
                fullWidth label="Descripción" value={formulario.descripcion || ''}
                onChange={e => setFormulario(f => ({ ...f, descripcion: e.target.value }))}
                multiline rows={2} size="small"
              />
            </Grid>
            <Grid size={4}>
              <FormControl fullWidth size="small" disabled={!!partidaEditar}>
                <InputLabel>Nivel</InputLabel>
                <Select value={formulario.nivel} label="Nivel"
                  onChange={e => setFormulario(f => ({ ...f, nivel: Number(e.target.value) }))}>
                  {NIVELES.map(n => <MenuItem key={n} value={n}>{n}</MenuItem>)}
                </Select>
              </FormControl>
            </Grid>
            <Grid size={4}>
              <FormControl fullWidth size="small">
                <InputLabel>¿Es Hoja?</InputLabel>
                <Select value={formulario.es_hoja ? 'true' : 'false'} label="¿Es Hoja?"
                  onChange={e => setFormulario(f => ({ ...f, es_hoja: e.target.value === 'true' }))}>
                  <MenuItem value="true">Sí</MenuItem>
                  <MenuItem value="false">No</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid size={4}>
              {partidaEditar && (
                <FormControl fullWidth size="small">
                  <InputLabel>Estado</InputLabel>
                  <Select value={formulario.estado || 'ACTIVO'} label="Estado"
                    onChange={e => setFormulario(f => ({ ...f, estado: e.target.value }))}>
                    <MenuItem value="ACTIVO">ACTIVO</MenuItem>
                    <MenuItem value="INACTIVO">INACTIVO</MenuItem>
                  </Select>
                </FormControl>
              )}
            </Grid>
          </Grid>
          {errorForm && <Alert severity="error" sx={{ mt: 2 }}>{errorForm}</Alert>}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setAbrirFormulario(false)}>Cancelar</Button>
          <Button variant="contained" onClick={handleGuardar} disabled={guardando}>
            {guardando ? <CircularProgress size={20} /> : (partidaEditar ? 'Guardar' : 'Crear')}
          </Button>
        </DialogActions>
      </Dialog>
    </MainCard>
  );
};

export default PartidasPage;
