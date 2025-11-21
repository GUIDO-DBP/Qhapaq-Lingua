import React, { useState } from 'react'
import Card from '../../components/ui/Card'
import Button from '../../components/ui/Button'
import { useSearchWords } from '../../api/hooks'
import { api } from '../../api/client'

const AdminWords = () => {
  const [termino, setTermino] = useState('')
  const [form, setForm] = useState({
    palabra: '',
    lengua: '',
    definicion: '',
    contexto_cultural: ''
  })
  
  const { data: resultadosData = {}, refetch } = useSearchWords(termino)
  const resultados = resultadosData.resultados || []

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  const handleCreate = async (e) => {
    e.preventDefault()
    try {
      await api.post('/palabras', form)
      setForm({ palabra: '', lengua: '', definicion: '', contexto_cultural: '' })
      refetch()
    } catch (err) {
      console.error('Error creando palabra:', err)
      alert('Error al crear la palabra: ' + (err.response?.data?.error || err.message))
    }
  }

  return (
    <div className="space-y-6">
      <h1 className="text-xl font-bold">Gestión de palabras</h1>

      <div className="grid lg:grid-cols-[minmax(0,0.8fr)_minmax(0,1.2fr)] gap-5">
        {/* Formulario */}
        <Card>
          <h2 className="text-sm font-semibold mb-3 uppercase tracking-wide text-slate-300">
            Registrar nueva palabra
          </h2>
          <form className="space-y-3" onSubmit={handleCreate}>
            <input
              name="palabra"
              value={form.palabra}
              onChange={handleChange}
              placeholder="Palabra"
              className="w-full text-sm rounded-md bg-slate-900/80 border border-slate-700 px-3 py-2"
              required
            />
            <input
              name="lengua"
              value={form.lengua}
              onChange={handleChange}
              placeholder="Lengua (aymara / quechua)"
              className="w-full text-sm rounded-md bg-slate-900/80 border border-slate-700 px-3 py-2"
              required
            />
            <textarea
              name="definicion"
              value={form.definicion}
              onChange={handleChange}
              placeholder="Definición"
              className="w-full text-sm rounded-md bg-slate-900/80 border border-slate-700 px-3 py-2"
              required
            />
            <textarea
              name="contexto_cultural"
              value={form.contexto_cultural}
              onChange={handleChange}
              placeholder="Contexto cultural"
              className="w-full text-sm rounded-md bg-slate-900/80 border border-slate-700 px-3 py-2"
            />

            <Button type="submit">Guardar palabra</Button>
          </form>
        </Card>

        {/* Búsqueda / tabla */}
        <Card>
          <div className="flex flex-col md:flex-row gap-3 mb-3 md:items-center justify-between">
            <h2 className="text-sm font-semibold uppercase tracking-wide text-slate-300">
              Palabras registradas {resultados.length > 0 && `(${resultados.length})`}
            </h2>
            <input
              type="text"
              placeholder="Buscar..."
              value={termino}
              onChange={(e) => setTermino(e.target.value)}
              className="text-sm rounded-full bg-slate-900/80 border border-slate-700 px-3 py-1.5 w-full md:w-56"
            />
          </div>
          <div className="max-h-[340px] overflow-auto text-xs">
            <table className="w-full border-collapse">
              <thead className="bg-slate-900/80 sticky top-0">
                <tr>
                  <th className="text-left py-2 px-2 border-b border-slate-700">ID</th>
                  <th className="text-left py-2 px-2 border-b border-slate-700">Palabra</th>
                  <th className="text-left py-2 px-2 border-b border-slate-700">Lengua</th>
                  <th className="text-left py-2 px-2 border-b border-slate-700">Definición</th>
                </tr>
              </thead>
              <tbody>
                {resultados.map((p) => (
                  <tr key={p.id} className="hover:bg-slate-900/60">
                    <td className="py-1.5 px-2 border-b border-slate-800">{p.id}</td>
                    <td className="py-1.5 px-2 border-b border-slate-800">{p.palabra}</td>
                    <td className="py-1.5 px-2 border-b border-slate-800">{p.idioma}</td>
                    <td className="py-1.5 px-2 border-b border-slate-800">
                      {p.significado || '—'}
                    </td>
                  </tr>
                ))}
                {resultados.length === 0 && (
                  <tr>
                    <td
                      colSpan={4}
                      className="py-3 px-2 text-center text-slate-500 border-t border-slate-800"
                    >
                      No se encontraron resultados.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </Card>
      </div>
    </div>
  )
}

export default AdminWords