'use client';

import React, { useCallback, useState } from 'react';
import {
  Alert, Box, Button, CircularProgress, LinearProgress,
  TextField, Typography
} from '@mui/material';
import { DataGrid, GridColDef, GridToolbar } from '@mui/x-data-grid';
import { IconSearch } from '@tabler/icons-react';

import MainCard from 'ui-component/cards/MainCard';
import { obtenerEjecucion } from 'api/presupuesto';
import { EjecucionPresupuestaria } from 'types/presupuesto';

const formatMonto = (v: number) =>
  new Intl.NumberFormat('es-EC', { style: 'currency', currency: 'USD' }).format(v);

const EjecucionPage = () => {
  const [anioFiscal, setAnioFiscal] = useState<number>(new Date().getFullYear());
  const [ejecucion, setEjecucion] = useState<EjecucionPresupuestaria[]>([]);
  const [cargando, setCargando] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [consultado, setConsultado] = useState(false);

  const cargarEjecucion = useCallback(async () => {
    setCargando(true);
    setError(null);
    try {
      const res = await obtenerEjecucion(anioFiscal);
      setEjecucion(res);
      setConsultado(true);
    } catch (err: any) {
      setError(err?.response?.data?.detail || err?.message || 'Error al cargar ejecución');
    } finally {
      setCargando(false);
    }
  }, [anioFiscal]);

  // Totales
  const totalCodificado = ejecucion.reduce((s, r) => s + Number(r.monto_codificado), 0);
  const totalDevengado = ejecucion.reduce((s, r) => s + Number(r.monto_devengado), 0);
  const totalSaldo = ejecucion.reduce((s, r) => s + Number(r.saldo_disponible), 0);
  const porcentajeGlobal = totalCodificado > 0 ? (totalDevengado / totalCodificado) * 100 : 0;

  const columnas: GridColDef[] = [
    { field: 'codigo_partida', headerName: 'Código Partida', width: 160 },
    { field: 'nombre_partida', headerName: 'Nombre Partida', flex: 1 },
    {
      field: 'monto_inicial', headerName: 'Inicial', width: 130,
      renderCell: ({ value }) => formatMonto(Number(value)),
    },
    {
      field: 'monto_codificado', headerName: 'Codificado', width: 130,
      renderCell: ({ value }) => formatMonto(Number(value)),
    },
    {
      field: 'monto_comprometido', headerName: 'Comprometido', width: 130,
      renderCell: ({ value }) => formatMonto(Number(value)),
    },
    {
      field: 'monto_devengado', headerName: 'Devengado', width: 130,
      renderCell: ({ value }) => formatMonto(Number(value)),
    },
    {
      field: 'monto_pagado', headerName: 'Pagado', width: 130,
      renderCell: ({ value }) => formatMonto(Number(value)),
    },
    {
      field: 'saldo_disponible', headerName: 'Saldo Disponible', width: 140,
      renderCell: ({ value }) => (
        <Typography variant="body2" color={Number(value) < 0 ? 'error' : 'inherit'}>
          {formatMonto(Number(value))}
        </Typography>
      ),
    },
    {
      field: 'porcentaje_ejecucion', headerName: '% Ejecución', width: 150,
      renderCell: ({ value }) => {
        const pct = Number(value);
        return (
          <Box sx={{ width: '100%', display: 'flex', alignItems: 'center', gap: 1 }}>
            <LinearProgress
              variant="determinate"
              value={Math.min(pct, 100)}
              sx={{ flex: 1, height: 8, borderRadius: 4 }}
              color={pct >= 80 ? 'success' : pct >= 50 ? 'warning' : 'error'}
            />
            <Typography variant="caption">{pct.toFixed(1)}%</Typography>
          </Box>
        );
      },
    },
  ];

  return (
    <MainCard title="Informe de Ejecución Presupuestaria">
      <Box sx={{ mb: 3, display: 'flex', gap: 2, alignItems: 'center' }}>
        <TextField
          label="Año Fiscal" type="number" size="small" sx={{ width: 140 }}
          value={anioFiscal}
          onChange={e => setAnioFiscal(Number(e.target.value))}
          inputProps={{ min: 2000, max: 2100 }}
        />
        <Button variant="contained" startIcon={<IconSearch />} onClick={cargarEjecucion} disabled={cargando}>
          {cargando ? <CircularProgress size={20} /> : 'Consultar'}
        </Button>
      </Box>

      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

      {consultado && ejecucion.length > 0 && (
        <Box sx={{ mb: 3, p: 2, bgcolor: 'background.paper', borderRadius: 1, border: '1px solid', borderColor: 'divider' }}>
          <Typography variant="h6" gutterBottom>Resumen Año Fiscal {anioFiscal}</Typography>
          <Box sx={{ display: 'flex', gap: 4, flexWrap: 'wrap' }}>
            <Box>
              <Typography variant="caption" color="text.secondary">Presupuesto Codificado</Typography>
              <Typography variant="h5">{formatMonto(totalCodificado)}</Typography>
            </Box>
            <Box>
              <Typography variant="caption" color="text.secondary">Total Devengado</Typography>
              <Typography variant="h5" color="primary">{formatMonto(totalDevengado)}</Typography>
            </Box>
            <Box>
              <Typography variant="caption" color="text.secondary">Saldo Disponible</Typography>
              <Typography variant="h5" color={totalSaldo < 0 ? 'error' : 'success.main'}>{formatMonto(totalSaldo)}</Typography>
            </Box>
            <Box sx={{ minWidth: 200 }}>
              <Typography variant="caption" color="text.secondary">Ejecución Global</Typography>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mt: 0.5 }}>
                <LinearProgress
                  variant="determinate"
                  value={Math.min(porcentajeGlobal, 100)}
                  sx={{ flex: 1, height: 12, borderRadius: 4 }}
                  color={porcentajeGlobal >= 80 ? 'success' : porcentajeGlobal >= 50 ? 'warning' : 'error'}
                />
                <Typography variant="body2" fontWeight="bold">{porcentajeGlobal.toFixed(1)}%</Typography>
              </Box>
            </Box>
          </Box>
        </Box>
      )}

      {consultado && (
        ejecucion.length === 0 ? (
          <Alert severity="info">No hay datos de ejecución para el año fiscal {anioFiscal}.</Alert>
        ) : (
          <DataGrid
            rows={ejecucion}
            columns={columnas}
            getRowId={(r, i) => `${r.codigo_partida}`}
            slots={{ toolbar: GridToolbar }}
            slotProps={{ toolbar: { showQuickFilter: true } }}
            autoHeight
            density="compact"
            initialState={{ pagination: { paginationModel: { pageSize: 50 } } }}
            pageSizeOptions={[50, 100]}
          />
        )
      )}
    </MainCard>
  );
};

export default EjecucionPage;
