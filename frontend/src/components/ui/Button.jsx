import React from 'react'
import { motion } from 'framer-motion'

const Button = ({ children, variant = 'primary', className = '', ...props }) => {
  const base =
    'inline-flex items-center justify-center rounded-full text-sm font-semibold px-4 py-2 transition'
  const variants = {
    primary: 'bg-gradient-to-r from-ql-primary to-ql-secondary text-white shadow-lg shadow-ql-primary/30',
    ghost: 'border border-slate-600 text-slate-100 hover:bg-slate-800',
    subtle: 'bg-slate-800/70 text-slate-100 hover:bg-slate-700/80'
  }
  return (
    <motion.button
      whileHover={{ scale: 1.02, y: -1 }}
      whileTap={{ scale: 0.98 }}
      className={`${base} ${variants[variant]} ${className}`}
      {...props}
    >
      {children}
    </motion.button>
  )
}

export default Button
