import React from 'react'
import { motion } from 'framer-motion'
import { useAlerts } from '../api/hooks'
import Card from '../components/ui/Card'

const levelColor = (nivel) => {
  if (!nivel) return 'bg-slate-700'
  const n = nivel.toLowerCase()
  if (n.includes('alta')) return 'bg-red-600'
  if (n.includes('media')) return 'bg-amber-500'
  if (n.includes('baja')) return 'bg-emerald-500'
  return 'bg-slate-600'
}

const AlertsPublic = () => {
  const { data: alertas = [], isLoading } = useAlerts()

  return (
    <div className="max-w-5xl mx-auto px-4 py-10">
      <div className="mb-6">
        <h1 className="text-2xl font-bold mb-1">Alertas lingüísticas</h1>
        <p className="text-sm text-slate-300">
          El sistema marca vocablos o relaciones que requieren atención especial: baja frecuencia,
          nuevas incorporaciones o cambios importantes.
        </p>
      </div>

      {isLoading && <p className="text-sm text-slate-300">Cargando alertas...</p>}

      <div className="grid md:grid-cols-2 gap-4">
        {alertas.map((a, idx) => (
          <motion.div
            key={a.id}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: idx * 0.03 }}
          >
            <Card className="h-full flex flex-col gap-2">
              <div className="flex items-center justify-between">
                <span className="text-xs font-semibold uppercase tracking-wide text-slate-400">
                  {a.tipo || 'Alerta'}
                </span>
                <span
                  className={`text-[10px] px-2 py-0.5 rounded-full font-semibold uppercase tracking-wide text-white ${levelColor(
                    a.nivel
                  )}`}
                >
                  {a.nivel || 'sin nivel'}
                </span>
              </div>
              <p className="text-sm">{a.mensaje}</p>
              {a.palabra_id && (
                <p className="text-xs text-slate-400">
                  Palabra relacionada: <span className="font-semibold">#{a.palabra_id}</span>
                </p>
              )}
            </Card>
          </motion.div>
        ))}
      </div>
      {alertas.length === 0 && !isLoading && (
        <p className="text-xs text-slate-400 mt-4">No hay alertas registradas por el momento.</p>
      )}
    </div>
  )
}

export default AlertsPublic
