"use client";

import { useEffect, useState } from "react";
import {
  Grid, Typography, Card, CardContent, Box,
  CircularProgress, Alert, Chip,
} from "@mui/material";
import {
  IconPackages, IconArrowDown, IconArrowUp, IconList,
} from "@tabler/icons-react";
import MainCard from "ui-component/cards/MainCard";
import { gridSpacing } from "store/constant";
import { obtenerResumen } from "api/inventario";
import { ResumenAnualInventario } from "types/inventario";

const formatMoneda = (val?: number) =>
  val != null
    ? `$${Number(val).toLocaleString("es-EC", { minimumFractionDigits: 2 })}`
    : "—";

const ResumenCard = ({
  anno,
  total_articulos,
  total_movimientos,
  total_lineas_kardex,
  valor_inventario_total,
}: ResumenAnualInventario) => (
  <Card variant="outlined" sx={{ height: "100%" }}>
    <CardContent>
      <Box
        display="flex"
        justifyContent="space-between"
        alignItems="center"
        mb={1}
      >
        <Typography variant="h4" color="primary">
          Año {anno}
        </Typography>
        <Chip
          label={anno === 2025 ? "Actual" : String(anno)}
          color={anno === 2025 ? "success" : "default"}
          size="small"
        />
      </Box>
      <Box display="flex" alignItems="center" gap={1} mb={0.5}>
        <IconPackages size={16} />
        <Typography variant="body2">
          <strong>{total_articulos.toLocaleString("es-EC")}</strong> artículos
        </Typography>
      </Box>
      <Box display="flex" alignItems="center" gap={1} mb={0.5}>
        <IconList size={16} />
        <Typography variant="body2">
          <strong>{total_movimientos.toLocaleString("es-EC")}</strong> movimientos
        </Typography>
      </Box>
      <Box display="flex" alignItems="center" gap={1} mb={0.5}>
        <IconArrowDown size={16} style={{ color: "#2e7d32" }} />
        <IconArrowUp size={16} style={{ color: "#c62828" }} />
        <Typography variant="body2">
          <strong>{total_lineas_kardex.toLocaleString("es-EC")}</strong> líneas kardex
        </Typography>
      </Box>
      <Typography variant="h5" color="secondary" mt={1}>
        {formatMoneda(valor_inventario_total)}
      </Typography>
      <Typography variant="caption" color="text.secondary">
        Valor total inventario
      </Typography>
    </CardContent>
  </Card>
);

export default function InventarioDashboard() {
  const [resumen, setResumen] = useState<ResumenAnualInventario[]>([]);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setCargando(true);
    obtenerResumen()
      .then(setResumen)
      .catch((e) => setError(e?.message || "Error al cargar resumen"))
      .finally(() => setCargando(false));
  }, []);

  if (cargando)
    return (
      <Box display="flex" justifyContent="center" mt={6}>
        <CircularProgress />
      </Box>
    );
  if (error) return <Alert severity="error">{error}</Alert>;

  const actual = resumen.find((r) => r.anno_fiscal === 2025);

  return (
    <Grid container spacing={gridSpacing}>
      <Grid size={12}>
        <MainCard title="Inventario / Existencias — Resumen Anual 2021–2025">
          <Grid container spacing={2}>
            {resumen.map((r) => (
              <Grid size={{ xs: 12, sm: 6, md: 4, lg: 2.4 }} key={r.anno_fiscal}>
                <ResumenCard {...r} />
              </Grid>
            ))}
          </Grid>
          {actual && (
            <Box mt={3} p={2} bgcolor="primary.light" borderRadius={2}>
              <Typography variant="h4" color="primary.dark">
                Inventario Vigente (2025)
              </Typography>
              <Typography variant="body1" mt={1}>
                <strong>{actual.total_articulos.toLocaleString("es-EC")}</strong> artículos
                activos &mdash; valor total:{" "}
                <strong>{formatMoneda(actual.valor_inventario_total)}</strong> &mdash;{" "}
                <strong>{actual.total_movimientos.toLocaleString("es-EC")}</strong> movimientos
                registrados
              </Typography>
            </Box>
          )}
        </MainCard>
      </Grid>
    </Grid>
  );
}
