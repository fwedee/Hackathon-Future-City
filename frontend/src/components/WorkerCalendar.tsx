import React, { useState } from 'react';
import { Box, Paper, Typography, Grid, IconButton, Card, CardContent } from '@mui/material';
import { ChevronLeft, ChevronRight, AccessTime, LocationOn } from '@mui/icons-material';
import dayjs from 'dayjs';
import isoWeek from 'dayjs/plugin/isoWeek';
import type { Job } from '../services/api';
import { useNavigate } from 'react-router-dom';

dayjs.extend(isoWeek);

interface WorkerCalendarProps {
    jobs: Job[];
}

const WorkerCalendar: React.FC<WorkerCalendarProps> = ({ jobs }) => {
    const [currentDate, setCurrentDate] = useState(dayjs());
    const navigate = useNavigate();

    const startOfWeek = currentDate.startOf('isoWeek');
    const endOfWeek = currentDate.endOf('isoWeek');

    const weekDays = [];
    let day = startOfWeek;
    while (day.isBefore(endOfWeek) || day.isSame(endOfWeek, 'day')) {
        weekDays.push(day);
        day = day.add(1, 'day');
    }

    const handlePrevWeek = () => {
        setCurrentDate(currentDate.subtract(1, 'week'));
    };

    const handleNextWeek = () => {
        setCurrentDate(currentDate.add(1, 'week'));
    };

    const handleToday = () => {
        setCurrentDate(dayjs());
    };

    const getJobsForDay = (date: dayjs.Dayjs) => {
        return jobs.filter(job => {
            if (!job.start_datetime) return false;
            return dayjs(job.start_datetime).isSame(date, 'day');
        }).sort((a, b) => dayjs(a.start_datetime).diff(dayjs(b.start_datetime)));
    };

    return (
        <Paper sx={{ p: 3, mt: 4, backgroundColor: 'var(--bg-light)', border: '1px solid var(--border)' }}>
            <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 3 }}>
                <Typography variant="h6" sx={{ color: 'var(--text)' }}>
                    Weekly Schedule
                </Typography>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                    <Typography sx={{ color: 'var(--text-muted)', fontWeight: 500 }}>
                        {startOfWeek.format('MMM D')} - {endOfWeek.format('MMM D, YYYY')}
                    </Typography>
                    <Box sx={{ display: 'flex', gap: 1 }}>
                        <IconButton onClick={handlePrevWeek} size="small" sx={{ color: 'var(--text)' }}>
                            <ChevronLeft />
                        </IconButton>
                        <IconButton onClick={handleToday} size="small" sx={{ fontSize: '0.875rem', color: 'var(--primary)' }}>
                            Today
                        </IconButton>
                        <IconButton onClick={handleNextWeek} size="small" sx={{ color: 'var(--text)' }}>
                            <ChevronRight />
                        </IconButton>
                    </Box>
                </Box>
            </Box>

            <Grid container spacing={2}>
                {weekDays.map((dayItem) => {
                    const dayJobs = getJobsForDay(dayItem);
                    const isToday = dayItem.isSame(dayjs(), 'day');

                    return (
                        <Grid size={{ xs: 12, md: 'grow' }} key={dayItem.toString()} sx={{ minWidth: { md: 0, xs: '100%' } }}>
                            <Box
                                sx={{
                                    p: 1.5,
                                    borderRadius: 2,
                                    backgroundColor: isToday ? 'rgba(var(--primary-rgb), 0.1)' : 'transparent',
                                    border: isToday ? '1px solid var(--primary)' : '1px solid transparent',
                                    height: '100%',
                                    minHeight: 200
                                }}
                            >
                                <Typography
                                    align="center"
                                    sx={{
                                        fontWeight: isToday ? 'bold' : 'normal',
                                        color: isToday ? 'var(--primary)' : 'var(--text-muted)',
                                        mb: 2
                                    }}
                                >
                                    {dayItem.format('ddd D')}
                                </Typography>

                                <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1.5 }}>
                                    {dayJobs.map((job) => (
                                        <Card
                                            key={job.job_id}
                                            variant="outlined"
                                            sx={{
                                                cursor: 'pointer',
                                                backgroundColor: 'var(--bg-dark)',
                                                borderColor: 'var(--border-muted)',
                                                transition: 'all 0.2s',
                                                '&:hover': {
                                                    borderColor: 'var(--primary)',
                                                    transform: 'translateY(-2px)',
                                                    boxShadow: '0 4px 8px rgba(0,0,0,0.1)'
                                                }
                                            }}
                                            onClick={() => navigate(`/jobs/${job.job_id}`)}
                                        >
                                            <CardContent sx={{ p: '12px !important' }}>
                                                <Typography variant="subtitle2" sx={{ fontWeight: 'bold', fontSize: '0.85rem', mb: 0.5, lineHeight: 1.2, color: 'var(--text)' }}>
                                                    {job.job_name || 'Unnamed Job'}
                                                </Typography>

                                                <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5, mb: 0.5 }}>
                                                    <AccessTime sx={{ fontSize: 14, color: 'var(--text-muted)' }} />
                                                    <Typography variant="caption" sx={{ color: 'var(--text-muted)' }}>
                                                        {dayjs(job.start_datetime).format('HH:mm')} - {dayjs(job.end_datetime).format('HH:mm')}
                                                    </Typography>
                                                </Box>

                                                {(job.city || job.street) && (
                                                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                                                        <LocationOn sx={{ fontSize: 14, color: 'var(--text-muted)' }} />
                                                        <Typography variant="caption" sx={{ color: 'var(--text-muted)', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                                                            {job.city}
                                                        </Typography>
                                                    </Box>
                                                )}
                                            </CardContent>
                                        </Card>
                                    ))}
                                    {dayJobs.length === 0 && (
                                        <Typography variant="caption" align="center" sx={{ color: 'var(--text-muted)', mt: 2, fontStyle: 'italic' }}>
                                            No jobs
                                        </Typography>
                                    )}
                                </Box>
                            </Box>
                        </Grid>
                    );
                })}
            </Grid>
        </Paper>
    );
};

export default WorkerCalendar;
