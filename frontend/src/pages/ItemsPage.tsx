import React, { useEffect, useState } from 'react';
import {
  Box,
  Typography,
  Grid,
  Card,
  CardContent,
  CardHeader,
  Divider,
  Chip,
  Stack,
  Breadcrumbs,
  Link,
  Avatar
} from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';
import NavigateNextIcon from '@mui/icons-material/NavigateNext';
import InventoryIcon from '@mui/icons-material/Inventory';
import BuildIcon from '@mui/icons-material/Build';
import { fetchItems, type Item } from '../services/api';

const ItemsPage: React.FC = () => {
  const [items, setItems] = useState<Item[]>([]);

  useEffect(() => {
    loadItems();
  }, []);

  const loadItems = async () => {
    try {
      const data = await fetchItems();
      setItems(data);
    } catch (error) {
      console.error("Failed to load items", error);
    }
  };

  return (
    <Box sx={{ p: { xs: 2, md: 4 }, maxWidth: 1200, mx: 'auto' }}>
      {/* Breadcrumbs */}
      <Breadcrumbs separator={<NavigateNextIcon fontSize="small" sx={{ color: '#60A5FA' }} />} aria-label="breadcrumb" sx={{ mb: 3 }}>
        <Link component={RouterLink} to="/" underline="hover" sx={{ color: '#60A5FA' }}>
          Home
        </Link>
        <Typography sx={{ color: '#60A5FA' }}>Items</Typography>
      </Breadcrumbs>

      <Stack direction="row" justifyContent="space-between" alignItems="center" mb={4}>
        <Typography variant="h3" sx={{ fontWeight: 'bold', color: 'var(--text)', fontSize: { xs: '2rem', md: '3rem' } }}>
          Items Inventory
        </Typography>
      </Stack>

      <Grid container spacing={3}>
        {items.map((item) => (
          <Grid size={{ xs: 12, sm: 6, md: 4 }} key={item.item_id}>
            <Link component={RouterLink} to={`/items/${item.item_id}`} style={{ textDecoration: 'none' }}>
              <Card variant="outlined" sx={{ height: '100%', display: 'flex', flexDirection: 'column', backgroundColor: 'var(--bg-light)', borderColor: 'var(--border)', transition: 'transform 0.2s', '&:hover': { transform: 'translateY(-4px)', borderColor: 'var(--primary)' } }}>
                <CardHeader
                  avatar={
                    <Avatar sx={{ bgcolor: 'var(--secondary)', color: 'var(--bg-dark)' }}>
                      <BuildIcon />
                    </Avatar>
                  }
                  title={
                    <Typography variant="h6" sx={{ fontWeight: 'bold', color: 'var(--text)' }}>
                      {item.item_name}
                    </Typography>
                  }
                />
                <Divider sx={{ borderColor: 'var(--border-muted)' }} />
                <CardContent sx={{ flexGrow: 1 }}>
                  <Typography variant="body2" sx={{ color: 'var(--text-muted)', mb: 2, minHeight: '40px' }}>
                    {item.item_description || "No description available."}
                  </Typography>

                  <Stack direction="row" alignItems="center" justifyContent="space-between" mt="auto">
                    <Chip
                      icon={<InventoryIcon sx={{ '&&': { color: 'var(--primary)' } }} />}
                      label={`Stock: ${item.total_stock !== undefined ? item.total_stock : '-'}`}
                      sx={{
                        backgroundColor: 'var(--highlight)',
                        color: 'var(--text)',
                        fontWeight: 'bold',
                        border: '1px solid var(--border)'
                      }}
                    />
                  </Stack>
                </CardContent>
              </Card>
            </Link>
          </Grid>
        ))}

        {items.length === 0 && (
          <Grid size={{ xs: 12 }}>
            <Box sx={{ textAlign: 'center', py: 8, color: 'var(--text-muted)' }}>
              <InventoryIcon sx={{ fontSize: 60, mb: 2, opacity: 0.5 }} />
              <Typography variant="h6">No items found in inventory.</Typography>
            </Box>
          </Grid>
        )}
      </Grid>
    </Box>
  );
};

export default ItemsPage;
