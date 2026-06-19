// app/dashboard/taller/page.tsx
import { Suspense } from "react";
import ListaOrdenesTrabajo from "@/componentes/ListaOrdenesTrabajo";

export default function TallerPage() {
  return (
    <main className="p-8 max-w-6xl mx-auto">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-100">Taller y Laboratorio</h1>
        <p className="text-gray-400 mt-2">Gestión de órdenes de trabajo y seguimiento de producción</p>
      </div>

      <Suspense
        fallback={
          <div className="flex items-center justify-center p-12 bg-gray-900 border border-gray-800 rounded-lg">
            <p className="text-indigo-400 font-medium animate-pulse flex items-center gap-2">
              <svg className="animate-spin h-5 w-5 text-indigo-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Cargando órdenes...
            </p>
          </div>
        }
      >
        <ListaOrdenesTrabajo />
      </Suspense>
    </main>
  );
}
