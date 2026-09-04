import { useEffect, useState } from 'react';
import { DataGrid } from '@mui/x-data-grid';
import { Alert, Box, CircularProgress, Typography, TextField, Button } from '@mui/material';
import apiClient from '../../api/client.js';

const columns = [
    { field: 'farmer_id', headerName: 'Field Hand ID', width: 70 },
    { field: 'farmers_name', headerName: 'Name', width: 180 },
    { field: 'active_jobs', headerName: 'Active Jobs', width: 160, type: 'number' },
    { field: 'supervisor_id', headerName: 'Supervisor ID', width: 180, type: 'number' },
];

function ReportingLinesDataGrid() {
    const [results, setResults] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [supervisorId, setSupervisorId] = useState(1);

    async function handleSearch() {
        setLoading(true);
        setError(null);
        try {
            const response = await apiClient.get('/farms/reporting_lines',
                { params: { supervisor_id: supervisorId } });
            setResults(response.data);
        } catch {
            setError('Could not load metric data (Reporting Lines).');
        } finally {
            setLoading(false);
        }
    }


    return (
        <Box sx={{ height: 400, width: '100%' }}>
            <Typography variant="h6" component="h2" color='secondary' gutterBottom>
                Reporting Lines:
            </Typography>
            <Box sx={{ display: 'flex', gap: 2, mb: 2 }}>
                <TextField
                    label="Supervisor ID"
                    value={supervisorId}
                    sx={{ width: 200 }}
                    type="number"
                    onChange={(event) => setSupervisorId(event.target.value)}
                />
                <Button variant="outlined" onClick={handleSearch}>Lookup</Button>
            </Box >
            {!loading && !error && <DataGrid rows={results} columns={columns} getRowId={(row) => row.farmer_id} />}
            {loading && !error && <CircularProgress />}
            {error && <Alert severity="error">{error}</Alert>}
        </Box>
    );
}

export default ReportingLinesDataGrid;
