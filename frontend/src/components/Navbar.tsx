import React from 'react'
import { AppBar, Toolbar, Typography, Button, Box } from '@mui/material';
import { Link } from 'react-router-dom'

const Navbar: React.FC = () => {
	return (
		<AppBar position="static" color="transparent" elevation={0} sx={{ height: 'var(--header-height)', display: 'flex', justifyContent: 'center' }}>
			<Toolbar sx={{ justifyContent: 'space-between', maxWidth: 'var(--max-content-width)', width: '100%', margin: '0 auto', padding: '0 var(--page-margin)', minHeight: 'unset !important' }}>
				<Box component={Link} to="/" sx={{ display: 'flex', alignItems: 'center', gap: 2, textDecoration: 'none', color: 'inherit', cursor: 'pointer' }}>
					<Box
						component="img"
						src="/logistream_logo_no_text_1763844999479.png"
						alt="LogiStream Logo"
						sx={{ width: 40, height: 40, objectFit: 'contain', borderRadius: '8px' }}
					/>
					<Typography variant="h6">LogiStream</Typography>
				</Box>

				<Box sx={{ display: 'flex', alignItems: 'center', gap: 4 }}>
					<Button component={Link} to="/dashboard" sx={{ color: 'white', fontSize: '1.25rem', textTransform: 'none' }}>Dashboard</Button>
					<Button component={Link} to="/jobs" sx={{ color: 'white', fontSize: '1.25rem', textTransform: 'none' }}>Jobs</Button>
					<Button component={Link} to="/workers" sx={{ color: 'white', fontSize: '1.25rem', textTransform: 'none' }}>Workers</Button>
					<Button component={Link} to="/items" sx={{ color: 'white', fontSize: '1.25rem', textTransform: 'none' }}>Items</Button>
				</Box>
			</Toolbar>
		</AppBar>
	)
}

export default Navbar

