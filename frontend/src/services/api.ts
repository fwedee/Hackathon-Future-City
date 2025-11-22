import axios from 'axios';

const API_URL = 'http://localhost:8000';

const api = axios.create({
    baseURL: API_URL,
});

export interface Branch {
    branch_id: string;
    branch_name?: string;
    latitude?: number;
    longitude?: number;
}

export interface Worker {
    worker_id: string;
    worker_first_name?: string;
    worker_last_name?: string;
    worker_phone_number?: string;
    fk_branch_id?: string;
    branch?: Branch;
    roles?: Role[];
}

export interface Item {
    item_id: string;
    item_name?: string;
    item_description?: string;
    fk_branch_id?: string;
}

export interface Role {
    role_id: string;
    role_name?: string;
    role_description?: string;
}

export interface JobCreate {
    job_name?: string;
    job_description?: string;
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
    items: { item_id: string; required_quantity: number }[];
    role_ids: string[];
}

export interface JobItemLink {
    item_id: string;
    required_quantity: number;
    item: Item;
}

export interface Job {
    job_id: string;
    job_name?: string;
    job_description?: string;
    longitude: number;
    latitude: number;
    country?: string;
    city?: string;
    house_number?: string;
    street?: string;
    postal_code?: string;
    start_datetime?: string;
    end_datetime?: string;
    workers: Worker[];
    item_links: JobItemLink[];
    roles: Role[];
}

export const fetchWorkers = async (): Promise<Worker[]> => {
    const response = await api.get('/workers');
    return response.data;
};

export const fetchWorker = async (workerId: string): Promise<Worker> => {
    const response = await api.get(`/workers/${workerId}`);
    return response.data;
};

export const fetchJobsByWorkerId = async (workerId: string): Promise<Job[]> => {
    const response = await api.get(`/worker/${workerId}/jobs`);
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

export const createItem = async (item_name: string, item_description?: string): Promise<Item> => {
    const response = await api.post('/items', { item_name, item_description });
    return response.data;
};

export const createRole = async (role_name: string, role_description?: string): Promise<Role> => {
    const response = await api.post('/roles', { role_name, role_description });
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
