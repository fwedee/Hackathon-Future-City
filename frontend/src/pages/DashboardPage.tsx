import React, { useState, useEffect } from 'react';
import { Link as RouterLink } from 'react-router-dom';
import { fetchJobs, fetchWorkers, type Job, type Worker } from '../services/api';
import dayjs from 'dayjs';
import {
    Box,
    Grid,
    Paper,
    Typography,
    TextField,
    Button,
    List,
    ListItem,
    ListItemText,
    ListItemIcon,
    Chip,
    Divider,
    Link,
} from '@mui/material';
import {
    LocalShipping,
    AccessTime,
    CheckCircle,
    Send,
    AutoAwesome,
    Timeline,
    TrendingUp,
} from '@mui/icons-material';
import OperationsMap from '../components/OperationsMap';

const Dashboard: React.FC = () => {
    const [aiInput, setAiInput] = useState('');
    const [jobs, setJobs] = useState<Job[]>([]);
    const [workers, setWorkers] = useState<Worker[]>([]);

    useEffect(() => {
        const loadData = async () => {
            try {
                const [jobsData, workersData] = await Promise.all([
                    fetchJobs(),
                    fetchWorkers()
                ]);
                setJobs(jobsData);
                setWorkers(workersData);
            } catch (error) {
                console.error("Failed to load dashboard data", error);
            }
        };
        loadData();
    }, []);

    const handleAiSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        console.log('AI Command:', aiInput);
        setAiInput('');
        // In a real app, this would trigger an API call
    };

    // Filter and sort upcoming jobs
    const upcomingJobs = jobs
        .filter(job => job.start_datetime && dayjs(job.start_datetime).isAfter(dayjs()))
        .sort((a, b) => dayjs(a.start_datetime).diff(dayjs(b.start_datetime)))
        .slice(0, 3);

    return (
        <Box sx={{ flexGrow: 1, p: 3, color: 'var(--text)' }}>
            <Box sx={{ mb: 4, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <Typography variant="h4" component="h1" sx={{ fontWeight: 'bold', color: 'var(--text)' }}>
                    Smart Logistics Dashboard
                </Typography>
                <Chip
                    icon={<AutoAwesome />}
                    label="AI Optimization Active"
                    sx={{
                        bgcolor: 'var(--secondary)',
                        color: 'var(--bg-dark)',
                        fontWeight: 'bold'
                    }}
                />
            </Box>

            {/* Stats Cards */}
            <Grid container spacing={3} sx={{ mb: 4 }}>
                {[
                    { title: 'Active Fleet', value: `${workers.length}/15`, icon: <LocalShipping />, color: 'var(--primary)' },
                    { title: 'On-Time Rate', value: '98.5%', icon: <CheckCircle />, color: 'var(--success)' },
                    { title: 'Pending Jobs', value: `${jobs.length}`, icon: <AccessTime />, color: 'var(--warning)' },
                    { title: 'Fuel Efficiency', value: '+12%', icon: <TrendingUp />, color: 'var(--info)' },
                ].map((stat, index) => (
                    <Grid size={{ xs: 12, sm: 6, md: 3 }} key={index}>
                        <Paper
                            elevation={0}
                            sx={{
                                p: 2,
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'space-between',
                                bgcolor: 'var(--bg-light)',
                                border: '1px solid var(--border)',
                                borderRadius: 2,
                            }}
                        >
                            <Box>
                                <Typography variant="body2" sx={{ color: 'var(--text-muted)' }}>
                                    {stat.title}
                                </Typography>
                                <Typography variant="h5" sx={{ fontWeight: 'bold', color: 'var(--text)' }}>
                                    {stat.value}
                                </Typography>
                            </Box>
                            <Box sx={{
                                p: 1,
                                borderRadius: '50%',
                                bgcolor: `${stat.color}20`,
                                color: stat.color,
                                display: 'flex'
                            }}>
                                {stat.icon}
                            </Box>
                        </Paper>
                    </Grid>
                ))}
            </Grid>

            <Grid container spacing={3}>
                {/* Left Column */}
                <Grid size={{ xs: 12, md: 8 }}>
                    {/* Map Section */}
                    <Paper
                        elevation={0}
                        sx={{
                            p: 0,
                            mb: 3,
                            height: 400,
                            bgcolor: 'var(--bg-light)',
                            border: '1px solid var(--border)',
                            borderRadius: 2,
                            overflow: 'hidden',
                        }}
                    >
                        <OperationsMap jobs={jobs} />
                    </Paper>

                    {/* Upcoming Schedule */}
                    <Paper
                        elevation={0}
                        sx={{
                            p: 3,
                            bgcolor: 'var(--bg-light)',
                            border: '1px solid var(--border)',
                            borderRadius: 2,
                        }}
                    >
                        <Typography variant="h6" sx={{ mb: 2, color: 'var(--text)' }}>
                            Upcoming Schedule
                        </Typography>
                        <List>
                            {upcomingJobs.length > 0 ? (
                                upcomingJobs.map((job, index) => (
                                    <React.Fragment key={job.job_id}>
                                        <ListItem alignItems="flex-start" sx={{ px: 0 }}>
                                            <ListItemText
                                                primary={
                                                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                                                        <Typography variant="subtitle1" sx={{ fontWeight: 'bold', color: 'var(--text)', minWidth: '60px' }}>
                                                            {dayjs(job.start_datetime).format('HH:mm')}
                                                        </Typography>
                                                        <Link component={RouterLink} to={`/jobs/${job.job_id}`} underline="hover" sx={{ color: 'var(--text)', fontWeight: 500 }}>
                                                            {job.job_name || 'Unnamed Job'}
                                                        </Link>
                                                    </Box>
                                                }
                                                secondary={
                                                    <Box sx={{ ml: '76px', mt: 0.5 }}>
                                                        <Typography variant="caption" sx={{ color: 'var(--text-muted)', display: 'block' }}>
                                                            {job.workers && job.workers.length > 0
                                                                ? `Assigned: ${job.workers.map(w => `${w.worker_first_name || ''} ${w.worker_last_name || ''}`.trim() || 'Worker').join(', ')}`
                                                                : 'Unassigned'}
                                                        </Typography>
                                                    </Box>
                                                }
                                            />
                                        </ListItem>
                                        {index < upcomingJobs.length - 1 && <Divider component="li" sx={{ borderColor: 'var(--border-muted)' }} />}
                                    </React.Fragment>
                                ))
                            ) : (
                                <Typography variant="body2" sx={{ color: 'var(--text-muted)', fontStyle: 'italic' }}>
                                    No upcoming jobs scheduled.
                                </Typography>
                            )}
                        </List>
                    </Paper>
                </Grid>

                {/* Right Column */}
                <Grid size={{ xs: 12, md: 4 }}>
                    {/* Quick Action AI */}
                    <Paper
                        elevation={0}
                        sx={{
                            p: 3,
                            mb: 3,
                            bgcolor: 'var(--bg-light)',
                            border: '1px solid var(--border)',
                            borderRadius: 2,
                            background: 'linear-gradient(145deg, var(--bg-light) 0%, rgba(66, 153, 225, 0.05) 100%)'
                        }}
                    >
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 2 }}>
                            <AutoAwesome sx={{ color: 'var(--secondary)' }} />
                            <Typography variant="h6" sx={{ color: 'var(--text)' }}>
                                AI Assistant
                            </Typography>
                        </Box>
                        <Typography variant="body2" sx={{ mb: 2, color: 'var(--text-muted)' }}>
                            Type a command to quickly create jobs or query data.
                        </Typography>
                        <form onSubmit={handleAiSubmit}>
                            <TextField
                                fullWidth
                                variant="outlined"
                                placeholder="e.g., 'Schedule 50 boxes to Main St tomorrow'"
                                value={aiInput}
                                onChange={(e) => setAiInput(e.target.value)}
                                sx={{
                                    mb: 1,
                                    '& .MuiOutlinedInput-root': {
                                        color: 'var(--text)',
                                        bgcolor: 'var(--bg)',
                                        '& fieldset': { borderColor: 'var(--border)' },
                                        '&:hover fieldset': { borderColor: 'var(--highlight)' },
                                        '&.Mui-focused fieldset': { borderColor: 'var(--primary)' },
                                    },
                                }}
                            />
                            <Button
                                fullWidth
                                variant="contained"
                                type="submit"
                                endIcon={<Send />}
                                sx={{
                                    bgcolor: 'var(--primary)',
                                    color: 'var(--bg-dark)',
                                    '&:hover': { bgcolor: 'var(--highlight)' }
                                }}
                            >
                                Process
                            </Button>
                        </form>
                    </Paper>

                    {/* Route Optimization */}
                    <Paper
                        elevation={0}
                        sx={{
                            p: 3,
                            mb: 3,
                            bgcolor: 'var(--bg-light)',
                            border: '1px solid var(--border)',
                            borderRadius: 2,
                        }}
                    >
                        <Typography variant="h6" sx={{ mb: 2, color: 'var(--text)' }}>
                            Smart Optimizations
                        </Typography>
                        <List dense>
                            {[
                                { text: 'Merge Route A & B to save 15km', impact: 'High', color: 'var(--success)' },
                                { text: 'Reassign Job #123 to Worker John', impact: 'Medium', color: 'var(--secondary)' },
                                { text: 'Delay Job #456 by 30m to avoid traffic', impact: 'Low', color: 'var(--info)' },
                            ].map((opt, index) => (
                                <ListItem key={index} sx={{
                                    mb: 1,
                                    bgcolor: 'var(--bg)',
                                    borderRadius: 1,
                                    border: '1px solid var(--border-muted)'
                                }}>
                                    <ListItemIcon sx={{ minWidth: 36 }}>
                                        <Timeline sx={{ color: opt.color }} />
                                    </ListItemIcon>
                                    <ListItemText
                                        primary={opt.text}
                                        primaryTypographyProps={{ variant: 'body2', color: 'var(--text)' }}
                                    />
                                </ListItem>
                            ))}
                        </List>
                    </Paper>

                    {/* Recent Activity */}
                    <Paper
                        elevation={0}
                        sx={{
                            p: 3,
                            bgcolor: 'var(--bg-light)',
                            border: '1px solid var(--border)',
                            borderRadius: 2,
                        }}
                    >
                        <Typography variant="h6" sx={{ mb: 2, color: 'var(--text)' }}>
                            Recent Activity
                        </Typography>
                        <List dense>
                            {[
                                { text: 'Job #992 completed by Sarah', time: '10m ago' },
                                { text: 'New route calculated for Fleet 1', time: '25m ago' },
                                { text: 'System alert: Heavy traffic on I-95', time: '1h ago' },
                            ].map((activity, index) => (
                                <ListItem key={index} disableGutters>
                                    <ListItemText
                                        primary={activity.text}
                                        secondary={activity.time}
                                        primaryTypographyProps={{ variant: 'body2', color: 'var(--text)' }}
                                        secondaryTypographyProps={{ variant: 'caption', color: 'var(--text-muted)' }}
                                    />
                                </ListItem>
                            ))}
                        </List>
                    </Paper>
                </Grid>
            </Grid>
        </Box>
    );
};

export default Dashboard;
