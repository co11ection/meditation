from django.contrib import admin
from .models import ProjectConfidential, ProjectInfo, ProjectPolitic


@admin.register(ProjectInfo)
class InfoAdmin(admin.ModelAdmin):
    list_display = ("id", "text")


@admin.register(ProjectPolitic)
class PoliticAdmin(admin.ModelAdmin):
    list_display = ("id", "text")


@admin.register(ProjectConfidential)
class ConfidentialAdmin(admin.ModelAdmin):
    list_display = ("id", "text")
