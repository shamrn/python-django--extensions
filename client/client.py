from typing import Optional, Tuple

import requests
from requests.exceptions import ConnectionError, HTTPError, Timeout, TooManyRedirects




class IntegrationBaseException(Exception):
    """Integration class that implements exception"""


class IntegrationConfigurationException(IntegrationBaseException):
    """Integration class that implements exception"""


from typing import Optional, Tuple

import requests
from requests.exceptions import RequestException

from extension.integration.exceptions import (
    IntegrationBaseException,
    IntegrationConfigurationException
)


class BaseClient:
    """Base class for implementing client"""

    url = None

    def __init__(self):
        """Dunder method for class initialization"""

        assert self.url, IntegrationBaseException('`url` parameter is None')

    def do_request(self, request_method,
                   endpoint: Optional[None | str] = None,
                   object_id: Optional[None | str] = None,
                   data: Optional[None | dict] = None,
                   params: Optional[None | dict] = None,
                   headers: Optional[None | dict] = None,
                   ) -> Tuple[int | None, dict]:
        """Method implements request"""

        url = (f"{self.url}{f'/{endpoint}' if endpoint else ''}"
               f"{f'/{object_id}' if object_id else ''}")

        requests_ = self._get_request_method(request_method)

        try:
            response = requests_(url=url, params=params, data=data, headers=headers)
            return response.status_code, response.json()

        except RequestException as exc:
            response = {'message_exc': f'Request exception: {exc}'}
        except Exception as exc:
            response = {'message_exc': f'Base exception: {exc}'}

        return None, response

    @staticmethod
    def _get_request_method(request_method: str) -> 'requests':
        """Method returns the request object with a specific method ( GET, POST, ... )"""

        method_raw = request_method.lower() if isinstance(request_method, str) else None
        assert method_raw, IntegrationConfigurationException('`request_method` parameter is None')

        method = getattr(requests, method_raw, None)
        assert method, IntegrationConfigurationException('`request_method` isn\'t valid')

        return method

