from django.urls import path
from main.views import (
    show_main, show_experience, create_experience, update_experience, delete_experience,
    create_project, create_project_ajax, update_project, show_projects, get_projects_json, delete_project, toggle_star,
    create_education, create_education_ajax, update_education, delete_education,
    get_education_json, show_education, toggle_education_star,
    create_skill, update_skill, delete_skill, get_skills_json, show_skills,
    register, login_user, logout_user,
)

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),

    # Experience
    path("experience/", show_experience, name="show_experience"),
    path("experience/add/", create_experience, name="create_experience"),
    path("experience/<uuid:experience_id>/edit/", update_experience, name="update_experience"),
    path("experience/<uuid:experience_id>/delete/", delete_experience, name="delete_experience"),

    # Projects
    path("projects/", show_projects, name="show_projects"),
    path("projects/add/", create_project, name="create_project"),
    path("projects/add-ajax/", create_project_ajax, name="create_project_ajax"),
    path("api/projects/", get_projects_json, name="get_projects_json"),
    path("projects/<uuid:project_id>/edit/", update_project, name="update_project"),
    path("projects/<uuid:project_id>/delete/", delete_project, name="delete_project"),
    path("projects/<uuid:project_id>/star/", toggle_star, name="toggle_star"),

    # Education
    path("education/", show_education, name="show_education"),
    path("education/add/", create_education, name="create_education"),
    path("education/add-ajax/", create_education_ajax, name="create_education_ajax"),
    path("api/education/", get_education_json, name="get_education_json"),
    path("education/<uuid:education_id>/edit/", update_education, name="update_education"),
    path("education/<uuid:education_id>/delete/", delete_education, name="delete_education"),
    path("education/<uuid:education_id>/star/", toggle_education_star, name="toggle_education_star"),

    # Skills
    path("skills/", show_skills, name="show_skills"),
    path("skills/add/", create_skill, name="create_skill"),
    path("api/skills/", get_skills_json, name="get_skills_json"),
    path("skills/<uuid:skill_id>/edit/", update_skill, name="update_skill"),
    path("skills/<uuid:skill_id>/delete/", delete_skill, name="delete_skill"),

    # Login
    path("register/", register, name="register"),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),
]