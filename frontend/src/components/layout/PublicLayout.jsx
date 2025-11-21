import React from 'react'
import { Link, NavLink, Outlet } from 'react-router-dom'

const PublicLayout = () => {
  return (
    <div className="min-h-screen bg-ql-hero text-slate-100 flex flex-col">
      {/* Navbar */}
      <header className="backdrop-blur bg-slate-900/40 border-b border-slate-700/40 sticky top-0 z-20">
        <nav className="max-w-6xl mx-auto flex items-center justify-between px-4 py-3">
          <Link to="/" className="flex items-center gap-2">
            <span className="text-xl font-black tracking-tight">
              Qhapaq <span className="text-ql-secondary">Lingua</span>
            </span>
          </Link>
          <div className="flex items-center gap-6 text-sm">
            <NavLink to="/explorar" className="hover:text-ql-secondary">
              Explorar
            </NavLink>
            <NavLink to="/alertas" className="hover:text-ql-secondary">
              Alertas
            </NavLink>
            <NavLink
              to="/admin"
              className="px-3 py-1.5 rounded-full bg-gradient-to-r from-ql-primary to-ql-secondary text-xs font-semibold"
            >
              Panel administración
            </NavLink>
          </div>
        </nav>
      </header>

      {/* Contenido */}
      <main className="flex-1">
        <Outlet />
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-800 bg-slate-950/80">
        <div className="max-w-6xl mx-auto px-4 py-6 text-xs text-slate-400 flex justify-between">
          <span>© {new Date().getFullYear()} Qhapaq Lingua · Puno, Perú</span>
          <span>Lenguas: Aymara · Quechua · Español</span>
        </div>
      </footer>
    </div>
  )
}

export default PublicLayout
