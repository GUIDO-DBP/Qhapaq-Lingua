import axios from 'axios'

// DETECTA AUTOMÁTICAMENTE si está en desarrollo o producción
const isDevelopment = import.meta.env.DEV
const API_BASE_URL = isDevelopment 
  ? '/api'  // ← Desarrollo: usa proxy local
  : 'https://qhapaq-backend.onrender.com/api'  // ← Producción: backend en Render

console.log(`🔧 Modo: ${isDevelopment ? 'Desarrollo' : 'Producción'}`)
console.log(`🌐 API URL: ${API_BASE_URL}`)

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})