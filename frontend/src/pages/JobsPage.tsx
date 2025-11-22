import React from 'react'
import { Typography, Container } from '@mui/material'
import JobCreationForm from '../components/JobCreationForm'

const JobsPage: React.FC = () => {
  return (
    <Container maxWidth="lg" sx={{ py: 8, backgroundColor: 'var(--bg)', minHeight: '100vh' }}>
      <Typography variant="h4" gutterBottom sx={{ mb: 4, color: 'var(--primary)', fontWeight: 'bold' }}>Jobs Management</Typography>
      <JobCreationForm />
    </Container>
  )
}

export default JobsPage
