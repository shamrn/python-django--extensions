"""Django settings for project Finance."""
import os

match os.environ.get('SETTINGS_CONFIGURATION'):
    case 'local':
        from .local import *
    case 'development':
        from .development import *
    case 'production':
        from .production import *
    case _:
        from .base import *
