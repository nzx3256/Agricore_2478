import { Button, TextField, Box, Alert, Grid, Typography } from '@mui/material';
import EquipmentCard from './EquipmentCard.jsx';
import { useState, useEffect } from 'react';
import apiClient from '../../api/client.js';

function EquipmentList() {
    const [equipment, setEquipment] = useState([]);
    const [error, setError] = useState(null);
    const [threshold, setThreshold] = useState(100.0);

    async function handleSearch() {
        setError(null);
        setEquipment([])
        try {
            const response = await apiClient.get("/equipment",
                {
                    params: { low_fuel_threshold: threshold },
                }
            );
            setEquipment(response.data);
        }
        catch { setError("Couldn't fetch the Equipment data"); }
    }
    let populateXML;
    if (error) {
        populateXML = <Alert severity='error'>{error}</Alert>;
    }
    else {
        populateXML = (
            <Grid container spacing={2}>
                {equipment.map((equ) => (
                    <Grid key={equ.id}>
                        <EquipmentCard equipment={equ} />
                    </Grid>
                ))}
            </Grid>
        );
    }
    return (
        <>
            <Typography variant="body1" component="span" color='secondary' sx={{ display: 'flex' }} gutterBottom>
                Fuel Level Alerts:
            </Typography>
            <Box sx={{ display: 'flex', gap: 2, mb: 2 }}>
                <TextField
                    label="<= Fuel Threshold"
                    value={threshold}
                    sx={{ width: 200 }}
                    type="number"
                    slotProps={{
                        htmlInput: { min: 0, max: 100 }
                    }}
                    onChange={(event) => setThreshold(event.target.value)}
                />
                <Button variant="outlined" onClick={handleSearch}>Lookup</Button>
            </Box>
            {populateXML}
        </>
    );
}

export default EquipmentList;
