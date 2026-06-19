// componentes/EstadoOrdenBadge.tsx
import { EstadoOrden, ESTADOS_COLORES, ESTADOS_LABEL } from "@/types/taller";

interface Props {
  estado: EstadoOrden;
  className?: string;
}

export default function EstadoOrdenBadge({ estado, className = "" }: Props) {
  const color = ESTADOS_COLORES[estado] || "bg-gray-600";
  const label = ESTADOS_LABEL[estado] || estado;

  return (
    <span className={`inline-block px-3 py-1 rounded-full text-white text-sm font-medium ${color} ${className}`}>
      {label}
    </span>
  );
}
