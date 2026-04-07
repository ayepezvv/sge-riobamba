"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import {
  Grid, Box, Typography, Chip, Button, CircularProgress,
  Alert, Divider, Paper, FormControl, InputLabel, Select, MenuItem,
} from "@mui/material";
import { DataGrid, GridColDef } from "@mui/x-data-grid";
import { IconArrowLeft, IconPackages } from "@tabler/icons-react";
import MainCard from "ui-component/cards/MainCard";
import { gridSpacing } from "store/constant";
import { obtenerArticulo, obtenerKardex } from "api/inventario";
import { Articulo, LineaKardex } from "types/inventario";

const ANNOS = [2021, 2022, 2023, 2024, 2025];

const fmt = (val?: number) =>
  val != null
    ? Number(val).toLocaleString("es-EC", { minimumFractionDigits: 2 })
    : "—";

const fmtMoneda = (val?: number) => (val != null ? `$${fmt(val)}` : "—");

const InfoRow = ({ label, value }: { label: string; value: React.ReactNode }) => (
  <Box display="flex" gap={1} mb={0.5}>
    <Typography variant="body2" color="text.secondary" minWidth={160}>
      {label}:
    </Typography>
    <Typography variant="body2">{value}</Typography>
  </Box>
);

export default function ArticuloDetallePage() {
  const params = useParams();
  const router = useRouter();
  const articuloId = Number(params.id);

  const [articulo, setArticulo] = useState<Articulo | null>(null);
  const [kardex, setKardex] = useState<LineaKardex[]>([]);
  const [cargando, setCargando] = useState(true);
  const [cargandoKardex, setCargandoKardex] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [annoKardex, setAnnoKardex] = useState<number | "">(2025);

  useEffect(() => {
    setCargando(true);
    obtenerArticulo(articuloId)
      .then(setArticulo)
      .catch((e) => setError(e?.message || "Error al cargar artículo"))
      .finally(() => setCargando(false));
  }, [articuloId]);

  useEffect(() => {
    setCargandoKardex(true);
    obtenerKardex(articuloId, {
      anno: annoKardex !== "" ? annoKardex : undefined,
      limit: 500,
    })
      .then(setKardex)
      .catch(() => setKardex([]))
      .finally(() => setCargandoKardex(false));
  }, [articuloId, annoKardex]);

  const columnasKardex: GridColDef[] = [
    {
      field: "fecha",
      headerName: "Fecha",
      width: 160,
      valueFormatter: (v) => v ? new Date(v as string).toLocaleDateString("es-EC") : "",
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
    {
      field: "cantidad",
      headerName: "Cantidad",
      width: 100,
      type: "number",
      valueFormatter: (v) => fmt(v as number),
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
    {
      field: "costo_promedio",
      headerName: "Costo Prom.",
      width: 120,
      type: "number",
      valueFormatter: (v) => fmtMoneda(v as number),
    },
    { field: "anno_fiscal", headerName: "Año", width: 70 },
  ];

  if (cargando)
    return (
      <Box display="flex" justifyContent="center" mt={6}>
        <CircularProgress />
      </Box>
    );
  if (error) return <Alert severity="error">{error}</Alert>;
  if (!articulo) return null;

  return (
    <Grid container spacing={gridSpacing}>
      <Grid item xs={12}>
        <Button
          startIcon={<IconArrowLeft size={16} />}
          onClick={() => router.push("/inventario/articulos")}
          sx={{ mb: 1 }}
        >
          Volver al catálogo
        </Button>
        <MainCard
          title={
            <Box display="flex" alignItems="center" gap={1}>
              <IconPackages size={20} />
              <span>
                {articulo.codigo_articulo} — {articulo.nombre}
              </span>
            </Box>
          }
        >
          {/* Información del artículo */}
          <Paper variant="outlined" sx={{ p: 2, mb: 3 }}>
            <Grid container spacing={2}>
              <Grid item xs={12} md={6}>
                <InfoRow label="Código" value={articulo.codigo_articulo} />
                <InfoRow label="Nombre" value={articulo.nombre} />
                <InfoRow
                  label="Descripción"
                  value={articulo.descripcion_extendida || "—"}
                />
                <InfoRow
                  label="Cuenta Contable"
                  value={articulo.codigo_cuenta}
                />
                <InfoRow label="Unidad de Medida" value={articulo.unidad_medida || "—"} />
                <InfoRow label="Código de Barras" value={articulo.codigo_barras || "—"} />
              </Grid>
              <Grid item xs={12} md={6}>
                <InfoRow
                  label="Existencia Actual"
                  value={
                    <strong>
                      {fmt(articulo.existencia_actual)} {articulo.unidad_medida}
                    </strong>
                  }
                />
                <InfoRow
                  label="Costo Unitario Actual"
                  value={fmtMoneda(articulo.costo_actual)}
                />
                <InfoRow
                  label="Valor Total"
                  value={<strong>{fmtMoneda(articulo.valor_total)}</strong>}
                />
                <InfoRow label="Stock Mínimo" value={fmt(articulo.stock_minimo)} />
                <InfoRow label="Stock Máximo" value={fmt(articulo.stock_maximo)} />
                <InfoRow label="Año Fiscal" value={articulo.anno_fiscal} />
                <InfoRow
                  label="Estado"
                  value={
                    <Chip
                      size="small"
                      label={articulo.activo ? "Activo" : "Inactivo"}
                      color={articulo.activo ? "success" : "default"}
                    />
                  }
                />
              </Grid>
            </Grid>
          </Paper>

          <Divider sx={{ mb: 2 }} />
          <Box
            display="flex"
            justifyContent="space-between"
            alignItems="center"
            mb={2}
          >
            <Typography variant="h5">Kardex de Movimientos</Typography>
            <FormControl size="small" sx={{ minWidth: 140 }}>
              <InputLabel>Año Kardex</InputLabel>
              <Select
                value={annoKardex}
                label="Año Kardex"
                onChange={(e) => setAnnoKardex(e.target.value as number | "")}
              >
                <MenuItem value="">Todos</MenuItem>
                {ANNOS.map((a) => (
                  <MenuItem key={a} value={a}>
                    {a}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Box>

          <Box sx={{ height: 400, width: "100%" }}>
            <DataGrid
              rows={kardex}
              columns={columnasKardex}
              loading={cargandoKardex}
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
    </Grid>
  );
}
