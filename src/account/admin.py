from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from . import models


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'date_of_birth',
        'bio',
        'photo',
    ]
    list_filter = [
        'date_of_birth',
    ]
    search_fields = [
        'user__username',
        'bio',
    ]
    date_hierarchy = 'date_of_birth'
    raw_id_fields = [
        'user',
    ]


@admin.register(models.CustomUser)
class CustomUserAdmin(UserAdmin):
    pass


admin.site.unregister(Group)
