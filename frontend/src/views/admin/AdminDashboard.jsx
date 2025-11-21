import React from 'react'
import StatCard from '../../components/ui/StatCard'
import { useAlerts } from '../../api/hooks'

const AdminDashboard = () => {
  const { data: alertas = [] } = useAlerts()
  const criticas = alertas.filter((a) => (a.nivel || '').toLowerCase().includes('alta')).length

  return (
    <div className="space-y-6">
      <h1 className="text-xl font-bold mb-2">Resumen del sistema</h1>
      <div className="grid sm:grid-cols-3 gap-4">
        <StatCard label="Alertas registradas" value={alertas.length} />
        <StatCard label="Alertas críticas" value={criticas} helper="Nivel alto de prioridad" />
        <StatCard
          label="Integridad del sistema"
          value="OK"
          helper="Conexión con backend Flask activa (si no ves errores en consola)"
        />
      </div>
    </div>
  )
}

export default AdminDashboard
