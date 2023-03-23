from .base import *

THIRD_PARTY_APPS = [
    'django_extensions',
    'debug_toolbar',
]

INSTALLED_APPS = [
    *BASE_INSTALLED_APPS,
    *THIRD_PARTY_APPS,
]

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    *BASE_MIDDLEWARE,
]

DEBUG = True

ALLOWED_HOSTS = [
    'mysite.com',
    '127.0.0.1',
    'localhost',
]

# Email
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
