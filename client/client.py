import json
from typing import Optional, Tuple

import requests
from requests.exceptions import RequestException

from client.functions import join_path
from client.exceptions import (
    IntegrationBaseException,
    IntegrationConfigurationException
)


class BaseClient:
    """Base class for implementing client"""

    url: str = None

    def __init__(self):
        """Dunder method for class initialization"""

        assert self.url, IntegrationBaseException('`url` parameter is None')

    def do_request(self, request_method,
                   endpoint: Optional[None | str] = None,
                   object_id: Optional[None | str] = None,
                   data: Optional[None | dict] = None,
                   params: Optional[None | dict] = None,
                   auth: Optional[None | tuple] = None,
                   headers: Optional[None | dict] = None,
                   ) -> Tuple[dict, int | None]:
        """Method implements request"""

        url = join_path(self.url, paths=[endpoint, object_id])
        requests_ = self._get_request_method(request_method)

        try:
            response = requests_(url=url, params=params, auth=auth, headers=headers,
                                 data=self._get_data(data=data, headers=headers))
            return response.json(), response.status_code

        except RequestException as exc:
            response = {'message_exc': f'Request exception: {exc}'}
        except Exception as exc:
            response = {'message_exc': f'Base exception: {exc}'}

        return response, None

    @staticmethod
    def _get_data(data: dict | None, headers: dict | None) -> dict | str:
        """Method returns json format data if content-type is application/json"""

        if headers and headers.get('Content-Type') == 'application/json':
            data = json.dumps(data)
        return data

    @staticmethod
    def _get_request_method(request_method: str) -> 'requests':
        """Method returns the request object with a specific method ( GET, POST, ... )"""

        method_raw = request_method.lower() if isinstance(request_method, str) else None
        assert method_raw, IntegrationConfigurationException('`request_method` parameter is None')

        method = getattr(requests, method_raw, None)
        assert method, IntegrationConfigurationException('`request_method` isn\'t valid')

        return method
