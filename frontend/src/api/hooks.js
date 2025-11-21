import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { api } from './client'

// Buscar palabras - CORREGIDO: siempre hacer request, incluso con término vacío
export const useSearchWords = (termino) =>
  useQuery({
    queryKey: ['palabras', 'buscar', termino],
    queryFn: async () => {
      // SIEMPRE hacer la request al backend
      const res = await api.get(`/palabras/buscar`, { 
        params: { termino: termino || '' }  // ← Enviar string vacío si no hay término
      })
      return res.data
    },
    enabled: true  // ← SIEMPRE activado para que funcione en el admin
  })

// Detalle palabra
export const useWordDetail = (id) =>
  useQuery({
    queryKey: ['palabras', id],
    queryFn: async () => {
      const res = await api.get(`/palabras/${id}`)
      return res.data
    },
    enabled: !!id
  })

// Grafo por palabra
export const useWordGraph = (id) =>
  useQuery({
    queryKey: ['grafos', 'palabra', id],
    queryFn: async () => {
      const res = await api.get(`/grafos/palabra/${id}`)
      return res.data
    },
    enabled: !!id
  })

// Alertas
export const useAlerts = () =>
  useQuery({
    queryKey: ['alertas'],
    queryFn: async () => {
      const res = await api.get('/alertas/')
      return res.data
    }
  })

// Crear alerta
export const useCreateAlert = () => {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: async (payload) => {
      const res = await api.post('/alertas/crear', payload)
      return res.data
    },
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['alertas'] })
    }
  })
}

// Marcar alerta leída
export const useMarkAlertRead = () => {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: async (id) => {
      const res = await api.put(`/alertas/${id}/leer`)
      return res.data
    },
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['alertas'] })
    }
  })
}