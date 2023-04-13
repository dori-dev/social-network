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

ALLOWED_HOSTS = [
    'app',
]
CSRF_TRUSTED_ORIGINS = []
for host in os.getenv('ALLOWED_HOSTS', '').split(','):
    CSRF_TRUSTED_ORIGINS.extend([
        f"http://{host}",
        f"https://{host}",
    ])

STATIC_ROOT = BASE_DIR / 'staticfiles'

# Email
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_USE_TLS = True
EMAIL_HOST = os.getenv('EMAIL_HOST', '')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
EMAIL_PORT = os.getenv('EMAIL_PORT', 587)
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', "Mohammad Dori")
