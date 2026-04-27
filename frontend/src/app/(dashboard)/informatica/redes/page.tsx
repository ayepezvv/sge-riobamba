'use client';

import { useState, useEffect } from 'react';
import {
    Grid,
    Typography,
    Button,
    Chip,
    Dialog,
    DialogTitle,
    DialogContent,
    DialogActions,
    TextField,
    Stack,
    IconButton,
    Tooltip,
    Box,
    CardActionArea
} from '@mui/material';
import MainCard from 'ui-component/cards/MainCard';
import AnimateButton from 'ui-component/extended/AnimateButton';
import { listarSegmentos, crearSegmento, listarIpsPorSegmento, crearIp, eliminarIp } from 'api/informatica';
import { listarPersonalAdministrativo } from 'api/administrativo';
import { listarActivos } from 'api/bodega';
import { useSnackbar } from 'notistack';
import { DataGrid, GridColDef } from '@mui/x-data-grid';
import { IconDeviceDesktop, IconServer, IconRouter, IconPlus, IconTrash } from '@tabler/icons-react';
import { useFormik } from 'formik';
import * as yup from 'yup';

// Tipos
interface SegmentoRed {
    id: string;
    nombre: string;
    red_cidr: string;
    descripcion?: string;
    is_active: boolean;
}

interface DireccionIpAsignada {
    id: string;
    segmento_id: string;
    direccion_ip: string;
    mac_address?: string;
    nombre_equipo?: string;
    dominio?: string;
    ubicacion_geografica?: string;
    personal_id?: number | null;
    personal?: {
        id: number;
        nombres: string;
        apellidos: string;
        cargo: string;
    };
    is_active: boolean;
}

interface Personal {
    id: number;
    nombres: string;
    apellidos: string;
    cargo: string;
}

interface ActivoFijo {
    id: number;
    codigo_inventario: string;
    nombre: string;
    marca: string;
    modelo: string;
}

const IpamRedesPage = () => {
    const { enqueueSnackbar } = useSnackbar();
    const [segmentos, setSegmentos] = useState<SegmentoRed[]>([]);
    const [ips, setIps] = useState<DireccionIpAsignada[]>([]);
    const [selectedSegmento, setSelectedSegmento] = useState<SegmentoRed | null>(null);
    const [openIpModal, setOpenIpModal] = useState(false);
    const [openSegModal, setOpenSegModal] = useState(false);
    const [isLoading, setIsLoading] = useState(false);
    const [personalList, setPersonalList] = useState<Personal[]>([]);
    const [activosList, setActivosList] = useState<ActivoFijo[]>([]);

    // Fetch Segmentos
    const fetchSegmentos = async () => {
        try {
            const data = await listarSegmentos();
            setSegmentos(data);
        } catch (error) {
            console.error(error);
            enqueueSnackbar('Error al cargar segmentos de red', { variant: 'error' });
        }
    };

    // Fetch IPs del segmento
    const fetchIps = async (segmentoId: string) => {
        setIsLoading(true);
        try {
            const data = await listarIpsPorSegmento(Number(segmentoId));
            setIps(data);
        } catch (error) {
            console.error(error);
            enqueueSnackbar('Error al cargar IPs asignadas', { variant: 'error' });
        } finally {
            setIsLoading(false);
        }
    };

    const fetchPersonal = async () => {
        try {
            const data = await listarPersonalAdministrativo();
            setPersonalList(data);
        } catch (error) {
            console.error('Error al cargar personal', error);
        }
    };

    const fetchActivos = async () => {
        try {
            const data = await listarActivos();
            setActivosList(data);
        } catch (error) {
            console.error('Error al cargar activos', error);
        }
    };

    useEffect(() => {
        fetchSegmentos();
        fetchPersonal();
        fetchActivos();
    }, []);

    const handleSelectSegmento = (seg: SegmentoRed) => {
        setSelectedSegmento(seg);
        fetchIps(seg.id);
    };

    // MAC Validation Regex
    const macRegex = /^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$/;
    // IP Validation Regex
    const ipRegex = /^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$/;

    const formikIp = useFormik({
        initialValues: {
            direccion_ip: '',
            mac_address: '',
            nombre_equipo: '',
            dominio: '',
            ubicacion_geografica: '',
            personal_id: '' as number | '',
            activo_id: '' as number | ''
        },
        validationSchema: yup.object().shape({
            direccion_ip: yup.string().matches(ipRegex, 'Formato IPv4 inválido').required('La IP es obligatoria'),
            mac_address: yup.string().matches(macRegex, 'Formato MAC inválido (ej: 00:1A:2B:3C:4D:5E)').nullable(),
            nombre_equipo: yup.string().nullable(),
            dominio: yup.string().nullable(),
            ubicacion_geografica: yup.string().nullable(),
            personal_id: yup.number().nullable(),
            activo_id: yup.number().nullable()
        }),
        onSubmit: async (values, { resetForm }) => {
            if (!selectedSegmento) return;
            try {
                await crearIp({
                    ...values,
                    personal_id: values.personal_id === '' ? null : values.personal_id,
                    activo_id: values.activo_id === '' ? null : values.activo_id,
                    segmento_id: selectedSegmento.id,
                    is_active: true
                });
                enqueueSnackbar('IP asignada correctamente', { variant: 'success' });
                fetchIps(selectedSegmento.id);
                setOpenIpModal(false);
                resetForm();
            } catch (error: any) {
                const detail = error.response?.data?.detail;
                const mensajeError = Array.isArray(detail) ? detail.map((e: any) => e.msg).join(', ') : (detail || 'Error al asignar IP');
                enqueueSnackbar(mensajeError, { variant: 'error' });
                console.error("Detalle del fallo:", error);
            }
        }
    });

    const formikSeg = useFormik({
        initialValues: {
            nombre: '',
            red_cidr: '',
            descripcion: ''
        },
        validationSchema: yup.object().shape({
            nombre: yup.string().required('El nombre es obligatorio'),
            red_cidr: yup.string().required('El CIDR es obligatorio (Ej: 192.168.1.0/24)'),
            descripcion: yup.string().nullable(),
        }),
        onSubmit: async (values, { resetForm }) => {
            try {
                await crearSegmento(values);
                enqueueSnackbar('Segmento creado con éxito', { variant: 'success' });
                fetchSegmentos();
                setOpenSegModal(false);
                resetForm();
            } catch (error: any) {
                const detail = error.response?.data?.detail;
                const mensajeError = Array.isArray(detail) ? detail.map((e: any) => e.msg).join(', ') : (detail || 'Error al crear segmento');
                enqueueSnackbar(mensajeError, { variant: 'error' });
                console.error("Detalle del fallo:", error);
            }
        }
    });

    const deleteIp = async (id: string) => {
        if (!window.confirm("¿Seguro que desea eliminar esta asignación de IP?")) return;
        try {
            await eliminarIp(Number(id));
            enqueueSnackbar('Asignación eliminada', { variant: 'success' });
            if (selectedSegmento) fetchIps(selectedSegmento.id);
        } catch (err) {
            enqueueSnackbar('Error eliminando IP', { variant: 'error' });
        }
    }

    const columns: GridColDef[] = [
        {
            field: 'nombre_equipo',
            headerName: 'Equipo',
            width: 200,
            renderCell: (params) => {
                const icon = params.value?.toLowerCase().includes('server') ? <IconServer size={18} /> :
                    params.value?.toLowerCase().includes('router') ? <IconRouter size={18} /> :
                        <IconDeviceDesktop size={18} />;
                return (
                    <Box display="flex" alignItems="center" gap={1}>
                        {icon}
                        <Typography variant="body2">{params.value || 'Desconocido'}</Typography>
                    </Box>
                );
            }
        },
        {
            field: 'direccion_ip', headerName: 'Direccion IPv4', width: 150,
            renderCell: (params) => <Typography sx={{ fontFamily: 'monospace', fontWeight: 'bold' }}>{params.value}</Typography>
        },
        { field: 'mac_address', headerName: 'MAC Address', width: 150 },
        {
            field: 'dominio',
            headerName: 'Dominio / Red',
            width: 150,
            renderCell: (params) => {
                const val = params.value;
                const color = val?.toLowerCase().includes('local') ? 'success' :
                    val?.toLowerCase().includes('dmz') ? 'error' : 'primary';
                return val ? <Chip label={val} color={color} size="small" variant="outlined" /> : <span>-</span>;
            }
        },
        {
            field: 'activo',
            headerName: 'Equipo / Bien Físico',
            width: 200,
            renderCell: (params) => {
                const a = params.value;
                return a ? (
                    <Box display="flex" flexDirection="column" justifyContent="center">
                        <Typography variant="body2" sx={{ fontWeight: 500 }}>{a.codigo_inventario} - {a.nombre}</Typography>
                        <Typography variant="caption" color="textSecondary">{a.marca} {a.modelo}</Typography>
                    </Box>
                ) : <Typography variant="caption" sx={{ fontStyle: 'italic', color: 'text.secondary' }}>Ninguno</Typography>;
            }
        },
        { field: 'ubicacion_geografica', headerName: 'Úbicación (Rack/Piso)', width: 220 },
        {
            field: 'personal',
            headerName: 'Responsable',
            width: 250,
            renderCell: (params) => {
                const p = params.value;
                return p ? (
                    <Box display="flex" flexDirection="column" justifyContent="center">
                        <Typography variant="body2" sx={{ fontWeight: 500 }}>{p.nombres} {p.apellidos}</Typography>
                        <Typography variant="caption" color="textSecondary">{p.cargo}</Typography>
                    </Box>
                ) : <Typography variant="caption" sx={{ fontStyle: 'italic', color: 'text.secondary' }}>Sin asignar</Typography>;
            }
        },
        {
            field: 'actions',
            headerName: 'Acciones',
            width: 100,
            renderCell: (params) => (
                <Tooltip title="Eliminar Asignación">
                    <IconButton color="error" onClick={() => deleteIp(params.row.id)}>
                        <IconTrash size={18} />
                    </IconButton>
                </Tooltip>
            )
        }
    ];

    return (
        <Grid container spacing={3}>
            {/* MASTER: Segmentos */}
            <Grid size={{ xs: 12, md: selectedSegmento ? 3 : 12 }}>
                <MainCard title="Infraestructura: VLANs y Subredes" secondary={
                    <AnimateButton>
                        <Button variant="contained" size="small" startIcon={<IconPlus />} onClick={() => setOpenSegModal(true)}>
                            Nueva Subred
                        </Button>
                    </AnimateButton>
                }>
                    <Grid container spacing={2}>
                        {segmentos.map(seg => (
                            <Grid size={{ xs: 12, sm: selectedSegmento ? 12 : 6, md: selectedSegmento ? 12 : 4 }} key={seg.id}>
                                <MainCard content={false} sx={{ border: selectedSegmento?.id === seg.id ? '2px solid' : '1px solid', borderColor: selectedSegmento?.id === seg.id ? 'primary.main' : 'divider', transition: 'all .2s ease-in-out' }}>
                                    <CardActionArea onClick={() => handleSelectSegmento(seg)} sx={{ p: 2 }}>
                                        <Typography variant="h5" sx={{ mb: 1, display: 'flex', alignItems: 'center', gap: 1 }}>
                                            <IconRouter size={22} color="#1565C0" /> {seg.nombre}
                                        </Typography>
                                        <Chip label={seg.red_cidr} size="small" color="primary" sx={{ fontFamily: 'monospace', fontWeight: 600, mb: 1 }} />
                                        <Typography variant="body2" color="textSecondary">{seg.descripcion}</Typography>
                                    </CardActionArea>
                                </MainCard>
                            </Grid>
                        ))}
                    </Grid>
                </MainCard>
            </Grid>

            {/* DETAIL: IPs del segmento seleccionado */}
            {selectedSegmento && (
                <Grid size={{ xs: 12, md: 9 }}>
                    <MainCard title={`IPs Asignadas: ${selectedSegmento.nombre}`} secondary={
                        <AnimateButton>
                            <Button variant="contained" color="secondary" size="small" startIcon={<IconPlus />} onClick={() => setOpenIpModal(true)}>
                                Asignar IP
                            </Button>
                        </AnimateButton>
                    }>
                        <Box sx={{ height: 600, width: '100%' }}>
                            <DataGrid
                                rows={ips}
                                columns={columns}
                                loading={isLoading}
                                disableRowSelectionOnClick
                                initialState={{
                                    pagination: { paginationModel: { pageSize: 15 } }
                                }}
                                pageSizeOptions={[15, 25, 50]}
                            />
                        </Box>
                    </MainCard>
                </Grid>
            )}

            {/* Modal Nueva IP */}
            <Dialog open={openIpModal} onClose={() => setOpenIpModal(false)} maxWidth="sm" fullWidth>
                <DialogTitle>Asignar Nueva Dirección IP</DialogTitle>
                <form onSubmit={formikIp.handleSubmit}>
                    <DialogContent>
                        <Stack spacing={2}>
                            <TextField
                                fullWidth label="Dirección IPv4" name="direccion_ip"
                                value={formikIp.values.direccion_ip} onChange={formikIp.handleChange}
                                error={formikIp.touched.direccion_ip && Boolean(formikIp.errors.direccion_ip)}
                                helperText={formikIp.touched.direccion_ip && formikIp.errors.direccion_ip}
                                placeholder="Ej. 192.168.1.50"
                            />
                            <TextField
                                fullWidth label="MAC Address" name="mac_address"
                                value={formikIp.values.mac_address} onChange={formikIp.handleChange}
                                error={formikIp.touched.mac_address && Boolean(formikIp.errors.mac_address)}
                                helperText={formikIp.touched.mac_address && formikIp.errors.mac_address}
                                placeholder="Ej. AA:BB:CC:DD:EE:FF"
                            />
                            <TextField
                                fullWidth label="Nombre del Equipo" name="nombre_equipo"
                                value={formikIp.values.nombre_equipo} onChange={formikIp.handleChange}
                                placeholder="Ej. SRV-DATABASE-01"
                            />
                            <TextField
                                fullWidth label="Dominio / Contexto" name="dominio"
                                value={formikIp.values.dominio} onChange={formikIp.handleChange}
                                placeholder="Ej. DMZ Públicos / riobamba.local"
                            />
                            <TextField
                                fullWidth label="Ubicación Física" name="ubicacion_geografica"
                                value={formikIp.values.ubicacion_geografica} onChange={formikIp.handleChange}
                                placeholder="Ej. Rack 4 - Unidad de Catastro"
                            />
                            <TextField
                                select
                                fullWidth label="Funcionario Responsable (Opcional)" name="personal_id"
                                value={formikIp.values.personal_id} onChange={formikIp.handleChange}
                                SelectProps={{ native: true }}
                            >
                                <option value="">--- Sin Asignar ---</option>
                                {personalList.map(p => (
                                    <option key={p.id} value={p.id}>{p.nombres} {p.apellidos} - {p.cargo}</option>
                                ))}
                            </TextField>
                            <TextField
                                select
                                fullWidth label="Vincular con Activo Fijo (Bodega)" name="activo_id"
                                value={formikIp.values.activo_id} onChange={formikIp.handleChange}
                                SelectProps={{ native: true }}
                            >
                                <option value="">--- Sin Vincular ---</option>
                                {activosList.map(a => (
                                    <option key={a.id} value={a.id}>[{a.codigo_inventario}] {a.nombre} - {a.marca}</option>
                                ))}
                            </TextField>
                        </Stack>
                    </DialogContent>
                    <DialogActions>
                        <Button onClick={() => setOpenIpModal(false)} color="error">Cancelar</Button>
                        <Button type="submit" variant="contained" color="primary">Asignar IP</Button>
                    </DialogActions>
                </form>
            </Dialog>

            {/* Modal Nuevo Segmento */}
            <Dialog open={openSegModal} onClose={() => setOpenSegModal(false)} maxWidth="xs" fullWidth>
                <DialogTitle>Crear Subred / VLAN</DialogTitle>
                <form onSubmit={formikSeg.handleSubmit}>
                    <DialogContent>
                        <Stack spacing={2}>
                            <TextField
                                fullWidth label="Nombre / VLAN" name="nombre"
                                value={formikSeg.values.nombre} onChange={formikSeg.handleChange}
                                error={formikSeg.touched.nombre && Boolean(formikSeg.errors.nombre)}
                                helperText={formikSeg.touched.nombre && formikSeg.errors.nombre}
                            />
                            <TextField
                                fullWidth label="Bloque CIDR" name="red_cidr"
                                value={formikSeg.values.red_cidr} onChange={formikSeg.handleChange}
                                error={formikSeg.touched.red_cidr && Boolean(formikSeg.errors.red_cidr)}
                                helperText={formikSeg.touched.red_cidr && formikSeg.errors.red_cidr}
                                placeholder="Ej. 192.168.10.0/24"
                            />
                            <TextField
                                fullWidth label="Descripción" name="descripcion"
                                value={formikSeg.values.descripcion} onChange={formikSeg.handleChange}
                            />
                        </Stack>
                    </DialogContent>
                    <DialogActions>
                        <Button onClick={() => setOpenSegModal(false)} color="error">Cancelar</Button>
                        <Button type="submit" variant="contained" color="primary">Guardar</Button>
                    </DialogActions>
                </form>
            </Dialog>
        </Grid>
    );
};

export default IpamRedesPage;
