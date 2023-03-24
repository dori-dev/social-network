"""social network URL Configuration
"""
import os
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', include('home.urls', namespace='home')),
    path('admin/', include('custom.urls')),
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('posts/', include('post.urls', namespace='post')),
    path('users/', include('contact.urls', namespace='user')),
    path('actions/', include('action.urls', namespace='action')),
    path('search/', include('search.urls', namespace='search')),
] + staticfiles_urlpatterns()

if settings.DEBUG and os.getenv('STATE') == 'development':
    urlpatterns += [
        path('__debug__/', include('debug_toolbar.urls')),
    ]
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
