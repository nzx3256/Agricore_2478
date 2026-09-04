import { Tab, Paper } from '@mui/material'
import { TabContext, TabList, TabPanel } from '@mui/lab'
import { useState } from 'react'
import { useAuth } from '../../context/AuthContext.jsx';

import ReliabilityDataGrid from '../equipment/ReliabilityDataGrid';
import EquipmentList from '../equipment/EquipmentList';
import FarmerDataGrid from '../farmers/FarmerDataGrid';
import FarmDataGrid from '../farms/FarmDataGrid';
import DiscrepancyDataGrid from '../jobs/DiscrepancyDataGrid.jsx';
import MaintenanceFlagsDataGrid from '../farms/MaintenanceFlagsDataGrid.jsx';
import ReportingLinesDataGrid from '../farms/ReportingLinesDataGrid.jsx';
import FieldJobDataGrid from '../jobs/FieldJobDataGrid.jsx';
import EquipmentDataGrid from '../equipment/EquipmentDataGrid.jsx';
import { FrontHand, SupervisorAccount } from '@mui/icons-material';


function ApiTab() {
    const { user } = useAuth();
    const [tab, setTab] = useState('read')
    const handleChange = (event, newValue) => {
        setTab(newValue)
    }
    const writeable = new Set(['Farm Operations Admin', 'Field Hand']);
    let canWrite = false;
    canWrite = writeable.has(user?.role);
    let isAdmin = false;
    isAdmin = (user?.role == 'Farm Operations Admin')
    return (
        <>
            <TabContext value={tab}>
                <Paper variant='outlined' square={true} sx={{ borderBottom: 1, display: 'flex' }}>
                    <TabList aria-label='API Tabs' centered onChange={handleChange}>
                        <Tab label='METRICS' value='metrics' color='black' />
                        <Tab label='READ' value='read' color='black' />
                        <Tab label='POST/PATCH' value='post'
                            icon={<FrontHand />}
                            iconPosition='start'
                            color={canWrite ? 'black' : 'grey'}
                            disabled={!canWrite}
                        />
                        <Tab label='AUTH' value='auth'
                            icon={<SupervisorAccount />}
                            iconPosition='start'
                            color={isAdmin ? 'black' : 'grey'}
                            disabled={!isAdmin}
                        />
                    </TabList>
                </Paper>
                <TabPanel value='metrics'>
                    <br />
                    <EquipmentList />
                    <br />
                    <DiscrepancyDataGrid />
                    <br />
                    <ReliabilityDataGrid />
                    <br />
                    <MaintenanceFlagsDataGrid />
                    <br />
                    <ReportingLinesDataGrid />
                </TabPanel>
                <TabPanel value='read'>
                    <FarmerDataGrid />
                    <br />
                    <FarmDataGrid />
                    <br />
                    <EquipmentDataGrid />
                    <br />
                    <FieldJobDataGrid />
                </TabPanel>
                <TabPanel value='post'>
                </TabPanel>
                <TabPanel value='auth'>
                </TabPanel>

            </TabContext>
        </>
    );
}
export default ApiTab;
