"use client";

import { useEffect, useState, useCallback } from "react";
import {
  Grid, Box, Chip, Button, CircularProgress, Alert,
  FormControl, InputLabel, Select, MenuItem,
  Dialog, DialogTitle, DialogContent, DialogActions,
  Typography, Divider, Paper,
} from "@mui/material";
import { DataGrid, GridColDef, GridToolbar } from "@mui/x-data-grid";
import { IconRefresh, IconEye } from "@tabler/icons-react";
import MainCard from "ui-component/cards/MainCard";
import { gridSpacing } from "store/constant";
import { listarMovimientos, obtenerMovimiento, obtenerDetalleMovimiento } from "api/inventario";
import { MovimientoListado, Movimiento, LineaKardex } from "types/inventario";

const ANNOS = [2021, 2022, 2023, 2024, 2025];
const fmtMoneda = (v?: number) =>
  v != null ? `$${Number(v).toLocaleString("es-EC", { minimumFractionDigits: 2 })}` : "—";
const fmtFecha = (v?: string) =>
  v ? new Date(v).toLocaleDateString("es-EC") : "—";

export default function MovimientosPage() {
  const [movimientos, setMovimientos] = useState<MovimientoListado[]>([]);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [anno, setAnno] = useState<number | "">(2025);
  const [tipoFiltro, setTipoFiltro] = useState<"" | "ENTRADA" | "SALIDA">("");

  // Modal detalle
  const [movDetalle, setMovDetalle] = useState<Movimiento | null>(null);
  const [lineasDetalle, setLineasDetalle] = useState<LineaKardex[]>([]);
  const [cargandoDetalle, setCargandoDetalle] = useState(false);
  const [abrirModal, setAbrirModal] = useState(false);

  const cargar = useCallback(async () => {
    setCargando(true);
    setError(null);
    try {
      const data = await listarMovimientos({
        anno: anno !== "" ? anno : undefined,
        tipo: tipoFiltro !== "" ? tipoFiltro : undefined,
        limit: 500,
      });
      setMovimientos(data);
    } catch (e: any) {
      setError(e?.message || "Error al cargar movimientos");
    } finally {
      setCargando(false);
    }
  }, [anno, tipoFiltro]);

  useEffect(() => { cargar(); }, [cargar]);

  const verDetalle = async (id: number) => {
    setCargandoDetalle(true);
    setAbrirModal(true);
    try {
      const [mov, lineas] = await Promise.all([
        obtenerMovimiento(id),
        obtenerDetalleMovimiento(id),
      ]);
      setMovDetalle(mov);
      setLineasDetalle(lineas);
    } catch {
      setMovDetalle(null);
      setLineasDetalle([]);
    } finally {
      setCargandoDetalle(false);
    }
  };

  const columnas: GridColDef[] = [
    { field: "numero_movimiento", headerName: "N° Mov.", width: 90 },
    {
      field: "fecha",
      headerName: "Fecha",
      width: 110,
      valueFormatter: (v) => fmtFecha(v as string),
    },
    {
      field: "tipo_movimiento",
      headerName: "Tipo",
      width: 100,
      renderCell: (p) => (
        <Chip
          size="small"
          label={p.value}
          color={p.value === "ENTRADA" ? "success" : "error"}
        />
      ),
    },
    { field: "proveedor", headerName: "Proveedor", flex: 1, minWidth: 160 },
    { field: "destino", headerName: "Destino / Área", flex: 1, minWidth: 160 },
    { field: "encargado", headerName: "Encargado", width: 160 },
    {
      field: "costo_total",
      headerName: "Costo Total",
      width: 130,
      type: "number",
      valueFormatter: (v) => fmtMoneda(v as number),
    },
    { field: "anno_fiscal", headerName: "Año", width: 70 },
    {
      field: "acciones",
      headerName: "Detalle",
      width: 80,
      sortable: false,
      renderCell: (p) => (
        <Button
          size="small"
          startIcon={<IconEye size={14} />}
          onClick={() => verDetalle(p.row.id)}
        >
          Ver
        </Button>
      ),
    },
  ];

  const columnasLineas: GridColDef[] = [
    {
      field: "articulo",
      headerName: "Artículo",
      flex: 1,
      minWidth: 200,
      valueGetter: (_, row) => row.articulo?.nombre ?? `ID ${row.id_articulo}`,
    },
    {
      field: "cantidad",
      headerName: "Cantidad",
      width: 100,
      type: "number",
      valueFormatter: (v) =>
        Number(v).toLocaleString("es-EC", { minimumFractionDigits: 2 }),
    },
    {
      field: "costo_unitario",
      headerName: "Costo Unit.",
      width: 120,
      type: "number",
      valueFormatter: (v) => fmtMoneda(v as number),
    },
    {
      field: "total_linea",
      headerName: "Total Línea",
      width: 120,
      type: "number",
      valueFormatter: (v) => fmtMoneda(v as number),
    },
  ];

  return (
    <Grid container spacing={gridSpacing}>
      <Grid size={12}>
        <MainCard title="Movimientos de Bodega — Entradas y Salidas">
          {/* Filtros */}
          <Grid container spacing={2} mb={2}>
            <Grid size={{ xs: 12, sm: 3 }}>
              <FormControl fullWidth size="small">
                <InputLabel>Año Fiscal</InputLabel>
                <Select
                  value={anno}
                  label="Año Fiscal"
                  onChange={(e) => setAnno(e.target.value as number | "")}
                >
                  <MenuItem value="">Todos los años</MenuItem>
                  {ANNOS.map((a) => (
                    <MenuItem key={a} value={a}>{a}</MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
            <Grid size={{ xs: 12, sm: 3 }}>
              <FormControl fullWidth size="small">
                <InputLabel>Tipo de Movimiento</InputLabel>
                <Select
                  value={tipoFiltro}
                  label="Tipo de Movimiento"
                  onChange={(e) =>
                    setTipoFiltro(e.target.value as "" | "ENTRADA" | "SALIDA")
                  }
                >
                  <MenuItem value="">Todos</MenuItem>
                  <MenuItem value="ENTRADA">Entradas</MenuItem>
                  <MenuItem value="SALIDA">Salidas</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid size={{ xs: 12, sm: 2 }}>
              <Button
                fullWidth
                variant="outlined"
                startIcon={<IconRefresh size={16} />}
                onClick={cargar}
              >
                Actualizar
              </Button>
            </Grid>
          </Grid>

          {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

          <Box sx={{ height: 580, width: "100%" }}>
            <DataGrid
              rows={movimientos}
              columns={columnas}
              loading={cargando}
              slots={{ toolbar: GridToolbar }}
              slotProps={{ toolbar: { showQuickFilter: true } }}
              initialState={{
                pagination: { paginationModel: { pageSize: 25 } },
              }}
              pageSizeOptions={[25, 50, 100]}
              disableRowSelectionOnClick
              density="compact"
            />
          </Box>
        </MainCard>
      </Grid>

      {/* Modal Detalle Movimiento */}
      <Dialog
        open={abrirModal}
        onClose={() => setAbrirModal(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>
          Detalle de Movimiento{" "}
          {movDetalle ? `N° ${movDetalle.numero_movimiento}` : ""}
        </DialogTitle>
        <DialogContent>
          {cargandoDetalle ? (
            <Box display="flex" justifyContent="center" py={4}>
              <CircularProgress />
            </Box>
          ) : movDetalle ? (
            <>
              <Paper variant="outlined" sx={{ p: 2, mb: 2 }}>
                <Grid container spacing={1}>
                  <Grid size={6}>
                    <Typography variant="body2" color="text.secondary">Tipo</Typography>
                    <Chip
                      size="small"
                      label={movDetalle.tipo_movimiento}
                      color={movDetalle.tipo_movimiento === "ENTRADA" ? "success" : "error"}
                    />
                  </Grid>
                  <Grid size={6}>
                    <Typography variant="body2" color="text.secondary">Fecha</Typography>
                    <Typography variant="body2">{fmtFecha(movDetalle.fecha)}</Typography>
                  </Grid>
                  <Grid size={6}>
                    <Typography variant="body2" color="text.secondary">N° Factura</Typography>
                    <Typography variant="body2">{movDetalle.numero_factura || "—"}</Typography>
                  </Grid>
                  <Grid size={6}>
                    <Typography variant="body2" color="text.secondary">Costo Total</Typography>
                    <Typography variant="body2"><strong>{fmtMoneda(movDetalle.costo_total)}</strong></Typography>
                  </Grid>
                  <Grid size={12}>
                    <Typography variant="body2" color="text.secondary">Observación</Typography>
                    <Typography variant="body2">{movDetalle.observacion || "—"}</Typography>
                  </Grid>
                </Grid>
              </Paper>
              <Divider sx={{ mb: 2 }} />
              <Typography variant="h6" mb={1}>
                Líneas del Movimiento ({lineasDetalle.length} artículo
                {lineasDetalle.length !== 1 ? "s" : ""})
              </Typography>
              <Box sx={{ height: 300, width: "100%" }}>
                <DataGrid
                  rows={lineasDetalle}
                  columns={columnasLineas}
                  density="compact"
                  disableRowSelectionOnClick
                  pageSizeOptions={[25, 50]}
                  initialState={{
                    pagination: { paginationModel: { pageSize: 25 } },
                  }}
                />
              </Box>
            </>
          ) : (
            <Alert severity="warning">No se pudo cargar el detalle.</Alert>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setAbrirModal(false)}>Cerrar</Button>
        </DialogActions>
      </Dialog>
    </Grid>
  );
}
