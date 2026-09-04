import { useEffect, useState } from 'react';
import { DataGrid } from '@mui/x-data-grid';
import { Alert, Box, CircularProgress, Typography, TextField, Button } from '@mui/material';
import apiClient from '../../api/client.js';

const columns = [
    { field: 'farm_id', headerName: 'Farm ID', width: 70 },
    { field: 'farm_name', headerName: 'Farm Name', width: 180 },
    { field: 'percent_maintenance', headerName: 'Maintenance %', width: 230 },
];

function MaintenanceFlagsDataGrid() {
    const [flags, setFlags] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [threshold, setThreshold] = useState(0.0);

    async function handleSearch() {
        setLoading(true);
        setError(null);
        try {
            const response = await apiClient.get('/farms/maintenance_flags',
                { params: { threshold: threshold } });
            setFlags(response.data);
        } catch {
            setError('Could not load metric data (Maintenance Flags).');
        } finally {
            setLoading(false);
        }
    }

    return (
        <Box sx={{ height: 400, width: '100%' }} >
            <Typography variant="h6" component="h2" color='secondary' gutterBottom>
                Maintenance Flags:
            </Typography>
            <Box sx={{ display: 'flex', gap: 2, mb: 2 }}>
                <TextField
                    label=">=Maintenance Threshold"
                    value={threshold}
                    type="number"
                    sx={{ width: 200 }}
                    slotProps={{
                        htmlInput: { min: 0, max: 100 }
                    }}
                    onChange={(event) => setThreshold(event.target.value)}
                />
                <Button variant="outlined" onClick={handleSearch}>Lookup</Button>
            </Box >
            {!loading && !error && <DataGrid rows={flags} columns={columns} getRowId={(row) => row.farm_id} />}
            {loading && !error && <CircularProgress />}
            {error && <Alert severity="error">{error}</Alert>}
        </Box>
    );
}

export default MaintenanceFlagsDataGrid;
