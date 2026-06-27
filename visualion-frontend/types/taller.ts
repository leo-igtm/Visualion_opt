// types/taller.ts
export type EstadoOrden = "recibida" | "en_proceso" | "lista_para_entrega" | "entregada" | "cancelada";

export interface OrdenTrabajo {
  id: number;
  venta_id: number;
  estado: EstadoOrden;
  descripcion_trabajo?: string;
  fecha_entrega_esperada?: string;
  fecha_creacion: string;
  fecha_actualizacion: string;
  etapas?: EtapaTrabajo[];
  historico_estados?: HistoricoEstados[];
}

export interface EtapaTrabajo {
  id: number;
  orden_id: number;
  etapa: string;
  tecnico_id?: number;
  completado: boolean;
  notas?: string;
  fecha_creacion?: string;
  fecha_actualizacion?: string;
}

export interface HistoricoEstados {
  id: number;
  orden_id: number;
  estado_anterior?: string;
  estado_nuevo: string;
  tecnico_id?: number;
  fecha_creacion: string;
}

export const ESTADOS_COLORES: Record<EstadoOrden, string> = {
  recibida: "bg-gray-600",
  en_proceso: "bg-yellow-600",
  lista_para_entrega: "bg-blue-600",
  entregada: "bg-green-600",
  cancelada: "bg-red-600"
};

export const ESTADOS_LABEL: Record<EstadoOrden, string> = {
  recibida: "Recibida",
  en_proceso: "En Proceso",
  lista_para_entrega: "Lista para Entrega",
  entregada: "Entregada",
  cancelada: "Cancelada"
};
