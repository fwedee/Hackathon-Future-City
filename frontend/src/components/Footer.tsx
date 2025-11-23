import React from 'react'
import { Box, Typography } from '@mui/material'

const Footer: React.FC = () => {
  return (
    <Box component="footer" sx={{ display: 'flex', gap: 3 }}>
      <Typography variant="body2" sx={{ color: 'var(--text-muted)' }}>
        © 2025 LogiStream
      </Typography>
      <Typography variant="body2" sx={{ color: 'var(--text-muted)' }}>
        Privacy Policy
      </Typography>
      <Typography variant="body2" sx={{ color: 'var(--text-muted)' }}>
        Data Protection
      </Typography>
    </Box>
  )
}

export default Footer
