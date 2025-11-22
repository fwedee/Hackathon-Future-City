import React from 'react'
import { Container } from '@mui/material'
import JobCreationForm from '../components/JobCreationForm'

const JobCreatePage: React.FC = () => {
  return (
    <Container maxWidth="lg" sx={{ py: 8, backgroundColor: 'var(--bg)', minHeight: '100vh' }}>
      <JobCreationForm />
    </Container>
  )
}

export default JobCreatePage
