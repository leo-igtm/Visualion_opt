// service/tallerService.ts
const API_BASE = process.env.NEXT_PUBLIC_API_URL ? `${process.env.NEXT_PUBLIC_API_URL}/taller` : "http://localhost:8000/taller";

export const tallerService = {
  async getOrdenes(estado?: string, tecnico_id?: number) {
    const params = new URLSearchParams();
    if (estado) params.append("estado", estado);
    if (tecnico_id) params.append("tecnico_id", tecnico_id.toString());

    const res = await fetch(`${API_BASE}/ordenes?${params.toString()}`, {
      cache: "no-store",
    });
    if (!res.ok) throw new Error("Failed to fetch ordenes");
    return res.json();
  },

  async getOrdenDetalles(ordenId: number) {
    const res = await fetch(`${API_BASE}/ordenes/${ordenId}`, {
      cache: "no-store",
    });
    if (!res.ok) throw new Error("Failed to fetch orden detalles");
    return res.json();
  },

  async crearOrden(ventaId: number, descripcion?: string, fechaEntrega?: string) {
    const res = await fetch(`${API_BASE}/ordenes`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        venta_id: ventaId,
        descripcion_trabajo: descripcion,
        fecha_entrega_esperada: fechaEntrega,
      }),
    });
    if (!res.ok) throw new Error("Failed to create orden");
    return res.json();
  },

  async cambiarEstado(ordenId: number, estadoNuevo: string, tecnicoId?: number, notas?: string) {
    const res = await fetch(`${API_BASE}/ordenes/${ordenId}/estado`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        estado_nuevo: estadoNuevo,
        tecnico_id: tecnicoId,
        notas,
      }),
    });
    if (!res.ok) {
      const error = await res.json();
      throw new Error(error.detail || "Failed to update estado");
    }
    return res.json();
  },

  async getHistoricoEstados(ordenId: number) {
    const res = await fetch(`${API_BASE}/ordenes/${ordenId}/historico`, {
      cache: "no-store",
    });
    if (!res.ok) throw new Error("Failed to fetch historico");
    return res.json();
  },
};
