from django.shortcuts import render
from main.models import Experience, Education, Skill, Project
from main.forms import ProjectForm, EducationForm, SkillForm, ExperienceForm
from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
import datetime
from django.contrib.auth.decorators import login_required  
from django.core.exceptions import PermissionDenied       
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import ensure_csrf_cookie
from django.db.models import Q
from django.utils import timezone
from django.utils.formats import date_format

PORTFOLIO_OWNER_NAME = "Della Permata Prasilda"


def is_editor(user):
    """
    True jika user sudah login dan tergabung dalam Django Group 'Editor'.
    Peran Editor: boleh mengubah (update) data portofolio, tapi TIDAK
    boleh membuat (create) atau menghapus (delete) data.
    """
    return user.is_authenticated and user.groups.filter(name="Editor").exists()


def show_main(request):
    experience_list = Experience.objects.all()
    last_login = request.COOKIES.get('last_login', 'Belum ada sesi login / Cookie tidak ditemukan')
    context = {
        "name": PORTFOLIO_OWNER_NAME,
        "npm": "2506656614",
        "study_program": "Information System",
        "bio": (
            "Hi, I’m Della! a Sistem Informasi student who enjoys turning curiosity into something meaningful."
            " I’m interested in how technology, people, and ideas can come together to create useful things."
            " From building digital projects to working on social initiatives, I’m always curious to learn, try something new, and see where it takes me."
            " Still learning, still exploring, and probably still figuring things out, but that’s what makes the journey interesting."
        ),
        "last_login": last_login,
    }
    return render(request, "index.html", context)


def show_experience(request):
    title_query = request.GET.get("title", "").strip()
    experience_list = Experience.objects.all().order_by("-started_at")

    if title_query:
        experience_list = experience_list.filter(title__icontains=title_query)

    context = {
        "name": PORTFOLIO_OWNER_NAME,
        "experience_list": experience_list,
        "title_query": title_query,
        "is_editor": is_editor(request.user),
    }
    return render(request, "experience.html", context)


@login_required(login_url="/login/")
def create_experience(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    form = ExperienceForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Pengalaman baru berhasil ditambahkan!")
        return redirect("main:show_experience")

    context = {
        "name": PORTFOLIO_OWNER_NAME,
        "form": form,
        "is_edit": False,
    }
    return render(request, "experience_form.html", context)


@login_required(login_url="/login/")
def update_experience(request, experience_id):
    if not (request.user.is_superuser or is_editor(request.user)):
        raise PermissionDenied
    experience = get_object_or_404(Experience, pk=experience_id)
    form = ExperienceForm(request.POST or None, instance=experience)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Pengalaman berhasil diperbarui!")
        return redirect("main:show_experience")

    context = {
        "name": PORTFOLIO_OWNER_NAME,
        "form": form,
        "is_edit": True,
        "experience": experience,
    }
    return render(request, "experience_form.html", context)


@login_required(login_url="/login/")
def delete_experience(request, experience_id):
    if not request.user.is_superuser:
        raise PermissionDenied
    experience = get_object_or_404(Experience, pk=experience_id)

    if request.method == "POST":
        experience.delete()
        messages.success(request, "Pengalaman berhasil dihapus!")
        return redirect("main:show_experience")

    return redirect("main:show_experience")


@login_required(login_url="/login/")
def create_project(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    form = ProjectForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Proyek baru berhasil ditambahkan!")
        return redirect("main:show_projects")
    context = {
        "name": PORTFOLIO_OWNER_NAME,
        "form": form,
        "is_edit": False,
    }
    return render(request, "projects_form.html", context)


@require_POST
def create_project_ajax(request):
    if not request.user.is_superuser:
        return JsonResponse(
            {"message": "Hanya pemilik portofolio yang dapat menambahkan proyek."},
            status=403,
        )

    form = ProjectForm(request.POST)
    if form.is_valid():
        project = form.save()
        return JsonResponse(
            {"message": "Proyek berhasil ditambahkan.", "pk": str(project.id)},
            status=201,
        )

    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)


@login_required(login_url="/login/")
def update_project(request, project_id):
    if not (request.user.is_superuser or is_editor(request.user)):
        raise PermissionDenied
    project = get_object_or_404(Project, pk=project_id)
    form = ProjectForm(request.POST or None, instance=project)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Proyek berhasil diperbarui!")
        return redirect("main:show_projects")

    context = {
        "name": PORTFOLIO_OWNER_NAME,
        "form": form,
        "is_edit": True,
        "project": project,
    }
    return render(request, "projects_form.html", context)


def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.prefetch_related('starred_by').all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    data = []
    for project in projects:
        starred_users = project.starred_by.all()
        is_starred = request.user in starred_users if request.user.is_authenticated else False
        starred_by_names = ", ".join([u.username for u in starred_users])

        data.append({
            "model": "main.project",
            "pk": str(project.id),
            "fields": {
                "title": project.title,
                "description": project.description,
                "tech_stack": project.tech_stack,
                "project_url": project.project_url,
                "project_image_url": project.project_image_url,
                "star_count": starred_users.count(),
                "is_starred": is_starred,
                "starred_by_names": starred_by_names,
            }
        })

    return JsonResponse(data, safe=False)


def show_projects(request):
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": PORTFOLIO_OWNER_NAME,
        "title_query": title_query,
        "is_editor": is_editor(request.user),
        "form": ProjectForm(),
    }
    return render(request, "project.html", context)


@login_required(login_url="/login/")
def delete_project(request, project_id):
    if not request.user.is_superuser:
        raise PermissionDenied
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        project.delete()
        messages.success(request, "Project berhasil dihapus!")
        return redirect("main:show_projects")

    return redirect("main:show_projects")

def _format_education_period(education):
    """Contoh: 'Sep 2023 – Sekarang' (sama dengan format di template lama)."""
    started = date_format(timezone.localtime(education.started_at), "M Y")
    if education.is_ongoing:
        ended = "Sekarang"
    else:
        ended = date_format(timezone.localtime(education.ended_at), "M Y")
    return f"{started} \u2013 {ended}"


def _serialize_education(education, user):
    """Menyusun satu item JSON secara manual, termasuk informasi star (Tugas 4)."""
    starred_users = list(education.starred_by.all())  # memakai prefetch_related
    return {
        "model": "main.education",
        "pk": str(education.id),
        "fields": {
            "institution": education.institution,
            "program": education.program,
            "level": education.level,
            "level_display": education.get_level_display(),
            "description": education.description,
            "thumbnail": education.thumbnail or "",
            "period": _format_education_period(education),
            "is_ongoing": education.is_ongoing,
            "star_count": len(starred_users),
            "is_starred": user.is_authenticated and any(u.pk == user.pk for u in starred_users),
            "starred_by_names": ", ".join(u.username for u in starred_users),
        },
    }


@require_GET
def get_education_json(request):
    """
    Endpoint JSON publik (pengunjung yang belum login boleh membaca).
    Parameter opsional ?q= mencari berdasarkan institusi atau program studi.
    """
    query = request.GET.get("q", "").strip()
    education_list = Education.objects.prefetch_related("starred_by").order_by("-started_at")

    if query:
        education_list = education_list.filter(
            Q(institution__icontains=query) | Q(program__icontains=query)
        )

    data = [_serialize_education(education, request.user) for education in education_list]
    return JsonResponse(data, safe=False)


@ensure_csrf_cookie  
def show_education(request):
    """
    Hanya merender KERANGKA halaman. Data dimuat oleh JavaScript lewat
    fetch() ke get_education_json.
    """
    context = {
        "name": PORTFOLIO_OWNER_NAME,
        "is_editor": is_editor(request.user),
        "form": EducationForm(),  
    }
    return render(request, "education.html", context)


@require_POST
def create_education_ajax(request):
    if not request.user.is_superuser:
        return JsonResponse(
            {"message": "Hanya pemilik portofolio yang dapat menambahkan riwayat pendidikan."},
            status=403,
        )

    form = EducationForm(request.POST)
    if form.is_valid():
        education = form.save()
        return JsonResponse(
            {"message": "Riwayat pendidikan berhasil ditambahkan.", "pk": str(education.id)},
            status=201,
        )

    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)


@require_POST
def toggle_education_star(request, education_id):
    if not request.user.is_authenticated:
        return JsonResponse({"message": "Login terlebih dahulu untuk memberi star."}, status=403)

    education = get_object_or_404(Education, pk=education_id)
    if education.starred_by.filter(pk=request.user.pk).exists():
        education.starred_by.remove(request.user)
    else:
        education.starred_by.add(request.user)

    education = Education.objects.prefetch_related("starred_by").get(pk=education_id)
    return JsonResponse(_serialize_education(education, request.user))


@login_required(login_url="/login/")
def create_education(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    form = EducationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Riwayat pendidikan berhasil ditambahkan!")
        return redirect("main:show_education")

    context = {
        "name": PORTFOLIO_OWNER_NAME,
        "form": form,
        "is_edit": False,
    }
    return render(request, "education_form.html", context)


@login_required(login_url="/login/")
def update_education(request, education_id):
    if not (request.user.is_superuser or is_editor(request.user)):
        raise PermissionDenied
    education = get_object_or_404(Education, pk=education_id)
    form = EducationForm(request.POST or None, instance=education)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Riwayat pendidikan berhasil diperbarui!")
        return redirect("main:show_education")

    context = {
        "name": PORTFOLIO_OWNER_NAME,
        "form": form,
        "is_edit": True,
        "education": education,
    }
    return render(request, "education_form.html", context)


@login_required(login_url="/login/")
def delete_education(request, education_id):
    if not request.user.is_superuser:
        raise PermissionDenied
    education = get_object_or_404(Education, pk=education_id)

    if request.method == "POST":
        education.delete()
        messages.success(request, "Riwayat pendidikan berhasil dihapus!")
        return redirect("main:show_education")

    return redirect("main:show_education")

def get_skills_json(request):
    """Mengembalikan seluruh data Skill dalam format JSON."""
    skills = Skill.objects.all()
    skills_json = serializers.serialize("json", skills)
    return HttpResponse(skills_json, content_type="application/json")


def show_skills(request):
    """
    Menampilkan halaman skills. Data diambil melalui fungsi JSON di atas,
    lalu di-deserialize kembali menjadi objek Skill sebelum ditampilkan
    ke template.
    """
    json_response = get_skills_json(request)

    deserialized_objects = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    skill_list = [item.object for item in deserialized_objects]

    context = {
        "name": PORTFOLIO_OWNER_NAME,
        "skill_list": skill_list,
        "is_editor": is_editor(request.user),
    }
    return render(request, "skills.html", context)


@login_required(login_url="/login/")
def create_skill(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    form = SkillForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Skill baru berhasil ditambahkan!")
        return redirect("main:show_skills")

    context = {
        "name": PORTFOLIO_OWNER_NAME,
        "form": form,
        "is_edit": False,
    }
    return render(request, "skills_form.html", context)


@login_required(login_url="/login/")
def update_skill(request, skill_id):
    if not (request.user.is_superuser or is_editor(request.user)):
        raise PermissionDenied
    skill = get_object_or_404(Skill, pk=skill_id)
    form = SkillForm(request.POST or None, instance=skill)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Skill berhasil diperbarui!")
        return redirect("main:show_skills")

    context = {
        "name": PORTFOLIO_OWNER_NAME,
        "form": form,
        "is_edit": True,
        "skill": skill,
    }
    return render(request, "skills_form.html", context)


@login_required(login_url="/login/")
def delete_skill(request, skill_id):
    if not request.user.is_superuser:
        raise PermissionDenied
    skill = get_object_or_404(Skill, pk=skill_id)

    if request.method == "POST":
        skill.delete()
        messages.success(request, "Skill berhasil dihapus!")
        return redirect("main:show_skills")

    return redirect("main:show_skills")

def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Akun berhasil dibuat. Silakan login.")
        return redirect("main:login")

    context = {
        "name": PORTFOLIO_OWNER_NAME,
        "form": form,
    }
    return render(request, "register.html", context)

def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        response = redirect("main:show_main")
        response.set_cookie('last_login', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return response

    context = {
        "name": PORTFOLIO_OWNER_NAME,
        "form": form,
    }
    return render(request, "login.html", context)

def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie('last_login')
    return response

@login_required(login_url="/login/")
def toggle_star(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        if request.user in project.starred_by.all():
            project.starred_by.remove(request.user)
        else:
            project.starred_by.add(request.user)

    return redirect("main:show_projects")