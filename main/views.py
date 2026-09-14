from django.shortcuts import render
from main.models import Experience, Education, Skill


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