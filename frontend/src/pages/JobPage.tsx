import React from 'react'
import { Typography } from '@mui/material'
import { useParams } from 'react-router-dom'

const JobPage: React.FC = () => {
  const { id } = useParams()
  return (
    <div>
      <Typography variant="h4" gutterBottom>Job {id}</Typography>
      <Typography>Job detail page (content intentionally left empty).</Typography>
    </div>
  )
}

export default JobPage
