// types/taller.ts
export type EstadoOrden = "recibida" | "biselado" | "montaje" | "control_calidad" | "listo";

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
  biselado: "bg-yellow-600",
  montaje: "bg-blue-600",
  control_calidad: "bg-orange-600",
  listo: "bg-green-600"
};

export const ESTADOS_LABEL: Record<EstadoOrden, string> = {
  recibida: "Recibida",
  biselado: "Biselado",
  montaje: "Montaje",
  control_calidad: "Control QC",
  listo: "Listo"
};
