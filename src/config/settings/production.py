import os
from .base import *


INSTALLED_APPS = [
    *BASE_INSTALLED_APPS,
]

MIDDLEWARE = [
    *BASE_MIDDLEWARE,
]

DEBUG = True

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')

STATIC_ROOT = os.getenv('STATIC_ROOT', 'staticfiles')

# Email
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_USE_TLS = True
EMAIL_HOST = os.getenv('EMAIL_HOST', '')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
EMAIL_PORT = os.getenv('EMAIL_PORT', 587)
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', "Mohammad Dori")
