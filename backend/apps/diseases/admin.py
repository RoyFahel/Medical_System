from django.contrib import admin
from .models import Disease


@admin.register(Disease)
class DiseaseAdmin(admin.ModelAdmin):
    list_display = ('id', '__str__', 'created_at')

