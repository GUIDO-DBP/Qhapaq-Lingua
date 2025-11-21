import axios from 'axios'

// ACTUALIZA con tu URL real de Render
const API_BASE_URL = import.meta.env.DEV 
  ? '/api'
  : 'https://qhapaq-lingua.onrender.com/api'  // ← ESTA URL

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})