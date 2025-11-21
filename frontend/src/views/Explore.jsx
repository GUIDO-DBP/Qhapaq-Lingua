import React, { useState } from 'react'
import { motion } from 'framer-motion'
import { useSearchWords, useWordDetail, useWordGraph } from '../api/hooks'
import Card from '../components/ui/Card'
import Button from '../components/ui/Button'

const Explore = () => {
  const [termino, setTermino] = useState('')
  const [seleccionId, setSeleccionId] = useState(null)

  const { data: resultadosData = {}, isFetching } = useSearchWords(termino)
  const { data: detalle } = useWordDetail(seleccionId)
  const { data: grafoData = {} } = useWordGraph(seleccionId)

  // CORRECCIÓN: Extraer el array de resultados correctamente
  const resultados = resultadosData.resultados || []
  
  // CORRECCIÓN: Extraer relaciones del grafo correctamente
  const relaciones = grafoData.relaciones || []

  const handleSelect = (id) => {
    setSeleccionId(id)
  }

  return (
    <div className="max-w-6xl mx-auto px-4 py-10 space-y-8">
      <header className="flex flex-col md:flex-row md:items-end justify-between gap-4">
        <div>
          <h1 className="text-2xl md:text-3xl font-bold mb-1">Explorar vocabulario</h1>
          <p className="text-sm text-slate-300">
            Busca palabras en aymara o quechua y explora sus relaciones semánticas.
          </p>
        </div>
      </header>

      <Card className="flex flex-col md:flex-row gap-4 items-center">
        <form
          onSubmit={(e) => e.preventDefault()}
          className="flex-1 flex flex-col md:flex-row gap-3 items-center"
        >
          <input
            type="text"
            className="w-full md:flex-1 rounded-full bg-slate-900/80 border border-slate-700 px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-ql-primary"
            placeholder="Escribe una palabra o raíz..."
            value={termino}
            onChange={(e) => setTermino(e.target.value)}
          />
          <Button type="button" variant="ghost">
            {isFetching ? 'Buscando...' : 'Buscar'}
          </Button>
        </form>
        <p className="text-xs text-slate-400">
          Sugerencia: prueba con términos frecuentes en tu comunidad.
        </p>
      </Card>

      <div className="grid md:grid-cols-[minmax(0,0.6fr)_minmax(0,1.4fr)] gap-6">
        {/* Lista resultados */}
        <Card>
          <h2 className="text-sm font-semibold mb-3 uppercase tracking-wide text-slate-300">
            Resultados
          </h2>
          {isFetching && <p className="text-xs text-slate-400">Buscando...</p>}
          {!isFetching && resultados.length === 0 && (
            <p className="text-xs text-slate-400">
              No hay resultados. Intenta con otro término o amplía tu búsqueda.
            </p>
          )}
          <ul className="space-y-2 mt-2 max-h-[360px] overflow-y-auto pr-1">
            {resultados.map((p) => (
              <li key={p.id}>
                <button
                  onClick={() => handleSelect(p.id)}
                  className={`w-full text-left px-3 py-2 rounded-lg text-sm hover:bg-slate-800/80 ${
                    seleccionId === p.id ? 'bg-slate-800 text-ql-accent' : 'text-slate-100'
                  }`}
                >
                  <span className="font-semibold">{p.palabra}</span>{' '}
                  <span className="text-xs text-slate-400">({p.idioma})</span>
                </button>
              </li>
            ))}
          </ul>
        </Card>

        {/* Detalle + grafo */}
        <motion.div
          key={seleccionId || 'placeholder'}
          initial={{ opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.25 }}
          className="space-y-4"
        >
          <Card>
            {detalle ? (
              <>
                <h2 className="text-lg font-semibold mb-1">{detalle.palabra}</h2>
                <p className="text-xs text-slate-400 mb-2">
                  Idioma: <span className="font-semibold text-slate-200">{detalle.idioma}</span>
                </p>
                <p className="text-sm mb-2">
                  <span className="font-semibold">Significado: </span>
                  {detalle.significado || 'Sin significado registrado.'}
                </p>
                <p className="text-sm text-slate-300">
                  <span className="font-semibold">Contexto de uso: </span>
                  {detalle.contexto_uso || 'Aún no se registró un contexto de uso.'}
                </p>
              </>
            ) : (
              <p className="text-sm text-slate-300">
                Selecciona una palabra de la lista para ver sus detalles.
              </p>
            )}
          </Card>

          <Card>
            <h3 className="text-sm font-semibold mb-2">Relaciones semánticas</h3>
            {seleccionId && relaciones.length === 0 && (
              <p className="text-xs text-slate-400">
                No se encontraron relaciones para esta palabra. Pueden registrarse en el panel de
                administración.
              </p>
            )}
            {relaciones.length > 0 && (
              <ul className="text-xs space-y-1">
                {relaciones.map((rel, index) => (
                  <li key={index} className="flex justify-between items-center p-2 hover:bg-slate-800/50 rounded">
                    <span>
                      <span className="font-medium text-ql-accent">{rel.tipo_relacion}</span>
                      {' → '}
                      <span className="text-slate-200">
                        {rel.palabra_destino?.palabra || 'Palabra relacionada'}
                      </span>
                    </span>
                    <span className="text-slate-400 text-xs">peso: {rel.peso}</span>
                  </li>
                ))}
              </ul>
            )}
          </Card>
        </motion.div>
      </div>
    </div>
  )
}

export default Explore