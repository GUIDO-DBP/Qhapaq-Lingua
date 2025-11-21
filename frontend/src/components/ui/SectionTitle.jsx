import React from 'react'

const SectionTitle = ({ eyebrow, title, subtitle }) => {
  return (
    <div className="mb-6 text-center">
      {eyebrow && (
        <p className="text-xs font-semibold tracking-[0.25em] uppercase text-ql-accent mb-2">
          {eyebrow}
        </p>
      )}
      <h2 className="text-3xl font-bold tracking-tight mb-2">{title}</h2>
      {subtitle && <p className="text-sm text-slate-300 max-w-xl mx-auto">{subtitle}</p>}
    </div>
  )
}

export default SectionTitle
