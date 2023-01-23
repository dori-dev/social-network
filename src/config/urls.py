"""social network URL Configuration
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin/', include('custom.urls', namespace='admin')),
    path('account/', include('account.urls')),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('posts/', include('post.urls', namespace='post')),
    path('users/', include('contact.urls', namespace='user')),
    path('actions/', include('action.urls', namespace='action')),
    path('__debug__/', include('debug_toolbar.urls')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
