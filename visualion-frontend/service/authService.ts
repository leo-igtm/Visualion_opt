// services/authService.ts
import { API, API_BASE, APIError } from "./api";

export interface AuthResponse {
  access_token: string;
  token_type?: string;
}

export interface Empleado {
  id: number;
  dni: string;
  nombre: string;
  apellido: string;
  telefono?: string;
  email?: string;
  legajo: string;
  usuario: string;
  rol: string; // "medico", "tecnico", "vendedor"
  matricula?: string;
  especialidad?: string;
  matricula_optico?: string;
  comisiones?: number;
}

export interface EmpleadoRegister {
  dni: string;
  nombre: string;
  apellido: string;
  telefono?: string;
  email?: string;
  legajo: string;
  usuario: string;
  contraseña: string;
  rol: string;
  matricula?: string;
  especialidad?: string;
  matricula_optico?: string;
  comisiones?: number;
}

export const authService = {
  async login(usuario: string, contraseña: string): Promise<AuthResponse> {
    const formData = new URLSearchParams();
    formData.append('username', usuario);
    formData.append('password', contraseña);

    const response = await fetch(`${API_BASE}/auth/login`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: formData.toString(),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new APIError(response.status, errorData.detail || "Error en la solicitud");
    }

    return response.json();
  },

  async register(userData: EmpleadoRegister): Promise<Empleado> {
    return API.POST<Empleado>("/auth/register", userData);
  },

  async obtenerUsuarios(): Promise<Empleado[]> {
    return API.GET<Empleado[]>("/auth/usuarios");
  },

  async obtenerUsuario(id: number): Promise<Empleado> {
    return API.GET<Empleado>(`/auth/usuarios/${id}`);
  },

  async actualizarUsuario(
    id: number,
    userData: Partial<Empleado>
  ): Promise<Empleado> {
    return API.PUT<Empleado>(`/auth/usuarios/${id}`, userData);
  },

  async eliminarUsuario(id: number): Promise<void> {
    return API.DELETE(`/auth/usuarios/${id}`);
  },

  logout(): void {
    if (typeof window !== "undefined") {
      localStorage.removeItem("token");
      localStorage.removeItem("user");
      document.cookie = "token=; path=/; max-age=0";
    }
  },

  guardarToken(token: string): void {
    if (typeof window !== "undefined") {
      localStorage.setItem("token", token);
      // Guardar en cookie para el middleware
      document.cookie = `token=${token}; path=/; max-age=86400`;
    }
  },

  obtenerToken(): string | null {
    if (typeof window !== "undefined") {
      return localStorage.getItem("token");
    }
    return null;
  },

  estaAutenticado(): boolean {
    return this.obtenerToken() !== null;
  },
};
