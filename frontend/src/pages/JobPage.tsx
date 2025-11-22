import React, { useEffect, useState } from 'react';
import { useParams, useNavigate, Link as RouterLink } from 'react-router-dom';
import {
    Box,
    Typography,
    Button,
    Paper,
    Grid,
    Stack,
    Breadcrumbs,
    Link,
    Avatar,
    IconButton,
    List,
    ListItem,
    ListItemText,
    ListItemAvatar,
    Chip,
    Card,
    CardContent,
    CardHeader,
    Divider
} from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import NavigateNextIcon from '@mui/icons-material/NavigateNext';
import ContentCopyIcon from '@mui/icons-material/ContentCopy';
import LocationOnIcon from '@mui/icons-material/LocationOn';
import AccessTimeIcon from '@mui/icons-material/AccessTime';
import BuildIcon from '@mui/icons-material/Build';
import PersonIcon from '@mui/icons-material/Person';
import { fetchJob, deleteJob, type Job } from '../services/api';
import dayjs from 'dayjs';

const JobDetailsPage: React.FC = () => {
    const { id } = useParams<{ id: string }>();
    const navigate = useNavigate();
    const [job, setJob] = useState<Job | null>(null);

    useEffect(() => {
        if (id) {
            loadJob(id);
        }
    }, [id]);

    const loadJob = async (jobId: string) => {
        try {
            const data = await fetchJob(jobId);
            setJob(data);
        } catch (error) {
            console.error("Failed to load job", error);
        }
    };

    const handleDelete = async () => {
        if (id && window.confirm("Are you sure you want to delete this job?")) {
            try {
                await deleteJob(id);
                navigate('/jobs');
            } catch (error) {
                console.error("Failed to delete job", error);
            }
        }
    };

    const handleCopyAddress = () => {
        if (job) {
            const address = `${job.street || ''} ${job.house_number || ''}, ${job.postal_code || ''} ${job.city || ''}, ${job.country || ''}`;
            navigator.clipboard.writeText(address);
        }
    };

    if (!job) return <Box sx={{ p: 4, color: 'var(--text)' }}>Loading...</Box>;

    const address = `${job.street || ''} ${job.house_number || ''}\n${job.postal_code || ''} ${job.city || ''}\n${job.country || ''}`;
    const googleMapsUrl = `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(`${job.street} ${job.house_number}, ${job.city}`)}`;

    // Fallback title if name is missing
    const jobTitle = job.job_name || `Job ${job.job_id.substring(0, 8)}`;

    return (
        <Box sx={{ p: { xs: 2, md: 4 }, maxWidth: 1200, mx: 'auto' }}>
            {/* Breadcrumbs */}
            <Breadcrumbs separator={<NavigateNextIcon fontSize="small" sx={{ color: '#60A5FA' }} />} aria-label="breadcrumb" sx={{ mb: 3 }}>
                <Link component={RouterLink} to="/" underline="hover" sx={{ color: '#60A5FA' }}>
                    Home
                </Link>
                <Link component={RouterLink} to="/jobs" underline="hover" sx={{ color: '#60A5FA' }}>
                    Jobs
                </Link>
                <Typography sx={{ color: '#60A5FA' }}>{jobTitle}</Typography>
            </Breadcrumbs>

            <Grid container spacing={4}>
                {/* Left Column: Main Info */}
                <Grid item xs={12} md={8}>
                    {/* Header & Actions */}
                    <Stack direction={{ xs: 'column', sm: 'row' }} justifyContent="space-between" alignItems={{ xs: 'flex-start', sm: 'center' }} mb={4} spacing={2}>
                        <Typography variant="h3" sx={{ fontWeight: 'bold', color: 'var(--text)', fontSize: { xs: '2rem', md: '3rem' } }}>
                            {jobTitle}
                        </Typography>
                        <Stack direction="row" spacing={2}>
                            <Button
                                variant="outlined"
                                onClick={() => navigate(`/jobs/${id}/update`)}
                                sx={{ color: 'var(--text)', borderColor: 'var(--border)', textTransform: 'none' }}
                            >
                                Update
                            </Button>
                            <Button
                                variant="outlined"
                                onClick={handleDelete}
                                sx={{ color: 'var(--error)', borderColor: 'var(--error)', textTransform: 'none' }}
                            >
                                Delete
                            </Button>
                        </Stack>
                    </Stack>

                    {/* Description */}
                    {job.job_description && (
                        <Box mb={6}>
                            <Typography variant="h5" sx={{ fontWeight: 'bold', color: 'var(--text)', mb: 2 }}>
                                Description
                            </Typography>
                            <Paper elevation={0} sx={{ p: 3, backgroundColor: 'var(--bg-light)', borderRadius: 2, border: '1px solid var(--border)' }}>
                                <Typography variant="body1" sx={{ color: 'var(--text)', whiteSpace: 'pre-line', fontSize: '1.1rem' }}>
                                    {job.job_description}
                                </Typography>
                            </Paper>
                        </Box>
                    )}

                    {/* Location & Time */}
                    <Box mb={6}>
                        <Typography variant="h5" sx={{ fontWeight: 'bold', color: 'var(--text)', mb: 3 }}>
                            Location & Time
                        </Typography>

                        <Paper elevation={0} sx={{ p: 3, backgroundColor: 'var(--bg-light)', borderRadius: 2, border: '1px solid var(--border)' }}>
                            <Stack spacing={3}>
                                {/* Address Block */}
                                <Stack direction="row" spacing={2} alignItems="flex-start">
                                    <LocationOnIcon sx={{ color: 'var(--primary)', mt: 0.5 }} />
                                    <Box>
                                        <Typography variant="body1" sx={{ color: 'var(--text)', whiteSpace: 'pre-line', mb: 1, fontSize: '1.1rem' }}>
                                            {address.trim() ? address : "No address provided"}
                                        </Typography>
                                        <Stack direction="row" spacing={2} alignItems="center">
                                            <Link href={googleMapsUrl} target="_blank" rel="noopener" sx={{ color: 'var(--primary)', textDecoration: 'none', fontWeight: 500 }}>
                                                Open in Google Maps
                                            </Link>
                                            <Button
                                                size="small"
                                                startIcon={<ContentCopyIcon fontSize="small" />}
                                                onClick={handleCopyAddress}
                                                sx={{ color: 'var(--text-muted)', textTransform: 'none' }}
                                            >
                                                Copy Address
                                            </Button>
                                        </Stack>
                                    </Box>
                                </Stack>

                                <Divider sx={{ borderColor: 'var(--border-muted)' }} />

                                {/* Time Block */}
                                <Stack direction="row" spacing={2} alignItems="flex-start">
                                    <AccessTimeIcon sx={{ color: 'var(--primary)', mt: 0.5 }} />
                                    <Box>
                                        <Typography variant="body1" sx={{ color: 'var(--text)', fontSize: '1.1rem' }}>
                                            <Box component="span" sx={{ fontWeight: 'bold', color: 'var(--text-muted)', mr: 1 }}>Start:</Box>
                                            {job.start_datetime ? dayjs(job.start_datetime).format('MMM D, YYYY — h:mm A') : 'Not set'}
                                        </Typography>
                                        {job.end_datetime && (
                                            <Typography variant="body1" sx={{ color: 'var(--text)', fontSize: '1.1rem', mt: 0.5 }}>
                                                <Box component="span" sx={{ fontWeight: 'bold', color: 'var(--text-muted)', mr: 1 }}>End:</Box>
                                                {dayjs(job.end_datetime).format('MMM D, YYYY — h:mm A')}
                                            </Typography>
                                        )}
                                    </Box>
                                </Stack>
                            </Stack>
                        </Paper>
                    </Box>
                </Grid>

                {/* Right Column: Sidebar */}
                <Grid item xs={12} md={4}>
                    <Stack spacing={3}>
                        {/* Workers Card */}
                        <Card variant="outlined" sx={{ backgroundColor: 'var(--bg-light)', borderColor: 'var(--border)' }}>
                            <CardHeader
                                title="Workers"
                                titleTypographyProps={{ variant: 'h6', fontWeight: 'bold', color: 'var(--text)' }}
                                action={
                                    <IconButton size="small" sx={{ border: '1px solid var(--border)', borderRadius: 1 }}>
                                        <AddIcon fontSize="small" />
                                    </IconButton>
                                }
                            />
                            <Divider sx={{ borderColor: 'var(--border-muted)' }} />
                            <CardContent sx={{ p: 0 }}>
                                <List disablePadding>
                                    {job.workers && job.workers.length > 0 ? (
                                        job.workers.map((worker) => (
                                            <ListItem key={worker.worker_id} divider sx={{ borderColor: 'var(--border-muted)' }}>
                                                <ListItemAvatar>
                                                    <Avatar sx={{ bgcolor: 'var(--highlight)', color: 'var(--text)' }}>
                                                        <PersonIcon />
                                                    </Avatar>
                                                </ListItemAvatar>
                                                <ListItemText
                                                    primary={`${worker.worker_first_name || ''} ${worker.worker_last_name || ''}`.trim() || "Unknown Worker"}
                                                    secondary="Assigned Worker"
                                                    primaryTypographyProps={{ color: 'var(--text)', fontWeight: 500 }}
                                                    secondaryTypographyProps={{ color: 'var(--text-muted)' }}
                                                />
                                            </ListItem>
                                        ))
                                    ) : (
                                        null
                                    )}

                                    {/* Display Roles as "Required" placeholders if no workers assigned or in addition */}
                                    {job.roles && job.roles.map((role) => (
                                        <ListItem key={role.role_id} divider sx={{ borderColor: 'var(--border-muted)' }}>
                                            <ListItemAvatar>
                                                <Avatar sx={{ bgcolor: 'transparent', border: '1px dashed var(--text-muted)', color: 'var(--text-muted)' }}>
                                                    <PersonIcon />
                                                </Avatar>
                                            </ListItemAvatar>
                                            <ListItemText
                                                primary={
                                                    <Stack direction="row" alignItems="center" spacing={1}>
                                                        <Typography variant="body1" color="var(--text)">Required Role</Typography>
                                                        <Chip label={role.role_name} size="small" sx={{ backgroundColor: 'var(--highlight)', color: 'var(--text)', fontWeight: 'bold' }} />
                                                    </Stack>
                                                }
                                                secondary={role.role_description || "No description"}
                                                secondaryTypographyProps={{ color: 'var(--text-muted)' }}
                                            />
                                        </ListItem>
                                    ))}

                                    {(!job.workers?.length && !job.roles?.length) && (
                                        <Box p={3} textAlign="center">
                                            <Typography variant="body2" sx={{ color: 'var(--text-muted)', fontStyle: 'italic' }}>
                                                No workers or roles assigned.
                                            </Typography>
                                        </Box>
                                    )}
                                </List>
                            </CardContent>
                        </Card>

                        {/* Items Card */}
                        <Card variant="outlined" sx={{ backgroundColor: 'var(--bg-light)', borderColor: 'var(--border)' }}>
                            <CardHeader
                                title="Items"
                                titleTypographyProps={{ variant: 'h6', fontWeight: 'bold', color: 'var(--text)' }}
                                action={
                                    <IconButton size="small" sx={{ border: '1px solid var(--border)', borderRadius: 1 }}>
                                        <AddIcon fontSize="small" />
                                    </IconButton>
                                }
                            />
                            <Divider sx={{ borderColor: 'var(--border-muted)' }} />
                            <CardContent sx={{ p: 0 }}>
                                <List disablePadding>
                                    {job.item_links && job.item_links.length > 0 ? (
                                        job.item_links.map((link) => (
                                            <ListItem key={link.item_id} divider sx={{ borderColor: 'var(--border-muted)' }}>
                                                <ListItemAvatar>
                                                    <Avatar sx={{ bgcolor: 'var(--secondary)', color: 'var(--bg-dark)' }}>
                                                        <BuildIcon fontSize="small" />
                                                    </Avatar>
                                                </ListItemAvatar>
                                                <ListItemText
                                                    primary={
                                                        <Stack direction="row" alignItems="center" spacing={1}>
                                                            <Typography variant="body1" sx={{ fontWeight: 500 }}>{link.item.item_name}</Typography>
                                                            <Chip label={`x${link.required_quantity}`} size="small" sx={{ height: 20, fontSize: '0.75rem', backgroundColor: 'var(--border)', color: 'var(--text)' }} />
                                                        </Stack>
                                                    }
                                                    secondary={link.item.item_description || "Item"}
                                                    primaryTypographyProps={{ color: 'var(--text)' }}
                                                    secondaryTypographyProps={{ color: 'var(--text-muted)' }}
                                                />
                                            </ListItem>
                                        ))
                                    ) : (
                                        <Box p={3} textAlign="center">
                                            <Typography variant="body2" sx={{ color: 'var(--text-muted)', fontStyle: 'italic' }}>
                                                No items assigned.
                                            </Typography>
                                        </Box>
                                    )}
                                </List>
                            </CardContent>
                        </Card>
                    </Stack>
                </Grid>
            </Grid>
        </Box>
    );
};

export default JobDetailsPage;
