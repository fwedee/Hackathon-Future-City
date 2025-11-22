import React from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import Layout from './components/Layout'
import HomePage from './pages/HomePage'
import JobsPage from './pages/JobsPage'
import JobsListPage from './pages/JobsListPage'
import JobEditPage from './pages/JobEditPage'
import JobDetailsPage from './pages/JobDetailsPage'
import WorkersPage from './pages/WorkersPage'
import ItemsPage from './pages/ItemsPage'
import WorkerPage from './pages/WorkerPage'

const App: React.FC = () => {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<Layout />}>
                    <Route index element={<HomePage />} />
                    <Route path="jobs" element={<JobsListPage />} />
                    <Route path="job/create" element={<JobsPage />} />
                    <Route path="jobs/:id" element={<JobDetailsPage />} />
                    <Route path="jobs/:id/update" element={<JobEditPage />} />
                    <Route path="workers" element={<WorkersPage />} />
                    <Route path="workers/:id" element={<WorkerPage />} />
                    <Route path="items" element={<ItemsPage />} />
                </Route>
                <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
        </BrowserRouter>
    )
}

export default App
