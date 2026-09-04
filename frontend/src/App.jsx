import { Container, Typography, Box } from '@mui/material'
import AppHeader from './components/layout/AppHeader.jsx'

import LoginForm from './components/auth/LoginForm.jsx';
import { AuthProvider, useAuth } from './context/AuthContext.jsx'

import FieldJobDataGrid from './components/jobs/FieldJobDataGrid.jsx';
import EquipmentDataGrid from './components/equipment/EquipmentDataGrid.jsx'
import DiscrepancyDataGrid from './components/jobs/DiscrepancyDataGrid.jsx'
import FarmerDataGrid from './components/farmers/FarmerDataGrid.jsx';
import ReliabilityDataGrid from './components/equipment/ReliabilityDataGrid.jsx';
import EquipmentList from './components/equipment/EquipmentList.jsx';

function Dashboard() {
    const { user, logout } = useAuth()
    return (
        <>
            <AppHeader username={user?.sub} role={user?.role} onLogout={logout} />
            <Container maxWidth='lg' sx={{ mt: 4, justifyContent: 'flex-start' }}>
                <Typography variant='h4' color='primary' component='h2' gutterBottom>
                    Overview
                </Typography>
                <br />
                <EquipmentList />
                < br />
                <DiscrepancyDataGrid />
                < br />
                {/*TODO: Add reliability metrics */}
                < ReliabilityDataGrid />
                <br />
                {/*TODO: Add Maintenance Flags Card List */}
                <br />
                {/*TODO: Add Reporting Lines Card list */}
                <FarmerDataGrid />
                <EquipmentDataGrid />
                <FieldJobDataGrid />
            </Container>
        </>
    );
}

function AppContent() {
    const { isAuthenticated } = useAuth();
    return isAuthenticated ? <Dashboard /> : <LoginForm />;
}

function App() {
    return (
        <AuthProvider>
            <AppContent />
        </AuthProvider>
    );
}

export default App;

