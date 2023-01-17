from django.contrib import admin
from . import models


@admin.register(models.Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'verb',
        'target',
        'created',
    ]
    list_filter = [
        'created',
        'target_ct',
    ]
    search_fields = [
        'user__username',
        'user__username',
        'verb',
    ]
    date_hierarchy = 'created'
    raw_id_fields = [
        'user',
    ]
