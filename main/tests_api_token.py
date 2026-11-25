from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from main.models import Project


class TokenAuthAPITest(APITestCase):
    """Alur autentikasi token untuk klien mobile (Tutorial 10)."""

    def setUp(self):
        self.owner = User.objects.create_superuser(
            username="owner", password="test-password", email="owner@example.com",
        )
        self.visitor = User.objects.create_user(username="visitor", password="test-password")
        self.token_url = reverse("api:api_token_auth")
        self.logout_url = reverse("api:api_logout")
        self.list_url = reverse("api:project-list")
        self.payload = {
            "title": "Mobile project", "description": "Dibuat dari Flutter", "tech_stack": "Flutter",
            "project_url": "https://example.com/", "project_image_url": "",
        }

    def _login(self, username="owner", password="test-password"):
        return self.client.post(
            self.token_url, {"username": username, "password": password}, format="json",
        )

    def test_obtain_token_with_valid_credentials(self):
        response = self._login()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["token"], Token.objects.get(user=self.owner).key)

    def test_obtain_token_with_wrong_password_is_rejected(self):
        response = self._login(password="salah")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(Token.objects.exists())

    def test_post_project_without_token_returns_401(self):
        response = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Project.objects.count(), 0)

    def test_post_project_with_invalid_token_returns_401(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token tokenpalsu")
        response = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_superuser_token_can_create_project(self):
        token = self._login().data["token"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
        response = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Project.objects.count(), 1)

    def test_non_superuser_token_cannot_create_project(self):
        token = self._login("visitor").data["token"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
        response = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_public_list_does_not_need_token(self):
        self.assertEqual(self.client.get(self.list_url).status_code, status.HTTP_200_OK)

    def test_logout_revokes_token(self):
        token = self._login().data["token"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Token.objects.filter(key=token).exists())
        # Token yang sudah dicabut tidak bisa dipakai lagi.
        response = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout_without_token_returns_401(self):
        self.assertEqual(self.client.post(self.logout_url).status_code, status.HTTP_401_UNAUTHORIZED)
