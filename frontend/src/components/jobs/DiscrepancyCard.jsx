import { Alert, Card, CardContent, Typography, Stack } from '@mui/material';

function DiscrepancyCard({ discrepancy }) {
    return (
        <Card variant='h6' sx={{ minWidth: 280 }}>
            <CardContent>
                <Typography variant='h6' component='div'>
                    {discrepancy.title}
                </Typography>
                <Typography color='text.secondary' gutterBottom>
                    Field Job #{discrepancy.jobId}
                </Typography>
                <Stack spacing={0.5} sx={{ mb: 1.5 }}>
                    <Typography>
                        Equipment Farm: {discrepancy.equipmentFarmId}
                    </Typography>
                    <Typography>
                        Field Hands Farm: {discrepancy.operatorFarmId}
                    </Typography>
                </Stack>
                <Alert severity='warning'>Farm Mismatch Detected</Alert>
            </CardContent>
        </Card>
    );
}

export default DiscrepancyCard;
