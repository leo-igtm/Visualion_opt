import { fetchObtenerPaciente } from '@/service/api';
import TablaPacientes from './tabla_pacientes';

export interface Paciente {
  id: number;
  dni: string;
  nombre: string;
  apellido: string;
  telefono?: string;       
  email?: string;
  obra_social?: string;
  historial_medico?: string;
}

export default async function ListaPacientes() {
  const pacientes: Paciente[] = await fetchObtenerPaciente();

  return (
    <TablaPacientes initialData={pacientes} />
  );
}