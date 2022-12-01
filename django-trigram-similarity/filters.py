
from django.core.validators import EMPTY_VALUES


class FilterSearchBySimilarityMixin:
    """Mixin for trigram similarity search"""

    @staticmethod
    def by_similarity(queryset, name: str, value: bool):  # NOQA
        if value not in EMPTY_VALUES:
            return queryset.annotate_similarity(value).order_by('-similarity')
        return queryset.none()
