import os

if os.getenv('STATE', 'development') == 'production':
    from .production import *
else:
    from .development import *
