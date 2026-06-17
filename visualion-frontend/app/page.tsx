// app/pacientes/page.tsx
import { Suspense } from 'react';
import ListaPacientes from '@/componentes/listar_paciente';
import ListaEmpleados  from '@/componentes/listar_empleados';
import Link from 'next/link';
export default function HomePage() {
  return (
<div className="min-h-screen bg-gray-950 text-gray-200">
      
      {/* Encabezado / Hero Section de la Óptica */}
      <header className="bg-gradient-to-r from-blue-700 to-indigo-800 text-white py-12 px-6 shadow-md text-center">
        <h1 className="text-4xl font-extrabold tracking-tight md:text-5xl mb-3">
          Visualion
        </h1>
        <p className="text-blue-100 max-w-md mx-auto text-lg mb-6">
          Sistema de gestión integral para el control de pacientes y personal técnico.
        </p>
        <Link
          href="/dashboard" 
          className="inline-block bg-white text-blue-700 font-bold px-6 py-3 rounded-lg shadow hover:bg-blue-50 transition-colors"
        >
          ⚙️ Ingresar al Panel de Control
        </Link>
        
      </header>

      {/* Grilla de Contenido Principal */}
      <main className="p-6 max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-8 mt-8">
        
        {/* Columna Izquierda: Pacientes */}
        <section className="bg-gray-900 p-6 rounded-2xl shadow-sm border border-gray-800">
          <h2 className="text-xl font-bold text-gray-200 mb-4 flex items-center gap-2">
            👥 Pacientes Registrados
          </h2>
          <p className="text-gray-400 mb-4">Acceda al módulo de pacientes para ver el listado completo, registrar nuevos pacientes y gestionar su historial médico.</p>
          <Link
            href="/dashboard/Paciente" 
            className="inline-block bg-indigo-600/10 text-indigo-400 font-medium px-4 py-2 rounded shadow-sm hover:bg-indigo-600 hover:text-white transition-colors border border-indigo-600/30"
          >
            Ir a Gestión de Pacientes →
          </Link>
        </section>

        {/* Columna Derecha: Empleados */}
        <section className="bg-gray-900 p-6 rounded-2xl shadow-sm border border-gray-800">
          <h2 className="text-xl font-bold text-gray-200 mb-4 flex items-center gap-2">
            👔 Personal de la Óptica
          </h2>
          
          <Suspense 
            fallback={
              <p className="text-gray-400 animate-pulse py-4">
                Obteniendo nómina de empleados de Laragon...
              </p>
            }
          >
            <ListaEmpleados />
          </Suspense>
        </section>

      </main>

      {/* Pie de página simple */}
      <footer className="text-center text-xs text-gray-400 py-8 border-t border-gray-200 mt-12">
        © {new Date().getFullYear()} Visualion Óptica. Todos los derechos reservados.
      </footer>
    </div>
  );
}