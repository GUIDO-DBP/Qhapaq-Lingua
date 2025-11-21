import React from 'react'
import { Routes, Route } from 'react-router-dom'

import PublicLayout from './components/layout/PublicLayout'
import AdminLayout from './components/layout/AdminLayout'

import Home from './views/Home'
import Explore from './views/Explore'
import AlertsPublic from './views/AlertsPublic'

import AdminDashboard from './views/admin/AdminDashboard'
import AdminWords from './views/admin/AdminWords'
import AdminGraphs from './views/admin/AdminGraphs'
import AdminAlerts from './views/admin/AdminAlerts'

import NotFound from './views/NotFound'

const App = () => {
  return (
    <Routes>
      <Route element={<PublicLayout />}>
        <Route path="/" element={<Home />} />
        <Route path="/explorar" element={<Explore />} />
        <Route path="/alertas" element={<AlertsPublic />} />
      </Route>

      <Route path="/admin" element={<AdminLayout />}>
        <Route index element={<AdminDashboard />} />
        <Route path="palabras" element={<AdminWords />} />
        <Route path="grafos" element={<AdminGraphs />} />
        <Route path="alertas" element={<AdminAlerts />} />
      </Route>

      <Route path="*" element={<NotFound />} />
    </Routes>
  )
}

export default App
