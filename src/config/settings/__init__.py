import os
from .base import *

if os.getenv('STATE', 'development') == 'production':
    from .production import *
    print('production state')
else:
    from .development import *
    print('development state')
