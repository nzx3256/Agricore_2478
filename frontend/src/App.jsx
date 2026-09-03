import { Container, Typography, Box } from '@mui/material'
import AppHeader from './components/layout/AppHeader.jsx'

import EquipmentDataGrid from './components/equipment/EquipmentDataGrid.jsx'
import DiscrepancyDataGrid from './components/jobs/DiscrepancyDataGrid.jsx'

import LoginForm from './components/auth/LoginForm.jsx';
import { AuthProvider, useAuth } from './context/AuthContext.jsx'

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
        <Typography variant="h6" component="h2" color='secondary' gutterBottom>
          Equipment:
        </Typography>
        <Box sx={{ mb: 4 }}>
          <EquipmentDataGrid />
        </Box>
        <Typography variant="h6" component="h2" color='secondary' gutterBottom>
          Co-Location Discrepancies:
        </Typography>
        <Box sx={{ mb: 4 }}>
          <DiscrepancyDataGrid />
        </Box>
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

