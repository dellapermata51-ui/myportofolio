import uuid

from django.contrib.auth.models import Group, User
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from main.models import Education


class EducationAPIEditorTest(APITestCase):
    """Peran Editor pada API Education: boleh PUT/PATCH, tidak boleh create/delete."""

    def setUp(self):
        self.owner = User.objects.create_superuser(
            username="owner", password="test-password", email="owner@example.com",
        )
        self.visitor = User.objects.create_user(username="visitor", password="test-password")
        self.editor = User.objects.create_user(username="editor", password="test-password")
        editor_group, _ = Group.objects.get_or_create(name="Editor")
        self.editor.groups.add(editor_group)

        self.education = Education.objects.create(
            institution="Universitas Indonesia", program="Sistem Informasi",
            level="s1", description="Kuliah", started_at=timezone.now(),
        )
        self.list_url = reverse("api:education-list")
        self.detail_url = reverse("api:education-detail", args=[self.education.id])
        self.star_url = reverse("api:education-star", args=[self.education.id])
        self.payload = {
            "institution": "SMA Negeri 1", "program": "IPA", "level": "sma",
            "description": "SMA", "thumbnail": "", "started_at": "2020-07-01T00:00:00Z",
            "ended_at": "2023-06-01T00:00:00Z",
        }

    def test_public_can_read_and_search(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["id"], str(self.education.id))
        self.assertNotIn("fields", response.data[0])
        self.assertEqual(len(self.client.get(self.list_url, {"q": "sistem"}).data), 1)
        self.assertEqual(self.client.get(self.list_url, {"q": "tidak-ada"}).data, [])
        self.assertEqual(self.client.get(self.detail_url).status_code, status.HTTP_200_OK)
        missing = reverse("api:education-detail", args=[uuid.uuid4()])
        self.assertEqual(self.client.get(missing).status_code, status.HTTP_404_NOT_FOUND)

    def test_guest_and_regular_user_cannot_write(self):
        for user in (None, self.visitor):
            self.client.force_authenticate(user=user)
            self.assertEqual(self.client.post(self.list_url, self.payload, format="json").status_code, 403)
            self.assertEqual(self.client.patch(self.detail_url, {"program": "X"}, format="json").status_code, 403)
            self.assertEqual(self.client.delete(self.detail_url).status_code, 403)
        self.assertEqual(Education.objects.count(), 1)

    def test_editor_can_patch_and_put_but_not_create_or_delete(self):
        self.client.force_authenticate(user=self.editor)

        response = self.client.patch(self.detail_url, {"program": "Ilmu Komputer"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.education.refresh_from_db()
        self.assertEqual(self.education.program, "Ilmu Komputer")
        self.assertEqual(self.education.institution, "Universitas Indonesia")

        response = self.client.put(self.detail_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Education.objects.count(), 1)

    def test_owner_can_create_and_delete(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.client.delete(self.detail_url).status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Education.objects.filter(pk=self.education.id).exists())

    def test_validation(self):
        self.client.force_authenticate(user=self.owner)
        for changes, field in [
            ({"institution": '<b></b>'}, "institution"),
            ({"ended_at": "2019-01-01T00:00:00Z"}, "ended_at"),
            ({"thumbnail": "javascript:alert(1)"}, "thumbnail"),
        ]:
            response = self.client.post(self.list_url, {**self.payload, **changes}, format="json")
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn(field, response.data)
        self.assertEqual(Education.objects.count(), 1)

    def test_star_available_to_every_logged_in_role(self):
        self.assertEqual(self.client.post(self.star_url).status_code, status.HTTP_403_FORBIDDEN)
        for user in (self.visitor, self.editor, self.owner):
            self.client.force_authenticate(user=user)
            response = self.client.post(self.star_url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertTrue(response.data["is_starred"])
            response = self.client.post(self.star_url)
            self.assertFalse(response.data["is_starred"])
