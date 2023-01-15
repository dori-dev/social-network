from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
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


@admin.register(models.CustomUser)
class CustomUserAdmin(UserAdmin):
    pass


@admin.register(models.Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = [
        'user_from',
        'user_to',
        'created',
    ]
    list_filter = [
        'created',
    ]
    search_fields = [
        'user_from__username',
        'user_to__username',
    ]
    date_hierarchy = 'created'
    raw_id_fields = [
        'user_from',
        'user_to',
    ]
