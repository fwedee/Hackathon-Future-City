import axios from 'axios';

const API_URL = 'http://localhost:8000';

const api = axios.create({
    baseURL: API_URL,
});

export interface Worker {
    worker_id: string;
    name?: string;
    fk_branch_id?: string;
}

export interface Item {
    item_id: string;
    name?: string;
    description?: string;
    fk_branch_id?: string;
}

export interface Role {
    role_id: string;
    name?: string;
    description?: string;
}

export interface JobCreate {
    longitude: number;
    latitude: number;
    country?: string;
    city?: string;
    house_number?: string;
    street?: string;
    postal_code?: string;
    start_datetime?: string;
    end_datetime?: string;
    worker_ids: string[];
    item_ids: string[];
    role_ids: string[];
}

export interface Job extends JobCreate {
    job_id: string;
    workers: Worker[];
    items: Item[];
    roles: Role[];
}

export const fetchWorkers = async (): Promise<Worker[]> => {
    const response = await api.get('/workers');
    return response.data;
};

export const fetchItems = async (): Promise<Item[]> => {
    const response = await api.get('/items');
    return response.data;
};

export const fetchRoles = async (): Promise<Role[]> => {
    const response = await api.get('/roles');
    return response.data;
};

export const createItem = async (name: string, description?: string): Promise<Item> => {
    const response = await api.post('/items', { name, description });
    return response.data;
};

export const createRole = async (name: string, description?: string): Promise<Role> => {
    const response = await api.post('/roles', { name, description });
    return response.data;
};

export const fetchJobs = async (): Promise<Job[]> => {
    const response = await api.get('/jobs');
    return response.data;
};

export const fetchJob = async (jobId: string): Promise<Job> => {
    const response = await api.get(`/jobs/${jobId}`);
    return response.data;
};

export const createJob = async (job: JobCreate) => {
    const response = await api.post('/jobs', job);
    return response.data;
};

export const updateJob = async (jobId: string, job: JobCreate) => {
    const response = await api.put(`/jobs/${jobId}`, job);
    return response.data;
};

export const deleteJob = async (jobId: string) => {
    const response = await api.delete(`/jobs/${jobId}`);
    return response.data;
};
