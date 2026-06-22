// componentes/ListaEmpleados.tsx
import { empleadosService } from '@/service/empleadosService';

// 1. Definimos la estructura exacta que devuelve tu backend (EmpleadoOut)
interface Empleado {
  id: number;
  dni: string;
  nombre: string;
  apellido: string;
  telefono?: string;
  email?: string;
  legajo: string;
  usuario: string;
  rol: string;
  
  // Campos específicos según el rol (los marcamos con '?' porque pueden ser nulos)
  especialidad?: string;
  matricula?: string;
  matricula_optico?: string;
  comisiones?: number;
}
/*Elaborar estilo oscuro*/ 

export default async function ListaEmpleados() {
  // 2. Ejecutamos la petición al servidor tipando la respuesta
  const empleados: Empleado[] = await empleadosService.listar();

  return (
    <div className="overflow-x-auto mt-4">
      <table className="min-w-full bg-dark border border-dark-200 shadow-sm rounded-lg overflow-hidden">
        <thead className="bg-dark-100 text-dark-600 uppercase text-sm leading-normal">
          <tr>
            <th className="py-3 px-6 text-left">Legajo</th>
            <th className="py-3 px-6 text-left">Nombre y Apellido</th>
            <th className="py-3 px-6 text-left">Rol</th>
            <th className="py-3 px-6 text-center">Usuario</th>
          </tr>
        </thead>
        <tbody className="text-dark-700 text-sm font-light">
          {empleados.map((empleado) => (
            <tr key={empleado.id} className="border-b border-dark-200 hover:bg-dark-50">
              <td className="py-3 px-6 text-left whitespace-nowrap font-medium">
                {empleado.legajo}
              </td>
              <td className="py-3 px-6 text-left">
                {empleado.nombre} {empleado.apellido}
              </td>
              <td className="py-3 px-6 text-left">
                <span className="bg-blue-100 text-blue-800 py-1 px-3 rounded-full text-xs font-semibold capitalize">
                  {empleado.rol}
                </span>
              </td>
              <td className="py-3 px-6 text-center">
                {empleado.usuario}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}