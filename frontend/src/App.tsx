import React from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import Layout from './components/Layout'
import JobCreatePage from './pages/JobCreatePage'
import JobsPage from './pages/JobsPage'
import JobEditPage from './pages/JobEditPage'
import JobPage from './pages/JobPage'
import WorkersPage from './pages/WorkersPage'
import ItemsPage from './pages/ItemsPage'
import WorkerPage from './pages/WorkerPage'
import Dashboard from './pages/DashboardPage'
import ItemPage from './pages/ItemPage'

const App: React.FC = () => {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<Layout />}>
                    <Route index element={<Navigate to="/dashboard" replace />} />
                    <Route path="dashboard" element={<Dashboard />} />
                    <Route path="jobs" element={<JobsPage />} />
                    <Route path="jobs/:id" element={<JobPage />} />
                    <Route path="job/create" element={<JobCreatePage />} />
                    <Route path="jobs/:id/update" element={<JobEditPage />} />
                    <Route path="workers" element={<WorkersPage />} />
                    <Route path="workers/:id" element={<WorkerPage />} />
                    <Route path="items" element={<ItemsPage />} />
                    <Route path="items/:id" element={<ItemPage />} />
                    <Route path="*" element={<Navigate to="/dashboard" replace />} />
                </Route>
            </Routes>
        </BrowserRouter>
    )
}

export default App
