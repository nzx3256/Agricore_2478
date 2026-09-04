import { Card, CardContent, Typography, Chip, Stack } from '@mui/material'

const LOW_BATTERY_THRESHOLD = 20;

function RobotCard({ equipment }) {
    const isLowFuel = equipment.fuel_level < LOW_BATTERY_THRESHOLD;
    return (
        <Card variant='outlined' sx={{ minWidth: 240 }}>
            <CardContent>
                <Typography variant='h6' component='div'>
                    {equipment.serialNumber}
                </Typography>
                <Typography color='text.secondary' gutterBottom>
                    {equipment.model}
                </Typography>
                <Stack direction='row' spacing={1} sx={{ alignItems: 'center' }}>
                    <Chip
                        label={`Fuel: ${equipment.fuel_level}`}
                        color={isLowFuel ? 'error' : 'success'}
                        size='small'
                    />
                    <Chip label={equipment.status} variant='outlined' size='small' />
                </Stack>
            </CardContent>
        </Card>
    );
}

export default RobotCard;
