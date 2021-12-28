
### This is used when we need to take several parameters as input
### json (example: object_id: "1", object_id: "2").
###  An override of the standard django "MultipleChoiceField" class.


from django_filters import fields
from django.core.exceptions import ValidationError


### Any value
class AnyValueField(fields.MultipleChoiceField):

    def valid_value(self, value):
        """Always returns True"""

        return True


### Required value
class IntegerMultipleChoiceField(AnyValueField):  # parent fields.MultipleChoiceField

    def to_python(self, value):
        """
        An overridden method "to_python" of the "MultipleChoiceField" class,
        validating and returning values of the correct type.
        """

        if not value:
            return []
        try:
            value = [int(val) for val in value]
        except ValueError:
            raise ValidationError('The input of the field isn\'t "integer" type')

        return value
