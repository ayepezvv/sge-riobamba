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
            <Grid size={12}>
                <Typography variant="h2" sx={{ mb: 3 }}>Panel de Gestión de Talento Humano</Typography>
            </Grid>
            <Grid size={12}>
                <Grid container spacing={gridSpacing}>
                    <Grid size={{ xs: 12, sm: 6, md: 6, lg: 4 }}>
                        <TotalIncomeDarkCard 
                            isLoading={isLoading} 
                            title="Total Empleados"
                            icon={<IconUsers />}
                            count="245"
                        />
                    </Grid>
                    <Grid size={{ xs: 12, sm: 6, md: 6, lg: 4 }}>
                        <TotalIncomeLightCard 
                            isLoading={isLoading} 
                            title="Masa Salarial Mensual"
                            icon={<IconReportMoney />}
                            count="$185,420.00"
                        />
                    </Grid>
                    <Grid size={{ xs: 12, sm: 12, md: 12, lg: 4 }}>
                        <TotalIncomeDarkCard 
                            isLoading={isLoading} 
                            title="Contratos por Vencer"
                            icon={<IconCalendarStats />}
                            count="12"
                        />
                    </Grid>
                </Grid>
            </Grid>
            <Grid size={12}>
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
