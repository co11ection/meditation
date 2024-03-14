from django.contrib import admin
from .models import DataForApp


@admin.register(DataForApp)
class DataForApp(admin.ModelAdmin):
    list_display = [field.name for field in DataForApp._meta.get_fields()]
    list_filter = ["language"]
    search_fields = ["language"]
