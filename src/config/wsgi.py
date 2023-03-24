"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os
import pathlib

from django.core.wsgi import get_wsgi_application
import dotenv

DOT_ENV_PATH = pathlib.Path() / '.env'
if not DOT_ENV_PATH.exists():
    DOT_ENV_PATH = pathlib.Path() / 'src/.env'
if DOT_ENV_PATH.exists():
    dotenv.read_dotenv(str(DOT_ENV_PATH))
else:
    print(
        "No .env found, be sure to make it.\n"
        "You can rename .env.example file to .env and "
        "set your environ variable in it."
    )

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()
