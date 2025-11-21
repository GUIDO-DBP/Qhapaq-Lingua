import React from 'react'

const Card = ({ children, className = '' }) => {
  return (
    <div
      className={`bg-ql-card/80 border border-slate-700/60 rounded-2xl p-4 shadow-lg shadow-black/30 ${className}`}
    >
      {children}
    </div>
  )
}

export default Card
