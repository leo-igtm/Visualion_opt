import { EstadoOrden } from "@/types/taller";

export const TRANSICIONES_VALIDAS: Record<EstadoOrden, EstadoOrden[]> = {
  recibida: ["en_proceso", "cancelada"],
  en_proceso: ["lista_para_entrega", "cancelada"],
  lista_para_entrega: ["entregada", "cancelada"],
  entregada: [],
  cancelada: [],
};

export function getEstadosPermitidos(estadoActual: EstadoOrden): EstadoOrden[] {
  return TRANSICIONES_VALIDAS[estadoActual] || [];
}

export const ESTADOS_LABEL: Record<EstadoOrden, string> = {
  recibida: "Recibida",
  en_proceso: "En Proceso",
  lista_para_entrega: "Lista para Entrega",
  entregada: "Entregada",
  cancelada: "Cancelada",
};

export function getEstadoLabel(estado: EstadoOrden): string {
  return ESTADOS_LABEL[estado] || estado;
}
