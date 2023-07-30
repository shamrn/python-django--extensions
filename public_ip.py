from typing import Optional

import requests
from requests.exceptions import RequestException
from requests.status_codes import codes as status_code

import logging

CHECK_IP_URL = 'https://checkip.amazonaws.com'

logger = logging.getLogger('public_ip')


class NetworkGetPublicIpException(Exception):
    """Network exception for get public ip"""


def get_public_ip() -> Optional[str]:
    """The function returns the public ip-address"""

    try:
        response = requests.get(CHECK_IP_URL)
        if response.status_code == status_code.OK:
            return response.text.strip()

    except RequestException as exc:
        logger.error(f'LOGGING FUNCTION. get_public_ip')
        logger.error(f'LOGGING MESSAGE. Failed to get ip address.')
        logger.error(f'LOGGING EXCEPTION. {exc}')

        raise NetworkGetPublicIpException(exc)
