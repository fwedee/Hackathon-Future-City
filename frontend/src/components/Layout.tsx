import React from 'react'
 
import { Outlet } from 'react-router-dom'
import Navbar from './Navbar'
import Footer from './Footer'

const Layout: React.FC = () => {
  return (
    <>
      <header className="app-header">
        <Navbar />
      </header>

      <main className="app-body">
        <div className="content-box">
          <div className="content-inner">
            <Outlet />
          </div>
        </div>
      </main>

      <footer className="app-footer">
        <Footer />
      </footer>
    </>
  )
}

export default Layout
