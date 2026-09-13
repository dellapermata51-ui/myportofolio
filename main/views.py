from django.shortcuts import render
from main.models import Experience, Education, Skill


def show_main(request):
    experience_list = Experience.objects.all()
    context = {
        "name": "Della Permata Prasilda",
        "npm": "2506656614",
        "study_program": "Information System",
        "bio": (
            "Mahasiswa program studi Sistem Informasi, Fakultas Ilmu Komputer, Universitas Indonesia yang tertarik "
            "pada pengembangan perangkat lunak dan pendidikan."
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