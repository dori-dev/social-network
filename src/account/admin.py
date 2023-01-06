from django.contrib import admin
from . import models


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'date_of_birth',
        'photo',
    ]
    list_filter = [
        'date_of_birth',
    ]
    search_fields = [
        'user__username',
    ]
    date_hierarchy = 'date_of_birth'
    raw_id_fields = [
        'user',
    ]
