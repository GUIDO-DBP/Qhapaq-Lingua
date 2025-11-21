import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-swc'

export default defineConfig({
  plugins: [react()],
  base: '/Qhapaq-Lingua/', // ← AÑADE ESTA LÍNEA (mismo nombre que tu repo)
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true,
        secure: false,
        rewrite: (path) => path
      }
    },
  },
  build: {
    outDir: 'dist' // ← AÑADE ESTO (opcional pero recomendado)
  }
})