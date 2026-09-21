import json

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from main.models import Experience, Education, Skill, Project


class MainTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="Staff BEM Pengabdian Masyarakat Fasilkom UI",
            description="Turning ideas into meaningful community initiatives through collaboration, planning, and hands-on execution.",
            category="organization",
            started_at=timezone.now(),
        )

    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertNotContains(response, self.experience.title)
        self.assertContains(response, f'href="{reverse("main:show_experience")}"')

    def test_experience_model(self):
        self.assertEqual(str(self.experience), f"Staff BEM Pengabdian Masyarakat Fasilkom UI {self.experience.started_at.year}")
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
            started_at=timezone.now(),
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

    def test_create_education_page_is_accessible(self):
        response = self.client.get(reverse("main:create_education"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "education_form.html")

    def test_create_education_via_post_saves_new_record(self):
        education_count_before = Education.objects.count()
        response = self.client.post(reverse("main:create_education"), {
            "institution": "Institut Teknologi Bandung",
            "program": "Teknik Informatika",
            "level": "s1",
            "description": "Pertukaran pelajar satu semester.",
            "thumbnail": "",
            "started_at": "2023-08-01T08:00",
            "ended_at": "",
        })

        self.assertEqual(Education.objects.count(), education_count_before + 1)
        self.assertRedirects(response, reverse("main:show_education"))
        self.assertTrue(Education.objects.filter(institution="Institut Teknologi Bandung").exists())

    def test_update_education_page_is_accessible_and_prefilled(self):
        response = self.client.get(reverse("main:update_education", args=[self.education.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "education_form.html")
        self.assertContains(response, self.education.institution)

    def test_update_education_via_post_changes_existing_record(self):
        response = self.client.post(reverse("main:update_education", args=[self.education.id]), {
            "institution": "Universitas Indonesia",
            "program": "Sistem Informasi (Updated)",
            "level": "s1",
            "description": self.education.description,
            "thumbnail": "",
            "started_at": self.education.started_at.strftime("%Y-%m-%dT%H:%M"),
            "ended_at": "",
        })

        self.education.refresh_from_db()
        self.assertRedirects(response, reverse("main:show_education"))
        self.assertEqual(self.education.program, "Sistem Informasi (Updated)")

    def test_delete_education_via_post_removes_record(self):
        response = self.client.post(reverse("main:delete_education", args=[self.education.id]))
        self.assertRedirects(response, reverse("main:show_education"))
        self.assertFalse(Education.objects.filter(id=self.education.id).exists())

    def test_education_json_endpoint_returns_valid_json(self):
        response = self.client.get(reverse("main:get_education_json"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["content-type"], "application/json")

        data = json.loads(response.content)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["model"], "main.education")
        self.assertEqual(data[0]["fields"]["institution"], self.education.institution)


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

    def test_create_skill_page_is_accessible(self):
        response = self.client.get(reverse("main:create_skill"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "skills_form.html")

    def test_create_skill_via_post_saves_new_record(self):
        skill_count_before = Skill.objects.count()
        response = self.client.post(reverse("main:create_skill"), {
            "name": "Python",
            "category": "language",
            "level": "expert",
            "icon": "",
        })

        self.assertEqual(Skill.objects.count(), skill_count_before + 1)
        self.assertRedirects(response, reverse("main:show_skills"))
        self.assertTrue(Skill.objects.filter(name="Python").exists())

    def test_update_skill_page_is_accessible_and_prefilled(self):
        response = self.client.get(reverse("main:update_skill", args=[self.skill.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "skills_form.html")
        self.assertContains(response, self.skill.name)

    def test_update_skill_via_post_changes_existing_record(self):
        response = self.client.post(reverse("main:update_skill", args=[self.skill.id]), {
            "name": "Django",
            "category": "framework",
            "level": "expert",
            "icon": "",
        })

        self.skill.refresh_from_db()
        self.assertRedirects(response, reverse("main:show_skills"))
        self.assertEqual(self.skill.level, "expert")

    def test_delete_skill_via_post_removes_record(self):
        response = self.client.post(reverse("main:delete_skill", args=[self.skill.id]))
        self.assertRedirects(response, reverse("main:show_skills"))
        self.assertFalse(Skill.objects.filter(id=self.skill.id).exists())

    def test_skill_json_endpoint_returns_valid_json(self):
        response = self.client.get(reverse("main:get_skills_json"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["content-type"], "application/json")

        data = json.loads(response.content)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["model"], "main.skill")
        self.assertEqual(data[0]["fields"]["name"], self.skill.name)


class ProjectPageTest(TestCase):

    def setUp(self):
        self.project = Project.objects.create(
            title="Portfolio Website",
            description="Website portofolio pribadi yang dibangun dengan Django.",
            tech_stack="Django, HTML, CSS",
        )

    def test_url_accessible_and_uses_correct_template(self):
        response = self.client.get(reverse("main:show_projects"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "project.html")

    def test_project_data_appears_when_data_exists(self):
        response = self.client.get(reverse("main:show_projects"))
        self.assertContains(response, self.project.title)
        self.assertContains(response, self.project.tech_stack)

    def test_empty_state_shown_when_no_data(self):
        Project.objects.all().delete()
        response = self.client.get(reverse("main:show_projects"))
        self.assertEqual(response.status_code, 200)

    def test_create_project_page_is_accessible(self):
        response = self.client.get(reverse("main:create_project"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "projects_form.html")

    def test_create_project_via_post_saves_new_record(self):
        project_count_before = Project.objects.count()
        response = self.client.post(reverse("main:create_project"), {
            "title": "Sistem Informasi Akademik",
            "description": "Sistem untuk mengelola data akademik mahasiswa.",
            "tech_stack": "Laravel, MySQL",
            "project_url": "",
            "project_image_url": "",
        })

        self.assertEqual(Project.objects.count(), project_count_before + 1)
        self.assertRedirects(response, reverse("main:show_projects"))
        self.assertTrue(Project.objects.filter(title="Sistem Informasi Akademik").exists())

    def test_delete_project_via_post_removes_record(self):
        response = self.client.post(reverse("main:delete_project", args=[self.project.id]))
        self.assertRedirects(response, reverse("main:show_projects"))
        self.assertFalse(Project.objects.filter(id=self.project.id).exists())

    def test_project_json_endpoint_returns_valid_json(self):
        response = self.client.get(reverse("main:get_projects_json"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["content-type"], "application/json")

        data = json.loads(response.content)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["model"], "main.project")
        self.assertEqual(data[0]["fields"]["title"], self.project.title)