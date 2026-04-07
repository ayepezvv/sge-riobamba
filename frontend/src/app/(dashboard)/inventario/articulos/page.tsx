"use client";

import { useEffect, useState, useCallback } from "react";
import {
  Grid, Box, Button, Chip, CircularProgress, Alert,
  TextField, MenuItem, FormControl, InputLabel, Select,
  IconButton, Tooltip,
} from "@mui/material";
import { DataGrid, GridColDef, GridToolbar } from "@mui/x-data-grid";
import { IconSearch, IconEye, IconRefresh } from "@tabler/icons-react";
import { useRouter } from "next/navigation";
import MainCard from "ui-component/cards/MainCard";
import { gridSpacing } from "store/constant";
import { listarArticulos } from "api/inventario";
import { ArticuloListado } from "types/inventario";

const ANNOS = [2021, 2022, 2023, 2024, 2025];

const formatMoneda = (val?: number) =>
  val != null
    ? `$${Number(val).toLocaleString("es-EC", { minimumFractionDigits: 2 })}`
    : "—";

export default function ArticulosPage() {
  const router = useRouter();
  const [articulos, setArticulos] = useState<ArticuloListado[]>([]);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [anno, setAnno] = useState<number | "">(2025);
  const [buscar, setBuscar] = useState("");
  const [soloActivos, setSoloActivos] = useState<"" | "true" | "false">("");

  const cargar = useCallback(async () => {
    setCargando(true);
    setError(null);
    try {
      const data = await listarArticulos({
        anno: anno !== "" ? anno : undefined,
        buscar: buscar.trim() || undefined,
        activo: soloActivos !== "" ? soloActivos === "true" : undefined,
        limit: 500,
      });
      setArticulos(data);
    } catch (e: any) {
      setError(e?.message || "Error al cargar artículos");
    } finally {
      setCargando(false);
    }
  }, [anno, buscar, soloActivos]);

  useEffect(() => { cargar(); }, [cargar]);

  const columnas: GridColDef[] = [
    { field: "codigo_articulo", headerName: "Código", width: 110 },
    { field: "nombre", headerName: "Artículo / Insumo", flex: 1, minWidth: 200 },
    { field: "unidad_medida", headerName: "U/M", width: 80 },
    {
      field: "existencia_actual",
      headerName: "Existencia",
      width: 110,
      type: "number",
      valueFormatter: (v) => v != null ? Number(v).toLocaleString("es-EC") : "—",
    },
    {
      field: "costo_actual",
      headerName: "Costo Unit.",
      width: 120,
      type: "number",
      valueFormatter: (v) => formatMoneda(v as number),
    },
    {
      field: "valor_total",
      headerName: "Valor Total",
      width: 130,
      type: "number",
      valueFormatter: (v) => formatMoneda(v as number),
    },
    { field: "codigo_cuenta", headerName: "Cuenta Contable", width: 150 },
    { field: "anno_fiscal", headerName: "Año", width: 70 },
    {
      field: "activo",
      headerName: "Estado",
      width: 90,
      renderCell: (p) => (
        <Chip
          size="small"
          label={p.value ? "Activo" : "Inactivo"}
          color={p.value ? "success" : "default"}
        />
      ),
    },
    {
      field: "acciones",
      headerName: "Kardex",
      width: 80,
      sortable: false,
      renderCell: (p) => (
        <Tooltip title="Ver kardex">
          <IconButton
            size="small"
            color="primary"
            onClick={() => router.push(`/inventario/articulos/${p.row.id}`)}
          >
            <IconEye size={18} />
          </IconButton>
        </Tooltip>
      ),
    },
  ];

  return (
    <Grid container spacing={gridSpacing}>
      <Grid item xs={12}>
        <MainCard title="Catálogo de Artículos / Insumos de Bodega">
          {/* Filtros */}
          <Grid container spacing={2} mb={2}>
            <Grid item xs={12} sm={3}>
              <FormControl fullWidth size="small">
                <InputLabel>Año Fiscal</InputLabel>
                <Select
                  value={anno}
                  label="Año Fiscal"
                  onChange={(e) => setAnno(e.target.value as number | "")}
                >
                  <MenuItem value="">Todos los años</MenuItem>
                  {ANNOS.map((a) => (
                    <MenuItem key={a} value={a}>
                      {a}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} sm={3}>
              <FormControl fullWidth size="small">
                <InputLabel>Estado</InputLabel>
                <Select
                  value={soloActivos}
                  label="Estado"
                  onChange={(e) =>
                    setSoloActivos(e.target.value as "" | "true" | "false")
                  }
                >
                  <MenuItem value="">Todos</MenuItem>
                  <MenuItem value="true">Solo Activos</MenuItem>
                  <MenuItem value="false">Solo Inactivos</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} sm={4}>
              <TextField
                fullWidth
                size="small"
                label="Buscar por nombre o código"
                value={buscar}
                onChange={(e) => setBuscar(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && cargar()}
                InputProps={{
                  endAdornment: (
                    <IconButton size="small" onClick={cargar}>
                      <IconSearch size={18} />
                    </IconButton>
                  ),
                }}
              />
            </Grid>
            <Grid item xs={12} sm={2}>
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
              rows={articulos}
              columns={columnas}
              loading={cargando}
              slots={{ toolbar: GridToolbar }}
              slotProps={{
                toolbar: { showQuickFilter: true },
              }}
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
