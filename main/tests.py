import json

from django.contrib.auth.models import User, Group
from django.test import Client, TestCase
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
        self.superuser = User.objects.create_superuser(
            username="admin_test", password="testpass123"
        )
        self.client.force_login(self.superuser)

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
        # Halaman hanya berisi kerangka; data dimuat lewat AJAX dari endpoint JSON.
        response = self.client.get(reverse("main:get_education_json"))
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
        self.superuser = User.objects.create_superuser(
            username="admin_test", password="testpass123"
        )
        self.client.force_login(self.superuser)

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
        self.superuser = User.objects.create_superuser(
            username="admin_test", password="testpass123"
        )
        self.client.force_login(self.superuser)

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
        # Halaman Projects dimuat lewat AJAX, jadi cek endpoint JSON-nya.
        response = self.client.get(reverse("main:get_projects_json"))
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


class AuthAndAuthorizationTest(TestCase):
    """
    Tes tambahan untuk memastikan 4 peran (Pengunjung, Pengguna biasa,
    Editor, Pemilik/superuser) berperilaku sesuai spesifikasi Individual
    Assignment 4. Pola yang diuji di sini pada model Project berlaku
    identik untuk Experience, Education, dan Skill karena logika
    is_editor()/is_superuser di views.py sama untuk keempatnya.
    """

    def setUp(self):
        self.project = Project.objects.create(
            title="Project Uji Otorisasi",
            description="Dipakai untuk menguji star dan pembatasan akses.",
            tech_stack="Django",
        )
        self.regular_user = User.objects.create_user(
            username="regular_test", password="testpass123"
        )
        self.superuser = User.objects.create_superuser(
            username="admin_test2", password="testpass123"
        )

        editor_group, _ = Group.objects.get_or_create(name="Editor")
        self.editor_user = User.objects.create_user(
            username="editor_test", password="testpass123"
        )
        self.editor_user.groups.add(editor_group)

    # --- Autentikasi & cookie (Tutorial 4, tetap divalidasi di sini) ---

    def test_register_creates_new_account(self):
        response = self.client.post(reverse("main:register"), {
            "username": "new_user_test",
            "password1": "SuperSecret123!",
            "password2": "SuperSecret123!",
        })
        self.assertRedirects(response, reverse("main:login"))
        self.assertTrue(User.objects.filter(username="new_user_test").exists())

    def test_login_sets_last_login_cookie(self):
        response = self.client.post(reverse("main:login"), {
            "username": self.regular_user.username,
            "password": "testpass123",
        })
        self.assertRedirects(response, reverse("main:show_main"))
        self.assertIn("last_login", response.cookies)

    def test_logout_deletes_last_login_cookie(self):
        self.client.login(username=self.regular_user.username, password="testpass123")
        response = self.client.get(reverse("main:logout"))
        self.assertRedirects(response, reverse("main:show_main"))
        self.assertEqual(response.cookies["last_login"].value, "")

    # --- Pengunjung tanpa login (Anonymous) ---

    def test_anonymous_user_redirected_to_login_for_create_project(self):
        response = self.client.get(reverse("main:create_project"))
        self.assertRedirects(
            response,
            f"{reverse('main:login')}?next={reverse('main:create_project')}",
        )

    def test_anonymous_user_redirected_to_login_for_update_project(self):
        response = self.client.get(reverse("main:update_project", args=[self.project.id]))
        self.assertRedirects(
            response,
            f"{reverse('main:login')}?next={reverse('main:update_project', args=[self.project.id])}",
        )

    def test_anonymous_user_redirected_to_login_for_toggle_star(self):
        response = self.client.post(
            reverse("main:toggle_star", args=[self.project.id])
        )
        self.assertRedirects(
            response,
            f"{reverse('main:login')}?next={reverse('main:toggle_star', args=[self.project.id])}",
        )

    # --- Pengguna biasa: hanya boleh baca + star ---

    def test_regular_user_can_toggle_star(self):
        self.client.login(username=self.regular_user.username, password="testpass123")

        response = self.client.post(
            reverse("main:toggle_star", args=[self.project.id])
        )
        self.assertRedirects(response, reverse("main:show_projects"))
        self.assertIn(self.regular_user, self.project.starred_by.all())

        # Toggle kedua kali membatalkan star
        response = self.client.post(
            reverse("main:toggle_star", args=[self.project.id])
        )
        self.assertNotIn(self.regular_user, self.project.starred_by.all())

    def test_regular_user_forbidden_from_create_project(self):
        self.client.login(username=self.regular_user.username, password="testpass123")
        response = self.client.get(reverse("main:create_project"))
        self.assertEqual(response.status_code, 403)

    def test_regular_user_forbidden_from_update_project(self):
        self.client.login(username=self.regular_user.username, password="testpass123")
        response = self.client.get(reverse("main:update_project", args=[self.project.id]))
        self.assertEqual(response.status_code, 403)

    def test_regular_user_forbidden_from_delete_project(self):
        self.client.login(username=self.regular_user.username, password="testpass123")
        response = self.client.post(reverse("main:delete_project", args=[self.project.id]))
        self.assertEqual(response.status_code, 403)

    # --- Editor: boleh update, TIDAK boleh create/delete ---

    def test_editor_can_access_update_project_page(self):
        self.client.login(username=self.editor_user.username, password="testpass123")
        response = self.client.get(reverse("main:update_project", args=[self.project.id]))
        self.assertEqual(response.status_code, 200)

    def test_editor_can_update_project_via_post(self):
        self.client.login(username=self.editor_user.username, password="testpass123")
        response = self.client.post(reverse("main:update_project", args=[self.project.id]), {
            "title": "Project Uji Otorisasi (Updated by Editor)",
            "description": self.project.description,
            "tech_stack": self.project.tech_stack,
            "project_url": "",
            "project_image_url": "",
        })
        self.project.refresh_from_db()
        self.assertRedirects(response, reverse("main:show_projects"))
        self.assertEqual(self.project.title, "Project Uji Otorisasi (Updated by Editor)")

    def test_editor_forbidden_from_create_project(self):
        self.client.login(username=self.editor_user.username, password="testpass123")
        response = self.client.get(reverse("main:create_project"))
        self.assertEqual(response.status_code, 403)

    def test_editor_forbidden_from_delete_project(self):
        self.client.login(username=self.editor_user.username, password="testpass123")
        response = self.client.post(reverse("main:delete_project", args=[self.project.id]))
        self.assertEqual(response.status_code, 403)

    def test_editor_can_toggle_star(self):
        self.client.login(username=self.editor_user.username, password="testpass123")
        response = self.client.post(
            reverse("main:toggle_star", args=[self.project.id])
        )
        self.assertRedirects(response, reverse("main:show_projects"))
        self.assertIn(self.editor_user, self.project.starred_by.all())

    # --- Pemilik (superuser): boleh semua ---

    def test_superuser_can_access_create_project(self):
        self.client.login(username=self.superuser.username, password="testpass123")
        response = self.client.get(reverse("main:create_project"))
        self.assertEqual(response.status_code, 200)

    def test_superuser_can_access_update_project(self):
        self.client.login(username=self.superuser.username, password="testpass123")
        response = self.client.get(reverse("main:update_project", args=[self.project.id]))
        self.assertEqual(response.status_code, 200)

    def test_superuser_can_delete_project(self):
        self.client.login(username=self.superuser.username, password="testpass123")
        response = self.client.post(reverse("main:delete_project", args=[self.project.id]))
        self.assertRedirects(response, reverse("main:show_projects"))
        self.assertFalse(Project.objects.filter(id=self.project.id).exists())


class EducationAjaxTest(TestCase):
    """Tugas 5: AJAX list, pencarian, tambah via modal, hak akses, CSRF, XSS, star."""

    VALID_DATA = {
        "institution": "Institut Teknologi Bandung",
        "program": "Teknik Informatika",
        "level": "s1",
        "description": "Pertukaran pelajar satu semester.",
        "thumbnail": "",
        "started_at": "2023-08-01T08:00",
        "ended_at": "",
    }

    def setUp(self):
        # Tanpa password agar test lebih cepat (login memakai force_login).
        self.superuser = User.objects.create_superuser(username="admin_t5")
        self.regular = User.objects.create_user(username="biasa_t5")
        self.editor = User.objects.create_user(username="editor_t5")
        editor_group, _ = Group.objects.get_or_create(name="Editor")
        self.editor.groups.add(editor_group)

        self.education = Education.objects.create(
            institution="Universitas Indonesia",
            program="Sistem Informasi",
            description="S1 di Fasilkom.",
            started_at=timezone.now(),
        )
        self.add_url = reverse("main:create_education_ajax")

    def test_page_renders_skeleton_without_data(self):
        response = self.client.get(reverse("main:show_education"))
        self.assertEqual(response.status_code, 200)
        for element_id in ('id="loading"', 'id="error"', 'id="empty"', 'id="grid"'):
            self.assertContains(response, element_id)
        self.assertNotContains(response, "S1 di Fasilkom.")  # data dimuat lewat AJAX

    def test_search_filters_json_by_institution(self):
        url = reverse("main:get_education_json")
        self.assertEqual(len(json.loads(self.client.get(url, {"q": "indonesia"}).content)), 1)
        self.assertEqual(json.loads(self.client.get(url, {"q": "tidak-ada"}).content), [])

    def test_superuser_can_create_returns_201(self):
        self.client.force_login(self.superuser)
        response = self.client.post(self.add_url, self.VALID_DATA)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Education.objects.filter(institution="Institut Teknologi Bandung").exists())

    def test_invalid_input_returns_400(self):
        self.client.force_login(self.superuser)
        response = self.client.post(self.add_url, {**self.VALID_DATA, "institution": ""})
        self.assertEqual(response.status_code, 400)
        self.assertIn("institution", response.json()["errors"])

    def test_non_superuser_returns_403(self):
        # pengunjung (anonim) lalu user biasa dan Editor
        self.assertEqual(self.client.post(self.add_url, self.VALID_DATA).status_code, 403)
        for user in (self.regular, self.editor):
            self.client.force_login(user)
            self.assertEqual(self.client.post(self.add_url, self.VALID_DATA).status_code, 403)
        self.assertEqual(Education.objects.count(), 1)

    def test_post_without_csrf_token_is_rejected(self):
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.superuser)
        self.assertEqual(client.post(self.add_url, self.VALID_DATA).status_code, 403)
        self.assertEqual(Education.objects.count(), 1)

    def test_html_is_rejected_or_stripped_on_server(self):
        self.client.force_login(self.superuser)
        # hanya berisi tag HTML -> kosong setelah strip_tags -> ditolak
        payload = "<img src=\"x\" onerror=\"alert('XSS!')\">"
        response = self.client.post(self.add_url, {**self.VALID_DATA, "institution": payload})
        self.assertEqual(response.status_code, 400)
        # campuran teks dan tag -> tag dibuang, teks disimpan
        response = self.client.post(self.add_url, {**self.VALID_DATA, "program": "<b>Informatika</b>"})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Education.objects.get(pk=response.json()["pk"]).program, "Informatika")

    def test_star_requires_login_and_toggles(self):
        url = reverse("main:toggle_education_star", args=[self.education.id])
        self.assertEqual(self.client.post(url).status_code, 403)  # pengunjung ditolak

        self.client.force_login(self.regular)
        fields = self.client.post(url).json()["fields"]
        self.assertEqual((fields["star_count"], fields["is_starred"]), (1, True))
        fields = self.client.post(url).json()["fields"]
        self.assertEqual((fields["star_count"], fields["is_starred"]), (0, False))