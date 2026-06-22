"""
OAuth2 Service para autenticación con servicios externos
"""

import os
import httpx
from typing import Optional, Dict


class GoogleOAuthService:
    """Google OAuth2 Service"""

    CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
    REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:3000/auth/google/callback")

    @staticmethod
    def get_auth_url() -> str:
        """Retorna URL para autenticar"""
        return (
            f"https://accounts.google.com/o/oauth2/v2/auth?"
            f"client_id={GoogleOAuthService.CLIENT_ID}&"
            f"redirect_uri={GoogleOAuthService.REDIRECT_URI}&"
            f"response_type=code&"
            f"scope=openid%20email%20profile"
        )

    @staticmethod
    async def verify_token(code: str) -> Optional[Dict]:
        """Verifica código y obtiene info del usuario"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://oauth2.googleapis.com/token",
                    data={
                        "client_id": GoogleOAuthService.CLIENT_ID,
                        "client_secret": GoogleOAuthService.CLIENT_SECRET,
                        "code": code,
                        "grant_type": "authorization_code",
                        "redirect_uri": GoogleOAuthService.REDIRECT_URI
                    }
                )

                if response.status_code != 200:
                    return None

                data = response.json()
                access_token = data.get("access_token")

                # Obtener info del usuario
                user_response = await client.get(
                    "https://www.googleapis.com/oauth2/v1/userinfo",
                    headers={"Authorization": f"Bearer {access_token}"}
                )

                if user_response.status_code != 200:
                    return None

                user_data = user_response.json()

                return {
                    "email": user_data.get("email"),
                    "name": user_data.get("name"),
                    "picture": user_data.get("picture"),
                    "provider": "google"
                }
        except Exception as e:
            print(f"Error in Google OAuth: {e}")
            return None


class GitHubOAuthService:
    """GitHub OAuth2 Service"""

    CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
    CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")
    REDIRECT_URI = os.getenv("GITHUB_REDIRECT_URI", "http://localhost:3000/auth/github/callback")

    @staticmethod
    def get_auth_url() -> str:
        """Retorna URL para autenticar"""
        return (
            f"https://github.com/login/oauth/authorize?"
            f"client_id={GitHubOAuthService.CLIENT_ID}&"
            f"redirect_uri={GitHubOAuthService.REDIRECT_URI}&"
            f"scope=user:email"
        )

    @staticmethod
    async def verify_token(code: str) -> Optional[Dict]:
        """Verifica código y obtiene info del usuario"""
        try:
            async with httpx.AsyncClient() as client:
                # Obtener access token
                response = await client.post(
                    "https://github.com/login/oauth/access_token",
                    data={
                        "client_id": GitHubOAuthService.CLIENT_ID,
                        "client_secret": GitHubOAuthService.CLIENT_SECRET,
                        "code": code,
                    },
                    headers={"Accept": "application/json"}
                )

                if response.status_code != 200:
                    return None

                token_data = response.json()
                access_token = token_data.get("access_token")

                if not access_token:
                    return None

                # Obtener info del usuario
                user_response = await client.get(
                    "https://api.github.com/user",
                    headers={"Authorization": f"Bearer {access_token}"}
                )

                if user_response.status_code != 200:
                    return None

                user_data = user_response.json()

                # Obtener email
                email_response = await client.get(
                    "https://api.github.com/user/emails",
                    headers={"Authorization": f"Bearer {access_token}"}
                )

                email = None
                if email_response.status_code == 200:
                    emails = email_response.json()
                    primary_email = next((e for e in emails if e.get("primary")), None)
                    email = primary_email.get("email") if primary_email else None

                return {
                    "email": email or user_data.get("email"),
                    "name": user_data.get("name"),
                    "avatar_url": user_data.get("avatar_url"),
                    "username": user_data.get("login"),
                    "provider": "github"
                }
        except Exception as e:
            print(f"Error in GitHub OAuth: {e}")
            return None
