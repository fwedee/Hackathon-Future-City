import React from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import Layout from './components/Layout'
import JobsPage from './pages/JobsPage'
import JobsListPage from './pages/JobsListPage'
import JobEditPage from './pages/JobEditPage'
import JobDetailsPage from './pages/JobDetailsPage'
import WorkersPage from './pages/WorkersPage'
import ItemsPage from './pages/ItemsPage'
import WorkerPage from './pages/WorkerPage'
import Dashboard from './pages/Dashboard'

const App: React.FC = () => {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<Layout />}>
                    <Route index element={<Navigate to="/dashboard" replace />} />
                    <Route path="dashboard" element={<Dashboard />} />
                    <Route path="jobs" element={<JobsListPage />} />
                    <Route path="job/create" element={<JobsPage />} />
                    <Route path="jobs/:id" element={<JobDetailsPage />} />
                    <Route path="jobs/:id/update" element={<JobEditPage />} />
                    <Route path="workers" element={<WorkersPage />} />
                    <Route path="workers/:id" element={<WorkerPage />} />
                    <Route path="items" element={<ItemsPage />} />
                    <Route path="*" element={<Navigate to="/dashboard" replace />} />
                </Route>
            </Routes>
        </BrowserRouter>
    )
}

export default App
