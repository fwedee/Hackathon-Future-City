import React from 'react';
import { useParams } from 'react-router-dom';
import JobCreationForm from '../components/JobCreationForm';

const JobEditPage: React.FC = () => {
    const { id } = useParams<{ id: string }>();
    return <JobCreationForm jobId={id} />;
};

export default JobEditPage;
