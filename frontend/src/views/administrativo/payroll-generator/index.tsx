import { useState } from 'react';
import { 
    Box, 
    Stepper, 
    Step, 
    StepLabel, 
    Button, 
    Typography, 
    Grid, 
    FormControl, 
    InputLabel, 
    Select, 
    MenuItem,
    Alert
} from '@mui/material';
import { IconReceipt2, IconChessFilled, IconCircleCheck } from '@tabler/icons-react';

// project imports
import MainCard from 'ui-component/cards/MainCard';

const steps = ['Selección de Mes/Año', 'Revisión de Novedades', 'Emisión de Roles'];

const PayrollGenerator = () => {
    const [activeStep, setActiveStep] = useState(0);
    const [periodo, setPeriodo] = useState({ mes: '', anio: '2026' });

    const handleNext = () => {
        setActiveStep((prevActiveStep) => prevActiveStep + 1);
    };

    const handleBack = () => {
        setActiveStep((prevActiveStep) => prevActiveStep - 1);
    };

    const handleReset = () => {
        setActiveStep(0);
    };

    const getStepContent = (step: number) => {
        switch (step) {
            case 0:
                return (
                    <Grid container spacing={3} sx={{ mt: 2 }}>
                        <Grid size={{ xs: 12, md: 6 }}>
                            <FormControl fullWidth>
                                <InputLabel>Mes</InputLabel>
                                <Select
                                    value={periodo.mes}
                                    label="Mes"
                                    onChange={(e) => setPeriodo({ ...periodo, mes: e.target.value })}
                                >
                                    <MenuItem value={1}>Enero</MenuItem>
                                    <MenuItem value={2}>Febrero</MenuItem>
                                    <MenuItem value={3}>Marzo</MenuItem>
                                    <MenuItem value={4}>Abril</MenuItem>
                                </Select>
                            </FormControl>
                        </Grid>
                        <Grid size={{ xs: 12, md: 6 }}>
                            <FormControl fullWidth>
                                <InputLabel>Año</InputLabel>
                                <Select
                                    value={periodo.anio}
                                    label="Año"
                                    onChange={(e) => setPeriodo({ ...periodo, anio: e.target.value })}
                                >
                                    <MenuItem value="2025">2025</MenuItem>
                                    <MenuItem value="2026">2026</MenuItem>
                                </Select>
                            </FormControl>
                        </Grid>
                    </Grid>
                );
            case 1:
                return (
                    <Box sx={{ mt: 2 }}>
                        <Alert severity="info" sx={{ mb: 2 }}>
                            Se han detectado 5 novedades pendientes (Horas Extras, Atrasos) para el período seleccionado.
                        </Alert>
                        <Typography variant="body1">
                            Listado de novedades cargadas desde el reloj biométrico y registros manuales...
                        </Typography>
                        {/* Aquí iría una pequeña tabla de novedades */}
                    </Box>
                );
            case 2:
                return (
                    <Box sx={{ mt: 2, textAlign: 'center' }}>
                        <IconChessFilled size="3rem" color="#673ab7" />
                        <Typography variant="h4" sx={{ mt: 2 }}>Listo para Procesar</Typography>
                        <Typography variant="body2" sx={{ mt: 1 }}>
                            Se generarán los roles de pago para 245 empleados activos.
                        </Typography>
                    </Box>
                );
            default:
                return 'Unknown step';
        }
    };

    return (
        <MainCard 
            title="Asistente de Generación de Nómina"
            secondary={<IconReceipt2 stroke={1.5} size="1.5rem" />}
        >
            <Stepper activeStep={activeStep}>
                {steps.map((label) => (
                    <Step key={label}>
                        <StepLabel>{label}</StepLabel>
                    </Step>
                ))}
            </Stepper>
            
            <Box sx={{ p: 3 }}>
                {activeStep === steps.length ? (
                    <Box sx={{ textAlign: 'center' }}>
                        <IconCircleCheck size="4rem" color="#4caf50" />
                        <Typography variant="h3" sx={{ mt: 2 }}>¡Nómina Generada Exitosamente!</Typography>
                        <Typography variant="body1" sx={{ mt: 1 }}>
                            Los roles de pago han sido guardados en estado 'BORRADOR'.
                        </Typography>
                        <Button onClick={handleReset} sx={{ mt: 2 }} variant="contained" color="secondary">
                            Generar Nueva
                        </Button>
                    </Box>
                ) : (
                    <div>
                        {getStepContent(activeStep)}
                        <Box sx={{ display: 'flex', flexDirection: 'row', pt: 4 }}>
                            <Button
                                color="inherit"
                                disabled={activeStep === 0}
                                onClick={handleBack}
                                sx={{ mr: 1 }}
                            >
                                Atrás
                            </Button>
                            <Box sx={{ flex: '1 1 auto' }} />
                            <Button onClick={handleNext} variant="contained" color="primary">
                                {activeStep === steps.length - 1 ? 'Finalizar y Generar' : 'Siguiente'}
                            </Button>
                        </Box>
                    </div>
                )}
            </Box>
        </MainCard>
    );
};

export default PayrollGenerator;
