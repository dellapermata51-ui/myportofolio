from django.shortcuts import render

from main.models import Experience


def show_main(request):
    context = {
        "name": "Della Permata Prasilda",
        "npm": "2506656614",
        "study_program": "S1 Sistem Informasi",
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