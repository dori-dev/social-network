from django.contrib import admin
from . import models


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
