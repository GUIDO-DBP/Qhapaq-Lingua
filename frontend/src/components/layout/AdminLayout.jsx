import React from 'react'
import { NavLink, Outlet, Link } from 'react-router-dom'

const AdminLayout = () => {
  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex">
      {/* Sidebar */}
      <aside className="w-64 border-r border-slate-800 bg-slate-950/90">
        <div className="px-5 py-4 border-b border-slate-800">
          <Link to="/" className="block text-lg font-black tracking-tight">
            Qhapaq <span className="text-ql-primary">Lingua</span>
          </Link>
          <p className="text-xs text-slate-400 mt-1">Panel de administración</p>
        </div>
        <nav className="px-4 py-4 space-y-2 text-sm">
          <NavLink
            to="/admin"
            end
            className={({ isActive }) =>
              `block px-3 py-2 rounded-md ${
                isActive ? 'bg-slate-800 text-ql-accent' : 'text-slate-300 hover:bg-slate-800/60'
              }`
            }
          >
            Dashboard
          </NavLink>
          <NavLink
            to="/admin/palabras"
            className={({ isActive }) =>
              `block px-3 py-2 rounded-md ${
                isActive ? 'bg-slate-800 text-ql-accent' : 'text-slate-300 hover:bg-slate-800/60'
              }`
            }
          >
            Palabras
          </NavLink>
          <NavLink
            to="/admin/grafos"
            className={({ isActive }) =>
              `block px-3 py-2 rounded-md ${
                isActive ? 'bg-slate-800 text-ql-accent' : 'text-slate-300 hover:bg-slate-800/60'
              }`
            }
          >
            Grafos
          </NavLink>
          <NavLink
            to="/admin/alertas"
            className={({ isActive }) =>
              `block px-3 py-2 rounded-md ${
                isActive ? 'bg-slate-800 text-ql-accent' : 'text-slate-300 hover:bg-slate-800/60'
              }`
            }
          >
            Alertas
          </NavLink>
        </nav>
      </aside>

      {/* Contenido */}
      <div className="flex-1 flex flex-col">
        <header className="border-b border-slate-800 px-6 py-3 flex justify-between items-center">
          <h1 className="text-sm font-semibold tracking-wide uppercase text-slate-300">
            Administración
          </h1>
          <span className="text-xs text-slate-500">v1.0</span>
        </header>
        <main className="flex-1 p-6">
          <Outlet />
        </main>
      </div>
    </div>
  )
}

export default AdminLayout
