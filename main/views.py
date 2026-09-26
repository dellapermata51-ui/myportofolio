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

PORTFOLIO_OWNER_NAME = "Della Permata Prasilda"


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
    if not request.user.is_superuser:
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


@login_required(login_url="/login/")
def update_project(request, project_id):
    if not request.user.is_superuser:
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
    projects = Project.objects.all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    projects_json = serializers.serialize("json", projects, use_natural_foreign_keys=True)
    return HttpResponse(projects_json, content_type="application/json")


def show_projects(request):
    json_response = get_projects_json(request)

    projects = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    projects = [project.object for project in projects]
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": PORTFOLIO_OWNER_NAME,
        "project_list": projects,
        "title_query": title_query,
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

def get_education_json(request):
    """Mengembalikan seluruh data Education dalam format JSON."""
    education_list = Education.objects.all().order_by("-started_at")
    education_json = serializers.serialize("json", education_list)
    return HttpResponse(education_json, content_type="application/json")


def show_education(request):
    """
    Menampilkan halaman education. Data diambil melalui fungsi JSON di atas,
    lalu di-deserialize kembali menjadi objek Education sebelum ditampilkan
    ke template — meniru alur pengambilan data lewat "API" internal.
    """
    json_response = get_education_json(request)

    deserialized_objects = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    education_list = [item.object for item in deserialized_objects]

    context = {
        "name": PORTFOLIO_OWNER_NAME,
        "education_list": education_list,
    }
    return render(request, "education.html", context)

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
    if not request.user.is_superuser:
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
    if not request.user.is_superuser:
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