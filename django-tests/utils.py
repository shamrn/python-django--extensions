from django.conf import settings


def get_throttle_rate(scope: str) -> int:
    """
    The function parses and returns rate with `REST_FRAMEWORK`, `DEFAULT_THROTTLE_RATES`
    configurations
    """

    throttle_rates = settings.REST_FRAMEWORK.get('DEFAULT_THROTTLE_RATES')
    assert throttle_rates, 'Throttle is not configured in `REST_FRAMEWORK` settings'

    rate = throttle_rates.get(scope)
    assert rate, '`scope` not found in configuration `DEFAULT_THROTTLE_RATES`'

    return int(rate.split('/')[0])
