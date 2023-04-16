import os
from pathlib import Path
import subprocess
import dotenv
from .base import *

BASE_DIR = Path(__file__).resolve().parent.parent.parent


DOT_ENV_PATH = BASE_DIR / '.env'
if DOT_ENV_PATH.exists():
    dotenv.read_dotenv(str(DOT_ENV_PATH))
else:
    print(
        "No .env found, be sure to make it.\n"
        "You can rename .env.example file to .env and "
        "set your environ variable in it."
    )

if os.getenv('STATE', 'development') == 'production':
    from .production import *
    print('production state')
else:
    from .development import *
    print('development state')

if os.environ.get('process_tasks') is None:
    os.environ['process_tasks'] = 'running'
    subprocess.Popen(['python', 'manage.py', 'process_tasks'])
