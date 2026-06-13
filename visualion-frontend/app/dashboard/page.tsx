// app/dashboard/page.tsx
/*Elaborar estilo oscuro*/ 


export default function DashboardHome() {
  return (
    <main className="p-8 max-w-7xl mx-auto w-full">
      <h1 className="text-3xl font-bold text-gray-800 mb-2">Panel de Control</h1>
      <p className="text-gray-500 mb-8">Bienvenido al sistema de administración de la óptica.</p>

      {/* Contenedor de las tarjetas de resumen */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        
        {/* Tarjeta 1: Pacientes */}
        <div className="bg-white p-6 rounded-xl border border-gray-200 shadow-sm flex flex-col">
          <h2 className="text-gray-500 text-sm font-semibold uppercase tracking-wider mb-2">
            Total Pacientes
          </h2>
          <span className="text-4xl font-bold text-blue-600">--</span>
          <p className="text-sm text-gray-400 mt-2">Registrados en el sistema</p>
        </div>

        {/* Tarjeta 2: Empleados */}
        <div className="bg-white p-6 rounded-xl border border-gray-200 shadow-sm flex flex-col">
          <h2 className="text-gray-500 text-sm font-semibold uppercase tracking-wider mb-2">
            Personal Activo
          </h2>
          <span className="text-4xl font-bold text-green-600">--</span>
          <p className="text-sm text-gray-400 mt-2">Médicos y vendedores</p>
        </div>

        {/* Tarjeta 3: Otra métrica a futuro */}
        <div className="bg-white p-6 rounded-xl border border-gray-200 shadow-sm flex flex-col">
          <h2 className="text-gray-500 text-sm font-semibold uppercase tracking-wider mb-2">
            Turnos de Hoy
          </h2>
          <span className="text-4xl font-bold text-purple-600">--</span>
          <p className="text-sm text-gray-400 mt-2">Pendientes de atención</p>
        </div>

      </div>
    </main>
  );
}