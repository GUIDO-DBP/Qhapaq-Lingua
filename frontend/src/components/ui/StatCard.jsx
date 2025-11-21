import React from 'react'
import Card from './Card'

const StatCard = ({ label, value, helper }) => (
  <Card className="flex flex-col gap-1">
    <p className="text-xs uppercase tracking-wide text-slate-400">{label}</p>
    <p className="text-2xl font-bold">{value}</p>
    {helper && <p className="text-xs text-slate-400">{helper}</p>}
  </Card>
)

export default StatCard
