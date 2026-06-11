// app/empleados/page.tsx
import { Suspense } from 'react';
import ListaEmpleados from '@/componentes/listar_empleados';

export default function EmpleadosPage() {
  return (
    <main className="p-8 max-w-5xl mx-auto">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold text-gray-800">
          Gestión de Personal
        </h1>
        {/* Aquí a futuro puedes agregar tu botón de "Nuevo Empleado" */}
        <button className="bg-green-600 hover:bg-green-700 text-white font-bold py-2 px-4 rounded transition-colors">
          + Agregar
        </button>
      </div>
      
      {/* React Suspense maneja el estado de carga sin bloquear la página */}
      <Suspense 
        fallback={
          <div className="flex justify-center items-center py-10">
            <p className="text-blue-500 font-medium animate-pulse text-lg">
              Cargando personal desde el servidor...
            </p>
          </div>
        }
      >
        <ListaEmpleados />
      </Suspense>
    </main>
  );
}