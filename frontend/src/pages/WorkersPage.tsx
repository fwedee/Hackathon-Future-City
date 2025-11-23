import React, { useEffect, useState } from 'react';
import {
    Box,
    Typography,
    Paper,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    IconButton,
    Chip,
    Stack,
    Breadcrumbs,
    Link
} from '@mui/material';
import VisibilityIcon from '@mui/icons-material/Visibility';
import NavigateNextIcon from '@mui/icons-material/NavigateNext';
import { useNavigate, Link as RouterLink } from 'react-router-dom';
import { fetchWorkers, type Worker } from '../services/api';

const WorkersPage: React.FC = () => {
    const navigate = useNavigate();
    const [workers, setWorkers] = useState<Worker[]>([]);

    useEffect(() => {
        loadWorkers();
    }, []);

    const loadWorkers = async () => {
        try {
            const data = await fetchWorkers();
            setWorkers(data);
        } catch (error) {
            console.error("Failed to load workers", error);
        }
    };

    return (
        <Box sx={{ p: { xs: 2, md: 4 }, maxWidth: 1200, mx: 'auto' }}>
            {/* Breadcrumbs */}
            <Breadcrumbs separator={<NavigateNextIcon fontSize="small" sx={{ color: '#60A5FA' }} />} aria-label="breadcrumb" sx={{ mb: 3 }}>
                <Link component={RouterLink} to="/" underline="hover" sx={{ color: '#60A5FA' }}>
                    Home
                </Link>
                <Typography sx={{ color: '#60A5FA' }}>Workers</Typography>
            </Breadcrumbs>

            <Stack direction="row" justifyContent="space-between" alignItems="center" mb={4}>
                <Typography variant="h3" sx={{ fontWeight: 'bold', color: 'var(--text)', fontSize: { xs: '2rem', md: '3rem' } }}>
                    Workers Management
                </Typography>
            </Stack>

            <TableContainer component={Paper} sx={{ backgroundColor: 'var(--bg-light)', border: '1px solid var(--border)' }}>
                <Table>
                    <TableHead>
                        <TableRow>
                            <TableCell sx={{ color: 'var(--text-muted)' }}>Name</TableCell>
                            <TableCell sx={{ color: 'var(--text-muted)' }}>Phone</TableCell>
                            <TableCell sx={{ color: 'var(--text-muted)' }}>Branch</TableCell>
                            <TableCell sx={{ color: 'var(--text-muted)' }}>Roles</TableCell>
                            <TableCell align="right" sx={{ color: 'var(--text-muted)' }}>Actions</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {workers.map((worker) => {
                            const workerName = `${worker.worker_first_name || ''} ${worker.worker_last_name || ''}`.trim() || 'N/A';
                            return (
                                <TableRow key={worker.worker_id} sx={{ '&:last-child td, &:last-child th': { border: 0 } }}>
                                    <TableCell sx={{ color: 'var(--text)' }}>
                                        {workerName}
                                    </TableCell>
                                    <TableCell sx={{ color: 'var(--text)' }}>
                                        {worker.worker_phone_number || 'N/A'}
                                    </TableCell>
                                    <TableCell sx={{ color: 'var(--text)' }}>
                                        {worker.branch?.branch_name || 'No branch'}
                                    </TableCell>
                                    <TableCell>
                                        <Stack direction="row" spacing={1}>
                                            {worker.roles && worker.roles.map(role => (
                                                <Chip 
                                                    key={role.role_id} 
                                                    label={role.role_name} 
                                                    size="small" 
                                                    sx={{ backgroundColor: 'var(--highlight)', color: 'var(--text)' }} 
                                                />
                                            ))}
                                        </Stack>
                                    </TableCell>
                                    <TableCell align="right">
                                        <IconButton onClick={() => navigate(`/workers/${worker.worker_id}`)} sx={{ color: 'var(--text-muted)' }} title="View Details">
                                            <VisibilityIcon />
                                        </IconButton>
                                    </TableCell>
                                </TableRow>
                            );
                        })}
                        {workers.length === 0 && (
                            <TableRow>
                                <TableCell colSpan={5} align="center" sx={{ py: 4, color: 'var(--text-muted)' }}>
                                    No workers found.
                                </TableCell>
                            </TableRow>
                        )}
                    </TableBody>
                </Table>
            </TableContainer>
        </Box>
    );
};

export default WorkersPage;
