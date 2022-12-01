import json
from typing import Optional, Tuple

import requests
from requests.exceptions import RequestException

from exceptions import (
    IntegrationBaseException,
    IntegrationConfigurationException
)


class BaseClient:
    """The base class implements a basic http http_client, used for requests"""

    url: str = None

    def __init__(self):
        """Dunder method for class initialization"""

        assert self.url, IntegrationBaseException('`url` parameter is None')

    def do_request(self, request_method: str,
                   endpoint: Optional[str] = None,
                   object_id: Optional[str] = None,
                   data: Optional[dict] = None,
                   params: Optional[dict] = None,
                   auth: Optional[tuple] = None,
                   headers: Optional[dict] = None,
                   use_json: bool = False) -> Tuple[dict, int | None]:
        """Method implements request"""

        url = self._join_path(self.url, paths=[endpoint, object_id])
        requests_ = self._get_request_method(request_method)

        status_code: Optional[int] = None

        try:
            raw_response = requests_(url=url, params=params, auth=auth, headers=headers,
                                     data=self._get_data(use_json=use_json, data=data))
            status_code = raw_response.status_code
            response = raw_response.json()

        except RequestException as exc:
            response = {'message_exc': f'Request exception: {exc}'}
        except Exception as exc:
            response = {'message_exc': f'Base exception: {exc}'}

        return response, status_code

    @staticmethod
    def _get_data(use_json: bool, data: dict) -> dict | str:
        """Method returns json format data if use_json is True"""

        if use_json:
            return json.dumps(data)
        return data

    @staticmethod
    def _get_request_method(request_method: str) -> 'requests':
        """Method returns the request object with a specific method ( GET, POST, ... )"""

        method_raw = request_method.lower() if isinstance(request_method, str) else None
        assert method_raw, IntegrationConfigurationException('`request_method` parameter is None')

        method = getattr(requests, method_raw, None)
        assert method, IntegrationConfigurationException('`request_method` isn\'t valid')

        return method

    @staticmethod
    def _join_path(url: str, paths: list) -> str:
        """Method returns full url include paths"""

        return f"{url}/{'/'.join(list(filter(None, paths)))}" if any(paths) else url
