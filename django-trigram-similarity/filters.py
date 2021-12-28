
from django.core.validators import EMPTY_VALUES


class TrigramSimilarityMixin:
    """Basic Mixin for trigram similarity search"""

    @staticmethod
    def by_trigram_similarity(queryset, name: str, value: str):  # NOQA

        if value not in EMPTY_VALUES:
            return (
                queryset.annotate_trigram_similarity(value)
                        .filter(trigram_similarity__gt=0.3)
                        .order_by('-trigram_similarity', '-created')
            )
        return queryset.none()
