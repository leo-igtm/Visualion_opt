// lib/auth/oauth.ts
import { API } from "@/service/api";
import { authService, AuthResponse } from "@/service/authService";

export const oauthFrontendService = {
  /**
   * Obtiene la URL de redirección para Google OAuth
   */
  async getGoogleAuthUrl(): Promise<string> {
    const response = await API.GET<{ url: string }>("/auth/oauth/google/url");
    return response.url;
  },

  /**
   * Obtiene la URL de redirección para GitHub OAuth
   */
  async getGithubAuthUrl(): Promise<string> {
    const response = await API.GET<{ url: string }>("/auth/oauth/github/url");
    return response.url;
  },

  /**
   * Procesa el código de Google y guarda la sesión
   */
  async handleGoogleCallback(code: string): Promise<AuthResponse> {
    const response = await API.POST<AuthResponse>(`/auth/oauth/google/callback?code=${code}`, {});
    if (response.access_token) {
      authService.guardarToken(response.access_token);
    }
    return response;
  },

  /**
   * Procesa el código de GitHub y guarda la sesión
   */
  async handleGithubCallback(code: string): Promise<AuthResponse> {
    const response = await API.POST<AuthResponse>(`/auth/oauth/github/callback?code=${code}`, {});
    if (response.access_token) {
      authService.guardarToken(response.access_token);
    }
    return response;
  }
};
