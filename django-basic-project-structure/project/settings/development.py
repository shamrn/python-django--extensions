"""Django development-settings for project Finance."""

from .base import *

# General
# --------------------------------------------------------------------------------------------------

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

ALLOWED_HOSTS = [
    # todo: add development host
]

DEBUG = True

INSTALLED_APPS.append('debug_toolbar', )

MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware', )

# Debug toolbar
# --------------------------------------------------------------------------------------------------
DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda request: True,
}


# Celery configuration
# --------------------------------------------------------------------------------------------------
USE_CELERY = True
