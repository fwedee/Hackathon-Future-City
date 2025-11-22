import React, { useState, useEffect, useRef } from 'react';
import {
    Box,
    Button,
    TextField,
    Typography,
    Autocomplete,
    Chip,
    Stack,
    Snackbar,
    Alert,
    Dialog,
    DialogTitle,
    DialogContent,
    DialogActions,
    Paper,
    Tooltip,
    Divider
} from '@mui/material';
import InfoIcon from '@mui/icons-material/Info';
import AddIcon from '@mui/icons-material/Add';
import { useLoadScript, Autocomplete as GoogleAutocomplete } from '@react-google-maps/api';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { DateTimePicker } from '@mui/x-date-pickers/DateTimePicker';
import dayjs, { Dayjs } from 'dayjs';
import { fetchRoles, fetchItems, createItem, createRole, createJob, updateJob, fetchJob, type Role, type Item } from '../services/api';
import { useNavigate } from 'react-router-dom';

const libraries: ("places")[] = ["places"];

interface JobCreationFormProps {
    jobId?: string;
}

const JobCreationForm: React.FC<JobCreationFormProps> = ({ jobId }) => {
    const navigate = useNavigate();
    const { isLoaded } = useLoadScript({
        googleMapsApiKey: import.meta.env.VITE_GOOGLE_MAPS_API_KEY || "",
        libraries,
    });

    const [roles, setRoles] = useState<Role[]>([]);
    const [items, setItems] = useState<Item[]>([]);
    const [selectedRoles, setSelectedRoles] = useState<Role[]>([]);
    const [selectedItems, setSelectedItems] = useState<Item[]>([]);

    // Location state
    const [address, setAddress] = useState('');
    const [coordinates, setCoordinates] = useState<{ lat: number; lng: number } | null>(null);
    const [locationDetails, setLocationDetails] = useState<any>({});
    const autocompleteRef = useRef<google.maps.places.Autocomplete | null>(null);

    // Datetime state
    const [startDatetime, setStartDatetime] = useState<Dayjs | null>(null);

    // Validation state
    const [errors, setErrors] = useState<{ [key: string]: string }>({});

    // New Item Dialog state
    const [openNewItemDialog, setOpenNewItemDialog] = useState(false);
    const [newItemName, setNewItemName] = useState('');
    const [newItemDesc, setNewItemDesc] = useState('');

    // New Role Dialog state
    const [openNewRoleDialog, setOpenNewRoleDialog] = useState(false);
    const [newRoleName, setNewRoleName] = useState('');
    const [newRoleDesc, setNewRoleDesc] = useState('');

    // Feedback state
    const [snackbar, setSnackbar] = useState<{ open: boolean; message: string; severity: 'success' | 'error' }>({
        open: false,
        message: '',
        severity: 'success'
    });

    useEffect(() => {
        loadData();
    }, []);

    useEffect(() => {
        if (jobId && roles.length > 0 && items.length > 0) {
            loadJobDetails();
        }
    }, [jobId, roles, items]);

    const loadData = async () => {
        try {
            const [rolesData, itemsData] = await Promise.all([fetchRoles(), fetchItems()]);
            setRoles(rolesData);
            setItems(itemsData);
        } catch (error) {
            console.error("Failed to load data", error);
            showSnackbar("Failed to load initial data", "error");
        }
    };

    const loadJobDetails = async () => {
        if (!jobId) return;
        try {
            const job = await fetchJob(jobId);
            // Set Location
            setAddress(`${job.street || ''} ${job.house_number || ''}, ${job.city || ''}`);
            setCoordinates({ lat: job.latitude, lng: job.longitude });
            setLocationDetails({
                street: job.street,
                house_number: job.house_number,
                city: job.city,
                country: job.country,
                postal_code: job.postal_code
            });

            // Set Datetime
            if (job.start_datetime) {
                setStartDatetime(dayjs(job.start_datetime));
            }

            // Set Roles
            // Map existing roles to the full role objects from the list to ensure equality checks work
            const jobRoles = job.roles.map(r => roles.find(role => role.role_id === r.role_id) || r);
            setSelectedRoles(jobRoles);

            // Set Items
            const jobItems = job.items.map(i => items.find(item => item.item_id === i.item_id) || i);
            setSelectedItems(jobItems);

        } catch (error) {
            console.error("Failed to load job details", error);
            showSnackbar("Failed to load job details", "error");
        }
    };

    const onLoadAutocomplete = (autocomplete: google.maps.places.Autocomplete) => {
        autocompleteRef.current = autocomplete;
    };

    const onPlaceChanged = () => {
        if (autocompleteRef.current) {
            const place = autocompleteRef.current.getPlace();
            if (place.geometry && place.geometry.location) {
                const lat = place.geometry.location.lat();
                const lng = place.geometry.location.lng();
                setCoordinates({ lat, lng });
                setAddress(place.formatted_address || '');

                // Extract address components
                const details: any = {};
                place.address_components?.forEach(component => {
                    const types = component.types;
                    if (types.includes('street_number')) details.house_number = component.long_name;
                    if (types.includes('route')) details.street = component.long_name;
                    if (types.includes('locality')) details.city = component.long_name;
                    if (types.includes('country')) details.long_name;
                    if (types.includes('postal_code')) details.postal_code = component.long_name;
                });
                setLocationDetails(details);
                setErrors(prev => ({ ...prev, location: '' }));
            }
        }
    };

    const handleCreateItem = async () => {
        try {
            const newItem = await createItem(newItemName, newItemDesc);
            setItems([...items, newItem]);
            setSelectedItems([...selectedItems, newItem]);
            setOpenNewItemDialog(false);
            setNewItemName('');
            setNewItemDesc('');
            showSnackbar("Item created successfully", "success");
        } catch (error) {
            console.error("Failed to create item", error);
            showSnackbar("Failed to create item", "error");
        }
    };

    const handleCreateRole = async () => {
        try {
            const newRole = await createRole(newRoleName, newRoleDesc);
            setRoles([...roles, newRole]);
            setSelectedRoles([...selectedRoles, newRole]);
            setOpenNewRoleDialog(false);
            setNewRoleName('');
            setNewRoleDesc('');
            showSnackbar("Role created successfully", "success");
        } catch (error) {
            console.error("Failed to create role", error);
            showSnackbar("Failed to create role", "error");
        }
    };

    const validateForm = () => {
        const newErrors: { [key: string]: string } = {};
        if (!coordinates) newErrors.location = "Please select a valid location from the dropdown.";
        if (!startDatetime || !startDatetime.isValid()) newErrors.datetime = "Please select a valid date and time.";
        if (selectedRoles.length === 0) newErrors.roles = "Please select at least one role.";

        setErrors(newErrors);
        return Object.keys(newErrors).length === 0;
    };

    const handleSubmit = async () => {
        if (!validateForm()) {
            showSnackbar("Please fix the errors in the form.", "error");
            return;
        }

        const jobData = {
            longitude: coordinates!.lng,
            latitude: coordinates!.lat,
            ...locationDetails,
            role_ids: selectedRoles.map(r => r.role_id),
            item_ids: selectedItems.map(i => i.item_id),
            start_datetime: startDatetime!.toISOString(),
            worker_ids: [],
        };

        try {
            if (jobId) {
                await updateJob(jobId, jobData);
                showSnackbar("Job updated successfully!", "success");
            } else {
                await createJob(jobData);
                showSnackbar("Job created successfully!", "success");
                // Reset form only on create
                setAddress('');
                setCoordinates(null);
                setSelectedRoles([]);
                setSelectedItems([]);
                setLocationDetails({});
                setStartDatetime(null);
                setErrors({});
            }

            // Navigate back to list after short delay
            setTimeout(() => navigate('/jobs'), 1500);

        } catch (error) {
            console.error("Failed to save job", error);
            showSnackbar("Failed to save job", "error");
        }
    };

    const showSnackbar = (message: string, severity: 'success' | 'error') => {
        setSnackbar({ open: true, message, severity });
    };

    if (!isLoaded) return <div>Loading Maps...</div>;

    const commonInputSx = {
        '& .MuiInputBase-root': { color: 'var(--text)', backgroundColor: 'var(--bg)' },
        '& .MuiInputLabel-root': { color: 'var(--text-muted)' },
        '& .MuiOutlinedInput-notchedOutline': { borderColor: 'var(--border-muted)' }, // Lightened border
        '&:hover .MuiOutlinedInput-notchedOutline': { borderColor: 'var(--highlight)' },
        '& .MuiSvgIcon-root': { color: 'var(--text-muted)' },
    };

    return (
        <LocalizationProvider dateAdapter={AdapterDayjs}>
            <Paper elevation={3} sx={{
                p: 4,
                maxWidth: 800,
                mx: 'auto',
                mt: 4,
                backgroundColor: 'var(--bg-light)',
                color: 'var(--text)',
                border: '1px solid var(--border)'
            }}>
                <Typography variant="h4" gutterBottom sx={{ mb: 4, color: 'var(--primary)', fontWeight: 'bold' }}>
                    {jobId ? 'Edit Job' : 'Create New Job'}
                </Typography>

                <Stack spacing={4}>
                    {/* Location Section */}
                    <Box>
                        <Stack direction="row" alignItems="center" spacing={1} mb={1}>
                            <Typography variant="h6" sx={{ color: 'var(--text)' }}>Location</Typography>
                            <Tooltip title="Search for an address, business, or place of interest.">
                                <InfoIcon fontSize="small" sx={{ color: 'var(--text-muted)' }} />
                            </Tooltip>
                        </Stack>
                        <GoogleAutocomplete
                            onLoad={onLoadAutocomplete}
                            onPlaceChanged={onPlaceChanged}
                        >
                            <TextField
                                fullWidth
                                error={!!errors.location}
                                helperText={errors.location}
                                label="Search Location"
                                value={address}
                                onChange={(e) => setAddress(e.target.value)}
                                placeholder="Search by address, facility, or region..."
                                sx={commonInputSx}
                            />
                        </GoogleAutocomplete>
                        {coordinates && (
                            <Typography variant="caption" sx={{ mt: 1, display: 'block', color: 'var(--success)' }}>
                                ✓ Location selected: {coordinates.lat.toFixed(4)}, {coordinates.lng.toFixed(4)}
                            </Typography>
                        )}
                    </Box>

                    <Divider sx={{ borderColor: 'var(--border-muted)' }} />

                    {/* Datetime Section */}
                    <Box>
                        <Stack direction="row" alignItems="center" spacing={1} mb={1}>
                            <Typography variant="h6" sx={{ color: 'var(--text)' }}>Start Date & Time</Typography>
                            <Tooltip title="When should the job start?">
                                <InfoIcon fontSize="small" sx={{ color: 'var(--text-muted)' }} />
                            </Tooltip>
                        </Stack>
                        <DateTimePicker
                            label="Select Date & Time"
                            value={startDatetime}
                            onChange={(newValue) => {
                                setStartDatetime(newValue);
                                setErrors(prev => ({ ...prev, datetime: '' }));
                            }}
                            slotProps={{
                                textField: {
                                    fullWidth: true,
                                    error: !!errors.datetime,
                                    helperText: errors.datetime,
                                    placeholder: "DD/MM/YYYY — HH:MM",
                                    sx: {
                                        ...commonInputSx,
                                        '& .MuiIconButton-root': { color: 'var(--primary)' }
                                    }
                                }
                            }}
                        />
                    </Box>

                    <Divider sx={{ borderColor: 'var(--border-muted)' }} />

                    {/* Roles Section */}
                    <Box>
                        <Stack direction="row" alignItems="center" spacing={1} mb={1}>
                            <Typography variant="h6" sx={{ color: 'var(--text)' }}>Required Roles</Typography>
                            <Tooltip title="Select the roles required for this job. You can add multiple.">
                                <InfoIcon fontSize="small" sx={{ color: 'var(--text-muted)' }} />
                            </Tooltip>
                        </Stack>
                        <Autocomplete
                            multiple
                            options={roles}
                            getOptionLabel={(option) => option.name || 'Unknown Role'}
                            value={selectedRoles}
                            isOptionEqualToValue={(option, value) => option.role_id === value.role_id}
                            onChange={(_, newValue) => {
                                setSelectedRoles(newValue);
                                setErrors(prev => ({ ...prev, roles: '' }));
                            }}
                            renderInput={(params) => (
                                <TextField
                                    {...params}
                                    label="Select Roles"
                                    placeholder="Select one or more roles..."
                                    error={!!errors.roles}
                                    helperText={errors.roles}
                                    sx={commonInputSx}
                                />
                            )}
                            renderTags={(value, getTagProps) =>
                                value.map((option, index) => (
                                    <Chip
                                        {...getTagProps({ index })}
                                        label={option.name}
                                        sx={{ backgroundColor: 'var(--highlight)', color: 'var(--text)' }}
                                    />
                                ))
                            }
                            noOptionsText={
                                <Typography variant="body2" sx={{ color: 'var(--text-muted)', p: 1 }}>
                                    No roles found. Create a new one below.
                                </Typography>
                            }
                        />
                        <Button
                            startIcon={<AddIcon />}
                            onClick={() => setOpenNewRoleDialog(true)}
                            sx={{ mt: 1, color: 'var(--primary)', textTransform: 'none' }}
                        >
                            Add a Custom Role
                        </Button>
                    </Box>

                    <Divider sx={{ borderColor: 'var(--border-muted)' }} />

                    {/* Items Section */}
                    <Box>
                        <Stack direction="row" alignItems="center" spacing={1} mb={1}>
                            <Typography variant="h6" sx={{ color: 'var(--text)' }}>Items & Equipment</Typography>
                            <Tooltip title="Select any equipment or items needed for the job.">
                                <InfoIcon fontSize="small" sx={{ color: 'var(--text-muted)' }} />
                            </Tooltip>
                        </Stack>
                        <Autocomplete
                            multiple
                            options={items}
                            getOptionLabel={(option) => option.name || 'Unknown Item'}
                            value={selectedItems}
                            isOptionEqualToValue={(option, value) => option.item_id === value.item_id}
                            onChange={(_, newValue) => setSelectedItems(newValue)}
                            renderInput={(params) => (
                                <TextField
                                    {...params}
                                    label="Select Items"
                                    placeholder="Select items..."
                                    sx={commonInputSx}
                                />
                            )}
                            renderTags={(value, getTagProps) =>
                                value.map((option, index) => (
                                    <Chip
                                        {...getTagProps({ index })}
                                        label={option.name}
                                        sx={{ backgroundColor: 'var(--highlight)', color: 'var(--text)' }}
                                    />
                                ))
                            }
                            noOptionsText={
                                <Button onMouseDown={() => setOpenNewItemDialog(true)} sx={{ color: 'var(--primary)' }}>
                                    Create "{newItemName || 'New Item'}"
                                </Button>
                            }
                        />
                        <Button
                            startIcon={<AddIcon />}
                            onClick={() => setOpenNewItemDialog(true)}
                            sx={{ mt: 1, color: 'var(--primary)', textTransform: 'none' }}
                        >
                            Add Custom Equipment
                        </Button>
                    </Box>

                    <Box sx={{ mt: 4 }}>
                        <Button
                            variant="contained"
                            size="large"
                            onClick={handleSubmit}
                            fullWidth
                            disabled={!coordinates || !startDatetime || selectedRoles.length === 0}
                            sx={{
                                py: 1.5,
                                fontSize: '1.1rem',
                                fontWeight: 'bold',
                                backgroundColor: 'var(--primary)',
                                color: 'var(--bg-dark)',
                                '&:hover': { backgroundColor: 'var(--secondary)' },
                                '&.Mui-disabled': {
                                    backgroundColor: 'var(--primary)',
                                    color: 'var(--bg-dark)',
                                    opacity: 0.4
                                }
                            }}
                        >
                            {jobId ? 'Update Job' : 'Create Job'}
                        </Button>
                        {(!coordinates || !startDatetime || selectedRoles.length === 0) && (
                            <Typography variant="caption" align="center" display="block" sx={{ mt: 1, color: 'var(--text-muted)' }}>
                                Please fill in all required fields to continue.
                            </Typography>
                        )}
                    </Box>
                </Stack>

                {/* New Item Dialog */}
                <Dialog
                    open={openNewItemDialog}
                    onClose={() => setOpenNewItemDialog(false)}
                    PaperProps={{
                        sx: {
                            backgroundColor: 'var(--bg-light)',
                            color: 'var(--text)',
                            border: '1px solid var(--border)'
                        }
                    }}
                >
                    <DialogTitle sx={{ color: 'var(--primary)' }}>Create New Item</DialogTitle>
                    <DialogContent>
                        <TextField
                            autoFocus
                            margin="dense"
                            label="Item Name"
                            fullWidth
                            value={newItemName}
                            onChange={(e) => setNewItemName(e.target.value)}
                            sx={commonInputSx}
                        />
                        <TextField
                            margin="dense"
                            label="Description"
                            fullWidth
                            value={newItemDesc}
                            onChange={(e) => setNewItemDesc(e.target.value)}
                            sx={commonInputSx}
                        />
                    </DialogContent>
                    <DialogActions>
                        <Button onClick={() => setOpenNewItemDialog(false)} sx={{ color: 'var(--text-muted)' }}>Cancel</Button>
                        <Button onClick={handleCreateItem} variant="contained" sx={{ backgroundColor: 'var(--primary)', color: 'var(--bg-dark)' }}>Create</Button>
                    </DialogActions>
                </Dialog>

                {/* New Role Dialog */}
                <Dialog
                    open={openNewRoleDialog}
                    onClose={() => setOpenNewRoleDialog(false)}
                    PaperProps={{
                        sx: {
                            backgroundColor: 'var(--bg-light)',
                            color: 'var(--text)',
                            border: '1px solid var(--border)'
                        }
                    }}
                >
                    <DialogTitle sx={{ color: 'var(--primary)' }}>Create New Role</DialogTitle>
                    <DialogContent>
                        <TextField
                            autoFocus
                            margin="dense"
                            label="Role Name"
                            fullWidth
                            value={newRoleName}
                            onChange={(e) => setNewRoleName(e.target.value)}
                            sx={commonInputSx}
                        />
                        <TextField
                            margin="dense"
                            label="Description"
                            fullWidth
                            value={newRoleDesc}
                            onChange={(e) => setNewRoleDesc(e.target.value)}
                            sx={commonInputSx}
                        />
                    </DialogContent>
                    <DialogActions>
                        <Button onClick={() => setOpenNewRoleDialog(false)} sx={{ color: 'var(--text-muted)' }}>Cancel</Button>
                        <Button onClick={handleCreateRole} variant="contained" sx={{ backgroundColor: 'var(--primary)', color: 'var(--bg-dark)' }}>Create</Button>
                    </DialogActions>
                </Dialog>

                {/* Feedback Snackbar */}
                <Snackbar
                    open={snackbar.open}
                    autoHideDuration={6000}
                    onClose={() => setSnackbar({ ...snackbar, open: false })}
                >
                    <Alert severity={snackbar.severity} onClose={() => setSnackbar({ ...snackbar, open: false })}>
                        {snackbar.message}
                    </Alert>
                </Snackbar>
            </Paper>
        </LocalizationProvider>
    );
};

export default JobCreationForm;
