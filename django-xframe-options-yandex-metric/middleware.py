from django.middleware import clickjacking
import re
from project.apps.extensions.functions import get_current_site


class CustomXFrameOptionsMiddleware(clickjacking.XFrameOptionsMiddleware):
    """Custom middleware for header "X-Frame-Options" http-responses, for Yandex-metrics."""

    def get_xframe_options_value(self, request, response):
        """
        Overridden method, check redirect link with request, if link is from yandex metric
        and current site, return value 'SAMEORIGN'
        """

        available_referer = None
        if http_referer := request.META.get('HTTP_REFERER'):  # NOQA
            available_referer = re.match(self._get_regex_yandex_metric(request), http_referer)
        return 'SAMEORIGIN' if available_referer else 'DENY'

    @staticmethod
    def _get_regex_yandex_metric(request):
        """Return a regular expression with our site and domain"""

        current_site = str(get_current_site(request))
        re_index = current_site.rfind('.')
        site, domain = current_site[:re_index], current_site[re_index:].replace('.', '')

        # regular expression taken with https://yandex.ru/support/metrica/behavior/click-map.html#iframe  # NOQA
        return (fr'^https?:\/\/([^\/]+\.)?({site}\.{domain}|webvisor\.com|metri[ck]a\.yandex\.'
                r'(com|ru|by|com\.tr))\/')
