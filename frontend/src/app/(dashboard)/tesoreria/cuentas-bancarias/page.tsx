'use client';

import React, { useCallback, useEffect, useState } from 'react';
import {
  Alert, Box, Button, Chip, CircularProgress, Dialog, DialogActions,
  DialogContent, DialogTitle, FormControl, Grid, InputLabel, MenuItem,
  Select, TextField, Typography
} from '@mui/material';
import { DataGrid, GridColDef, GridToolbar, GridActionsCellItem, GridRowParams } from '@mui/x-data-grid';
import { IconPlus, IconEdit } from '@tabler/icons-react';

import MainCard from 'ui-component/cards/MainCard';
import {
  listarEntidadesBancarias, crearEntidadBancaria,
  listarCuentasBancarias, crearCuentaBancaria, actualizarCuentaBancaria,
} from 'api/tesoreria';
import { CuentaBancaria, CuentaBancariaCrear, EntidadBancaria, TipoCuentaBancaria } from 'types/tesoreria';

const TIPOS: TipoCuentaBancaria[] = ['CORRIENTE', 'AHORROS', 'RECAUDACION', 'PAGOS'];

const FORMULARIO_VACIO: CuentaBancariaCrear = {
  entidad_bancaria_id: 0,
  numero_cuenta: '',
  nombre: '',
  tipo: 'CORRIENTE',
  moneda: 'USD',
  saldo_inicial: 0,
  es_activa: true,
};

const CuentasBancariasPage = () => {
  const [cuentas, setCuentas] = useState<CuentaBancaria[]>([]);
  const [entidades, setEntidades] = useState<EntidadBancaria[]>([]);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [abrirModal, setAbrirModal] = useState(false);
  const [formulario, setFormulario] = useState<CuentaBancariaCrear>(FORMULARIO_VACIO);
  const [editandoId, setEditandoId] = useState<number | null>(null);
  const [guardando, setGuardando] = useState(false);
  const [errorFormulario, setErrorFormulario] = useState<string | null>(null);

  const cargarDatos = useCallback(async () => {
    setCargando(true);
    setError(null);
    try {
      const [resCuentas, resEntidades] = await Promise.all([
        listarCuentasBancarias({ solo_activas: false }),
        listarEntidadesBancarias(false),
      ]);
      setCuentas(resCuentas);
      setEntidades(resEntidades);
    } catch (err: any) {
      setError(err?.detail || err?.message || 'Error al cargar los datos');
    } finally {
      setCargando(false);
    }
  }, []);

  useEffect(() => { cargarDatos(); }, [cargarDatos]);

  const abrirNuevo = () => {
    setEditandoId(null);
    setFormulario(FORMULARIO_VACIO);
    setErrorFormulario(null);
    setAbrirModal(true);
  };

  const abrirEditar = (cuenta: CuentaBancaria) => {
    setEditandoId(cuenta.id);
    setFormulario({
      entidad_bancaria_id: cuenta.entidad_bancaria_id,
      numero_cuenta: cuenta.numero_cuenta,
      nombre: cuenta.nombre,
      tipo: cuenta.tipo,
      moneda: cuenta.moneda,
      saldo_inicial: cuenta.saldo_inicial,
      es_activa: cuenta.es_activa,
    });
    setErrorFormulario(null);
    setAbrirModal(true);
  };

  const handleGuardar = async () => {
    if (!formulario.entidad_bancaria_id || !formulario.numero_cuenta || !formulario.nombre) {
      setErrorFormulario('Entidad bancaria, número de cuenta y nombre son obligatorios.');
      return;
    }
    setGuardando(true);
    setErrorFormulario(null);
    try {
      if (editandoId) {
        await actualizarCuentaBancaria(editandoId, formulario);
      } else {
        await crearCuentaBancaria(formulario);
      }
      setAbrirModal(false);
      await cargarDatos();
    } catch (err: any) {
      setErrorFormulario(err?.detail || err?.message || 'Error al guardar');
    } finally {
      setGuardando(false);
    }
  };

  const columnas: GridColDef[] = [
    { field: 'numero_cuenta', headerName: 'N° Cuenta', width: 150, renderCell: p => <Typography variant="body2" fontFamily="monospace">{p.value}</Typography> },
    { field: 'nombre', headerName: 'Nombre', flex: 1, minWidth: 180 },
    {
      field: 'entidad_bancaria_id', headerName: 'Entidad Bancaria', width: 160,
      valueGetter: (p: any) => entidades.find(e => e.id === p.row.entidad_bancaria_id)?.nombre ?? '—',
    },
    { field: 'tipo', headerName: 'Tipo', width: 120, renderCell: p => <Chip label={p.value} size="small" variant="outlined" /> },
    { field: 'moneda', headerName: 'Moneda', width: 80 },
    {
      field: 'saldo_inicial', headerName: 'Saldo Inicial', width: 130, type: 'number',
      valueFormatter: (p: any) => Number(p.value).toFixed(2),
    },
    {
      field: 'es_activa', headerName: 'Estado', width: 90,
      renderCell: p => <Chip label={p.value ? 'Activa' : 'Inactiva'} color={p.value ? 'success' : 'default'} size="small" />,
    },
    {
      field: 'acciones', type: 'actions', headerName: '', width: 60,
      getActions: (params: GridRowParams) => [
        <GridActionsCellItem key="editar" icon={<IconEdit size={18} />} label="Editar" onClick={() => abrirEditar(params.row as CuentaBancaria)} />,
      ],
    },
  ];

  return (
    <MainCard
      title="Cuentas Bancarias"
      secondary={
        <Button variant="contained" startIcon={<IconPlus size={18} />} onClick={abrirNuevo}>
          Nueva Cuenta
        </Button>
      }
    >
      {error && <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError(null)}>{error}</Alert>}

      <Box sx={{ height: 560, width: '100%' }}>
        <DataGrid
          rows={cuentas}
          columns={columnas}
          loading={cargando}
          pageSizeOptions={[25, 50]}
          slots={{ toolbar: GridToolbar }}
          slotProps={{ toolbar: { showQuickFilter: true } }}
          initialState={{ pagination: { paginationModel: { pageSize: 25 } } }}
          disableRowSelectionOnClick
          sx={{ border: 'none', '& .MuiDataGrid-columnHeaders': { backgroundColor: '#f8fafc', fontWeight: 700 } }}
        />
      </Box>

      <Dialog open={abrirModal} onClose={() => setAbrirModal(false)} maxWidth="sm" fullWidth>
        <DialogTitle>{editandoId ? 'Editar Cuenta Bancaria' : 'Nueva Cuenta Bancaria'}</DialogTitle>
        <DialogContent dividers>
          {errorFormulario && <Alert severity="error" sx={{ mb: 2 }}>{errorFormulario}</Alert>}
          <Grid container spacing={2} sx={{ pt: 1 }}>
            <Grid item xs={12}>
              <FormControl fullWidth>
                <InputLabel>Entidad Bancaria *</InputLabel>
                <Select value={formulario.entidad_bancaria_id || ''} label="Entidad Bancaria *"
                  onChange={e => setFormulario({ ...formulario, entidad_bancaria_id: Number(e.target.value) })}>
                  {entidades.map(e => <MenuItem key={e.id} value={e.id}>{e.nombre}</MenuItem>)}
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField label="Número de Cuenta *" fullWidth value={formulario.numero_cuenta}
                onChange={e => setFormulario({ ...formulario, numero_cuenta: e.target.value })} />
            </Grid>
            <Grid item xs={12} md={6}>
              <FormControl fullWidth>
                <InputLabel>Tipo *</InputLabel>
                <Select value={formulario.tipo} label="Tipo *"
                  onChange={e => setFormulario({ ...formulario, tipo: e.target.value as TipoCuentaBancaria })}>
                  {TIPOS.map(t => <MenuItem key={t} value={t}>{t}</MenuItem>)}
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12}>
              <TextField label="Nombre *" fullWidth value={formulario.nombre}
                onChange={e => setFormulario({ ...formulario, nombre: e.target.value })} />
            </Grid>
            <Grid item xs={6}>
              <TextField label="Moneda" fullWidth value={formulario.moneda}
                onChange={e => setFormulario({ ...formulario, moneda: e.target.value })} />
            </Grid>
            <Grid item xs={6}>
              <TextField label="Saldo Inicial" type="number" fullWidth value={formulario.saldo_inicial}
                onChange={e => setFormulario({ ...formulario, saldo_inicial: parseFloat(e.target.value) || 0 })} />
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setAbrirModal(false)} color="inherit">Cancelar</Button>
          <Button onClick={handleGuardar} variant="contained" disabled={guardando}
            startIcon={guardando ? <CircularProgress size={16} /> : undefined}>
            {guardando ? 'Guardando...' : 'Guardar'}
          </Button>
        </DialogActions>
      </Dialog>
    </MainCard>
  );
};

export default CuentasBancariasPage;
