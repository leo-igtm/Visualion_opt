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

// Auth functions have been moved to authService.ts and empleadosService.ts
