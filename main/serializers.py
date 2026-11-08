from django.utils import timezone
from django.utils.formats import date_format
from django.utils.html import strip_tags
from rest_framework import serializers

from main.models import Education, Project


class StarredModelSerializer(serializers.ModelSerializer):
    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()
    starred_by_names = serializers.SerializerMethodField()

    def get_star_count(self, obj):
        return obj.starred_by.count()

    def get_is_starred(self, obj):
        request = self.context.get("request")
        if request is None or not request.user.is_authenticated:
            return False
        return request.user in obj.starred_by.all()

    def get_starred_by_names(self, obj):
        return ", ".join(user.username for user in obj.starred_by.all())


class ProjectSerializer(StarredModelSerializer):
    class Meta:
        model = Project
        fields = [
            "id", "title", "description", "tech_stack",
            "project_url", "project_image_url",
            "star_count", "is_starred", "starred_by_names",
        ]
        read_only_fields = ["id"]

    def validate_title(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Title cannot be empty.")
        return value

    def validate_description(self, value):
        return strip_tags(value)

    def validate_tech_stack(self, value):
        return strip_tags(value)


class EducationSerializer(StarredModelSerializer):
    level_display = serializers.CharField(source="get_level_display", read_only=True)
    is_ongoing = serializers.BooleanField(read_only=True)
    period = serializers.SerializerMethodField()

    class Meta:
        model = Education
        fields = [
            "id", "institution", "program", "level", "level_display",
            "description", "thumbnail", "started_at", "ended_at",
            "period", "is_ongoing",
            "star_count", "is_starred", "starred_by_names",
        ]
        read_only_fields = ["id"]

    def validate_institution(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Nama institusi tidak boleh kosong atau hanya berisi tag HTML.")
        return value

    def validate_program(self, value):
        return strip_tags(value).strip()

    def validate_description(self, value):
        return strip_tags(value).strip()

    def validate(self, attrs):
        started_at = attrs.get("started_at", getattr(self.instance, "started_at", None))
        ended_at = attrs.get("ended_at", getattr(self.instance, "ended_at", None))
        if started_at and ended_at and ended_at < started_at:
            raise serializers.ValidationError(
                {"ended_at": "Tanggal selesai tidak boleh sebelum tanggal mulai."}
            )
        return attrs

    def get_period(self, obj):
        started = date_format(timezone.localtime(obj.started_at), "M Y")
        if obj.is_ongoing:
            ended = "Sekarang"
        else:
            ended = date_format(timezone.localtime(obj.ended_at), "M Y")
        return f"{started} \u2013 {ended}"
