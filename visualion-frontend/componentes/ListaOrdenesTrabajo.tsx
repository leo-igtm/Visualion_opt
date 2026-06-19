// componentes/ListaOrdenesTrabajo.tsx
"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { tallerService } from "@/service/tallerService";
import { OrdenTrabajo } from "@/types/taller";
import { APIError } from "@/service/api";
import EstadoOrdenBadge from "./EstadoOrdenBadge";
import { LoadingSpinner } from "./Loading";
import { ErrorAlert } from "./Error";

export default function ListaOrdenesTrabajo() {
  const [ordenes, setOrdenes] = useState<OrdenTrabajo[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<APIError | null>(null);
  const [filtroEstado, setFiltroEstado] = useState<string | null>(null);

  useEffect(() => {
    const fetchOrdenes = async () => {
      try {
        setLoading(true);
        setError(null);
        const data = await tallerService.getOrdenes(filtroEstado || undefined);
        setOrdenes(data);
      } catch (err) {
        if (err instanceof APIError) {
          setError(err);
        } else {
          setError(new APIError(500, "Error al cargar órdenes"));
        }
      } finally {
        setLoading(false);
      }
    };

    fetchOrdenes();
  }, [filtroEstado]);

  const handleRetry = () => {
    const event = new Event("retry");
    window.dispatchEvent(event);
    setLoading(true);
    setError(null);
  };

  if (loading) {
    return <LoadingSpinner message="Cargando órdenes de trabajo..." />;
  }

  if (error) {
    return (
      <ErrorAlert
        title="Error al cargar órdenes"
        message={error.detail}
        retry={handleRetry}
      />
    );
  }

  return (
    <div>
      <div className="mb-4 flex gap-4">
        <div>
          <label className="block text-gray-300 text-sm mb-2">
            Filtrar por estado:
          </label>
          <select
            value={filtroEstado || ""}
            onChange={(e) => setFiltroEstado(e.target.value || null)}
            className="px-3 py-2 bg-gray-800 border border-gray-700 text-gray-100 rounded hover:border-indigo-500 transition-colors"
          >
            <option value="">Todos</option>
            <option value="recibida">Recibida</option>
            <option value="biselado">Biselado</option>
            <option value="montaje">Montaje</option>
            <option value="control_calidad">Control QC</option>
            <option value="listo">Listo</option>
          </select>
        </div>
      </div>

      <div className="grid gap-4">
        {ordenes.length === 0 ? (
          <div className="p-8 text-center bg-gray-900 border border-gray-800 rounded-lg">
            <p className="text-gray-400 text-lg">📭 No hay órdenes de trabajo</p>
            <p className="text-gray-500 text-sm mt-2">
              Las órdenes aparecerán aquí cuando se creen nuevas ventas
            </p>
          </div>
        ) : (
          ordenes.map((orden) => (
            <Link href={`/dashboard/taller/${orden.id}`} key={orden.id}>
              <div className="p-4 bg-gray-800 border border-gray-700 rounded-lg hover:border-indigo-500 cursor-pointer transition-all duration-300 hover:shadow-lg hover:shadow-indigo-500/20">
                <div className="flex justify-between items-start">
                  <div>
                    <p className="text-gray-300 text-sm font-semibold">
                      Orden #{orden.id}
                    </p>
                    <p className="text-gray-400 text-xs mt-1">
                      Venta: {orden.venta_id}
                    </p>
                  </div>
                  <EstadoOrdenBadge estado={orden.estado} />
                </div>

                {orden.descripcion_trabajo && (
                  <p className="text-gray-400 text-xs mt-3 line-clamp-2">
                    {orden.descripcion_trabajo}
                  </p>
                )}

                {orden.fecha_entrega_esperada && (
                  <p className="text-gray-500 text-xs mt-2">
                    📅 Entrega: {new Date(orden.fecha_entrega_esperada).toLocaleDateString()}
                  </p>
                )}
              </div>
            </Link>
          ))
        )}
      </div>
    </div>
  );
}
