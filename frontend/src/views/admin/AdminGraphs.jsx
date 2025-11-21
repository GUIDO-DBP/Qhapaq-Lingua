import React from "react";

const AdminGraphs = () => {
  return (
    <div className="space-y-6">
      <h1 className="text-xl font-bold">Gestión de Grafos</h1>

      <div className="text-sm text-slate-300">
        <p>Aquí irá el módulo de administración de grafos semánticos.</p>
        <p>Puedes agregar:</p>
        <ul className="list-disc ml-6 mt-2">
          <li>Tabla de relaciones</li>
          <li>Formulario para crear relaciones</li>
          <li>Visualizador de nodos-palabra</li>
        </ul>
      </div>
    </div>
  );
};

export default AdminGraphs;
