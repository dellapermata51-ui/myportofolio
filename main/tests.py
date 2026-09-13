from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from main.models import Experience, Education, Skill

class MainTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="Staff BEM Pengabdian Masyarakat Fasilkom UI",
            description="Turning ideas into meaningful community initiatives through collaboration, planning, and hands-on execution.",
            category="organization",
        )

    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertNotContains(response, self.experience.title)
        self.assertContains(response, f'href="{reverse("main:show_experience")}"')

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/halaman-yang-tidak-ada/")

        self.assertEqual(response.status_code, 404)

    def test_experience_model(self):
        self.assertEqual(str(self.experience), "Staff BEM Pengabdian Masyarakat Fasilkom UI 2026")
        self.assertEqual(self.experience.category, "organization")
        self.assertTrue(self.experience.is_ongoing)

    def test_experience_page(self):
        response = self.client.get(reverse("main:show_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")
        self.assertContains(response, self.experience.title)
        self.assertContains(response, self.experience.description)
        self.assertContains(response, "Organisasi")
        self.assertContains(response, "Sedang berlangsung")
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))

        self.assertContains(response, "Belum ada pengalaman yang ditambahkan.")

    def test_completed_experience(self):
        self.experience.ended_at = timezone.now()
        self.experience.save()
        response = self.client.get(reverse("main:show_experience"))

        self.assertFalse(self.experience.is_ongoing)
        self.assertContains(response, "Selesai")
        self.assertNotContains(response, "Sedang berlangsung")


class EducationPageTest(TestCase):

    def setUp(self):
        self.education = Education.objects.create(
            institution="Universitas Indonesia",
            program="Sistem Informasi",
            level="s1",
            description="Menempuh pendidikan S1 Sistem Informasi di Fakultas Ilmu Komputer.",
        )

    def test_url_accessible_and_uses_correct_template(self):
        response = self.client.get(reverse("main:show_education"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "education.html")

    def test_education_data_appears_when_data_exists(self):
        response = self.client.get(reverse("main:show_education"))
        self.assertContains(response, self.education.institution)
        self.assertContains(response, self.education.program)
        self.assertContains(response, self.education.description)

    def test_empty_state_shown_when_no_data(self):
        Education.objects.all().delete()
        response = self.client.get(reverse("main:show_education"))
        self.assertContains(response, "Belum ada riwayat pendidikan yang ditambahkan.")


class SkillPageTest(TestCase):

    def setUp(self):
        self.skill = Skill.objects.create(
            name="Django",
            category="framework",
            level="advanced",
        )

    def test_url_accessible_and_uses_correct_template(self):
        response = self.client.get(reverse("main:show_skills"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "skills.html")

    def test_skill_data_appears_when_data_exists(self):
        response = self.client.get(reverse("main:show_skills"))
        self.assertContains(response, self.skill.name)
        self.assertContains(response, "Advanced")
        self.assertContains(response, "Framework / Library")

    def test_empty_state_shown_when_no_data(self):
        Skill.objects.all().delete()
        response = self.client.get(reverse("main:show_skills"))
        self.assertContains(response, "Belum ada skill yang ditambahkan.")