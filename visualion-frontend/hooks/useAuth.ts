// hooks/useAuth.ts
"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { authService } from "@/service/authService";

export function useAuth() {
  const router = useRouter();
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const checkAuth = async () => {
      try {
        const token = authService.obtenerToken();
        if (!token) {
          router.push("/login");
          return;
        }
        setIsAuthenticated(true);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Error de autenticación");
        router.push("/login");
      } finally {
        setIsLoading(false);
      }
    };

    checkAuth();
  }, [router]);

  const logout = () => {
    authService.logout();
    router.push("/login");
  };

  return {
    isAuthenticated,
    isLoading,
    error,
    logout,
  };
}
