import React from 'react'
import { Outlet } from 'react-router-dom'
import Navbar from './Navbar'
import Footer from './Footer'

const Layout: React.FC = () => {
  return (
    <div className="layout-container">
      <header className="app-header">
        <Navbar />
      </header>

      <main className="app-body">
        <Outlet />
      </main>

      <footer className="app-footer">
        <Footer />
      </footer>
    </div>
  )
}

export default Layout
