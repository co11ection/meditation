from django.contrib import admin
from .models import Feedback


@admin.register(Feedback)
class InfoAdmin(admin.ModelAdmin):
    list_display = ("topic", "description", "email_feedback")
