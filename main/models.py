import uuid
from django.db import models
from django.contrib.auth.models import User

class Experience(models.Model):

    EXPERIENCE_CHOICES = [
        ('organization', 'Organisasi'),
        ('committee', 'Kepanitiaan'),
        ('volunteer', 'Volunteer'),
        ('competition', 'Lomba/Kompetisi'),
        ('training', 'Pelatihan/Sertifikasi'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    organization = models.CharField(max_length=255, blank=True, default="")
    description = models.TextField()
    category = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, default='organization')
    thumbnail = models.URLField(blank=True, null=True)
    started_at = models.DateTimeField()
    ended_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} {self.started_at.year}"

    @property
    def is_ongoing(self):
        return self.ended_at is None


class Education(models.Model):

    LEVEL_CHOICES = [
        ('sd', 'SD'),
        ('smp', 'SMP'),
        ('sma', 'SMA'),
        ('s1', 'S1'),
        ('s2', 'S2'),
        ('s3', 'S3'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    institution = models.CharField(max_length=255)
    program = models.CharField(max_length=255, blank=True, default="")
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='s1')
    description = models.TextField(blank=True, default="")
    thumbnail = models.URLField(blank=True, null=True)
    started_at = models.DateTimeField()
    ended_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.institution} ({self.get_level_display()})"

    @property
    def is_ongoing(self):
        return self.ended_at is None


class Skill(models.Model):

    CATEGORY_CHOICES = [
        ('language', 'Programming Language'),
        ('framework', 'Framework / Library'),
        ('tool', 'Tool/Platform'),
        ('soft', 'Soft Skill'),
    ]

    LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('expert', 'Expert'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='language')
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='intermediate')
    icon = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['category', 'name']

    def __str__(self):
        return f"{self.name} ({self.get_level_display()})"

class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    tech_stack = models.CharField(max_length=255)
    project_url = models.URLField(blank=True)
    project_image_url = models.URLField(blank=True, max_length=500)
    starred_by = models.ManyToManyField(
        User, related_name="starred_projects", blank=True
    )
    def __str__(self):
        return self.title