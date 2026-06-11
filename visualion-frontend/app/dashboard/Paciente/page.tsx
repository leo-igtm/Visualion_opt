// app/pacientes/page.tsx
import { Suspense } from 'react';
import ListaPacientes from '@/componentes/listar_paciente';

export default function PacientesPage() {
  return (
    <main className="p-8 max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold mb-6 text-gray-800">
        Gestión de Pacientes
      </h1>
      
      {/* El Streaming se encarga de mostrar el fallback mientras la promesa se resuelve */}
      <Suspense 
        fallback={
          <p className="text-blue-500 font-medium animate-pulse">
            Cargando datos desde FastAPI...
          </p>
        }
      >
        <ListaPacientes />
      </Suspense>
    </main>
  );
}