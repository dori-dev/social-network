from .base import *


INSTALLED_APPS = [
    *BASE_INSTALLED_APPS,
    'django_extensions',
    'debug_toolbar',
]

MIDDLEWARE = [
    *BASE_MIDDLEWARE,
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

DEBUG = True

ALLOWED_HOSTS = [
    'mysite.com',
    '127.0.0.1',
    'localhost',
    '0.0.0.0',
]

# Email
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
