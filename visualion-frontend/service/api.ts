// services/api.ts - Configuración base
const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export class APIError extends Error {
  constructor(
    public status: number,
    public detail: string
  ) {
    super(detail);
    this.name = "APIError";
  }
}

async function fetchAPI<T>(
  endpoint: string,
  options?: RequestInit
): Promise<T> {
  const url = `${API_BASE}${endpoint}`;
  const token = typeof window !== "undefined" ? localStorage.getItem("token") : null;

  const headers: HeadersInit = {
    "Content-Type": "application/json",
    ...(token && { Authorization: `Bearer ${token}` }),
    ...options?.headers,
  };

  try {
    const response = await fetch(url, {
      ...options,
      headers,
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new APIError(response.status, errorData.detail || "Error en la solicitud");
    }

    return await response.json();
  } catch (error) {
    if (error instanceof APIError) throw error;
    throw new APIError(500, error instanceof Error ? error.message : "Error desconocido");
  }
}

export async function GET<T>(endpoint: string): Promise<T> {
  return fetchAPI<T>(endpoint, { method: "GET" });
}

export async function POST<T>(endpoint: string, data: any): Promise<T> {
  return fetchAPI<T>(endpoint, {
    method: "POST",
    body: JSON.stringify(data),
  });
}

export async function PUT<T>(endpoint: string, data: any): Promise<T> {
  return fetchAPI<T>(endpoint, {
    method: "PUT",
    body: JSON.stringify(data),
  });
}

export async function DELETE<T>(endpoint: string): Promise<T> {
  return fetchAPI<T>(endpoint, { method: "DELETE" });
}

export const API = { GET, POST, PUT, DELETE };

// Auth functions
export async function login(usuario: string, contraseña: string) {
  const response = await POST<{ access_token: string }>("/auth/login", { usuario, contraseña });
  if (response.access_token) {
    // Store token in both localStorage and cookies
    if (typeof window !== "undefined") {
      localStorage.setItem("token", response.access_token);
      document.cookie = `token=${response.access_token}; path=/; max-age=86400`;
    }
  }
  return response;
}

export async function register(userData: any) {
  return POST("/auth/register", userData);
}

export async function logout() {
  if (typeof window !== "undefined") {
    localStorage.removeItem("token");
    document.cookie = "token=; path=/; max-age=0";
  }
}

export async function fetchUsuarios() {
  return GET("/auth/usuarios");
}

export async function obtenerUsuario(id: number) {
  return GET(`/auth/usuarios/${id}`);
}

export async function actualizarUsuario(id: number, userData: any) {
  return PUT(`/auth/usuarios/${id}`, userData);
}

export async function eliminarUsuario(id: number) {
  return DELETE(`/auth/usuarios/${id}`);
}
