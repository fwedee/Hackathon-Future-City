import React from 'react'
import { Typography } from '@mui/material'
import { useParams } from 'react-router-dom'

const ItemPage: React.FC = () => {
  const { id } = useParams()
  return (
    <div>
      <Typography variant="h4" gutterBottom>Item {id}</Typography>
      <Typography>Item detail page (content intentionally left empty).</Typography>
    </div>
  )
}

export default ItemPage