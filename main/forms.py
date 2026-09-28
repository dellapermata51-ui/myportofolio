from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm, TextInput, Textarea, URLInput, Select, DateTimeInput
from django.utils.html import strip_tags

from main.models import Project, Education, Skill, Experience


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = [
            "title",
            "description",
            "tech_stack",
            "project_url",
            "project_image_url",
        ]

        labels = {
            "title": "Nama Proyek",
            "description": "Deskripsi Proyek",
            "tech_stack": "Teknologi yang Digunakan",
            "project_url": "URL Proyek",
            "project_image_url": "URL Gambar Proyek",
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Portfolio Website",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Ceritakan Proyekmu",
                    "rows": 3,
                }
            ),
            "tech_stack": TextInput(
                attrs={
                    "placeholder": "Django, Python, HTML, CSS",
                }
            ),
            "project_url": URLInput(
                attrs={
                    "placeholder": "https://github.com/kakBurhan/burhanquestv4",
                }
            ),
            "project_image_url": URLInput(
                attrs={
                    "placeholder": "https://drive.google.com/thumbnail?id=...&sz=w1000",
                }
            ),
        }

    # Lapisan pertahanan kedua terhadap XSS: buang tag HTML saat data masuk.
    # Pertahanan utama tetap escapeHtml() di sisi JavaScript saat menampilkan.
    def clean_title(self):
        title = strip_tags(self.cleaned_data["title"]).strip()
        if not title:
            raise ValidationError("Nama proyek tidak boleh hanya berisi tag HTML.")
        return title

    def clean_tech_stack(self):
        tech_stack = strip_tags(self.cleaned_data["tech_stack"]).strip()
        if not tech_stack:
            raise ValidationError("Teknologi yang digunakan tidak boleh hanya berisi tag HTML.")
        return tech_stack

    def clean_description(self):
        description = strip_tags(self.cleaned_data["description"]).strip()
        if not description:
            raise ValidationError("Deskripsi proyek tidak boleh hanya berisi tag HTML.")
        return description


class EducationForm(ModelForm):
    started_at = forms.DateTimeField(
        label="Tanggal Mulai",
        required=True,
        input_formats=["%Y-%m-%dT%H:%M"],
        widget=DateTimeInput(
            attrs={"type": "datetime-local"},
            format="%Y-%m-%dT%H:%M",
        ),
    )

    ended_at = forms.DateTimeField(
        label="Tanggal Selesai",
        required=False,
        input_formats=["%Y-%m-%dT%H:%M"],
        widget=DateTimeInput(
            attrs={"type": "datetime-local"},
            format="%Y-%m-%dT%H:%M",
        ),
        help_text="Kosongkan jika pendidikan ini masih berlangsung.",
    )

    class Meta:
        model = Education
        fields = [
            "institution",
            "program",
            "level",
            "description",
            "thumbnail",
            "started_at",
            "ended_at",
        ]

        labels = {
            "institution": "Institusi",
            "program": "Program Studi",
            "level": "Jenjang",
            "description": "Deskripsi",
            "thumbnail": "URL Gambar/Logo",
        }

        widgets = {
            "institution": TextInput(
                attrs={
                    "placeholder": "Universitas Indonesia",
                    "maxlength": 255,
                }
            ),
            "program": TextInput(
                attrs={
                    "placeholder": "Sistem Informasi",
                }
            ),
            "level": Select(),
            "description": Textarea(
                attrs={
                    "placeholder": "Ceritakan pengalaman pendidikanmu",
                    "rows": 3,
                }
            ),
            "thumbnail": URLInput(
                attrs={
                    "placeholder": "https://.../logo-institusi.png",
                }
            ),
        }


class SkillForm(ModelForm):
    class Meta:
        model = Skill
        fields = [
            "name",
            "category",
            "level",
        ]

        labels = {
            "name": "Nama Skill",
            "category": "Kategori",
            "level": "Level",
        }

        widgets = {
            "name": TextInput(
                attrs={
                    "placeholder": "Django",
                    "maxlength": 100,
                }
            ),
            "category": Select(),
            "level": Select(),
        }


class ExperienceForm(ModelForm):
    started_at = forms.DateTimeField(
        label="Tanggal Mulai",
        required=True,
        input_formats=["%Y-%m-%dT%H:%M"],
        widget=DateTimeInput(
            attrs={"type": "datetime-local"},
            format="%Y-%m-%dT%H:%M",
        ),
    )

    ended_at = forms.DateTimeField(
        label="Tanggal Selesai",
        required=False,
        input_formats=["%Y-%m-%dT%H:%M"],
        widget=DateTimeInput(
            attrs={"type": "datetime-local"},
            format="%Y-%m-%dT%H:%M",
        ),
        help_text="Kosongkan jika pengalaman ini masih berlangsung.",
    )

    class Meta:
        model = Experience
        fields = [
            "title",
            "organization",
            "category",
            "description",
            "thumbnail",
            "started_at",
            "ended_at",
        ]

        labels = {
            "title": "Judul Pengalaman",
            "organization": "Organisasi/Instansi",
            "category": "Kategori",
            "description": "Deskripsi",
            "thumbnail": "URL Gambar/Logo",
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Staff BEM Fasilkom UI",
                    "maxlength": 255,
                }
            ),
            "organization": TextInput(
                attrs={
                    "placeholder": "BEM Fasilkom UI",
                }
            ),
            "category": Select(),
            "description": Textarea(
                attrs={
                    "placeholder": "Ceritakan pengalamanmu",
                    "rows": 3,
                }
            ),
            "thumbnail": URLInput(
                attrs={
                    "placeholder": "https://.../logo-organisasi.png",
                }
            ),
        }