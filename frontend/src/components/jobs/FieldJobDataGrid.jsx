import { useEffect, useState } from 'react';
import { DataGrid } from '@mui/x-data-grid';
import { Alert, Box, CircularProgress, Typography } from '@mui/material';
import apiClient from '../../api/client.js';

//defines our DataGrid columns and maps them to our backend API response data
const columns = [
    { field: 'id', headerName: 'ID', width: 70 },
    { field: 'title', headerName: 'Job Title', width: 150 },
    { field: 'priority', headerName: 'Priority', width: 100 },
    { field: 'status', headerName: 'Status', width: 120 },
    { field: 'equipment_id', headerName: 'Equipment ID', width: 70, type: 'number' },
    { field: 'farmer_id', headerName: 'Field Hand ID', width: 70, type: 'number' },
];

//local state variables for tracking table rows, loading status, and network errors
//to track the lifecycle of the async API request so the UI can render appropriately
function FieldJobDataGrid() {
    const [jobs, setJobs] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        let isMounted = true;

        async function fetchJobs() {
            try {
                let response = await apiClient.get('/jobs');
                if (isMounted) setJobs(response.data);
            } catch {
                if (isMounted) setError('Could not load fleet data.');
            } finally {
                if (isMounted) setLoading(false);
            }
        }

        fetchJobs();

        return () => {
            isMounted = false;
        };
    }, []);

    //shows a spinning progress indicator if loading data
    if (loading) return <CircularProgress />;
    //shows error alert if API call fails
    if (error) return <Alert severity="error">{error}</Alert>;

    //loads data grid component if all goes well
    return (
        <>
            <Typography variant="h6" component="h2" color='secondary' gutterBottom>
                Field Jobs:
            </Typography>
            <Box sx={{ height: 400, width: '100%' }}>
                <DataGrid rows={jobs} columns={columns} />
            </Box>
        </>
    );
}

export default FieldJobDataGrid; 
