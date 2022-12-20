"""The file contains the implementation of the base client"""

import json
from abc import abstractmethod, ABCMeta
from typing import Optional, Iterable, Callable

import requests
from requests.exceptions import RequestException

from exceptions import BaseClientConfigurationException


class BaseClient(metaclass=ABCMeta):
    """The base class implements a basic http client, used for requests"""

    def __init__(self):
        """Dunder method for class initialization"""

        self._success: bool = False
        self._status_code: Optional[int] = None
        self._result: Optional[dict] = None
        self._error_msg: Optional[dict] = None

    @property
    @abstractmethod
    def _url(self) -> str:
        """Implement the property that contains the url"""

    @property
    def success(self) -> bool:
        """The method returns a boolean value about the successful request"""

        return self._success

    @property
    def status_code(self) -> Optional[int]:
        """The method returns the status code of the request"""

        return self._status_code

    @property
    def result(self) -> Optional[dict]:
        """The method returns the result of the request"""

        return self._result

    @property
    def error_msg(self) -> Optional[dict]:
        """The method returns the error message of the request"""

        return self._error_msg

    def _do_request(self, request_method: str,
                    endpoint: Optional[str] = None,
                    object_id: Optional[str] = None,
                    data: Optional[dict] = None,
                    params: Optional[dict] = None,
                    auth: Optional[tuple] = None,
                    headers: Optional[dict] = None,
                    use_json: bool = False):
        """Method implements request"""

        url = self._join_path(url=self._url, paths=(endpoint, object_id))
        request = self._get_request_method(request_method)

        try:
            response = request(url=url, params=params, auth=auth, headers=headers,
                               data=self._get_data(use_json=use_json, data=data))
            self._status_code = response.status_code
            self._result = response.json()
            self._success = True

        except RequestException as exc:
            self._error_msg = {'message_exc': f'Request exception: {exc}'}
        except Exception as exc:
            self._error_msg = {'message_exc': f'Base exception: {exc}'}

    @staticmethod
    def _get_data(use_json: bool, data: dict) -> dict | str:
        """Method returns json format data if use_json is True"""

        if use_json:
            return json.dumps(data)
        return data

    @staticmethod
    def _get_request_method(request_method: str) -> Callable:
        """Method returns the request object with a specific method ( GET, POST, ... )"""

        method_raw = request_method.lower() if isinstance(request_method, str) else None
        assert method_raw, BaseClientConfigurationException('`request_method` parameter is None')

        method = getattr(requests, method_raw, None)
        assert method, BaseClientConfigurationException('`request_method` isn\'t valid')

        return method

    @staticmethod
    def _join_path(url: str, paths: Iterable) -> str:
        """Method returns full url include paths"""

        return f"{url}/{'/'.join(list(filter(None, paths)))}" if any(paths) else url
