import React from 'react'
import { AppBar, Toolbar, Typography, Button, Box, Avatar } from '@mui/material'
import { Link } from 'react-router-dom'

const Navbar: React.FC = () => {
	return (
		<AppBar position="static" color="transparent" elevation={0}>
			<Toolbar sx={{ justifyContent: 'space-between' }}>
				<Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
					<Avatar sx={{ bgcolor: '#ccc', width: 40, height: 40 }} />
					<Typography variant="h6">Logo</Typography>
				</Box>

				<Box sx={{ display: 'flex', alignItems: 'center', gap: 4 }}>
					<Button component={Link} to="/jobs">Jobs</Button>
					<Button component={Link} to="/workers">Workers</Button>
					<Button component={Link} to="/items">Items</Button>
					<Button>Lang</Button>
				</Box>
			</Toolbar>
		</AppBar>
	)
}

export default Navbar

