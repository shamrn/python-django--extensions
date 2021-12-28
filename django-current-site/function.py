from rest_framework.request import Request
from django.contrib.sites.requests import RequestSite
from django.contrib.sites.models import Site
from django.conf import settings
from django.apps import apps


def get_current_site(request: Request = None):
    """
    Check if contrib.sites is installed and return either the current
    "Site" object or a "RequestSite" object based on the request.
    """

    # Imports are inside the function because its point is to avoid importing
    # the Site models when django.contrib.sites isn't installed.
    if apps.is_installed('django.contrib.sites'):
        return Site.objects.get_current(request)
    else:
        return RequestSite(request)


def get_current_site_url(request: Request = None, scheme: str = None):
    """
    Check if contrib.sites is installed and return either the current
    "Site" URL or a "RequestSite" URL based on the request.
    """

    site = get_current_site(request)
    site_scheme = settings.SITE_SCHEME or scheme or 'http'
    return f'{site_scheme}://{site.domain}'
