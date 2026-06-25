// hooks/useAuth.ts
"use client";

import { useEffect, useState, useCallback } from "react";
import { useRouter } from "next/navigation";
import { authService } from "@/service/authService";

export function useAuth() {
  const router = useRouter();
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const checkAuth = () => {
      try {
        const token = authService.obtenerToken();
        if (token) {
          setIsAuthenticated(true);
        }
      } catch (err) {
        // In case of error reading token, assume not authenticated
        setIsAuthenticated(false);
      } finally {
        setIsLoading(false);
      }
    };

    checkAuth();
  }, []);

  const login = useCallback(
    async (usuario: string, contraseña: string) => {
      try {
        const response = await authService.login(usuario, contraseña);
        authService.guardarToken(response.access_token);
        setIsAuthenticated(true);
        setError(null);
        router.push("/dashboard"); // Redirigir a dashboard
      } catch (err) {
        setError(err instanceof Error ? err.message : "Error de autenticación");
        setIsAuthenticated(false);
        throw err;
      }
    },
    [router]
  );

  const logout = useCallback(() => {
    authService.logout();
    setIsAuthenticated(false);
    router.push("/login");
  }, [router]);

  return {
    isAuthenticated,
    isLoading,
    error,
    login,
    logout,
  };
}
