import React from 'react'
import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import SectionTitle from '../components/ui/SectionTitle'
import Card from '../components/ui/Card'
import Button from '../components/ui/Button'

const Home = () => {
  return (
    <div className="bg-ql-hero min-h-screen pt-10 pb-16">
      {/* HERO */}
      <section className="max-w-6xl mx-auto px-4 grid md:grid-cols-2 gap-10 items-center">
        <motion.div
          initial={{ opacity: 0, x: -40 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.7 }}
        >
          <p className="text-xs uppercase tracking-[0.3em] text-ql-accent mb-3">
            Lenguas originarias · Puno
          </p>
          <h1 className="text-4xl md:text-5xl font-black tracking-tight mb-4">
            Plataforma viva para las lenguas
            <span className="block text-ql-secondary">Aymara y Quechua</span>
          </h1>
          <p className="text-sm md:text-base text-slate-200/90 mb-6 max-w-xl">
            Qhapaq Lingua combina estructuras TRIE, grafos semánticos y un sistema de alertas para
            documentar, explorar y proteger el patrimonio lingüístico de las comunidades de Puno.
          </p>
          <div className="flex flex-wrap gap-3">
            <Button>
              <Link to="/explorar">Explorar vocabulario</Link>
            </Button>
            <Button variant="ghost">
              <Link to="/alertas">Ver alertas lingüísticas</Link>
            </Button>
          </div>
          <p className="mt-4 text-xs text-slate-300">
            Tecnología + tradición: datos comunitarios, analítica de frecuencia y visualización de
            relaciones semánticas.
          </p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, x: 40 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.7, delay: 0.1 }}
          className="relative"
        >
          <div className="absolute -inset-4 bg-gradient-to-br from-ql-primary/30 via-ql-secondary/20 to-ql-accent/30 blur-3xl opacity-70" />
          <div className="relative grid grid-cols-2 gap-4">
            <Card className="h-36 flex flex-col justify-between">
              <h3 className="text-sm font-semibold">TRIE léxico</h3>
              <p className="text-xs text-slate-300">
                Búsqueda eficiente de palabras con autocompletado en O(L).
              </p>
            </Card>
            <Card className="h-36 flex flex-col justify-between">
              <h3 className="text-sm font-semibold">Grafos semánticos</h3>
              <p className="text-xs text-slate-300">
                Conexiones entre términos según contexto y uso cultural.
              </p>
            </Card>
            <Card className="h-36 col-span-2 flex flex-col justify-between">
              <h3 className="text-sm font-semibold">Alertas de riesgo</h3>
              <p className="text-xs text-slate-300">
                Identifica vocablos poco usados para priorizar su enseñanza y registro.
              </p>
            </Card>
          </div>
        </motion.div>
      </section>

      {/* FEATURES */}
      <section className="max-w-6xl mx-auto px-4 mt-20">
        <SectionTitle
          eyebrow="Características clave"
          title="Diseñado para comunidades, educadores e investigadores"
          subtitle="Qhapaq Lingua no es solo un diccionario: es un observatorio vivo de la lengua."
        />
        <div className="grid md:grid-cols-3 gap-6">
          <Card>
            <h3 className="font-semibold mb-2">Exploración bilingüe</h3>
            <p className="text-sm text-slate-300">
              Permite registrar y buscar vocablos en aymara, quechua y español, incluyendo
              contexto de uso y variantes locales.
            </p>
          </Card>
          <Card>
            <h3 className="font-semibold mb-2">Enfoque comunitario</h3>
            <p className="text-sm text-slate-300">
              Facilita la participación de docentes, hablantes nativos y estudiantes en la
              construcción del corpus.
            </p>
          </Card>
          <Card>
            <h3 className="font-semibold mb-2">Analítica lingüística</h3>
            <p className="text-sm text-slate-300">
              El sistema de alertas detecta términos con baja frecuencia de uso y los marca como
              prioritarios.
            </p>
          </Card>
        </div>
      </section>

      {/* CTA */}
      <section className="max-w-6xl mx-auto px-4 mt-20">
        <Card className="flex flex-col md:flex-row items-center justify-between gap-6">
          <div>
            <h2 className="text-xl font-bold mb-2">
              Preservemos hoy las palabras que cuentan nuestra historia.
            </h2>
            <p className="text-sm text-slate-300 max-w-xl">
              Usa Qhapaq Lingua como herramienta educativa, repositorio de memoria lingüística y
              punto de encuentro entre tecnología y cultura.
            </p>
          </div>
          <div className="flex flex-col gap-3">
            <Button>
              <Link to="/explorar">Explorar vocabulario</Link>
            </Button>
            <Button variant="subtle">
              <Link to="/admin">Entrar al panel de administración</Link>
            </Button>
          </div>
        </Card>
      </section>
    </div>
  )
}

export default Home
