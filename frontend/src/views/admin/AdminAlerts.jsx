import React from "react";

const AdminAlerts = () => {
  return (
    <div className="space-y-6">
      <h1 className="text-xl font-bold">Gestión de Alertas</h1>

      <div className="text-sm text-slate-300">
        <p>Este módulo permitirá administrar alertas del sistema.</p>
        <p>Puedes agregar:</p>
        <ul className="list-disc ml-6 mt-2">
          <li>Lista de alertas con filtros</li>
          <li>Botón de “Marcar como leída”</li>
          <li>Crear nueva alerta manualmente</li>
        </ul>
      </div>
    </div>
  );
};

export default AdminAlerts;
