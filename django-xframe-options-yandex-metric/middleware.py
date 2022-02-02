from django.middleware import clickjacking
import re
from project.apps.extensions.functions import get_current_site


class CustomXFrameOptionsMiddleware(clickjacking.XFrameOptionsMiddleware):
    """Custom middleware for header "X-Frame-Options" http-responses, for Yandex-metrics."""

    def process_response(self, request, response):
        """Overridden method assign 'X-Frame-Options' for http header"""

        # If the method returns False (the link is not this site or Yandex),
        # assign a header and its value 'DENY'
        if not self.available_referer(request):
            return super(CustomXFrameOptionsMiddleware, self).process_response(request, response)
        return response

    def available_referer(self, request):
        """
        Check redirect link with request, if link not is from yandex metric and current site
        return True
        """

        http_referer = request.META.get('HTTP_REFERER')
        return True if not http_referer else bool(
            re.match(self._get_regex_yandex_metric(request), http_referer))

    @staticmethod
    def _get_regex_yandex_metric(request):
        """Return a regular expression with our site and domain"""

        current_site = str(get_current_site(request))
        re_index = current_site.rfind('.')
        site, domain = current_site[:re_index], current_site[re_index:].replace('.', '')

        # regular expression taken with https://yandex.ru/support/metrica/behavior/click-map.html#iframe  # NOQA
        return (fr'^https?:\/\/([^\/]+\.)?({site}\.{domain}|webvisor\.com|metri[ck]a\.yandex\.'
                r'(com|ru|by|com\.tr))\/')
