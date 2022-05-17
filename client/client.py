from typing import Union, Optional

import requests
from requests.exceptions import ConnectionError, HTTPError, Timeout, TooManyRedirects

from .exceptions import IntegrationBaseException, IntegrationConfigurationException


class CdekClient:
    """Base class for implementing client with the `cdek` service"""

    endpoint = None
    request_method = None
    url = 'http://example.com/'

    status_code = None
    result = dict()

    def __init__(self, data: Optional[Union[None, dict]] = None,
                 params: Optional[Union[None, dict]] = None,
                 token: Optional[Union[None, str]] = None,
                 object_id: Optional[Union[None, str]] = None):
        """Dunder method for class initialization"""

        assert self.endpoint, IntegrationBaseException('`endpoint` parameter is None')
        assert self.request_method, IntegrationBaseException('`request_method` parameter is None')

        self.data = data
        self.params = params
        self.object_id = object_id
        self.token = token
        self._do_request()

    def __getattr__(self, item):
        """Dunder method for assigning class attributes from received data"""

        result = self.result.get(item, None)
        if result is None:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{item}'")
        return result

    def _do_request(self):
        """Method implements request to the `cdek` service"""

        url = f"{self.url}{self.endpoint}/{self.object_id if self.object_id else ''}"
        headers = {}  # TODO
        requests_ = self._get_request_method()
        try:
            response_cdek = requests_(url=url, params=self.params, data=self.data, headers=headers)
            self.status_code = response_cdek.status_code
            response = response_cdek.json()

        except (ConnectionError, Timeout):
            response = {'message': 'Connection/Timeout error.'}
        except HTTPError:
            response = {'message': 'Unknown HTTP request.'}
        except TooManyRedirects:
            response = {'message': 'Too many redirects.'}

        self.result = response

    def _get_request_method(self) -> 'requests':
        """Method returns the request object with a specific method ( GET, POST, ... )"""

        method_raw = self.request_method.lower() if isinstance(self.request_method, str) else None
        assert method_raw, IntegrationConfigurationException('`request_method` parameter is None')

        method = getattr(requests, method_raw, None)
        assert method, IntegrationConfigurationException('`request_method` isn\'t valid')

        return method
