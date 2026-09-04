import { useEffect, useState } from 'react';
import { DataGrid } from '@mui/x-data-grid';
import { Alert, Box, CircularProgress, Typography } from '@mui/material';
import apiClient from '../../api/client.js';

const columns = [
    { field: 'id', headerName: 'Field Hand ID', width: 70 },
    { field: 'full_name', headerName: 'Full Name', width: 150 },
    { field: 'farm_id', headerName: 'Farm ID', width: 70, type: 'number' }
];

function FarmerDataGrid() {
    const [farmers, setFarmers] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        let isMounted = true;
        setLoading(true);
        async function fetchFarmers() {
            try {
                let response = await apiClient.get("/farmers");
                if (isMounted) setFarmers(response.data);
            }
            catch {
                if (isMounted) setError("Could not fetch Field Hand data");
            }
            finally {
                if (isMounted) setLoading(false);
            }
        }
        fetchFarmers();
        return () => {
            isMounted = false
        };
    }, []);

    if (loading) return <CircularProgress />;
    if (error) return <Alert severity="error">{error}</Alert>;
    return (
        <>
            <Typography variant="h6" component="h2" color='secondary' gutterBottom>
                Field Hands:
            </Typography>
            <Box sx={{ mb: 4, height: 400, width: '100%' }}>
                <DataGrid
                    rows={farmers}
                    columns={columns}
                    getRowId={(row) => row.id}
                />
            </Box>
        </>
    );
}

export default FarmerDataGrid;
