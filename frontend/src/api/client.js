import axios from 'axios'

const API_BASE_URL = import.meta.env.DEV 
  ? '/api'
  : 'https://qhapaq-lingua.onrender.com/api'

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})