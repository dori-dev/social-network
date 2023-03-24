import os
from .base import *


INSTALLED_APPS = [
    *BASE_INSTALLED_APPS,
    'corsheaders',
]

MIDDLEWARE = [
    *BASE_MIDDLEWARE,
    'corsheaders.middleware.CorsMiddleware',
]

DEBUG = False

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')
CSRF_TRUSTED_ORIGINS = [f"https://{host}" for host in ALLOWED_HOSTS]

STATIC_ROOT = BASE_DIR / 'staticfiles'

# Email
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_USE_TLS = True
EMAIL_HOST = os.getenv('EMAIL_HOST', '')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
EMAIL_PORT = os.getenv('EMAIL_PORT', 587)
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', "Mohammad Dori")
