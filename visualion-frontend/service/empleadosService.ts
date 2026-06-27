// services/empleadosService.ts
import { API } from "./api";
import { Empleado } from "./authService";

export type { Empleado } from "./authService";

export const empleadosService = {
  async listar(): Promise<Empleado[]> {
    return API.GET<Empleado[]>("/auth/usuarios");
  },

  async obtenerPorId(id: number): Promise<Empleado> {
    return API.GET<Empleado>(`/auth/usuarios/${id}`);
  },

  async crear(empleado: Omit<Empleado, "id">): Promise<Empleado> {
    return API.POST<Empleado>("/auth/usuarios", empleado);
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
