import unittest
import asyncio
from unittest.mock import patch, MagicMock

from Backend.services.oauth_service import GoogleOAuthService, GitHubOAuthService

class TestOAuthServices(unittest.TestCase):
    
    def test_google_auth_url(self):
        with patch("Backend.services.oauth_service.GoogleOAuthService.CLIENT_ID", "mock_id"):
            url = GoogleOAuthService.get_auth_url()
            self.assertIn("accounts.google.com/o/oauth2/v2/auth", url)
            self.assertIn("client_id=", url)
            
    def test_github_auth_url(self):
        with patch("Backend.services.oauth_service.GitHubOAuthService.CLIENT_ID", "mock_id"):
            url = GitHubOAuthService.get_auth_url()
            self.assertIn("github.com/login/oauth/authorize", url)
            self.assertIn("client_id=", url)

    # Note: verify_token methods are async and require HTTP calls, which would normally 
    # be mocked using a library like aioresponses or by mocking httpx.AsyncClient.
    # For a basic test suite without external dependencies, we focus on the synchronous methods.

if __name__ == "__main__":
    unittest.main()
