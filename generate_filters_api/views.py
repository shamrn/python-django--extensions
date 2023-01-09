from abc import ABCMeta, abstractmethod
from typing import Iterable, Callable

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from reference.services import generate_filters


class BaseGenerateFilterApiView(APIView, metaclass=ABCMeta):
    """Base abstract class to implement a filter API"""

    @property
    @abstractmethod
    def _generated_filters(self) -> Iterable[Callable[..., generate_filters.BaseGenerateFilter]]:
        """Implement the property that contains the class which
        inherited from a base abstraction class - `BaseGenerateFilter` in iterable object"""

    def get(self, *args, **kwargs):
        return Response(status=status.HTTP_200_OK,
                        data=[filter_().get_generated_filter()
                              for filter_ in self._generated_filters])


class BonusGenerateFilterAPIView(BaseGenerateFilterApiView):
    _generated_filters = (
        generate_filters.GenerateCategoryFilter,
        generate_filters.GenerateTypeFilter,
    )
