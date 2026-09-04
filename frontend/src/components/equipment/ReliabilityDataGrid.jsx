import { useEffect, useState } from "react";
import { DataGrid } from "@mui/x-data-grid";
import { Alert, Box, CircularProgress, Typography } from '@mui/material';
import apiClient from '../../api/client.js';

const columns = [
    { field: 'equipment_id', headerName: 'Equipment ID', width: 70 },
    { field: 'equipment_model', headerName: 'Model', width: 200 },
    { field: 'completed_failed_ratio', headerName: 'Reliability (Completed:Failed)', width: 240 },
];

function ReliabilityDataGrid() {
    const [metrics, setMetrics] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        let isMounted = true;
        //setError(null);
        //setLoading(true);

        async function fetchMetrics() {
            try {
                let response = await apiClient.get("/equipment/reliability_metrics");
                if (isMounted) setMetrics(response.data);
            } catch {
                if (isMounted) setError("Could not fetch Reliability Metrics");
            } finally {
                if (isMounted) setLoading(false);
            }
        }

        fetchMetrics();

        return () => {
            isMounted = false;
        };
    }, []);

    if (loading) return <CircularProgress />
    if (error) return <Alert severity='error'>{error}</Alert>

    return (
        <>
            <Typography variant="h6" component="h2" color='secondary' gutterBottom>
                Reliability Metrics:
            </Typography>
            <Box sx={{ mb: 4, height: 400, width: '100%' }}>
                <DataGrid
                    rows={metrics}
                    columns={columns}
                    getRowId={(row) => row.equipment_id}
                />
            </Box>
        </>
    );
}

export default ReliabilityDataGrid;
