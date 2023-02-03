from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from . import models


class LikeFilter(admin.SimpleListFilter):
    title = 'تعداد لایک'
    parameter_name = 'likes'

    def lookups(self, request, model_admin):
        return (
            ('low', 'کم'),
            ('normal', 'متوسط'),
            ('much', 'زیاد'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'low':
            return queryset.filter(
                total_likes__lte=100,
            )
        if self.value() == 'normal':
            return queryset.filter(
                total_likes__gt=100,
                total_likes__lt=500,
            )
        if self.value() == 'much':
            return queryset.filter(
                total_likes__gte=500,
            )


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'post_link',
        'image_file',
        'created',
        'total_likes',
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
            _('Information'), {
                'fields': [
                    'description',
                ]
            }
        ),
        (
            _('Image'), {
                'fields': [
                    'image',
                ]
            }
        ),
        (
            _('Other'), {
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
