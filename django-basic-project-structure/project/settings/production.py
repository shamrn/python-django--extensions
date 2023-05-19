"""Django production-settings for project Finance."""
from .base import *  # NOQA


# General
# --------------------------------------------------------------------------------------------------

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

ALLOWED_HOSTS = [
    # todo: add production host
]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
