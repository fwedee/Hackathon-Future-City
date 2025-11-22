import React, { useEffect, useState } from 'react';
import {
    Box,
    Button,
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
    Stack
} from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';
import EditIcon from '@mui/icons-material/Edit';
import AddIcon from '@mui/icons-material/Add';
import VisibilityIcon from '@mui/icons-material/Visibility';
import { useNavigate } from 'react-router-dom';
import { fetchJobs, deleteJob, type Job } from '../services/api';
import dayjs from 'dayjs';

const JobsPage: React.FC = () => {
    const navigate = useNavigate();
    const [jobs, setJobs] = useState<Job[]>([]);

    useEffect(() => {
        loadJobs();
    }, []);

    const loadJobs = async () => {
        try {
            const data = await fetchJobs();
            setJobs(data);
        } catch (error) {
            console.error("Failed to load jobs", error);
        }
    };

    const handleDelete = async (jobId: string) => {
        if (window.confirm("Are you sure you want to delete this job?")) {
            try {
                await deleteJob(jobId);
                loadJobs(); // Refresh list
            } catch (error) {
                console.error("Failed to delete job", error);
            }
        }
    };

    return (
        <Box sx={{ p: 4, maxWidth: 1200, mx: 'auto' }}>
            <Stack direction="row" justifyContent="space-between" alignItems="center" mb={4}>
                <Typography variant="h4" sx={{ color: 'var(--primary)', fontWeight: 'bold' }}>
                    Jobs Management
                </Typography>
                <Button
                    variant="contained"
                    startIcon={<AddIcon />}
                    onClick={() => navigate('/job/create')}
                    sx={{
                        backgroundColor: 'var(--primary)',
                        color: 'var(--bg-dark)',
                        '&:hover': { backgroundColor: 'var(--secondary)' }
                    }}
                >
                    Create New Job
                </Button>
            </Stack>

            <TableContainer component={Paper} sx={{ backgroundColor: 'var(--bg-light)', border: '1px solid var(--border)' }}>
                <Table>
                    <TableHead>
                        <TableRow>
                            <TableCell sx={{ color: 'var(--text-muted)' }}>Location</TableCell>
                            <TableCell sx={{ color: 'var(--text-muted)' }}>Start Date</TableCell>
                            <TableCell sx={{ color: 'var(--text-muted)' }}>End Date</TableCell>
                            <TableCell sx={{ color: 'var(--text-muted)' }}>Roles</TableCell>
                            <TableCell sx={{ color: 'var(--text-muted)' }}>Items</TableCell>
                            <TableCell align="right" sx={{ color: 'var(--text-muted)' }}>Actions</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {jobs.map((job) => (
                            <TableRow key={job.job_id} sx={{ '&:last-child td, &:last-child th': { border: 0 } }}>
                                <TableCell sx={{ color: 'var(--text)' }}>
                                    {job.street} {job.house_number}, {job.city}
                                </TableCell>
                                <TableCell sx={{ color: 'var(--text)' }}>
                                    {job.start_datetime ? dayjs(job.start_datetime).format('DD/MM/YYYY HH:mm') : 'N/A'}
                                </TableCell>
                                <TableCell sx={{ color: 'var(--text)' }}>
                                    {job.end_datetime ? dayjs(job.end_datetime).format('DD/MM/YYYY HH:mm') : 'N/A'}
                                </TableCell>
                                <TableCell>
                                    <Stack direction="row" spacing={1}>
                                        {job.roles.map(role => (
                                            <Chip key={role.role_id} label={role.role_name} size="small" sx={{ backgroundColor: 'var(--highlight)', color: 'var(--text)' }} />
                                        ))}
                                    </Stack>
                                </TableCell>
                                <TableCell>
                                    <Stack direction="row" spacing={1}>
                                        {job.item_links && job.item_links.map(link => (
                                            <Chip
                                                key={link.item_id}
                                                label={`${link.item.item_name}${link.required_quantity > 1 ? ` (x${link.required_quantity})` : ''}`}
                                                size="small"
                                                variant="outlined"
                                                sx={{ color: 'var(--text)', borderColor: 'var(--border)' }}
                                            />
                                        ))}
                                    </Stack>
                                </TableCell>
                                <TableCell align="right">
                                    <IconButton onClick={() => navigate(`/jobs/${job.job_id}`)} sx={{ color: 'var(--text)' }} title="View Details">
                                        <VisibilityIcon />
                                    </IconButton>
                                    <IconButton onClick={() => navigate(`/jobs/${job.job_id}/update`)} sx={{ color: 'var(--primary)' }} title="Edit">
                                        <EditIcon />
                                    </IconButton>
                                    <IconButton onClick={() => handleDelete(job.job_id)} sx={{ color: 'var(--error)' }} title="Delete">
                                        <DeleteIcon />
                                    </IconButton>
                                </TableCell>
                            </TableRow>
                        ))}
                        {jobs.length === 0 && (
                            <TableRow>
                                <TableCell colSpan={5} align="center" sx={{ py: 4, color: 'var(--text-muted)' }}>
                                    No jobs found. Create one to get started.
                                </TableCell>
                            </TableRow>
                        )}
                    </TableBody>
                </Table>
            </TableContainer>
        </Box>
    );
};

export default JobsPage;
