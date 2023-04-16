#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from pathlib import Path
import dotenv


def main():
    """Run administrative tasks."""
    BASE_DIR = Path(__file__).resolve().parent
    DOT_ENV_PATH = BASE_DIR / '.env'
    if DOT_ENV_PATH.exists():
        dotenv.read_dotenv(str(DOT_ENV_PATH))
    else:
        print(
            "No .env found, be sure to make it.\n"
            "You can rename .env.example file to .env and "
            "set your environ variable in it."
        )
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
