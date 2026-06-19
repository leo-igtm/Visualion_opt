// app/dashboard/taller/[id]/page.tsx
import { Suspense } from "react";
import Link from "next/link";
import DetallesOrdenTrabajo from "@/componentes/DetallesOrdenTrabajo";

export default function OrdenDetallesPage({ params }: { params: { id: string } }) {
  const ordenId = parseInt(params.id, 10);

  if (isNaN(ordenId)) {
    return <div className="text-red-400 p-8">ID de orden inválido</div>;
  }

  return (
    <main className="p-8 max-w-4xl mx-auto">
      <div className="mb-6">
        <Link href="/dashboard/taller" className="text-indigo-400 hover:text-indigo-300 mb-4 inline-block">
          ← Volver a órdenes
        </Link>
        <h1 className="text-3xl font-bold text-gray-100">Detalles de Orden</h1>
      </div>

      <Suspense
        fallback={
          <div className="flex items-center justify-center p-12 bg-gray-900 border border-gray-800 rounded-lg">
            <p className="text-indigo-400 font-medium animate-pulse">Cargando detalles...</p>
          </div>
        }
      >
        <DetallesOrdenTrabajo ordenId={ordenId} />
      </Suspense>
    </main>
  );
}
