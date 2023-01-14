from django.contrib import admin
from django.db.models import Count
from django.utils.html import format_html
from . import models


class LikeFilter(admin.SimpleListFilter):
    title = 'likes count'
    parameter_name = 'likes'

    def lookups(self, request, model_admin):
        return (
            ('low', 'Few likes'),
            ('normal', 'Lot of Likes'),
            ('much', "Too many likes"),
        )

    def queryset(self, request, queryset):
        likes = queryset.annotate(
            likes=Count('users_like'),
        )
        if self.value() == 'low':
            return likes.filter(
                likes__lte=1000,
            )
        if self.value() == 'normal':
            return likes.filter(
                likes__gt=1000,
                likes__lt=50_000,
            )
        if self.value() == 'much':
            return likes.filter(
                likes__gte=50_000,
            )


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'post_link',
        'image_file',
        'created',
        'likes',
    ]
    search_fields = [
        'user__username',
        'description',
        'slug',
    ]
    date_hierarchy = 'created'
    raw_id_fields = [
        'user',
    ]
    fieldsets = [
        (
            None, {
                'fields': [
                    'user',
                ]
            }
        ),
        (
            'Information', {
                'fields': [
                    'description',
                ]
            }
        ),
        (
            'Image', {
                'fields': [
                    'image',
                ]
            }
        ),
        (
            'Other', {
                'fields': [
                    'slug',
                    'users_like',
                ]
            }
        ),
    ]
    list_filter = [
        'created',
        LikeFilter,
    ]

    def post_link(self, model: models.Post):
        url = model.get_absolute_url()
        return format_html(
            f'<a target="_blank" href="{url}">Url</a>'
        )

    def image_file(self, model: models.Post):
        image_url = model.image.url
        return format_html(
            f'<a target="_blank" href="{image_url}">File</a>'
        )

    def likes(self, model: models.Post):
        return model.users_like.count()
