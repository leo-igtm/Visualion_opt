import { pacientesService } from '@/service/pacientesService';
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
  const pacientes: Paciente[] = await pacientesService.listar();

  return (
    <TablaPacientes initialData={pacientes} />
  );
}