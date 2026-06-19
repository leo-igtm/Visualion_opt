// services/empleadosService.ts
import { API } from "./api";
import { Empleado, EmpleadoRegister } from "./authService";

export { Empleado, EmpleadoRegister } from "./authService";

export const empleadosService = {
  async listar(): Promise<Empleado[]> {
    return API.GET<Empleado[]>("/auth/usuarios");
  },

  async obtenerPorId(id: number): Promise<Empleado> {
    return API.GET<Empleado>(`/auth/usuarios/${id}`);
  },

  async crear(empleado: EmpleadoRegister): Promise<Empleado> {
    return API.POST<Empleado>("/auth/register", empleado);
  },

  async actualizar(id: number, empleado: Partial<Empleado>): Promise<Empleado> {
    return API.PUT<Empleado>(`/auth/usuarios/${id}`, empleado);
  },

  async eliminar(id: number): Promise<void> {
    return API.DELETE(`/auth/usuarios/${id}`);
  },

  async listarPorRol(rol: string): Promise<Empleado[]> {
    const todos = await this.listar();
    return todos.filter((emp) => emp.rol === rol);
  },
};
