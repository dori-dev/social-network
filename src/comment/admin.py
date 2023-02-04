from django.contrib import admin
from . import models


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'post',
        'is_reply',
        'created',
    ]
    list_filter = [
        'created',
        'is_reply',
    ]
    search_fields = [
        'user__username',
        'body',
        'post__slug',
        'reply__body',
    ]
    date_hierarchy = 'created'
    raw_id_fields = [
        'user',
        'post',
        'reply',
    ]
