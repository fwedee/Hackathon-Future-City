import React from 'react'
import { AppBar, Toolbar, Typography, Button, Box } from '@mui/material';
import { Link } from 'react-router-dom'

const Navbar: React.FC = () => {
	return (
		<AppBar position="static" color="transparent" elevation={0}>
			<Toolbar sx={{ justifyContent: 'space-between' }}>
				<Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
					<Box
						component="img"
						src="/logistream_logo_no_text_1763844999479.png"
						alt="LogiStream Logo"
						sx={{ width: 40, height: 40, objectFit: 'contain', borderRadius: '8px' }}
					/>
					<Typography variant="h6">LogiStream</Typography>
				</Box>

				<Box sx={{ display: 'flex', alignItems: 'center', gap: 4 }}>
					<Button component={Link} to="/dashboard">Dashboard</Button>
					<Button component={Link} to="/jobs">Jobs</Button>
					<Button component={Link} to="/workers">Workers</Button>
					<Button component={Link} to="/items">Items</Button>
				</Box>
			</Toolbar>
		</AppBar>
	)
}

export default Navbar

