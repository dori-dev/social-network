import os
import subprocess
from .base import *

if os.getenv('STATE') == 'production':
    from .production import *
    print('production state')
else:
    from .development import *
    print('development state')

if os.environ.get('process_tasks') is None:
    os.environ['process_tasks'] = 'running'
    subprocess.Popen(['python', 'manage.py', 'process_tasks'])
