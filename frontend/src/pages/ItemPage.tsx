import React, { useEffect, useState } from 'react';
import { Typography, Box, Card, CardContent, Link as MuiLink, Stack, Breadcrumbs, Link, Chip } from '@mui/material';
import { useParams, Link as RouterLink } from 'react-router-dom';
import NavigateNextIcon from '@mui/icons-material/NavigateNext';
import InventoryIcon from '@mui/icons-material/Inventory';
import StorageIcon from '@mui/icons-material/Storage';
import { fetchItem, fetchJobsByItemId } from '../services/api';
import type { Job, Item } from '../services/api';

const ItemPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [item, setItem] = useState<Item | null>(null);
  const [jobs, setJobs] = useState<Job[]>([]);

  useEffect(() => {
    if (id) {
      loadItem(id);
      loadJobsByItemId(id);
    }
  }, [id]);

  const loadItem = async (itemId: string) => {
    try {
      const data = await fetchItem(itemId);
      setItem(data);
    } catch (error) {
      console.error("Failed to load item", error);
    }
  };

  const loadJobsByItemId = async (itemId: string) => {
    try {
      const data = await fetchJobsByItemId(itemId);
      // Sort jobs by start_datetime
      const sortedJobs = data.sort((a, b) => {
        if (!a.start_datetime) return 1;
        if (!b.start_datetime) return -1;
        return new Date(a.start_datetime).getTime() - new Date(b.start_datetime).getTime();
      });
      setJobs(sortedJobs);
    } catch (error) {
      console.error("Failed to load jobs for item", error);
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

  if (!item) {
    return <Typography>Loading...</Typography>;
  }

  const itemName = item.item_name || item.item_id;

  return (
    <Box sx={{ p: 3 }}>
      {/* Breadcrumbs */}
      <Breadcrumbs separator={<NavigateNextIcon fontSize="small" sx={{ color: '#60A5FA' }} />} aria-label="breadcrumb" sx={{ mb: 3 }}>
        <Link component={RouterLink} to="/" underline="hover" sx={{ color: '#60A5FA' }}>
          Home
        </Link>
        <Link component={RouterLink} to="/items" underline="hover" sx={{ color: '#60A5FA' }}>
          Items
        </Link>
        <Typography sx={{ color: '#60A5FA' }}>{itemName}</Typography>
      </Breadcrumbs>

      <Box sx={{ display: 'flex', gap: 4, alignItems: 'flex-start' }}>
        {/* Left side - Item Profile */}
        <Box sx={{ flex: '0 0 400px' }}>
          <Stack direction="row" alignItems="center" spacing={2} mb={2}>
            <InventoryIcon sx={{ fontSize: 40, color: 'var(--secondary)' }} />
            <Typography variant="h4" sx={{ color: 'var(--text)' }}>
              {itemName}
            </Typography>
          </Stack>

          <Box sx={{ mt: 2 }}>
            <Typography variant="body1" sx={{ color: 'var(--text-muted)', mb: 1, fontSize: '1.1rem' }}>
              <strong>Description:</strong>
            </Typography>
            <Typography variant="body1" sx={{ color: 'var(--text)', fontSize: '1rem' }}>
              {item.item_description || 'No description available'}
            </Typography>
          </Box>

          <Box sx={{ mt: 3 }}>
            <Typography variant="body1" sx={{ color: 'var(--text-muted)', mb: 1.5, fontSize: '1.1rem' }}>
              <strong>Total Stock:</strong>
            </Typography>
            <Chip
              icon={<StorageIcon />}
              label={`${item.total_stock !== undefined ? item.total_stock : '-'} units`}
              sx={{
                backgroundColor: 'var(--highlight)',
                color: 'var(--text)',
                fontWeight: 'bold',
                fontSize: '1.1rem',
                height: '48px',
                px: 2,
                '& .MuiChip-label': {
                  fontSize: '1.1rem'
                },
                '& .MuiChip-icon': {
                  fontSize: '1.5rem',
                  color: 'white !important'
                }
              }}
            />
          </Box>
        </Box>

        {/* Right side - Jobs List */}
        <Box sx={{ flex: 1 }}>
          <Typography variant="h5" gutterBottom sx={{ color: 'var(--text)' }}>Jobs Using This Item</Typography>

          {jobs.length === 0 ? (
            <Typography sx={{ color: 'var(--text-muted)' }}>No jobs using this item</Typography>
          ) : (
            <Stack spacing={2} sx={{ mt: 2 }}>
              {jobs.map((job) => (
                <Card key={job.job_id} variant="outlined" sx={{ backgroundColor: 'var(--bg-light)', border: '1px solid var(--border)', '&:hover': { borderColor: 'var(--primary)' } }}>
                  <CardContent>
                    <MuiLink component={RouterLink} to={`/jobs/${job.job_id}`} underline="hover" sx={{ color: 'var(--primary)' }}>
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
    </Box>
  );
};

export default ItemPage;
