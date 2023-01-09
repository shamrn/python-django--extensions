from abc import ABCMeta, abstractmethod
from dataclasses import asdict
from typing import Union

from django.conf import settings

from reference.models import Category, BonusType
from reference.services.enums import GenerateFilterTypeEnum
from reference.services.typing import GeneratedFilter, GenerateFilterOption


class BaseGenerateFilter(metaclass=ABCMeta):
    """Base abstract class to implement a filter for the API"""

    def get_generated_filter(self) -> dict:
        """Returns generated filter as dict"""

        return asdict(self._generate)

    @property
    def _generate(self) -> GeneratedFilter:
        """Returns generate filter as DTO ( GenerateFilter )"""

        generated_filter = GeneratedFilter(
            display_text=self._display_text,
            query_parameter=self._query_parameter,
            selection_type=self._selection_type,
            options=self._options,
        )

        # Checking for type as string
        assert all([isinstance(option['id'], str) for option in generated_filter.options]), \
            TypeError('The `id` field must be a string.')

        return generated_filter

    @property
    @abstractmethod
    def _display_text(self) -> str:
        """Implement the property that contains the display text"""

    @property
    @abstractmethod
    def _query_parameter(self) -> str:
        """Implement the property that contains the query parameter"""

    @property
    @abstractmethod
    def _selection_type(self) -> Union[GenerateFilterTypeEnum.MULTIPLE,
                                       GenerateFilterTypeEnum.SINGLE]:
        """Implement the property that contains the selection type"""

    @property
    @abstractmethod
    def _options(self) -> list[GenerateFilterOption]:
        """Implement the property that contains the options as list with GenerateFilterOption """


# Example:
class GenerateCategoryFilter(BaseGenerateFilter):
    _display_text = settings.GENERATE_CATEGORY_FILTER_DISPLAY_TEXT
    _query_parameter = 'category_id'
    _selection_type = GenerateFilterTypeEnum.MULTIPLE
    _options = [GenerateFilterOption(id='1', name='test_1'),
                GenerateFilterOption(id='2', name='test_2'), ...]


class GenerateTypeFilter(BaseGenerateFilter):
    _display_text = settings.GENERATE_TYPE_FILTER_DISPLAY_TEXT
    _query_parameter = 'type_id'
    _selection_type = GenerateFilterTypeEnum.MULTIPLE

    @property
    def _options(self) -> list[GenerateFilterOption]:
        return self._ids_cast_int(BonusType.objects.values('id', 'name'))

    @staticmethod
    def _ids_cast_int(options: list[dict[int:str]]) -> list[GenerateFilterOption]:
        return [GenerateFilterOption(id=str(option['id']), name=option['name'])
                for option in options]
