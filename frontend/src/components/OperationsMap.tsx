import React, { useState, useMemo } from 'react';
import { GoogleMap, Marker, InfoWindow, useLoadScript } from '@react-google-maps/api';
import { Box, Typography, Paper, Chip, Button } from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';
import dayjs from 'dayjs';
import { type Job } from '../services/api';

interface OperationsMapProps {
    jobs: Job[];
}

const libraries: ("places")[] = ["places"];

const mapContainerStyle = {
    width: '100%',
    height: '100%',
    borderRadius: '8px',
};

const defaultCenter = {
    lat: 52.5200, // Berlin
    lng: 13.4050,
};

const mapOptions = {
    disableDefaultUI: false,
    zoomControl: true,
    streetViewControl: false,
    mapTypeControl: false,
    styles: [
        {
            featureType: "all",
            elementType: "geometry",
            stylers: [{ color: "#242f3e" }]
        },
        {
            featureType: "all",
            elementType: "labels.text.stroke",
            stylers: [{ color: "#242f3e" }]
        },
        {
            featureType: "all",
            elementType: "labels.text.fill",
            stylers: [{ color: "#746855" }]
        },
        {
            featureType: "administrative.locality",
            elementType: "labels.text.fill",
            stylers: [{ color: "#d59563" }]
        },
        {
            featureType: "poi",
            elementType: "labels.text.fill",
            stylers: [{ color: "#d59563" }]
        },
        {
            featureType: "poi.park",
            elementType: "geometry",
            stylers: [{ color: "#263c3f" }]
        },
        {
            featureType: "poi.park",
            elementType: "labels.text.fill",
            stylers: [{ color: "#6b9a76" }]
        },
        {
            featureType: "road",
            elementType: "geometry",
            stylers: [{ color: "#38414e" }]
        },
        {
            featureType: "road",
            elementType: "geometry.stroke",
            stylers: [{ color: "#212a37" }]
        },
        {
            featureType: "road",
            elementType: "labels.text.fill",
            stylers: [{ color: "#9ca5b3" }]
        },
        {
            featureType: "road.highway",
            elementType: "geometry",
            stylers: [{ color: "#746855" }]
        },
        {
            featureType: "road.highway",
            elementType: "geometry.stroke",
            stylers: [{ color: "#1f2835" }]
        },
        {
            featureType: "road.highway",
            elementType: "labels.text.fill",
            stylers: [{ color: "#f3d19c" }]
        },
        {
            featureType: "water",
            elementType: "geometry",
            stylers: [{ color: "#17263c" }]
        },
        {
            featureType: "water",
            elementType: "labels.text.fill",
            stylers: [{ color: "#515c6d" }]
        },
        {
            featureType: "water",
            elementType: "labels.text.stroke",
            stylers: [{ color: "#17263c" }]
        }
    ]
};

const OperationsMap: React.FC<OperationsMapProps> = ({ jobs }) => {
    const { isLoaded, loadError } = useLoadScript({
        googleMapsApiKey: import.meta.env.VITE_GOOGLE_MAPS_API_KEY || "",
        libraries,
    });

    const [selectedJob, setSelectedJob] = useState<Job | null>(null);

    const center = useMemo(() => {
        if (jobs.length > 0) {
            // Find first job with valid coordinates
            const validJob = jobs.find(j => j.latitude && j.longitude);
            if (validJob) {
                return { lat: validJob.latitude, lng: validJob.longitude };
            }
        }
        return defaultCenter;
    }, [jobs]);

    if (loadError) return <Box sx={{ p: 2, color: 'var(--error)' }}>Error loading maps</Box>;
    if (!isLoaded) return <Box sx={{ p: 2, color: 'var(--text-muted)' }}>Loading Maps...</Box>;

    return (
        <GoogleMap
            mapContainerStyle={mapContainerStyle}
            zoom={12}
            center={center}
            options={mapOptions}
        >
            {jobs.map((job) => (
                job.latitude && job.longitude ? (
                    <Marker
                        key={job.job_id}
                        position={{ lat: job.latitude, lng: job.longitude }}
                        onClick={() => setSelectedJob(job)}
                    />
                ) : null
            ))}

            {selectedJob && (
                <InfoWindow
                    position={{ lat: selectedJob.latitude, lng: selectedJob.longitude }}
                    onCloseClick={() => setSelectedJob(null)}
                >
                    <Paper elevation={0} sx={{ p: 1, maxWidth: 200 }}>
                        <Typography variant="subtitle2" sx={{ fontWeight: 'bold', mb: 0.5 }}>
                            {selectedJob.job_name || 'Unnamed Job'}
                        </Typography>
                        <Typography variant="caption" display="block" sx={{ mb: 1, color: 'text.secondary' }}>
                            {dayjs(selectedJob.start_datetime).format('MMM D, HH:mm')}
                        </Typography>
                        <Chip
                            label={selectedJob.workers && selectedJob.workers.length > 0 ? 'Assigned' : 'Pending'}
                            size="small"
                            color={selectedJob.workers && selectedJob.workers.length > 0 ? 'success' : 'warning'}
                            sx={{ mb: 1, height: 20, fontSize: '0.7rem' }}
                        />
                        <Button
                            component={RouterLink}
                            to={`/jobs/${selectedJob.job_id}`}
                            size="small"
                            variant="outlined"
                            fullWidth
                            sx={{ fontSize: '0.7rem', py: 0.5 }}
                        >
                            View Details
                        </Button>
                    </Paper>
                </InfoWindow>
            )}
        </GoogleMap>
    );
};

export default OperationsMap;
