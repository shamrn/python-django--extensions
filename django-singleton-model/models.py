from django.db import models


class SingletonModelMixin(models.Model):
    """Singleton model mixin"""

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """Overridden `save` method"""

        object_ = self.get_object()
        if object_ and object_ != self:
            raise 'Singleton Model: no more than 1 record can be stored in the database.'

        super().save(*args, **kwargs)

    @classmethod
    def _get_object(cls):
        """Get object from the database. Failing that, return None."""

        try:
            return cls.objects.get()
        except cls.DoesNotExist:
            return None

    @classmethod
    def get_object(cls):
        """Checking the method `_get_object` for implementation"""

        if hasattr(cls, '_get_object'):
            return cls._get_object()
        return None
