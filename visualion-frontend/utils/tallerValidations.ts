export const TRANSICIONES_VALIDAS: Record<string, string[]> = {
  recibida: ["biselado"],
  biselado: ["montaje"],
  montaje: ["control_calidad"],
  control_calidad: ["listo", "montaje"],
  listo: [],
};

export function getEstadosPermitidos(estadoActual: string): string[] {
  return TRANSICIONES_VALIDAS[estadoActual] || [];
}

export const ESTADOS_LABEL: Record<string, string> = {
  recibida: "Recibida",
  biselado: "Biselado",
  montaje: "Montaje",
  control_calidad: "Control QC",
  listo: "Listo",
};

export function getEstadoLabel(estado: string): string {
  return ESTADOS_LABEL[estado] || estado;
}
