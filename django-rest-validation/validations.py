from abc import ABCMeta, abstractmethod

from django.core.exceptions import PermissionDenied
from django.http import Http404
from rest_framework import exceptions, status
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import set_rollback

CUSTOM_VALIDATION = 'custom_validation'
PRIMARY_INPUT_MESSAGE = 'message'
PRIMARY_INPUT_FIELDS = 'fields_error'


def custom_exception_handler(exc, context):  # NOQA
    """Custom exception handler"""

    if isinstance(exc, Http404):
        exc = exceptions.NotFound()
    elif isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied()

    if isinstance(exc, exceptions.APIException):
        headers = {}
        if getattr(exc, 'auth_header', None):
            headers['WWW-Authenticate'] = exc.auth_header  # NOQA
        if getattr(exc, 'wait', None):
            headers['Retry-After'] = '%d' % exc.wait  # NOQA

        detail = exc.detail
        if isinstance(detail, dict) and (custom_validation := detail.get(CUSTOM_VALIDATION)):
            data = custom_validation
        elif isinstance(detail, dict):
            data = {
                PRIMARY_INPUT_FIELDS: {
                    key: next(iter(value), None)
                    for key, value in detail.items()
                }
            }
        elif isinstance(detail, list):
            data = detail
        else:
            data = {PRIMARY_INPUT_MESSAGE: detail}

        set_rollback()
        return Response(data, status=exc.status_code, headers=headers)

    return None


class BaseValidationError(APIException, metaclass=ABCMeta):
    """Base validation error"""

    _primary_input: str
    _default_status_code: int = status.HTTP_400_BAD_REQUEST

    def __init__(self, message: str, status_code: int = _default_status_code):
        """Dunder method for class initialization"""

        self.message = message
        self.status_code = status_code
        self.detail = {CUSTOM_VALIDATION: self._get_detail()}

    @abstractmethod
    def _get_detail(self) -> dict[str, dict[str, str]]:
        """Abstract method. The method should output detailed data."""


class ValidationMessageError(BaseValidationError):
    """Custom validation message error"""

    _primary_input = PRIMARY_INPUT_MESSAGE

    def __init__(self, *args, **kwargs):
        """Dunder method for class initialization"""

        super().__init__(*args, **kwargs)

    def _get_detail(self) -> dict[str, dict[str, str]]:
        """Method returns detail"""

        return {self._primary_input: self.message}


class ValidationFieldError(BaseValidationError):
    """Custom validation field error"""

    _primary_input = PRIMARY_INPUT_FIELDS

    def __init__(self, field: str, *args, **kwargs):
        """Dunder method for class initialization"""

        self.field = field

        super().__init__(*args, **kwargs)

    def _get_detail(self) -> dict[str, dict[str, str]]:
        """Method returns detail"""

        return {self._primary_input: {self.field: self.message}}
