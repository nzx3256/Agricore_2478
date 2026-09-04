import { Container, Typography, Box } from '@mui/material'
import AppHeader from './components/layout/AppHeader.jsx'

import LoginForm from './components/auth/LoginForm.jsx';
import { AuthProvider, useAuth } from './context/AuthContext.jsx'

// import FieldJobDataGrid from './components/jobs/FieldJobDataGrid.jsx';
// import EquipmentDataGrid from './components/equipment/EquipmentDataGrid.jsx'
// import DiscrepancyDataGrid from './components/jobs/DiscrepancyDataGrid.jsx'
// import FarmerDataGrid from './components/farmers/FarmerDataGrid.jsx';
// import ReportingLinesDataGrid from './components/farms/ReportingLinesDataGrid.jsx';
// import FarmDataGrid from './components/farms/FarmDataGrid.jsx';
// import ReliabilityDataGrid from './components/equipment/ReliabilityDataGrid.jsx';
// import EquipmentList from './components/equipment/EquipmentList.jsx';
// import MaintenanceFlagsDataGrid from './components/farms/MaintenanceFlagsDataGrid.jsx'
import ApiTab from './components/layout/ApiTab.jsx';

function Dashboard() {
    const { user, logout } = useAuth()
    return (
        <>
            <AppHeader username={user?.sub} role={user?.role} onLogout={logout} />
            <Container maxWidth='lg' sx={{ mt: 4, justifyContent: 'flex-start' }}>
                <ApiTab />
                {/*<Typography variant='h4' color='primary' component='h2' gutterBottom>
                    Farm Provisions Overview
                </Typography>
                <br />
                <EquipmentList />
                < br />
                <DiscrepancyDataGrid />
                <br />
                <ReliabilityDataGrid />
                <br />
                <MaintenanceFlagsDataGrid />
                <br />
                <ReportingLinesDataGrid />
                <br />
                <FarmerDataGrid />
                <EquipmentDataGrid />
                <FieldJobDataGrid />*/}
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

