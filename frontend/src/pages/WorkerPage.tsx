import React from 'react'
import { Typography } from '@mui/material'
import { useParams } from 'react-router-dom'

const WorkerPage: React.FC = () => {
  const { id } = useParams()
  return (
    <div>
      <Typography variant="h4" gutterBottom>Worker {id}</Typography>
      <Typography>Worker detail page (content intentionally left empty).</Typography>
    </div>
  )
}

export default WorkerPage
