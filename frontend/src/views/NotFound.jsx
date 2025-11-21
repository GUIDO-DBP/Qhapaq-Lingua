import React from 'react'
import { Link } from 'react-router-dom'

const NotFound = () => (
  <div className="min-h-[60vh] flex flex-col items-center justify-center text-center px-4">
    <h1 className="text-4xl font-black mb-3">404</h1>
    <p className="text-sm text-slate-300 mb-4">No encontramos la página que buscabas.</p>
    <Link
      to="/"
      className="text-xs px-4 py-2 rounded-full bg-slate-800 border border-slate-600 hover:bg-slate-700"
    >
      Volver al inicio
    </Link>
  </div>
)

export default NotFound
