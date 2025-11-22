import React, { useEffect, useState } from 'react'
import { Typography, Box, Card, CardContent, Link as MuiLink, Stack, Chip } from '@mui/material'
import { useParams, Link } from 'react-router-dom';
import { fetchJobsByWorkerId, fetchWorker } from '../services/api';
import type { Job, Worker } from '../services/api';

const WorkerPage: React.FC = () => {
  
  const { id } = useParams<{ id: string }>();
  const [worker, setWorker] = useState<Worker | null>(null);
  const [jobs, setJobs] = useState<Job[]>([]);

  useEffect(() => {
      if (id) {
          loadWorker(id);
          loadJobsByWorkerId(id);
      }
  }, [id]);

  const loadWorker = async (workerId: string) => {
      try {
          const data = await fetchWorker(workerId);
          setWorker(data);
      } catch (error) {
          console.error("Failed to load worker", error);
      }
  };

  const loadJobsByWorkerId = async (workerId: string) => {
      try {
          const data = await fetchJobsByWorkerId(workerId);
          // Sort jobs by start_datetime
          const sortedJobs = data.sort((a, b) => {
              if (!a.start_datetime) return 1;
              if (!b.start_datetime) return -1;
              return new Date(a.start_datetime).getTime() - new Date(b.start_datetime).getTime();
          });
          setJobs(sortedJobs);
      } catch (error) {
          console.error("Failed to load jobs for worker", error);
      }
  };

  const formatDateTime = (datetime?: string) => {
      if (!datetime) return 'Not scheduled';
      const date = new Date(datetime);
      return date.toLocaleString('en-US', {
          month: '2-digit',
          day: '2-digit',
          year: 'numeric',
          hour: '2-digit',
          minute: '2-digit'
      });
  };

  if (!worker) {
      return <Typography>Loading...</Typography>;
  }

  const workerName = `${worker.worker_first_name || ''} ${worker.worker_last_name || ''}`.trim() || worker.worker_id;
  const workerRole = worker.branch?.branch_name || 'No branch assigned';

  return (
    <Box sx={{ display: 'flex', gap: 4, alignItems: 'flex-start' }}>
      {/* Left side - Worker Profile */}
      <Box sx={{ flex: '0 0 400px' }}>
        <Typography variant="h4" gutterBottom sx={{ color: 'var(--text)' }}>
          {workerName}
        </Typography>
        <Typography variant="subtitle1" sx={{ color: 'var(--text-muted)' }}>
          {workerRole}
        </Typography>
        
        <Box sx={{ mt: 2 }}>
          <Typography variant="body2" sx={{ color: 'var(--text-muted)' }}>
            <strong>Phone:</strong> {worker.worker_phone_number || 'N/A'}
          </Typography>
        </Box>
        
        {worker.roles && worker.roles.length > 0 && (
          <Box sx={{ mt: 2 }}>
            <Typography variant="body2" sx={{ color: 'var(--text-muted)', mb: 1 }}>
              <strong>Roles:</strong>
            </Typography>
            <Stack direction="row" spacing={1} flexWrap="wrap" useFlexGap>
              {worker.roles.map(role => (
                <Chip 
                  key={role.role_id} 
                  label={role.role_name} 
                  size="small"
                  sx={{ backgroundColor: 'var(--highlight)', color: 'var(--text)' }} 
                />
              ))}
            </Stack>
          </Box>
        )}
      </Box>

      {/* Right side - Jobs List */}
      <Box sx={{ flex: 1 }}>
        <Typography variant="h5" gutterBottom sx={{ color: 'var(--text)' }}>Jobs</Typography>
        
        {jobs.length === 0 ? (
          <Typography sx={{ color: 'var(--text-muted)' }}>No jobs assigned</Typography>
        ) : (
          <Stack spacing={2} sx={{ mt: 2 }}>
            {jobs.map((job) => (
              <Card key={job.job_id} variant="outlined" sx={{ backgroundColor: 'var(--bg-light)', border: '1px solid var(--border)', '&:hover': { borderColor: 'var(--primary)' } }}>
                <CardContent>
                  <MuiLink component={Link} to={`/jobs/${job.job_id}`} underline="hover" sx={{ color: 'var(--primary)' }}>
                    <Typography variant="h6">{job.job_name || 'Unnamed Job'}</Typography>
                  </MuiLink>
                  
                  <Typography variant="body2" sx={{ color: 'var(--text-muted)', mt: 1 }}>
                    {formatDateTime(job.start_datetime)} - {formatDateTime(job.end_datetime)}
                  </Typography>
                  
                  {job.city && (
                    <Typography variant="body2" sx={{ color: 'var(--text-muted)', mt: 0.5 }}>
                      {job.city}{job.street ? `, ${job.street}` : ''}
                    </Typography>
                  )}
                </CardContent>
              </Card>
            ))}
          </Stack>
        )}
      </Box>
    </Box>
  )
}

export default WorkerPage
