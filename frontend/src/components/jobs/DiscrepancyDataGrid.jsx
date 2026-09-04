import { useEffect, userState, useState } from 'react';
import { DataGrid } from '@mui/x-data-grid';
import {
    Alert, Box, CircularProgress, FormControl,
    InputLabel, MenuItem, Select, Typography
} from '@mui/material';
import apiClient from '../../api/client.js';

const columns = [
    { field: 'job_id', headerName: 'Job ID', width: 110 },
    { field: 'job_title', headerName: 'Title', width: 220 },
    { field: 'equipment_farm_id', headerName: 'Equipment Farm', width: 140, type: 'number' },
    { field: 'farmer_farm_id', headerName: 'Field Hand\'s Farm', width: 150, type: 'number' },
];

const PRIORITY_OPTIONS = ['', 'Low', 'Medium', 'Critical'];

function DiscrepancyDataGrid() {
    const [priority, setPriority] = useState('');
    const [discrepancies, setDiscrepancies] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        let isMounted = true
        setLoading(true);

        async function fetchDiscrepancies() {
            try {
                const response = await apiClient.get('/jobs/discrepencies', {
                    params: { priority: priority || undefined }
                });
                if (isMounted) setDiscrepancies(response.data);
            }
            catch {
                if (isMounted) setError("Could not load Discrepancies report");
            }
            finally {
                if (isMounted) setLoading(false);
            }
        }
        fetchDiscrepancies();

        return () => {
            isMounted = false;
        }
    }, [priority]);

    return (
        <Box>
            <>
                <Typography variant="h6" component="h2" color='secondary' gutterBottom>
                    Co-Location Discrepancies:
                </Typography>
                <FormControl size='small' sx={{ mb: 2, minWidth: 100 }}>
                    <InputLabel id='priority-filter-label'>Priority</InputLabel>
                    <Select
                        labelId='priority-filter-label'
                        label='priority'
                        value={priority}
                        onChange={(event) => setPriority(event.target.value)}
                    >
                        {PRIORITY_OPTIONS.map((option) => (
                            <MenuItem key={option || 'All'} value={option}>
                                {option === '' ? 'All' : option}
                            </MenuItem>
                        ))}
                    </Select>
                </FormControl>
                {loading && <CircularProgress />}
                {error && <Alert severity='error'>{error}</Alert>}
                {!loading && !error && (
                    <Box sx={{ height: 400, width: '100%' }}>
                        <DataGrid
                            rows={discrepancies}
                            columns={columns}
                            getRowId={(row) => row.job_id}
                        />
                    </Box>
                )}
            </>
        </Box>
    );
}

export default DiscrepancyDataGrid;
