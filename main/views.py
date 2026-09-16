from django.shortcuts import render
from main.models import Experience, Education, Skill, Project
from main.forms import ProjectForm
from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render


def show_main(request):
    experience_list = Experience.objects.all()
    context = {
        "name": "Della Permata Prasilda",
        "npm": "2506656614",
        "study_program": "Information System",
        "bio": (
            "Hi, I’m Della! a Sistem Informasi student who enjoys turning curiosity into something meaningful."
            " I’m interested in how technology, people, and ideas can come together to create useful things."
            " From building digital projects to working on social initiatives, I’m always curious to learn, try something new, and see where it takes me."
            " Still learning, still exploring, and probably still figuring things out, but that’s what makes the journey interesting."
        ),
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Della Permata Prasilda",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)


def show_education(request):
    context = {
        "name": "Della Permata Prasilda",
        "education_list": Education.objects.all().order_by('-started_at'),
    }
    return render(request, "education.html", context)


def show_skills(request):
    context = {
        "name": "Della Permata Prasilda",
        "skill_list": Skill.objects.all(),
    }
    return render(request, "skills.html", context)


def create_project(request):
    form = ProjectForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Proyek baru berhasil ditambahkan!")
        return redirect("main:show_projects")
    context = {
        "name": "Della Permata Prasilda",
        "form": form,
    }
    return render(request, "projects_form.html", context)


def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    projects_json = serializers.serialize("json", projects)
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
        "name": "Della Permata Prasilda",
        "project_list": projects,
        "title_query": title_query,
    }
    return render(request, "project.html", context)


def delete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        project.delete()
        messages.success(request, "Project berhasil dihapus!")
        return redirect("main:show_projects")

    return redirect("main:show_projects")