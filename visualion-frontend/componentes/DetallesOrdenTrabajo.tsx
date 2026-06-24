// componentes/DetallesOrdenTrabajo.tsx
"use client";

import { useEffect, useState } from "react";
import { tallerService } from "@/service/tallerService";
import { OrdenTrabajo, HistoricoEstados } from "@/types/taller";
import { getEstadosPermitidos, getEstadoLabel } from "@/utils/tallerValidations";
import EstadoOrdenBadge from "./EstadoOrdenBadge";

interface Props {
  ordenId: number;
}

export default function DetallesOrdenTrabajo({ ordenId }: Props) {
  const [orden, setOrden] = useState<OrdenTrabajo | null>(null);
  const [historico, setHistorico] = useState<HistoricoEstados[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [nuevoEstado, setNuevoEstado] = useState<string | null>(null);
  const [notas, setNotas] = useState("");
  const [actualizando, setActualizando] = useState(false);

  useEffect(() => {
    const fetchOrden = async () => {
      try {
        setLoading(true);
        const [ordenData, historicoData] = await Promise.all([
          tallerService.getOrdenDetalles(ordenId),
          tallerService.getHistoricoEstados(ordenId),
        ]);
        setOrden(ordenData);
        setHistorico(historicoData);
        setError(null);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Error al cargar orden");
      } finally {
        setLoading(false);
      }
    };

    fetchOrden();
  }, [ordenId]);

  const handleCambiarEstado = async () => {
    if (!nuevoEstado || !orden) return;

    try {
      setActualizando(true);
      const ordenActualizada = await tallerService.cambiarEstado(
        ordenId,
        nuevoEstado,
        undefined,
        notas
      );
      setOrden(ordenActualizada);
      setNuevoEstado(null);
      setNotas("");
      // Refetch historico
      const historicoData = await tallerService.getHistoricoEstados(ordenId);
      setHistorico(historicoData);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Error al actualizar estado");
    } finally {
      setActualizando(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center p-12 bg-gray-900 border border-gray-800 rounded-lg">
        <p className="text-indigo-400 font-medium animate-pulse">Cargando detalles...</p>
      </div>
    );
  }

  if (error) {
    return <div className="p-4 bg-red-900/20 border border-red-600 text-red-400 rounded">{error}</div>;
  }

  if (!orden) {
    return <div className="text-gray-400">Orden no encontrada</div>;
  }

  const estadosPermitidos = getEstadosPermitidos(orden.estado);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="p-6 bg-gray-800 border border-gray-700 rounded-lg">
        <div className="flex justify-between items-start mb-4">
          <div>
            <h2 className="text-2xl font-bold text-gray-100">Orden #{orden.id}</h2>
            <p className="text-gray-400 mt-1">Venta: {orden.venta_id}</p>
          </div>
          <EstadoOrdenBadge estado={orden.estado} />
        </div>
        {orden.descripcion_trabajo && (
          <p className="text-gray-300 mt-2">{orden.descripcion_trabajo}</p>
        )}
        {orden.fecha_entrega_esperada && (
          <p className="text-gray-400 text-sm mt-2">
            Entrega esperada: {new Date(orden.fecha_entrega_esperada).toLocaleDateString()}
          </p>
        )}
      </div>

      {/* Cambiar estado */}
      {estadosPermitidos.length > 0 && (
        <div className="p-6 bg-gray-800 border border-gray-700 rounded-lg">
          <h3 className="font-bold text-gray-100 mb-4">Cambiar Estado</h3>
          <div className="space-y-3">
            <select
              value={nuevoEstado || ""}
              onChange={(e) => setNuevoEstado(e.target.value)}
              className="w-full px-3 py-2 bg-gray-900 border border-gray-600 text-gray-100 rounded"
            >
              <option value="">Seleccionar nuevo estado...</option>
              {estadosPermitidos.map((estado) => (
                <option key={estado} value={estado}>
                  {getEstadoLabel(estado)}
                </option>
              ))}
            </select>
            <textarea
              value={notas}
              onChange={(e) => setNotas(e.target.value)}
              placeholder="Notas (opcional)"
              className="w-full px-3 py-2 bg-gray-900 border border-gray-600 text-gray-100 rounded"
              rows={3}
            />
            <button
              onClick={handleCambiarEstado}
              disabled={!nuevoEstado || actualizando}
              className="px-4 py-2 bg-indigo-600 text-white rounded disabled:opacity-50 disabled:cursor-not-allowed hover:bg-indigo-700"
            >
              {actualizando ? "Actualizando..." : "Actualizar Estado"}
            </button>
          </div>
        </div>
      )}

      {/* Etapas */}
      {orden.etapas && orden.etapas.length > 0 && (
        <div className="p-6 bg-gray-800 border border-gray-700 rounded-lg">
          <h3 className="font-bold text-gray-100 mb-4">Etapas de Trabajo</h3>
          <div className="space-y-2">
            {orden.etapas.map((etapa) => (
              <div key={etapa.id} className="p-3 bg-gray-900 border border-gray-700 rounded text-sm">
                <div className="flex justify-between items-start">
                  <div>
                    <p className="text-gray-300 font-medium">{etapa.etapa}</p>
                    {etapa.notas && <p className="text-gray-400 text-xs mt-1">{etapa.notas}</p>}
                  </div>
                  <span className={`px-2 py-1 rounded text-xs ${etapa.completado ? "bg-green-900 text-green-300" : "bg-gray-700 text-gray-300"}`}>
                    {etapa.completado ? "✓ Completa" : "Pendiente"}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Histórico */}
      {historico.length > 0 && (
        <div className="p-6 bg-gray-800 border border-gray-700 rounded-lg">
          <h3 className="font-bold text-gray-100 mb-4">Histórico de Cambios</h3>
          <div className="space-y-2">
            {historico.map((item) => (
              <div key={item.id} className="p-3 bg-gray-900 border border-gray-700 rounded text-sm">
                <p className="text-gray-300">
                  {item.estado_anterior ? `${item.estado_anterior} → ${item.estado_nuevo}` : `Inicial: ${item.estado_nuevo}`}
                </p>
                <p className="text-gray-500 text-xs mt-1">{new Date(item.fecha_creacion).toLocaleString()}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
