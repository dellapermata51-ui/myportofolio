import uuid

from django.contrib.auth.models import Group, User
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from main.models import Education


class EducationAPITestBase(APITestCase):
    """Data uji bersama: empat peran (pengunjung, pengguna biasa, Editor, pemilik)."""

    def setUp(self):
        self.owner = User.objects.create_superuser(
            username="owner", password="test-password", email="owner@example.com",
        )
        self.regular = User.objects.create_user(
            username="regular", password="test-password", email="regular@example.com",
        )
        self.editor = User.objects.create_user(username="editor", password="test-password")
        # Database uji kosong, tetapi grup Editor sudah dibuat oleh migration 0009.
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

    def assert_education_unchanged(self):
        self.assertEqual(Education.objects.count(), 1)
        self.education.refresh_from_db()
        self.assertEqual(self.education.institution, "Universitas Indonesia")
        self.assertEqual(self.education.program, "Sistem Informasi")
        self.assertEqual(self.education.description, "Kuliah")
        self.assertEqual(self.education.starred_by.count(), 0)


class EducationAPIEditorTest(EducationAPITestBase):
    """Peran Editor pada API Education: boleh PUT/PATCH, tidak boleh create/delete."""

    def test_public_can_read_and_search(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["id"], str(self.education.id))
        self.assertNotIn("fields", response.data[0])
        self.assertEqual(len(self.client.get(self.list_url, {"q": "sistem"}).data), 1)
        self.assertEqual(len(self.client.get(self.list_url, {"q": "indonesia"}).data), 1)
        self.assertEqual(self.client.get(self.list_url, {"q": "tidak-ada"}).data, [])
        self.assertEqual(self.client.get(self.detail_url).status_code, status.HTTP_200_OK)
        missing = reverse("api:education-detail", args=[uuid.uuid4()])
        self.assertEqual(self.client.get(missing).status_code, status.HTTP_404_NOT_FOUND)

    def test_guest_and_regular_user_cannot_write(self):
        for user in (None, self.regular):
            self.client.force_authenticate(user=user)
            self.assertEqual(self.client.post(self.list_url, self.payload, format="json").status_code, 403)
            self.assertEqual(self.client.put(self.detail_url, self.payload, format="json").status_code, 403)
            self.assertEqual(self.client.patch(self.detail_url, {"program": "X"}, format="json").status_code, 403)
            self.assertEqual(self.client.delete(self.detail_url).status_code, 403)
            self.assert_education_unchanged()  # isi database, bukan hanya status HTTP

    def test_editor_can_patch_and_put_but_not_create_or_delete(self):
        self.client.force_authenticate(user=self.editor)

        response = self.client.patch(self.detail_url, {"program": "Ilmu Komputer"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.education.refresh_from_db()
        self.assertEqual(self.education.program, "Ilmu Komputer")
        self.assertEqual(self.education.institution, "Universitas Indonesia")  # PATCH parsial

        response = self.client.put(self.detail_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.education.refresh_from_db()
        self.assertEqual(self.education.institution, "SMA Negeri 1")  # PUT mengganti semua

        response = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Education.objects.count(), 1)
        self.assertTrue(Education.objects.filter(pk=self.education.id).exists())

    def test_owner_can_create_and_delete(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Education.objects.filter(pk=response.data["id"], institution="SMA Negeri 1").exists())

        self.assertEqual(self.client.delete(self.detail_url).status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Education.objects.filter(pk=self.education.id).exists())

    def test_missing_object_returns_404_for_writers(self):
        missing = reverse("api:education-detail", args=[uuid.uuid4()])
        self.client.force_authenticate(user=self.owner)
        self.assertEqual(self.client.patch(missing, {"program": "X"}, format="json").status_code, 404)
        self.assertEqual(self.client.delete(missing).status_code, 404)
        missing_star = reverse("api:education-star", args=[uuid.uuid4()])
        self.assertEqual(self.client.post(missing_star).status_code, 404)


class EducationAPIValidationTest(EducationAPITestBase):
    """Validasi input di serializer: 400 untuk input tidak valid, strip_tags untuk teks."""

    def test_invalid_input_returns_400_and_changes_nothing(self):
        self.client.force_authenticate(user=self.owner)
        for changes, field in [
            ({"institution": "<b></b>"}, "institution"),
            ({"institution": ""}, "institution"),
            ({"ended_at": "2019-01-01T00:00:00Z"}, "ended_at"),
            ({"thumbnail": "javascript:alert(1)"}, "thumbnail"),
            ({"level": "profesor"}, "level"),
        ]:
            response = self.client.post(self.list_url, {**self.payload, **changes}, format="json")
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, changes)
            self.assertIn(field, response.data)
        self.assertEqual(Education.objects.count(), 1)

    def test_invalid_patch_returns_400_and_keeps_data(self):
        self.client.force_authenticate(user=self.editor)
        response = self.client.patch(self.detail_url, {"institution": "<i></i>"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.patch(self.detail_url, {"ended_at": "1990-01-01T00:00:00Z"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("ended_at", response.data)
        self.assert_education_unchanged()
        self.assertIsNone(self.education.ended_at)

    def test_text_is_cleaned_with_strip_tags(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, {
            **self.payload,
            "institution": "  <b>SMA</b> Negeri 2 ",
            "program": "<script>alert('x')</script>IPS",
            "description": "<img src=x onerror=alert(1)>Juara kelas",
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        saved = Education.objects.get(pk=response.data["id"])
        self.assertEqual(saved.institution, "SMA Negeri 2")
        self.assertNotIn("<", saved.program)
        self.assertIn("IPS", saved.program)
        self.assertEqual(saved.description, "Juara kelas")

    def test_computed_fields_are_read_only(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, {
            **self.payload,
            "id": str(uuid.uuid4()), "star_count": 99, "is_starred": True,
            "starred_by_names": "hacker", "period": "palsu", "level_display": "palsu",
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["star_count"], 0)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(response.data["starred_by_names"], "")
        self.assertEqual(response.data["level_display"], "SMA")
        self.assertEqual(response.data["period"], "Jul 2020 \u2013 Jun 2023")
        self.assertFalse(response.data["is_ongoing"])
        self.assertEqual(Education.objects.get(pk=response.data["id"]).starred_by.count(), 0)

    def test_explicit_fields_exclude_sensitive_account_data(self):
        self.education.starred_by.add(self.owner, self.regular)
        self.client.force_authenticate(user=self.owner)
        response = self.client.get(self.detail_url)
        self.assertEqual(
            set(response.data),
            {
                "id", "institution", "program", "level", "level_display",
                "description", "thumbnail", "started_at", "ended_at",
                "period", "is_ongoing", "star_count", "is_starred", "starred_by_names",
            },
        )
        raw = response.content.decode()
        self.assertNotIn("@example.com", raw)   # email tidak ikut tampil
        self.assertNotIn("pbkdf2", raw)         # password hash tidak ikut tampil
        self.assertEqual(response.data["star_count"], 2)


class EducationAPIStarTest(EducationAPITestBase):
    def test_guest_cannot_star(self):
        self.assertEqual(self.client.post(self.star_url).status_code, status.HTTP_403_FORBIDDEN)
        self.assert_education_unchanged()  # tidak ada star yang tersimpan

    def test_star_available_to_every_logged_in_role(self):
        for user in (self.regular, self.editor, self.owner):
            self.client.force_authenticate(user=user)
            response = self.client.post(self.star_url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertTrue(response.data["is_starred"])
            self.assertTrue(self.education.starred_by.filter(pk=user.pk).exists())
            response = self.client.post(self.star_url)
            self.assertFalse(response.data["is_starred"])
            self.assertFalse(self.education.starred_by.filter(pk=user.pk).exists())

    def test_starrer_always_comes_from_request_user(self):
        self.client.force_authenticate(user=self.regular)
        response = self.client.post(self.star_url, {"user": self.owner.pk, "username": "owner"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(list(self.education.starred_by.all()), [self.regular])
        self.assertEqual(response.data["star_count"], 1)
        self.assertEqual(response.data["starred_by_names"], "regular")

    def test_star_rejects_get(self):
        self.client.force_authenticate(user=self.regular)
        self.assertEqual(self.client.get(self.star_url).status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class EducationAPICsrfTest(EducationAPITestBase):
    """SessionAuthentication wajib CSRF. force_authenticate melewati proses ini,
    jadi bukti CSRF memakai APIClient(enforce_csrf_checks=True) dan .login()."""

    def setUp(self):
        super().setUp()
        self.csrf_client = APIClient(enforce_csrf_checks=True)

    def _csrf_headers(self):
        """Ambil cookie csrftoken dari halaman Education (memakai @ensure_csrf_cookie)."""
        self.csrf_client.get(reverse("main:show_education"))
        return {"HTTP_X_CSRFTOKEN": self.csrf_client.cookies["csrftoken"].value}

    def test_owner_post_without_csrf_token_is_rejected(self):
        self.assertTrue(self.csrf_client.login(username="owner", password="test-password"))
        response = self.csrf_client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("CSRF", str(response.data["detail"]))
        self.assertEqual(Education.objects.count(), 1)

    def test_owner_post_with_csrf_token_succeeds(self):
        self.assertTrue(self.csrf_client.login(username="owner", password="test-password"))
        response = self.csrf_client.post(
            self.list_url, self.payload, format="json", **self._csrf_headers(),
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Education.objects.count(), 2)

    def test_editor_patch_and_delete_without_csrf_token_are_rejected(self):
        self.assertTrue(self.csrf_client.login(username="editor", password="test-password"))
        response = self.csrf_client.patch(self.detail_url, {"program": "X"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assert_education_unchanged()

        self.assertTrue(self.csrf_client.login(username="owner", password="test-password"))
        self.assertEqual(self.csrf_client.delete(self.detail_url).status_code, status.HTTP_403_FORBIDDEN)
        self.assert_education_unchanged()

    def test_editor_patch_with_csrf_token_succeeds(self):
        self.assertTrue(self.csrf_client.login(username="editor", password="test-password"))
        response = self.csrf_client.patch(
            self.detail_url, {"program": "Ilmu Komputer"}, format="json", **self._csrf_headers(),
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.education.refresh_from_db()
        self.assertEqual(self.education.program, "Ilmu Komputer")

    def test_star_without_csrf_token_is_rejected_even_when_logged_in(self):
        self.assertTrue(self.csrf_client.login(username="regular", password="test-password"))
        response = self.csrf_client.post(self.star_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assert_education_unchanged()

        response = self.csrf_client.post(self.star_url, **self._csrf_headers())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.education.starred_by.count(), 1)

    def test_force_authenticate_skips_csrf_so_it_cannot_prove_protection(self):
        client = APIClient(enforce_csrf_checks=True)
        client.force_authenticate(user=self.owner)
        response = client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # tanpa token, tetap lolos
