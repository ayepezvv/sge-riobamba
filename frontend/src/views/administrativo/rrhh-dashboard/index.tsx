import React, { useEffect, useState } from 'react';
import { Grid, Typography } from '@mui/material';
import { useTheme } from '@mui/material/styles';
import { 
    IconUsers, 
    IconCurrentLocation, 
    IconReportMoney, 
    IconUserPlus,
    IconCalendarStats
} from '@tabler/icons-react';

// project imports
import MainCard from 'ui-component/cards/MainCard';
import TotalIncomeDarkCard from 'ui-component/cards/TotalIncomeDarkCard';
import TotalIncomeLightCard from 'ui-component/cards/TotalIncomeLightCard';
import { gridSpacing } from 'store/constant';

// ==============================|| RRHH DASHBOARD ||============================== //

const RRHHDashboard = () => {
    const theme = useTheme();
    const [isLoading, setLoading] = useState(true);

    useEffect(() => {
        setLoading(false);
    }, []);

    return (
        <Grid container spacing={gridSpacing}>
            <Grid item xs={12}>
                <Typography variant="h2" sx={{ mb: 3 }}>Panel de Gestión de Talento Humano</Typography>
            </Grid>
            <Grid item xs={12}>
                <Grid container spacing={gridSpacing}>
                    <Grid item lg={4} md={6} sm={6} xs={12}>
                        <TotalIncomeDarkCard 
                            isLoading={isLoading} 
                            title="Total Empleados"
                            icon={<IconUsers />}
                            count="245"
                        />
                    </Grid>
                    <Grid item lg={4} md={6} sm={6} xs={12}>
                        <TotalIncomeLightCard 
                            isLoading={isLoading} 
                            title="Masa Salarial Mensual"
                            icon={<IconReportMoney />}
                            count="$185,420.00"
                        />
                    </Grid>
                    <Grid item lg={4} md={12} sm={12} xs={12}>
                        <TotalIncomeDarkCard 
                            isLoading={isLoading} 
                            title="Contratos por Vencer"
                            icon={<IconCalendarStats />}
                            count="12"
                        />
                    </Grid>
                </Grid>
            </Grid>
            <Grid item xs={12}>
                <MainCard title="Distribución por Unidades">
                    <Typography variant="body2">
                        Próximamente: Gráficos dinámicos de distribución de personal por direcciones y unidades administrativas.
                    </Typography>
                </MainCard>
            </Grid>
        </Grid>
    );
};

export default RRHHDashboard;
