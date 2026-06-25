"""
OAuth2 service para autenticacion con servicios externos.
"""

import os
from typing import TypedDict
from urllib.parse import urlencode

import httpx


class OAuthUserInfo(TypedDict, total=False):
    email: str | None
    name: str | None
    picture: str | None
    avatar_url: str | None
    username: str | None
    provider: str


class GoogleOAuthService:
    """Google OAuth2 service."""

    CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
    REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:3000/auth/google/callback")

    @staticmethod
    def get_auth_url() -> str:
        """Retorna URL para autenticar."""
        params = {
            "client_id": GoogleOAuthService.CLIENT_ID or "",
            "redirect_uri": GoogleOAuthService.REDIRECT_URI,
            "response_type": "code",
            "scope": "openid email profile",
        }
        return f"https://accounts.google.com/o/oauth2/v2/auth?{urlencode(params)}"

    @staticmethod
    async def verify_token(code: str) -> OAuthUserInfo | None:
        """Verifica codigo y obtiene informacion del usuario."""
        if not GoogleOAuthService.CLIENT_ID or not GoogleOAuthService.CLIENT_SECRET:
            return None

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(
                    "https://oauth2.googleapis.com/token",
                    data={
                        "client_id": GoogleOAuthService.CLIENT_ID,
                        "client_secret": GoogleOAuthService.CLIENT_SECRET,
                        "code": code,
                        "grant_type": "authorization_code",
                        "redirect_uri": GoogleOAuthService.REDIRECT_URI,
                    },
                )

                if response.status_code != 200:
                    return None

                access_token = response.json().get("access_token")
                if not access_token:
                    return None

                user_response = await client.get(
                    "https://www.googleapis.com/oauth2/v1/userinfo",
                    headers={"Authorization": f"Bearer {access_token}"},
                )

                if user_response.status_code != 200:
                    return None

                user_data = user_response.json()
                return {
                    "email": user_data.get("email"),
                    "name": user_data.get("name"),
                    "picture": user_data.get("picture"),
                    "provider": "google",
                }
        except httpx.HTTPError:
            return None


class GitHubOAuthService:
    """GitHub OAuth2 service."""

    CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
    CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")
    REDIRECT_URI = os.getenv("GITHUB_REDIRECT_URI", "http://localhost:3000/auth/github/callback")

    @staticmethod
    def get_auth_url() -> str:
        """Retorna URL para autenticar."""
        params = {
            "client_id": GitHubOAuthService.CLIENT_ID or "",
            "redirect_uri": GitHubOAuthService.REDIRECT_URI,
            "scope": "user:email",
        }
        return f"https://github.com/login/oauth/authorize?{urlencode(params)}"

    @staticmethod
    async def verify_token(code: str) -> OAuthUserInfo | None:
        """Verifica codigo y obtiene informacion del usuario."""
        if not GitHubOAuthService.CLIENT_ID or not GitHubOAuthService.CLIENT_SECRET:
            return None

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(
                    "https://github.com/login/oauth/access_token",
                    data={
                        "client_id": GitHubOAuthService.CLIENT_ID,
                        "client_secret": GitHubOAuthService.CLIENT_SECRET,
                        "code": code,
                    },
                    headers={"Accept": "application/json"},
                )

                if response.status_code != 200:
                    return None

                access_token = response.json().get("access_token")
                if not access_token:
                    return None

                user_response = await client.get(
                    "https://api.github.com/user",
                    headers={"Authorization": f"Bearer {access_token}"},
                )

                if user_response.status_code != 200:
                    return None

                user_data = user_response.json()
                email = user_data.get("email")

                email_response = await client.get(
                    "https://api.github.com/user/emails",
                    headers={"Authorization": f"Bearer {access_token}"},
                )
                if email_response.status_code == 200:
                    emails = email_response.json()
                    primary_email = next((item for item in emails if item.get("primary")), None)
                    email = primary_email.get("email") if primary_email else email

                return {
                    "email": email,
                    "name": user_data.get("name"),
                    "avatar_url": user_data.get("avatar_url"),
                    "username": user_data.get("login"),
                    "provider": "github",
                }
        except httpx.HTTPError:
            return None
