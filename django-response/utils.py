from typing import TYPE_CHECKING, Union

from rest_framework.views import Response

from common.validations import ValidationMessageError

if TYPE_CHECKING:
    from django.db.models import Model
    from django.db.models.base import ModelBase
    from rest_framework import status


def get_object_or_404(model: Union['ModelBase', 'Model'], error_message: str, *args, **kwargs):
    try:
        return model.objects.get(*args, **kwargs)  # NOQA
    except model.DoesNotExist:
        raise ValidationMessageError(status_code=status.HTTP_404_NOT_FOUND, message=error_message)


def response_message(status_code: int, message: str) -> Response:
    return Response(status=status_code, data={'message': message})
