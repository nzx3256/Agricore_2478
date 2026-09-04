import { useEffect, useState } from 'react';
import { DataGrid } from '@mui/x-data-grid';
import { Alert, Box, CircularProgress, Button, Dialog, DialogActions, DialogContent, DialogTitle, MenuItem, Stack, TextField, Typography } from '@mui/material';
import apiClient from '../../api/client.js';

const columns = [
    { field: 'id', headerName: 'ID', width: 70 },
    { field: 'name', headerName: 'Farm Name', width: 150 },
    { field: 'location_region', headerName: 'Location Region', width: 280 },
    { field: 'capacity', headerName: 'Max Capacity', width: 120, type: 'number' },
    { field: 'supervisor_id', headerName: 'Supervisor ID', width: 110, type: 'number' },
];

function FarmDataGrid() {
    const [farms, setFarms] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    useEffect(() => {
        let isMounted = true
        async function fetchFarms() {
            setLoading(true);
            setError(null);
            try {
                const response = await apiClient.get('/farms');
                if (isMounted) setFarms(response.data);
            } catch {
                if (isMounted) setError('Could not load Farm data.');
            } finally {
                if (isMounted) setLoading(false);
            }
        }

        fetchFarms();

        return () => {
            isMounted = false;
        }
    }, []);

    if (loading) return <CircularProgress />;
    if (error) return <Alert severity="error">{error}</Alert>;

    return (
        <Box sx={{ height: 400, width: '100%' }}>
            <Typography variant="h6" component="h2" color='secondary' gutterBottom>
                Farms:
            </Typography>
            <DataGrid rows={farms} columns={columns} getRowId={(row) => row.id} />
        </Box>
    );
}

export default FarmDataGrid;
