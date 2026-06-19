// services/pacientesService.ts
import { API, APIError } from "./api";

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

export const pacientesService = {
  async listar(): Promise<Paciente[]> {
    return API.GET<Paciente[]>("/pacientes");
  },

  async obtenerPorId(id: number): Promise<Paciente> {
    return API.GET<Paciente>(`/pacientes/${id}`);
  },

  async obtenerPorDni(dni: string): Promise<Paciente | null> {
    try {
      return await API.GET<Paciente>(`/pacientes/dni/${dni}`);
    } catch (error) {
      if (error instanceof APIError && error.status === 404) {
        return null;
      }
      throw error;
    }
  },

  async crear(paciente: Omit<Paciente, "id">): Promise<Paciente> {
    return API.POST<Paciente>("/pacientes", paciente);
  },

  async actualizar(id: number, paciente: Partial<Paciente>): Promise<Paciente> {
    return API.PUT<Paciente>(`/pacientes/${id}`, paciente);
  },

  async eliminar(dni: string): Promise<void> {
    return API.DELETE(`/pacientes/${dni}`);
  },
};
