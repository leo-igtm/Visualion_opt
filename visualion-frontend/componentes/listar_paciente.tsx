// componentes/ListaPacientes.tsx
import { fetchObtenerPaciente } from '@/service/api';


interface Paciente {
  id: number;
  dni: string;
  nombre: string;
  apellido: string;
  telefono?: string;       
  email?: string;
  obra_social?: string;
  historial_medico?: string;
}
/*Elaborar estilo oscuro*/ 
export default async function ListaPacientes() {
  // 2. Le avisamos a TypeScript que 'pacientes' será un array de objetos tipo Paciente
  const pacientes: Paciente[] = await fetchObtenerPaciente();

  return (
    <ul className="space-y-2">
      {pacientes.map((p) => (
        <li key={p.id} className="p-3 bg-dark-50 rounded border border-dark-200">
          <span className="font-semibold text-dark-700">
            {p.nombre} {p.apellido}
          </span>{' '}
          — <span className="text-sm text-dark-500">{p.obra_social || 'Sin Obra Social'}</span>
        </li>
      ))}
    </ul>
  );
}