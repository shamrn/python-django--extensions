
### An example of functionality

from extension import IntegerMultipleChoiceField
from django_filters import rest_framework as filters
from django.core.validators import EMPTY_VALUES


class PostTypeFilter(filters.MultipleChoiceFilter):

    field_class = IntegerMultipleChoiceField

    def filter(self, queryset, value):
        """Filtering rules"""

        if value not in EMPTY_VALUES: # (None, '', [], (), {})
            queryset = queryset.by_post_types(value)

            if list(filter(lambda val: val == PostBase.PostType.CHALLENGE_POST, value)):
                queryset = queryset.exclude(is_primary=True)

            return queryset

        return queryset
